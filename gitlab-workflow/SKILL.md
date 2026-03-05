---
name: gitlab-workflow
description: 当任务需要基于已配置凭据操作 GitLab 仓库时使用，包括获取全部可访问项目、查询项目 clone 地址、创建 group、创建 project、克隆到本地、推送本地代码，以及通过终端脚本执行安全的分支化 Git 工作流。
---

# GitLab 工作流

使用本技能可通过脚本完成 GitLab 仓库常见操作，减少重复提示词与 token 消耗。

## 快速开始
1. 创建配置文件（JSON）：`~/.config/codex/gitlab.json`。
2. 运行 `python3 scripts/gitlab_ops.py list-projects`。
3. 按需使用 `create-group`、`create-project`、`clone`、`workflow` 等子命令。

## 配置
创建 `~/.config/codex/gitlab.json`：

```json
{
  "url": "https://gitlab.example.com",
  "token": "glpat-xxxx",
  "default_clone_protocol": "ssh"
}
```

支持的配置项：
- `url`：GitLab 基础地址。
- `token`：个人访问令牌（查询至少需要 `read_api`；创建 group/project 建议 `api`；推送建议 `write_repository`）。
- `default_clone_protocol`：`ssh` 或 `http`。

环境变量可覆盖配置文件：
- `GITLAB_URL`
- `GITLAB_TOKEN`
- `GITLAB_DEFAULT_CLONE_PROTOCOL`

## 脚本命令
在技能目录执行：

```bash
python3 scripts/gitlab_ops.py <subcommand> [options]
```

常用子命令：
- `list-projects`：列出全部可访问项目（自动分页）。
- `get-clone-url`：按项目 ID 或路径获取 clone 地址。
- `create-group`：创建 group（支持 parent_id 创建子组）。
- `create-project`：创建 project（支持 namespace_id 指定组/用户空间）。
- `clone`：按项目 ID 或路径克隆仓库。
- `push`：在本地仓库执行 add/commit/push。
- `workflow`：一键执行 fetch/rebase/切分支/commit/push。
- `init-config`：输出示例配置 JSON。

## 推荐流程
1. 若需要新空间，先创建 group：`create-group`。
2. 在目标 group（namespace）创建项目：`create-project`。
3. 用 `list-projects` 定位仓库并 `clone` 到本地。
4. 本地开发完成后，用 `push` 或 `workflow` 推送。

## 安全规则
- 不在输出中打印 token。
- 生产环境先在测试 group/project 验证命令。
- 首次执行创建与推送前，确认目标 `namespace_id` 与权限。
- 优先在 `feature/*`、`fix/*` 分支开发，避免直接推送受保护分支。

## 参考
- 详细示例见 `references/config-and-usage.md`。
