---
name: "yss-web-controller"
description: "根据 YSS 开发规范，基于 Domain 模型生成 Web Adapter (Controller) 层代码，仅依赖 Domain Gateway。"
metadata:
  author: yss datamiddle team
  version: "1.0"
---

# YSS Web Controller Generator

本 Skill 用于快速生成符合 YSS 后端开发规范的 Web Controller 层代码。它根据数据库元数据和领域名称（domain segment）自动生成 REST API，并统一直接调用 Domain Gateway。

## 1. 功能概述 (Features)

### 1.1 核心功能

- **Controller 生成**: 自动生成标准的 REST Controller，包含 CRUD 接口。
- **Gateway 直连**: Controller 基础操作统一调用 Domain Gateway，不生成或依赖 Application Service。
- **DTO 请求模型**: Controller 入参统一使用 `AddCmd`、`UpdateCmd`、`Page(Query)`。
- **VO 返回模型**: Controller 出参统一使用 `VO`（`SingleResult<VO>` / `PageResult<VO>`）。
- **MapStruct 转换**: 自动生成 `rest.convertor` 转换器，统一处理 `Cmd/Query/Domain/VO` 映射。
- **DTO/VO 生成**: 自动生成请求参数与返回对象。
- **领域包对齐**: 通过 `--domain-segment` 对齐 `com.yss.{module}.domain.{domain_name}` 包结构定位 Gateway。

### 1.2 生成代码规范

- **路径规范**: `/api/{module}/{domain}`
- **返回值规范**: 使用 `SingleResult`, `PageResult`, `MultiResult` 统一封装。
- **参数校验**: 自动添加 `@Valid` 注解。
- **Swagger**: (可选) 集成 Swagger/Knife4j 注解。

## 2. 使用方法 (Usage)

### 2.1 命令行调用

```bash
# 确保在项目根目录下
python .trae/skills/yss-web-controller/scripts/generate_controller.py \
  --metadata-file /path/to/metadata.json \
  --base-package com.yss.quality \
  --module-name quality \
  --domain-segment metadata \
  --domain-project-dir ./my-service-domain \
  --web-project-dir ./my-service-adapter/my-service-web \
  --force
```

### 2.2 参数说明

| 参数                   | 说明                                                                | 必填 | 默认值                               |
| ---------------------- | ------------------------------------------------------------------- | ---- | ------------------------------------ |
| `--metadata-file`      | 元数据文件路径 (JSON 格式，由 yss-db2mybatis 生成)                  | 是   | -                                    |
| `--base-package`       | 基础包名 (e.g., com.yss.quality)                                    | 是   | -                                    |
| `--module-name`        | 模块名称 (e.g., quality)                                            | 是   | -                                    |
| `--output-dir`         | 默认根输出目录                                                      | 否   | `./output`                           |
| `--domain-project-dir` | Domain 工程根目录，自动定位到 `src/main/java/{base_package}/client` | 否   | -                                    |
| `--web-project-dir`    | Web 工程根目录，自动定位到 `src/main/java/{base_package}/rest`      | 否   | -                                    |
| `--domain-output-dir`  | Domain 包根目录或 client 目录（兼容旧方式）                         | 否   | `{output-dir}/{base_package}/client` |
| `--web-output-dir`     | Web 包根目录或 rest 目录（兼容旧方式）                              | 否   | `{output-dir}/{base_package}/rest`   |
| `--domain-segment`     | 领域名称，对应 `domain.{domain_name}` 包段                          | 是   | -                                    |
| `--author`             | 作者名称                                                            | 否   | `System`                             |
| `--force`              | 是否覆盖已存在的文件                                                | 否   | `False`                              |

### 2.3 输出目录规则

- 当传 `--domain-project-dir` 时，DTO/VO 输出到 `{domain-project-dir}/src/main/java/{base_package}/client`。
- 当传 `--web-project-dir` 时，Controller 输出到 `{web-project-dir}/src/main/java/{base_package}/rest`。
- 当传 `--domain-output-dir` 或 `--web-output-dir` 时，支持传包根目录（自动补 `client/rest`）或直接传 `client/rest` 目录。

## 3. 生成代码示例

### 3.1 Controller (Gateway Mode)

```java
@RestController
@RequestMapping("/api/quality/template")
@RequiredArgsConstructor
@Api(tags = "数据质量模板管理")
public class QualityTemplateController {

    private final QualityTemplateGateway qualityTemplateGateway;

    @PostMapping("/page")
    @ApiOperation("分页查询")
    public PageResult<QualityTemplateVO> page(@RequestBody QualityTemplatePage query) {
        return toVOPage(qualityTemplateGateway.pageQualityTemplate(query));
    }

    @PostMapping
    @ApiOperation("新增模板")
    public SingleResult<Long> add(@RequestBody QualityTemplateAddCmd cmd) {
        return SingleResult.of(qualityTemplateGateway.addQualityTemplate(toDomain(cmd)));
    }
}
```

### 3.2 DTO/VO 示例

```java
// AddCmd
@Data
@EqualsAndHashCode(callSuper = true)
public class UserAddCmd extends CommandDTO {
    @NotBlank(message = "用户名不能为空")
    private String userName;
    // ...
}

// VO
@Data
public class UserVO implements Serializable {
    private static final long serialVersionUID = 1L;
    private Long userId;
    // ...
}
```

## 4. 依赖说明

生成的代码依赖以下组件：

- `yss-spring-boot-starter-web` (Result 封装)
- `lombok`
- `swagger` (可选)
- `mapstruct`
- 项目内部的 Domain 模块 (Gateway, Model)

## 5. 常见问题

### 5.1 如何获取 metadata.json?

请先使用 `yss-db2mybatis` Skill 的 `extract` 命令从数据库提取元数据。

### 5.2 生成的代码报错找不到类?

本工具默认会生成 DTO/VO 文件，并要求 Domain 层 Gateway 与 Model 已存在。请先运行 `yss-db2mybatis` 生成 Domain Gateway/Model，再使用本工具生成 Controller 与 DTO/VO。

### 5.3 转换为什么不使用 BeanUtils?

本工具统一生成 MapStruct 转换器（`{base_package}.rest.convertor.*WebConvertor`），Controller 通过转换器完成对象映射，不再使用 BeanUtils。

### 5.4 如何按多模块工程落盘到 domain/web?

说明：`ai1c` 仅为示例项目名，不同项目请替换为实际项目标识，并保持 `base-package`、`module-name`、`domain-project-dir`、`web-project-dir` 四者命名一致。

可直接使用：

```bash
python .trae/skills/yss-web-controller/scripts/generate_controller.py \
  --metadata-file ./metadata.json \
  --base-package com.yss.datamiddle.ai1c \
  --module-name ai1c \
  --domain-segment metadata \
  --domain-project-dir ./output/yss-datamiddle-ai1c/yss-datamiddle-ai1c-domain \
  --web-project-dir ./output/yss-datamiddle-ai1c/yss-datamiddle-ai1c-adapter/yss-datamiddle-ai1c-web \
  --force
```
