#!/usr/bin/env python3
"""GitLab project and git workflow helper.

This script reduces prompt/token usage by handling common GitLab and git tasks
through deterministic CLI subcommands.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import http.client
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_CONFIG = Path.home() / ".config" / "codex" / "gitlab.json"
DEFAULT_NAMESPACE = "Data-Middleground-Develop-Area/product-code/datamiddle-backend"


@dataclass
class GitLabConfig:
    url: str
    token: str
    default_clone_protocol: str = "ssh"


def fail(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in config file {path}: {exc}")
    return {}


def load_config(config_path: Path) -> GitLabConfig:
    file_cfg = load_json(config_path)

    url = os.getenv("GITLAB_URL", file_cfg.get("url", "")).strip().rstrip("/")
    token = os.getenv("GITLAB_TOKEN", file_cfg.get("token", "")).strip()
    protocol = (
        os.getenv("GITLAB_DEFAULT_CLONE_PROTOCOL", file_cfg.get("default_clone_protocol", "ssh"))
        .strip()
        .lower()
    )

    if not url:
        fail(f"Missing GitLab URL. Set GITLAB_URL or config {config_path}")
    if not token:
        fail(f"Missing GitLab token. Set GITLAB_TOKEN or config {config_path}")
    if protocol not in {"ssh", "http"}:
        fail("default_clone_protocol must be 'ssh' or 'http'")

    return GitLabConfig(url=url, token=token, default_clone_protocol=protocol)


def request_json(
    cfg: GitLabConfig,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET",
    body: Optional[Dict[str, Any]] = None,
) -> tuple[Any, Dict[str, str]]:
    query = ""
    if params:
        query = "?" + urllib.parse.urlencode(params)
    url = f"{cfg.url}{path}{query}"

    data = None
    req = urllib.request.Request(url, method=method)
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req.data = data
        req.add_header("Content-Type", "application/json")
    req.add_header("PRIVATE-TOKEN", cfg.token)
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            parsed = json.loads(resp_body) if resp_body else None
            headers = {k: v for k, v in resp.headers.items()}
            return parsed, headers
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="ignore")
        # 提供更友好的错误信息
        if exc.code == 403:
            try:
                err_json = json.loads(err_body)
                err_msg = err_json.get("error", err_json.get("message", err_body))
                if "不允许创建个人项目" in err_msg or "personal project" in err_msg.lower():
                    fail(f"GitLab API 403: {err_msg}\n\n提示: 请使用 --namespace 或 --namespace-id 指定项目所属的组/命名空间。\n"
                         f"可以使用以下命令查看可用的命名空间:\n"
                         f"  python3 scripts/gitlab_ops.py list-namespaces")
            except json.JSONDecodeError:
                pass
        fail(f"GitLab API HTTP {exc.code} at {path}: {err_body[:500]}")
    except urllib.error.URLError as exc:
        fail(f"GitLab API request failed: {exc}")
    except http.client.IncompleteRead as exc:
        fail(f"GitLab API request incomplete: {exc}")

    return None, {}


def resolve_namespace(cfg: GitLabConfig, namespace: str) -> Optional[int]:
    """将 namespace 路径或名称解析为 namespace_id。
    
    支持:
    - 数字ID直接返回
    - 完整路径 (如: group/subgroup)
    - 组名搜索
    """
    # 如果是纯数字，直接返回
    if namespace.isdigit():
        return int(namespace)
    
    # 尝试通过 API 查找 namespace
    # 先尝试作为完整路径查找
    try:
        data, _ = request_json(cfg, f"/api/v4/namespaces/{urllib.parse.quote(namespace, safe='')}")
        if data and data.get("id"):
            return data.get("id")
    except SystemExit:
        pass  # 路径查找失败，继续尝试搜索
    
    # 通过搜索查找
    try:
        data, _ = request_json(cfg, "/api/v4/namespaces", {"search": namespace, "per_page": 20})
        if data:
            for ns in data:
                if ns.get("full_path") == namespace or ns.get("name") == namespace:
                    return ns.get("id")
            # 如果没有精确匹配，返回第一个相似结果并打印警告
            if len(data) > 0:
                ns = data[0]
                print(f"警告: 未找到精确匹配的 namespace '{namespace}'，使用最接近的: {ns.get('full_path')} (id={ns.get('id')})", 
                      file=sys.stderr)
                return ns.get("id")
    except SystemExit:
        pass
    
    return None


def paginate_projects(cfg: GitLabConfig, extra_params: Dict[str, Any], max_items: Optional[int] = None, namespace: Optional[str] = None) -> Iterable[Dict[str, Any]]:
    page = 1
    per_page = 10
    item_count = 0
    if namespace is None:
        namespace = DEFAULT_NAMESPACE
    while True:
        params = {
            "simple": "true",
            "per_page": per_page,
            "page": page,
        }
        params.update(extra_params)
        data, headers = request_json(cfg, "/api/v4/projects", params)
        items = data or []
        if not items:
            break
        for item in items:
            item_namespace = item.get("path_with_namespace", "")
            if item_namespace.startswith(namespace):
                if max_items is not None and item_count >= max_items:
                    return
                yield item
                item_count += 1

        next_page = headers.get("X-Next-Page", "").strip()
        if not next_page:
            break
        page = int(next_page)


def print_projects(projects: List[Dict[str, Any]], output_json: bool) -> None:
    if output_json:
        print(json.dumps(projects, ensure_ascii=False, indent=2))
        return

    print("id\tpath_with_namespace\thttp_url\tssh_url")
    for p in projects:
        print(
            f"{p.get('id')}\t{p.get('path_with_namespace')}\t"
            f"{p.get('http_url_to_repo')}\t{p.get('ssh_url_to_repo')}"
        )


def select_project(
    projects: List[Dict[str, Any]],
    project_id: Optional[int],
    project_path: Optional[str],
) -> Dict[str, Any]:
    if project_id is not None:
        for p in projects:
            if int(p.get("id", -1)) == project_id:
                return p
        fail(f"Project id not found in accessible projects: {project_id}")

    if project_path:
        target = project_path.strip().lower()
        for p in projects:
            if str(p.get("path_with_namespace", "")).lower() == target:
                return p
        fail(f"Project path not found in accessible projects: {project_path}")

    fail("Provide either --project-id or --project-path")
    return {}


def run_cmd(cmd: List[str], cwd: Optional[Path] = None, dry_run: bool = False) -> None:
    printable = " ".join(cmd)
    print(f"$ {printable}")
    if dry_run:
        return
    try:
        subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)
    except subprocess.CalledProcessError as exc:
        fail(f"Command failed ({exc.returncode}): {printable}")


def cmd_init_config(_: argparse.Namespace) -> None:
    sample = {
        "url": "https://gitlab.example.com",
        "token": "glpat-xxxx",
        "default_clone_protocol": "ssh",
    }
    print(json.dumps(sample, ensure_ascii=False, indent=2))


def cmd_list_namespaces(args: argparse.Namespace) -> None:
    """列出用户可访问的命名空间。"""
    cfg = load_config(Path(args.config))
    params: Dict[str, Any] = {"per_page": 100}
    if args.search:
        params["search"] = args.search
    
    data, _ = request_json(cfg, "/api/v4/namespaces", params)
    
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    
    print("id\tname\tfull_path\tkind")
    for ns in data or []:
        print(f"{ns.get('id')}\t{ns.get('name')}\t{ns.get('full_path')}\t{ns.get('kind')}")


def cmd_list_projects(args: argparse.Namespace) -> None:
    cfg = load_config(Path(args.config))
    params: Dict[str, Any] = {}
    if args.search:
        params["search"] = args.search
    if args.membership:
        params["membership"] = "true"
    if args.owned:
        params["owned"] = "true"
    if args.archived:
        params["archived"] = "true"

    namespace = args.namespace
    if not namespace:
        namespace = DEFAULT_NAMESPACE

    projects = list(paginate_projects(cfg, params, args.max_items, namespace))
    print_projects(projects, args.json)


def cmd_get_clone_url(args: argparse.Namespace) -> None:
    cfg = load_config(Path(args.config))
    namespace = args.namespace
    if not namespace:
        namespace = DEFAULT_NAMESPACE
    
    search_params = {}
    if args.project_path:
        path_parts = args.project_path.split("/")
        for part in reversed(path_parts):
            if part:
                search_params["search"] = part
                break
    
    projects = list(paginate_projects(cfg, search_params, max_items=50, namespace=namespace))
    p = select_project(projects, args.project_id, args.project_path)

    protocol = args.protocol or cfg.default_clone_protocol
    if protocol == "ssh":
        print(p.get("ssh_url_to_repo", ""))
    else:
        print(p.get("http_url_to_repo", ""))


def cmd_clone(args: argparse.Namespace) -> None:
    cfg = load_config(Path(args.config))
    namespace = args.namespace
    if not namespace:
        namespace = DEFAULT_NAMESPACE
    
    search_params = {}
    if args.project_path:
        path_parts = args.project_path.split("/")
        for part in reversed(path_parts):
            if part:
                search_params["search"] = part
                break
    
    projects = list(paginate_projects(cfg, search_params, max_items=50, namespace=namespace))
    
    if args.project_id:
        project_data, _ = request_json(cfg, f"/api/v4/projects/{args.project_id}")
        if project_data:
            p = project_data
        else:
            fail(f"Project id not found: {args.project_id}")
    else:
        p = select_project(projects, args.project_id, args.project_path)

    protocol = args.protocol or cfg.default_clone_protocol
    clone_url = p.get("ssh_url_to_repo") if protocol == "ssh" else p.get("http_url_to_repo")
    if not clone_url:
        fail("Clone URL is empty")

    dest = args.dest
    cmd = ["git", "clone", clone_url]
    if dest:
        cmd.append(dest)
    run_cmd(cmd, dry_run=args.dry_run)


def cmd_create_group(args: argparse.Namespace) -> None:
    cfg = load_config(Path(args.config))
    payload: Dict[str, Any] = {
        "name": args.name,
        "path": args.path,
    }
    if args.parent_id is not None:
        payload["parent_id"] = args.parent_id
    if args.visibility:
        payload["visibility"] = args.visibility
    if args.description:
        payload["description"] = args.description

    data, _ = request_json(cfg, "/api/v4/groups", method="POST", body=payload)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"group_id={data.get('id')}")
    print(f"full_path={data.get('full_path')}")
    print(f"web_url={data.get('web_url')}")


def cmd_create_project(args: argparse.Namespace) -> None:
    cfg = load_config(Path(args.config))
    
    # 处理 namespace：支持路径、名称或ID
    namespace_id = args.namespace_id
    if args.namespace:
        resolved = resolve_namespace(cfg, args.namespace)
        if resolved:
            namespace_id = resolved
        else:
            fail(f"无法解析 namespace: {args.namespace}\n"
                 f"请使用 list-namespaces 命令查看可用的命名空间，或直接提供 namespace_id")
    
    # 如果没有指定 namespace，使用默认的
    if namespace_id is None:
        resolved = resolve_namespace(cfg, DEFAULT_NAMESPACE)
        if resolved:
            namespace_id = resolved
            print(f"使用默认命名空间: {DEFAULT_NAMESPACE} (id={namespace_id})")
    
    payload: Dict[str, Any] = {
        "name": args.name,
    }
    if args.path:
        payload["path"] = args.path
    if namespace_id is not None:
        payload["namespace_id"] = namespace_id
    if args.visibility:
        payload["visibility"] = args.visibility
    if args.description:
        payload["description"] = args.description
    if args.initialize_readme:
        payload["initialize_with_readme"] = True
    if args.default_branch:
        payload["default_branch"] = args.default_branch

    data, _ = request_json(cfg, "/api/v4/projects", method="POST", body=payload)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"project_id={data.get('id')}")
    print(f"path_with_namespace={data.get('path_with_namespace')}")
    print(f"http_url={data.get('http_url_to_repo')}")
    print(f"ssh_url={data.get('ssh_url_to_repo')}")


def cmd_push(args: argparse.Namespace) -> None:
    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        fail(f"Not a git repository: {repo}")

    branch = args.branch
    if not branch:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            fail("Cannot detect current branch. Use --branch")
        branch = result.stdout.strip()

    run_cmd(["git", "add", "-A"], cwd=repo, dry_run=args.dry_run)
    run_cmd(["git", "commit", "-m", args.message], cwd=repo, dry_run=args.dry_run)

    push_cmd = ["git", "push"]
    if args.set_upstream:
        push_cmd.extend(["-u", "origin", branch])
    else:
        push_cmd.append("origin")
        push_cmd.append(branch)
    run_cmd(push_cmd, cwd=repo, dry_run=args.dry_run)


def cmd_workflow(args: argparse.Namespace) -> None:
    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        fail(f"Not a git repository: {repo}")

    run_cmd(["git", "fetch", "origin"], cwd=repo, dry_run=args.dry_run)

    if args.base_branch:
        run_cmd(["git", "checkout", args.base_branch], cwd=repo, dry_run=args.dry_run)
        if args.rebase:
            run_cmd(["git", "pull", "--rebase", "origin", args.base_branch], cwd=repo, dry_run=args.dry_run)

    run_cmd(["git", "checkout", "-B", args.branch], cwd=repo, dry_run=args.dry_run)
    run_cmd(["git", "add", "-A"], cwd=repo, dry_run=args.dry_run)
    run_cmd(["git", "commit", "-m", args.message], cwd=repo, dry_run=args.dry_run)
    run_cmd(["git", "push", "-u", "origin", args.branch], cwd=repo, dry_run=args.dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GitLab project and git workflow helper")
    parser.set_defaults(func=None)

    sub = parser.add_subparsers(dest="subcommand")

    p_init = sub.add_parser("init-config", help="Print sample config JSON")
    p_init.set_defaults(func=cmd_init_config)

    # 新增 list-namespaces 命令
    p_ns = sub.add_parser("list-namespaces", help="List accessible GitLab namespaces/groups")
    p_ns.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    p_ns.add_argument("--search", help="Search keyword")
    p_ns.add_argument("--json", action="store_true", help="Output JSON")
    p_ns.set_defaults(func=cmd_list_namespaces)

    p_list = sub.add_parser("list-projects", help="List accessible GitLab projects")
    p_list.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    p_list.add_argument("--search", help="Search keyword")
    p_list.add_argument("--membership", action="store_true", help="Only projects with membership")
    p_list.add_argument("--owned", action="store_true", help="Only owned projects")
    p_list.add_argument("--archived", action="store_true", help="Include archived projects")
    p_list.add_argument("--json", action="store_true", help="Output JSON")
    p_list.add_argument("--max-items", type=int, help="Maximum number of projects to return")
    p_list.add_argument("--namespace", help=f"Namespace to search (default: {DEFAULT_NAMESPACE})")
    p_list.set_defaults(func=cmd_list_projects)

    p_url = sub.add_parser("get-clone-url", help="Get project clone URL")
    p_url.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    p_url.add_argument("--project-id", type=int, help="GitLab project id")
    p_url.add_argument("--project-path", help="group/subgroup/repo")
    p_url.add_argument("--protocol", choices=["ssh", "http"], help="Clone protocol")
    p_url.add_argument("--namespace", help=f"Namespace to search (default: {DEFAULT_NAMESPACE})")
    p_url.set_defaults(func=cmd_get_clone_url)

    p_clone = sub.add_parser("clone", help="Clone project by id/path")
    p_clone.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    p_clone.add_argument("--project-id", type=int, help="GitLab project id")
    p_clone.add_argument("--project-path", help="group/subgroup/repo")
    p_clone.add_argument("--protocol", choices=["ssh", "http"], help="Clone protocol")
    p_clone.add_argument("--dest", help="Clone destination directory name/path")
    p_clone.add_argument("--target-dir", dest="dest", help="Clone destination directory name/path (alias for --dest)")
    p_clone.add_argument("--dry-run", action="store_true", help="Show git command only")
    p_clone.add_argument("--namespace", help=f"Namespace to search (default: {DEFAULT_NAMESPACE})")
    p_clone.set_defaults(func=cmd_clone)

    p_cg = sub.add_parser("create-group", help="Create GitLab group")
    p_cg.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    p_cg.add_argument("--name", required=True, help="Group name")
    p_cg.add_argument("--path", required=True, help="Group path")
    p_cg.add_argument("--parent-id", type=int, help="Parent group id (for subgroup)")
    p_cg.add_argument("--visibility", choices=["private", "internal", "public"], help="Group visibility")
    p_cg.add_argument("--description", help="Group description")
    p_cg.add_argument("--json", action="store_true", help="Output JSON")
    p_cg.set_defaults(func=cmd_create_group)

    p_cp = sub.add_parser("create-project", help="Create GitLab project")
    p_cp.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    p_cp.add_argument("--name", required=True, help="Project name")
    p_cp.add_argument("--path", help="Project path")
    p_cp.add_argument("--namespace", help="Target namespace path/name (e.g., 'group/subgroup')")
    p_cp.add_argument("--namespace-id", type=int, help="Target namespace id (group/user)")
    p_cp.add_argument("--visibility", choices=["private", "internal", "public"], help="Project visibility")
    p_cp.add_argument("--description", help="Project description")
    p_cp.add_argument("--initialize-readme", action="store_true", help="Initialize project with README")
    p_cp.add_argument("--default-branch", help="Default branch name")
    p_cp.add_argument("--json", action="store_true", help="Output JSON")
    p_cp.set_defaults(func=cmd_create_project)

    p_push = sub.add_parser("push", help="Add/commit/push from local git repo")
    p_push.add_argument("--repo", default=".", help="Local git repo path")
    p_push.add_argument("--branch", help="Target branch; default is current branch")
    p_push.add_argument("--message", required=True, help="Commit message")
    p_push.add_argument("--set-upstream", action="store_true", help="Use -u origin <branch>")
    p_push.add_argument("--dry-run", action="store_true", help="Show commands only")
    p_push.set_defaults(func=cmd_push)

    p_wf = sub.add_parser("workflow", help="Run branch-based fetch/rebase/commit/push flow")
    p_wf.add_argument("--repo", default=".", help="Local git repo path")
    p_wf.add_argument("--base-branch", default="main", help="Base branch to update before work")
    p_wf.add_argument("--branch", required=True, help="Feature branch to create/switch")
    p_wf.add_argument("--message", required=True, help="Commit message")
    p_wf.add_argument("--rebase", action="store_true", help="Rebase base branch before branching")
    p_wf.add_argument("--dry-run", action="store_true", help="Show commands only")
    p_wf.set_defaults(func=cmd_workflow)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not args.subcommand or not args.func:
        parser.print_help()
        raise SystemExit(2)
    args.func(args)


if __name__ == "__main__":
    main()
