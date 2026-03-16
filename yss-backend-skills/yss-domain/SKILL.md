---
name: "yss-domain"
description: "生成YSS规范的核心领域层代码（Entity、Domain Gateway、领域规则）。当用户要求建设或重构Domain模型、补齐领域能力时调用。"
metadata:
  author: yss datamiddle team
  version: "1.0"
---

# yss-domain

面向 YSS DDD 后端项目的核心领域建模 Skill。  
目标是基于业务语义、数据库结构（DDL/DB）或 metadata，生成符合分层约束的 **Domain 模型、领域网关接口、领域行为规则**。

## 1. 何时调用

以下场景应优先调用本 Skill：

- 用户要求“先做 domain”、“先抽象实体/聚合”。
- 用户要求新增或重构核心领域模型（Entity / Value Object / 聚合行为）。
- 用户要求补齐 Domain Gateway 接口与领域能力边界。
- 用户给出 DDL/表结构，希望先落 Domain 再做 Repository/Web。
- 用户要求明确状态机、领域动作（如发布、终止、撤销、退回）及规则约束。

以下场景不建议单独使用本 Skill：

- 主要目标是 Repository 持久层生成（优先 `yss-repository` / `yss-mybatis`）。
- 主要目标是 Controller 接口生成（优先 `yss-web-controller`）。
- 主要目标是完整多模块脚手架初始化（优先 `yss-ddd-scaffold-generator`）。

## 2. 输入来源与优先级

支持输入来源：

1. 业务需求与页面流程（最高优先，决定领域行为）
2. metadata / DB schema（用于字段补全与约束映射）
3. DDL 文本（兜底输入）

要求：

- 必须先识别聚合边界与领域术语，不可直接按表“平铺对象”。
- 字段映射仅作辅助，领域行为优先于数据库形态。
- 对不明确规则给出显式假设并可追踪，不做隐式猜测。

## 3. 生成产物范围

典型输出：

- `domain/{segment}/model/*Entity.java`
- `domain/{segment}/gateway/*Gateway.java`
- （可选）`client/dto/cmd/*`、`client/dto/query/*`、`client/vo/*`（若任务明确要求）

可选增强：

- 状态常量与状态流转方法
- 领域校验方法（前置条件）
- 聚合内子实体列表与策略对象建模

## 4. 代码生成要求

### 4.1 分层与依赖约束

- Domain 层不得依赖 Infrastructure / Adapter 实现类型。
- Domain Gateway 仅定义领域所需能力，不泄漏持久化细节。
- 领域对象不得出现 SQL、Mapper、Repository 注解。
- 领域行为应封装在模型方法中，不下沉到 Controller。

### 4.2 Entity / 聚合建模规范

- 使用业务语义命名，不使用数据库缩写命名。
- 聚合根负责核心状态变化与一致性边界。
- 子实体通过聚合维护，不暴露跨聚合写入。
- 必须实现 `Serializable`，并保持 `serialVersionUID`。

### 4.3 领域规则规范

- 状态流转必须可读、可控、可校验（如 `publish()`、`terminate()`）。
- 对非法流转需阻断或显式返回失败语义。
- 规则优先在领域层表达，不放在 Web 层硬编码。
- 规则方法命名使用业务动词，禁止技术导向命名。

### 4.4 Domain Gateway 规范

- 接口命名：`{Domain}Gateway`。
- 方法命名使用领域动作，如 `addXxx`、`updateXxx`、`pageXxx`、`publishXxx`。
- 入参优先使用领域对象或领域 DTO，出参与调用场景一致。
- 接口粒度按业务能力设计，不按单表 CRUD 机械拆分。

## 5. 命名与目录规范

- Entity：`{Domain}Entity`
- 子实体：`{Domain}{Sub}Entity`
- 策略对象：`{Domain}{Strategy}Entity`
- Gateway：`{Domain}Gateway`

目录须落在：

- `.../domain/{segment}/model`
- `.../domain/{segment}/gateway`

## 6. 质量门禁

生成后必须满足：

- 编译通过，无缺失类型与循环依赖。
- 领域对象字段、行为与业务页面语义一致。
- 关键状态流转有明确方法表达。
- 无持久化实现泄漏到 Domain。
- 无敏感信息与无意义注释污染。

## 7. 与其他 Skill 协同

- 需要持久层实现时，后续调用 `yss-repository` 或 `yss-mybatis`。
- 需要 Web 接口时，后续调用 `yss-web-controller`。
- 需要从零建工程时，先 `yss-ddd-scaffold-generator`，再用本 Skill 细化领域。

## 8. 最小执行流程

1. 提取业务流程与核心领域术语。
2. 识别聚合根、子实体、状态与规则。
3. 生成 Domain Entity 与领域行为方法。
4. 生成 Domain Gateway 接口能力边界。
5. 编译校验并输出建模假设与后续协同建议。
