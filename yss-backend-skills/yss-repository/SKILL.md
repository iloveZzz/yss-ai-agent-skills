---
name: "yss-repository"
description: "生成YSS规范的Repository持久层与Domain网关实现。用户要求按表结构、DDL或数据库生成repository相关代码时调用。"
metadata:
  author: yss datamiddle team
  version: "1.0"
---

# yss-repository

面向 YSS 后端项目的 Repository 专项代码生成 Skill。  
目标是基于 **数据库表 / DDL / metadata**，稳定生成可编译、可扩展、符合分层规范的持久层与领域网关实现代码。

## 1. 何时调用

以下场景应优先调用本 Skill：

- 用户要求“生成 repository / PO / convertor / gateway impl”代码。
- 用户提供 DDL（或写作 dll）并要求生成持久层代码。
- 用户要求把数据库表映射为 Domain + Infrastructure 持久化能力。
- 用户要求批量补齐某个领域下的 repository 层缺失代码。
- 用户要求统一为现有模块补充分页查询、逻辑删除、基础 CRUD 持久化模板。

以下场景不建议单独使用本 Skill：

- 主要目标是生成 Controller（优先 `yss-web-controller`）。
- 主要目标是初始化完整多模块工程（优先 `yss-ddd-scaffold-generator`）。
- 主要目标是复杂 SQL 调优或手写 XML（应人工实现）。

## 2. 输入来源与优先级

支持三类输入来源，优先级如下：

1. `metadata.json`（结构最完整，优先）
2. 数据库直连元数据（次优）
3. DDL 文本或 DDL 文件（兜底）

要求：

- 必须识别主键、逻辑删除字段、审计字段、可空性与注释。
- 主键为联合主键时，默认报错并提示策略，不做静默猜测。
- 未识别类型必须给出映射告警并回退到可编译类型。

## 3. 生成产物范围

以领域 `approvaltask` 为例，生成产物应包含：

- `domain/{segment}/model/*Entity.java`
- `domain/{segment}/gateway/*Gateway.java`
- `repository/entity/*PO.java`
- `repository/*Repository.java`
- `repository/convertor/*Convertor.java`
- `repository/gateway/impl/*GatewayImpl.java`

可选生成：

- 领域查询 DTO、VO（若当前任务明确要求）。
- 批量导入/导出辅助方法签名（不默认开启）。

## 4. 代码生成要求

### 4.1 分层与依赖约束

- Domain 层不得依赖 Infrastructure 层类型。
- Gateway 接口定义在 Domain，Gateway 实现在 Infrastructure。
- Controller 或 Application 不得直接依赖 Repository。
- Convertor 统一使用 MapStruct。

### 4.2 Repository 规范

- Repository 接口继承 `BasePlusRepository<PO>`。
- 基础 CRUD 使用 MyBatis-Plus 通用能力。
- 分页查询统一通过 `PageUtil.page(query)`。
- 逻辑删除字段统一使用 `@TableLogic`。

### 4.3 PO 规范

- PO 必须使用 `@TableName`、`@TableId`、`@TableField` 明确映射。
- 审计字段优先复用 `AuditableEntity`。
- 逻辑删除字段名默认 `deleted`，值语义 `0/1`。
- 字段命名遵循数据库下划线到 Java 驼峰映射。

### 4.4 GatewayImpl 规范

- 构造器注入 Repository（`@RequiredArgsConstructor`）。
- 查询条件使用 `LambdaQueryWrapper`。
- 分页返回统一 `PageResult.of(records,total,size,current)`。
- 读写前需做必要空值与删除状态校验。

### 4.5 Convertor 规范

- 统一配置：
  - `NullValuePropertyMappingStrategy.IGNORE`
  - `NullValueCheckStrategy.ALWAYS`
- 提供单对象与列表转换方法。
- 非同构字段（如 `List<String>` -> `String`）必须提供显式转换函数。

## 5. 命名与目录规范

- Entity：`{Domain}Entity`
- PO：`{Domain}PO`
- Repository：`{Domain}Repository`
- Gateway：`{Domain}Gateway`
- GatewayImpl：`{Domain}GatewayImpl`
- Convertor：`{Domain}Convertor`

目录必须与 `base-package` 对齐，不允许跨层混放。

## 6. 质量门禁

生成后必须满足：

- 所有新增代码可编译通过。
- 包路径、类名、注解完整且一致。
- 生成代码不包含未使用 import。
- 不输出敏感配置（账号、密码、密钥）。
- 对无法自动推断项给出明确 TODO 或错误提示，不进行隐式猜测。

## 7. 与其他 Skill 的协同

- 需要从数据库/DDL提取 metadata 时，先调用 `yss-db2mybatis`。
- 需要补齐 Web 接口时，再调用 `yss-web-controller`。
- 需要从零构建完整工程时，优先 `yss-ddd-scaffold-generator`，本 Skill 用于补全或增强 repository 层。

## 8. 最小执行流程

1. 识别输入来源（metadata / DB / DDL）。
2. 解析表结构与字段约定（主键、逻辑删除、审计字段）。
3. 生成 Domain（Entity + Gateway）。
4. 生成 Infrastructure（PO + Repository + Convertor + GatewayImpl）。
5. 编译校验并输出生成清单与限制说明。
