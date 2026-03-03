---
name: "yss-mybatis-orm-ddl-scaffold"
description: "基于SQL DDL生成YSS基础设施层PO、Repository与Gateway实现规范。新增表或重构持久层、需要快速落库建模时调用。"
metadata:
  author: yss datamiddle team
  version: "1.0"
---

# YSS MyBatis ORM DDL 脚手架规范 (DDL-driven Infrastructure Scaffold)

本 Skill 采用“短说明 + 外部模板/脚本”方式，优先降低上下文 token 消耗。

## 1. 使用入口 (Invoke)

- 你拿到 `CREATE TABLE` DDL，需要快速生成 `PO + Repository + GatewayImpl`。
- 你要重构已有持久层，统一为 YSS MyBatis Plus 风格。

## 2. 外部资源 (Low-token Assets)

- `assets/po.template.java`
- `assets/repository.template.java`
- `assets/gateway_impl.template.java`
- `references/type-mapping.json`
- `references/entity-example.java`
- `references/repository-example.java`
- `references/gateway-example.java`
- `scripts/ddl_to_yss_orm.py`

调用时优先引用上述文件，不在 Skill 主文档内展开长代码。

## 3. 生成流程 (Workflow)

1. 从 DDL 解析：表名、字段名、字段类型、主键。
2. 按 `references/type-mapping.json` 映射 Java 类型。
3. 按模板生成 3 个文件：
   - `entity/{DomainName}PO.java`
   - `{DomainName}Repository.java`
   - `gateway/impl/{DomainName}GatewayImpl.java`
4. 默认跳过审计字段 `created_by/created_date/last_modified_by/last_modified_date`，由 `AuditableEntity` 承接。
5. 生成后根据 Domain 网关接口修正 import 与方法签名。

## 4. 脚本命令 (Script)

```bash
python3 .trae/skills/yss-mybatis-orm-ddl-scaffold/scripts/ddl_to_yss_orm.py \
  --skill-root /Users/zhudaoming/yss-datamiddle-quality/.trae/skills/yss-mybatis-orm-ddl-scaffold \
  --ddl-file /path/to/table.sql \
  --base-package com.yss.quality \
  --output-dir /path/to/yss-datamiddle-quality-v3-infrastructure/src/main/java/com/yss/quality/repository
```

可选参数：

- `--domain-name` 指定领域名（默认由表名推断）
- `--table-name` 指定表名（默认从DDL解析）
- `--table-prefix` 默认 `t_`
- `--domain-segment` 指定 domain 包段
- `--gateway-interface-fqn` 显式指定网关接口全限定名
- `--keep-audit-columns` 不跳过审计字段

## 5. 验收规则 (Checklist)

- PO 使用 `@TableName/@TableId/@TableField` 且命名规范。
- Repository 继承 `BasePlusRepository<PO>`。
- GatewayImpl 使用 `Wrappers.lambdaQuery` + `PageUtil` + `PageResult`。
- 包路径、类名、字段名与现有模块风格一致。
