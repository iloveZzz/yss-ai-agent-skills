# AI Agent Skills 集合

本仓库包含了三个主要的AI Agent技能集合，分别针对不同领域和应用场景。这些技能是专门为AI助手设计的指令集、脚本和资源，用于提升在特定任务上的性能。

## 📚 目录结构

```
ai-agent-skills/
├── claude-skills-demo/     # Claude AI技能示例集合
├── vue-skills/            # Vue.js开发专业技能
├── yss-backend-skills/    # YSS后端开发技能框架
└── README.md              # 本说明文档
```

## 🤖 Claude Skills Demo

**[claude-skills-demo](./claude-skills-demo)** 是Anthropic公司为Claude AI设计的技能集合，提供了各种类型的技能示例：

### 🔧 技能分类
- **创意与设计**: 算法艺术、画布设计等
- **开发与技术**: MCP服务器生成、Web应用测试等
- **企业与通信**: 内部沟通、品牌准则等
- **文档技能**: DOCX、PDF、PPTX、XLSX文档处理

### ✨ 主要功能
- **文档处理**: PDF表格提取、文档合并、OCR识别、表单填充
- **设计辅助**: 品牌指南遵循、Canvas字体管理
- **技术应用**: MCP构建器、Slack GIF生成器
- **办公自动化**: Word、Excel、PowerPoint文档智能处理

### 🚀 使用方式
适用于Claude Code、Claude.ai和API环境，可通过插件市场安装使用。

## 🌿 Vue Skills

**[vue-skills](./vue-skills)** 是专为Vue 3开发设计的AI代理技能集合：

### 🎯 技能列表

| 技能 | 适用场景 | 描述 |
|------|----------|------|
| **vue-best-practices** | Vue 3 + Composition API + TypeScript | 最佳实践、常见陷阱、SSR指导、性能优化 |
| **vue-options-api-best-practices** | Options API | `this`上下文、生命周期、TypeScript配合使用 |
| **vue-router-best-practices** | Vue Router 4 | 导航守卫、路由参数、路由组件生命周期 |
| **vue-pinia-best-practices** | Pinia状态管理 | Store设置、响应性、状态模式 |
| **vue-testing-best-practices** | 组件或E2E测试 | Vitest、Vue Test Utils、Playwright |
| **vue-jsx-best-practices** | Vue中JSX使用 | 与React JSX的语法差异 |
| **vue-development-guides** | Vue/Nuxt项目构建 | 组件拆分、数据流、核心原则 |
| **vue-debug-guides** | Vue 3问题调试 | 运行时错误、警告、异步错误处理、水合问题 |
| **create-adaptable-composable** | 可复用composables创建 | `MaybeRef`/`MaybeRefOrGetter`输入模式 |

### 💡 特色功能
- 提供经过验证的Vue开发最佳实践
- 包含详细的示例和调试指南
- 支持TypeScript和现代Vue开发工作流

## ⚙️ YSS Backend Skills

**[yss-backend-skills](./yss-backend-skills)** 是一套面向后端开发的专业技能框架：

### 🏗️ 核心技能

| 技能 | 功能 | 描述 |
|------|------|------|
| **yss-ddd-scaffold-generator** | DDD脚手架生成器 | 快速创建领域驱动设计的分层架构项目 |
| **yss-dto** | 统一数据传输对象 | 定义统一响应格式、分页查询、基础命令/查询对象 |
| **yss-audit-log** | 审计日志系统 | 提供系统操作审计和日志记录功能 |
| **yss-cache** | 缓存管理 | 缓存查询、更新、清除操作管理 |
| **yss-distributed-id** | 分布式ID生成 | 提供分布式环境下的唯一ID生成机制 |
| **yss-excel-mvc** | Excel处理 | MVC模式下的Excel导入导出功能 |
| **yss-jdbc** | JDBC工具集 | 数据库连接和SQL操作工具 |
| **yss-mybatis** | MyBatis增强 | MyBatis Plus集成和分页查询支持 |

### 🏗️ 架构特色
- **DDD分层架构**: Domain、Application、Infrastructure、Adapter四层分离
- **标准化组件**: 统一的DTO、响应格式和异常处理
- **企业级功能**: 审计日志、缓存管理、分布式ID等基础设施

## 🛠️ 使用指南

### Claude Skills
在Claude中使用技能时，在提示前加上 `use <skill-name>` 来明确触发特定技能。

### Vue Skills  
在Vue开发任务前使用 `use vue skill` 前缀以确保AI遵循Vue特定的最佳实践。

### YSS Backend Skills
适用于企业级Java后端开发，特别适合采用DDD架构的项目。

## 🤝 贡献

欢迎对这些技能集合进行改进和扩展。每个技能都是独立的文件夹，包含SKILL.md文件定义AI应遵循的指令和规范。

## 📄 许可证

- Claude Skills Demo: Apache 2.0许可证
- Vue Skills: MIT许可证  
- YSS Backend Skills: 专有许可证（企业内部使用）

---

> **注意**: 这些技能主要用于演示和教育目的，使用前请在自己的环境中充分测试。