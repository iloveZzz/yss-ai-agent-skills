---
name: "yss-openapi"
description: "基于 smart-doc-maven-plugin 生成 YSS 后端接口文档。用户需要导出 OpenAPI、Word、Markdown 文档时调用。"
---

# yss-openapi

用于 YSS 后端脚手架项目的接口文档导出。依赖 `smart-doc-maven-plugin:yss-3.1.2`，支持从 Controller 提取接口并生成 OpenAPI、Word、Markdown 文档。

## 1. 适用场景

- 项目由 `yss-ddd-scaffold-generator` 生成，`bootstrap` 模块已配置 smart-doc 插件
- 需要对外提供 OpenAPI 规范文件
- 需要输出可读文档（Word、Markdown）

## 2. 前置条件

- 在 `bootstrap` 模块的 `pom.xml` 中存在插件：
  - `groupId`: `com.github.shalousun`
  - `artifactId`: `smart-doc-maven-plugin`
  - `version`: `yss-3.1.2`
- 存在配置文件：`src/main/resources/smart-doc.json`

### 2.1 smart-doc 配置模板

- 可直接参考模板：`.trae/skills/yss-openapi/references/smart-doc.example.json`
- 建议复制到 `bootstrap` 模块：

```bash
cp .trae/skills/yss-openapi/references/smart-doc.example.json ./src/main/resources/smart-doc.json
```

- 使用前按实际项目修改：
  - `sourceCodePaths`
  - `packageFilters`
  - `outPath`

## 3. 常用命令

在 `bootstrap` 模块目录执行：

```bash
mvn com.github.shalousun:smart-doc-maven-plugin:yss-3.1.2:openapi
```

```bash
mvn com.github.shalousun:smart-doc-maven-plugin:yss-3.1.2:word
```

```bash
mvn com.github.shalousun:smart-doc-maven-plugin:yss-3.1.2:markdown
```

## 4. 推荐工作流

1. 先执行 `openapi` 生成机器可读规范
2. 再执行 `markdown` 或 `word` 生成评审文档
3. 将文档产物归档到 `docs/` 或发版附件

## 5. 常见问题

- 未找到插件目标：确认在 `bootstrap` 模块执行命令，并检查 plugin 版本是否为 `yss-3.1.2`
- 文档缺少模型字段：检查 `smart-doc.json` 的 `includes` 是否包含 domain/infrastructure 依赖
- 文档为空：确认 Controller 在 web 模块并被 bootstrap 依赖引入
