#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


AUDIT_COLUMNS = {"created_by", "created_date", "last_modified_by", "last_modified_date"}


def to_pascal_case(name):
    return "".join(part.capitalize() for part in re.split(r"[_\-\s]+", name) if part)


def to_camel_case(name):
    pascal = to_pascal_case(name)
    return pascal[:1].lower() + pascal[1:] if pascal else pascal


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def load_type_mapping(reference_file):
    return json.loads(read_text(reference_file))


def infer_domain_name(table_name, prefix):
    name = table_name
    if prefix and table_name.startswith(prefix):
        name = table_name[len(prefix):]
    return to_pascal_case(name)


def parse_table_name(ddl):
    m = re.search(r"create\s+table\s+`?([a-zA-Z0-9_]+)`?", ddl, flags=re.IGNORECASE)
    if not m:
        raise ValueError("未能在DDL中识别表名")
    return m.group(1)


def extract_columns_block(ddl):
    start = ddl.find("(")
    if start < 0:
        raise ValueError("DDL缺少字段定义区")
    depth = 0
    for i in range(start, len(ddl)):
        if ddl[i] == "(":
            depth += 1
        elif ddl[i] == ")":
            depth -= 1
            if depth == 0:
                return ddl[start + 1:i]
    raise ValueError("DDL字段定义区括号不匹配")


def split_column_lines(block):
    lines = []
    current = []
    depth = 0
    for ch in block:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            lines.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    tail = "".join(current).strip()
    if tail:
        lines.append(tail)
    return lines


def parse_column(line):
    raw = line.strip()
    if not raw:
        return None
    upper = raw.upper()
    if upper.startswith("PRIMARY KEY") or upper.startswith("UNIQUE KEY") or upper.startswith("KEY ") or upper.startswith("INDEX ") or upper.startswith("CONSTRAINT "):
        return None
    m = re.match(r"`?([a-zA-Z0-9_]+)`?\s+([a-zA-Z0-9]+)(\([^)]*\))?(.*)$", raw)
    if not m:
        return None
    name = m.group(1)
    sql_type = m.group(2).lower()
    extras = (m.group(4) or "").lower()
    return {
        "name": name,
        "sql_type": sql_type,
        "primary": "primary key" in extras
    }


def resolve_java_type(sql_type, mapping):
    return mapping.get(sql_type, "String")


def build_field_block(columns, mapping, skip_audit):
    field_lines = []
    imports = set()
    for col in columns:
        col_name = col["name"]
        if skip_audit and col_name in AUDIT_COLUMNS:
            continue
        java_type = resolve_java_type(col["sql_type"], mapping)
        field_name = to_camel_case(col_name)
        if java_type == "BigDecimal":
            imports.add("import java.math.BigDecimal;")
        if java_type == "LocalDateTime":
            imports.add("import java.time.LocalDateTime;")
        if java_type == "LocalDate":
            imports.add("import java.time.LocalDate;")
        if java_type == "LocalTime":
            imports.add("import java.time.LocalTime;")
        if col_name == "id" or col.get("primary"):
            field_lines.append(f'    @TableId(value = "{col_name}", type = IdType.ASSIGN_ID)')
        else:
            field_lines.append(f'    @TableField("{col_name}")')
        field_lines.append(f"    private {java_type} {field_name};")
        field_lines.append("")
    while field_lines and not field_lines[-1].strip():
        field_lines.pop()
    return "\n".join(field_lines), "\n".join(sorted(imports))


def fill_template(template, values):
    content = template
    for k, v in values.items():
        content = content.replace("${" + k + "}", v)
    return content


def gateway_interface_fqn(base_package, domain_name, domain_segment):
    segment = domain_segment if domain_segment else to_camel_case(domain_name.replace("PO", ""))
    return f"{base_package}.domain.{segment}.gateway.{domain_name}Gateway"


def generate_files(ddl, args):
    table_name = args.table_name if args.table_name else parse_table_name(ddl)
    domain_name = args.domain_name if args.domain_name else infer_domain_name(table_name, args.table_prefix)
    mapping = load_type_mapping(args.type_mapping)
    block = extract_columns_block(ddl)
    raw_lines = split_column_lines(block)
    columns = [c for c in (parse_column(line) for line in raw_lines) if c]
    fields_block, extra_imports = build_field_block(columns, mapping, args.skip_audit_columns)
    repository_field_name = to_camel_case(domain_name) + "Repository"
    gw_fqn = args.gateway_interface_fqn if args.gateway_interface_fqn else gateway_interface_fqn(args.base_package, domain_name, args.domain_segment)

    po_content = fill_template(read_text(args.po_template), {
        "base_package": args.base_package,
        "table_name": table_name,
        "domain_name": domain_name,
        "fields_block": fields_block,
        "extra_imports": extra_imports
    })
    repository_content = fill_template(read_text(args.repository_template), {
        "base_package": args.base_package,
        "domain_name": domain_name
    })
    gateway_content = fill_template(read_text(args.gateway_template), {
        "base_package": args.base_package,
        "domain_name": domain_name,
        "repository_field_name": repository_field_name,
        "gateway_interface_fqn": gw_fqn,
        "gateway_interface_name": domain_name + "Gateway"
    })
    return domain_name, po_content, repository_content, gateway_content


def write_outputs(output_dir, domain_name, po_content, repository_content, gateway_content):
    base = Path(output_dir)
    po_path = base / "entity" / f"{domain_name}PO.java"
    repo_path = base / f"{domain_name}Repository.java"
    gateway_path = base / "gateway" / "impl" / f"{domain_name}GatewayImpl.java"
    po_path.parent.mkdir(parents=True, exist_ok=True)
    repo_path.parent.mkdir(parents=True, exist_ok=True)
    gateway_path.parent.mkdir(parents=True, exist_ok=True)
    po_path.write_text(po_content + "\n", encoding="utf-8")
    repo_path.write_text(repository_content + "\n", encoding="utf-8")
    gateway_path.write_text(gateway_content + "\n", encoding="utf-8")
    return po_path, repo_path, gateway_path


def default_path(skill_root, rel):
    return str((Path(skill_root) / rel).resolve())


def build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ddl-file", required=True)
    parser.add_argument("--base-package", default="com.yss.quality")
    parser.add_argument("--domain-name")
    parser.add_argument("--table-name")
    parser.add_argument("--table-prefix", default="t_")
    parser.add_argument("--domain-segment")
    parser.add_argument("--gateway-interface-fqn")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--skill-root", required=True)
    parser.add_argument("--po-template")
    parser.add_argument("--repository-template")
    parser.add_argument("--gateway-template")
    parser.add_argument("--type-mapping")
    parser.add_argument("--skip-audit-columns", action="store_true", default=True)
    parser.add_argument("--keep-audit-columns", action="store_true")
    return parser


def normalize_args(args):
    if args.keep_audit_columns:
        args.skip_audit_columns = False
    if not args.po_template:
        args.po_template = default_path(args.skill_root, "assets/po.template.java")
    if not args.repository_template:
        args.repository_template = default_path(args.skill_root, "assets/repository.template.java")
    if not args.gateway_template:
        args.gateway_template = default_path(args.skill_root, "assets/gateway_impl.template.java")
    if not args.type_mapping:
        args.type_mapping = default_path(args.skill_root, "references/type-mapping.json")
    return args


def main():
    parser = build_arg_parser()
    args = normalize_args(parser.parse_args())
    ddl = read_text(args.ddl_file)
    domain_name, po_content, repo_content, gateway_content = generate_files(ddl, args)
    po_path, repo_path, gateway_path = write_outputs(
        args.output_dir, domain_name, po_content, repo_content, gateway_content
    )
    print(f"generated: {po_path}")
    print(f"generated: {repo_path}")
    print(f"generated: {gateway_path}")


if __name__ == "__main__":
    main()
