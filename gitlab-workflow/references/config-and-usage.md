# GitLab 工作流参考

## 1. 配置访问

创建 `~/.config/codex/gitlab.json`：

```json
{
  "url": "https://gitlab.example.com",
  "token": "glpat-xxxx",
  "default_clone_protocol": "ssh"
}
```

令牌建议权限：
- 查询项目与 clone 地址：`read_api`
- 创建 group/project：`api`
- 通过 HTTPS 推送代码：`write_repository`

## 2. 列出项目

```bash
python3 scripts/gitlab_ops.py list-projects
python3 scripts/gitlab_ops.py list-projects --search data-platform
python3 scripts/gitlab_ops.py list-projects --json
```

输出字段：
- `id`
- `path_with_namespace`
- `http_url`
- `ssh_url`

## 3. 创建 Group

```bash
python3 scripts/gitlab_ops.py create-group --name "Data Platform" --path data-platform
python3 scripts/gitlab_ops.py create-group --name "ETL Team" --path etl-team --parent-id 123 --visibility private
```

常用参数：
- `--name`：组名称（必填）
- `--path`：组路径（必填）
- `--parent-id`：父组 ID（用于创建子组）
- `--visibility`：`private/internal/public`

## 4. 创建 Project

```bash
python3 scripts/gitlab_ops.py create-project --name "etl-service" --path etl-service --namespace-id 123 --initialize-readme
python3 scripts/gitlab_ops.py create-project --name "dm-job" --namespace-id 123 --visibility private --default-branch main
```

常用参数：
- `--name`：项目名（必填）
- `--path`：项目路径（可选）
- `--namespace-id`：目标命名空间 ID（组或用户）
- `--initialize-readme`：初始化 README
- `--default-branch`：默认分支名

## 5. 获取 clone 地址

```bash
python3 scripts/gitlab_ops.py get-clone-url --project-id 1234 --protocol ssh
python3 scripts/gitlab_ops.py get-clone-url --project-path group/sub/repo --protocol http
```

## 6. 克隆仓库

```bash
python3 scripts/gitlab_ops.py clone --project-id 1234 --dest ./repo-local
python3 scripts/gitlab_ops.py clone --project-path group/sub/repo --protocol ssh
```

## 7. 推送本地修改

```bash
python3 scripts/gitlab_ops.py push --repo ./repo-local --message "feat: add batch export" --set-upstream
python3 scripts/gitlab_ops.py push --repo ./repo-local --message "fix: correct api timeout"
```

## 8. 分支化 Git 工作流

```bash
python3 scripts/gitlab_ops.py workflow \
  --repo ./repo-local \
  --base-branch main \
  --branch feature/add-export \
  --message "feat: add export workflow" \
  --rebase
```

上述命令执行顺序：
1. `git fetch origin`
2. `git checkout <base-branch>`
3. 可选：`git pull --rebase origin <base-branch>`
4. `git checkout -B <branch>`
5. `git add -A`
6. `git commit -m <message>`
7. `git push -u origin <branch>`

## 9. Shell 快捷别名

```bash
bash scripts/gitlab_ops.sh cg --name "Data Platform" --path data-platform
bash scripts/gitlab_ops.sh cp --name "etl-service" --namespace-id 123 --initialize-readme
bash scripts/gitlab_ops.sh ls
bash scripts/gitlab_ops.sh wf --repo ./repo-local --branch feature/demo --message "chore: demo"
```
