---
name: "yss-db2mybatis"
description: "读取 MySQL/Oracle/PostgreSQL 元数据并生成 YSS MyBatis 代码：repository 操作逻辑、domain gateway 接口、infrastructure gateway 实现。"
metadata:
  author: yss datamiddle team
  version: "1.1"
---

# yss-db2mybatis

面向开发者的数据库元数据脚手架 Skill。目标是用固定命令在低 token 消耗下快速生成可编译的基础持久层代码。

## 1. 适用范围

适用：
- 已有数据库表，需批量生成 YSS 风格持久层。
- 需要统一生成 `domain model + domain gateway + repository + gateway impl`。
- 需要多数据源配置、按表名规则批量生成。

不适用：
- 复杂关联查询、手写 SQL 优化、复杂 XML Mapper。
- 联合主键业务（默认 `pk_strategy=error`，需显式策略确认）。

## 2. 目录结构

- `scripts/db2mybatis.py`：主脚本
- `references/type-mapping.json`：SQL -> Java 类型映射
- `references/datasource-config.example.json`：多数据源配置示例
- `references/project-convention.example.json`：项目约定配置示例
- `assets/*.template.java`：代码模板

## 3. 依赖

- MySQL: `pip install pymysql`
- PostgreSQL: `pip install psycopg2-binary`
- Oracle: `pip install oracledb`

## 4. 快速开始（最小可运行）

### 4.1 MySQL

```bash
python3 yss-db2mybatis/scripts/db2mybatis.py extract \
  --datasource-config yss-db2mybatis/references/datasource-config.example.json \
  --datasource-name quality-mysql \
  --tables t_quality_template \
  --output /tmp/metadata.json

python3 yss-db2mybatis/scripts/db2mybatis.py scaffold \
  --skill-root /Users/zhudaoming/Documents/yss-project/test-ai-c/yss-db2mybatis \
  --metadata-file /tmp/metadata.json \
  --base-package com.yss.quality \
  --domain-segment template \
  --domain-java-root /path/project-domain/src/main/java \
  --infra-java-root /path/project-infrastructure/src/main/java \
  --dry-run
```

### 4.2 PostgreSQL

```bash
python3 yss-db2mybatis/scripts/db2mybatis.py extract \
  --datasource-config yss-db2mybatis/references/datasource-config.example.json \
  --datasource-name quality-postgres \
  --include-tables-regex '^t_quality_.*' \
  --output /tmp/metadata.json
```

### 4.3 Oracle

```bash
python3 yss-db2mybatis/scripts/db2mybatis.py extract \
  --datasource-config yss-db2mybatis/references/datasource-config.example.json \
  --datasource-name quality-oracle \
  --tables t_quality_template \
  --output /tmp/metadata.json
```

## 5. 生成前后目录对照

输入：数据库表 `t_quality_template`

输出：
- `domain/{segment}/model/QualityTemplate.java`
- `domain/{segment}/gateway/QualityTemplateGateway.java`
- `repository/entity/QualityTemplatePO.java`
- `repository/QualityTemplateRepository.java`
- `repository/gateway/impl/QualityTemplateGatewayImpl.java`
- 可选：`repository/convertor/QualityTemplateConvertor.java`

## 6. 常用参数

- 过滤表：`--tables` / `--include-tables-regex` / `--exclude-tables-regex`
- 安全生成：`--dry-run`（只预览） + `--overwrite`（允许覆盖）
- 可观测性：`--verbose`
- 主键策略：`--pk-strategy error|first`
- 项目约定：`--convention-file`
- 可选 Convertor：`--generate-convertor`

## 7. 项目约定文件

参考：`references/project-convention.example.json`

关键字段：
- `audit_columns`：默认跳过字段
- `logic_delete_fields`：分页时自动附加 `wrapper.eq(field, 0)`
- `base_entity_class`：PO 继承父类
- `pk_strategy`：联合主键处理策略
- `generate_convertor`：是否生成 MapStruct Convertor

## 8. 校验与执行建议

先校验：

```bash
python3 yss-db2mybatis/scripts/db2mybatis.py validate \
  --skill-root /Users/zhudaoming/Documents/yss-project/test-ai-c/yss-db2mybatis \
  --base-package com.yss.quality \
  --domain-segment template \
  --domain-java-root /path/project-domain/src/main/java \
  --infra-java-root /path/project-infrastructure/src/main/java \
  --datasource-config yss-db2mybatis/references/datasource-config.example.json \
  --convention-file yss-db2mybatis/references/project-convention.example.json
```

再执行：先 `scaffold --dry-run`，确认路径后去掉 `--dry-run`。

## 9. 常见问题与排障

- 场景：未配置数据源或连接失败（推荐按下面顺序处理）
  1. 复制示例配置：`cp yss-db2mybatis/references/datasource-config.example.json /path/datasource.json`
  2. 在 `/path/datasource.json` 中新增或修改你的数据源（`db_type/host/port/user/password/database`）
  3. 执行校验命令确认配置文件可用：
     ```bash
     python3 yss-db2mybatis/scripts/db2mybatis.py validate \
       --skill-root /Users/zhudaoming/Documents/yss-project/test-ai-c/yss-db2mybatis \
       --base-package com.yss.quality \
       --domain-segment template \
       --domain-java-root /path/project-domain/src/main/java \
       --infra-java-root /path/project-infrastructure/src/main/java \
       --datasource-config /path/datasource.json
     ```
  4. 再执行元数据提取：
     ```bash
     python3 yss-db2mybatis/scripts/db2mybatis.py extract \
       --datasource-config /path/datasource.json \
       --datasource-name your-datasource-name \
       --tables t_your_table \
       --output /tmp/metadata.json
     ```
  5. 如果仍连接失败，优先检查网络连通性、数据库账号权限、schema 名称（PostgreSQL）和服务名（Oracle）。

- `mysql 需要安装 pymysql`：安装对应驱动。
- `datasource 未找到`：检查 `--datasource-name` 与 JSON key。
- `缺少连接参数`：说明数据源配置缺字段，补齐 `db_type/host/port/user/password/database` 后重试。
- `文件已存在`：默认防覆盖，确认后加 `--overwrite`。
- `联合主键...pk_strategy=error`：改 `--pk-strategy first` 或手工处理。
- `metadata 中没有表`：检查 `--tables`、include/exclude regex、schema 权限。

## 10. Oracle 特殊说明

- 已支持 `IDENTITY` 字段识别。
- `SEQUENCE + TRIGGER` 自动关联不做强识别，建议生成后按项目规则手工调整主键策略。
