---
name: "yss-ddd-scaffold-generator"
description: "YSS DDD 分层架构脚手架生成器。用于快速创建基于 DDD 的后端项目结构，包含 Domain、Application、Infrastructure、Adapter 四层架构。"
metadata:
  author: yss datamiddle team
  version: "1.0"
---

# YSS DDD 脚手架生成器 (YSS DDD Scaffold Generator)

本 Skill 提供了一个完整的 DDD 分层架构脚手架生成工具，可以快速创建符合 YSS 开发规范的后端项目。

## 1. 功能概述 (Features)

### 1.1 核心功能

- **项目结构生成**: 自动创建 Domain、Application、Infrastructure、Adapter、Bootstrap 五层模块
- **代码模板生成**: 提供完整的示例代码（User CRUD）
- **配置文件生成**: 自动生成 Maven POM、application.yml、logback 配置
- **数据库脚本生成**: 生成建表 SQL 和初始化数据脚本
- **自动初始化数据库**: (仅限 SQLite) 自动创建数据库文件并执行建表和初始化数据脚本
- **文档生成**: 自动生成项目 README 和 API 文档

### 1.2 技术栈

- **JDK**: 8
- **Spring Boot**: 2.7.18
- **MyBatis Plus**: 3.5.x
- **MapStruct**: 1.5.x
- **Lombok**: 1.18.x

## 2. 使用方法 (Usage)

### 2.1 快速开始

```bash
# 进入脚手架目录
cd yss-datamiddle-scaffold

# 运行生成器
python .trae/skills/yss-ddd-scaffold-generator/scripts/generate_scaffold.py \
  --project-name my-service \
  --base-package com.yss.myservice \
  --output-dir ./output
```

### 2.2 参数说明

| 参数             | 说明                   | 必填 | 默认值                                 |
| ---------------- | ---------------------- | ---- | -------------------------------------- |
| `--project-name` | 项目名称（kebab-case） | 是   | -                                      |
| `--base-package` | 基础包名               | 是   | -                                      |
| `--output-dir`   | 输出目录               | 否   | `./output`                             |
| `--with-example` | 是否包含示例代码       | 否   | `true`                                 |
| `--database`     | 数据库类型             | 否   | `sqlite` (若需MySQL请显式指定 `mysql`) |

### 2.3 生成的项目结构

```
{project-name}/
├── pom.xml                                    # 父级 POM
├── README.md                                  # 项目文档
├── {project-name}-domain/                     # 领域层
│   ├── pom.xml
│   └── src/main/java/{base-package}/
│       ├── client/dto/
│       │   ├── cmd/                          # 命令对象
│       │   └── query/                        # 查询对象
│       ├── client/vo/                        # 值对象
│       └── domain/
│           └── {domain-name}/                # 具体领域 (e.g., user, metadata)
│               ├── gateway/                  # 网关接口
│               ├── model/                    # 领域模型
│               └── service/                  # 领域服务
├── {project-name}-application/                # 应用层
│   ├── pom.xml
│   └── src/main/java/{base-package}/core/
│       └── service/
│           ├── impl/                         # 服务实现
│           └── convertor/                    # 对象转换器
├── {project-name}-infrastructure/             # 基础设施层
│   ├── pom.xml
│   └── src/main/java/{base-package}/repository/
│       ├── entity/                           # PO 对象
│       ├── gateway/impl/                     # 网关实现
│       ├── convertor/                        # 转换器
│       └── {Domain}Repository.java           # Repository 接口
├── {project-name}-adapter/                    # 适配器层
│   ├── pom.xml
│   └── {project-name}-web/                   # Web 适配器
│       ├── pom.xml
│       └── src/main/java/{base-package}/rest/
│           └── {Domain}Controller.java       # REST 控制器
└── {project-name}-bootstrap/                  # 启动模块
    ├── pom.xml
    └── src/main/
        ├── java/{base-package}/
        │   └── Application.java              # 启动类
        └── resources/
            ├── application.yml               # 应用配置
            └── logback-spring.xml            # 日志配置
```

## 3. 常见问题 (FAQ)

### 3.1 默认数据库依赖

默认生成的项目使用 SQLite。如果需要 MySQL，请在生成时指定 `--database mysql`。
如果已经生成了 SQLite 项目想要切换到 MySQL：

1. 修改 `infrastructure/pom.xml`，移除 `sqlite-jdbc`，添加 `mysql-connector-j`。
2. 修改 `bootstrap/src/main/resources/application.yml` 中的数据源配置。

### 3.2 启动类注解

生成的 `Application.java` 可能包含 `@EnableYssCloudRedisCache` 等注解。如果项目未配置 Redis，请注释掉该注解以免启动失败。

## 3. 示例代码 (Examples)

生成器会自动创建一个完整的 User 实体示例，包括：

### 3.1 Domain 层示例

- `UserAddCmd`: 用户新增命令
- `UserUpdateCmd`: 用户更新命令
- `UserPageQuery`: 用户分页查询
- `UserVO`: 用户值对象
- `UserGateway`: 用户网关接口

### 3.2 Application 层示例

- `UserService`: 用户应用服务接口
- `UserServiceImpl`: 用户应用服务实现
- `UserConvertor`: 用户对象转换器

### 3.3 Infrastructure 层示例

- `UserPO`: 用户持久化对象
- `UserRepository`: 用户仓储接口
- `UserGatewayImpl`: 用户网关实现
- `UserConvertor`: PO/VO 转换器

### 3.4 Adapter 层示例

- `UserController`: 用户 REST 控制器

## 4. 配置说明 (Configuration)

### 4.1 数据库配置

生成的 `application.yml` 包含数据库配置模板：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/{db_name}?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
```

### 4.2 MyBatis Plus 配置

```yaml
mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  global-config:
    db-config:
      id-type: assign_id
      logic-delete-field: deleted
```

## 5. 构建和运行 (Build & Run)

### 5.1 编译项目

```bash
cd {project-name}
./mvnw clean compile
```

### 5.2 打包项目

```bash
./mvnw clean package -DskipTests
```

### 5.3 运行项目

```bash
java -jar {project-name}-bootstrap/target/{project-name}-bootstrap-1.0.0-SNAPSHOT.jar
```

或使用 Maven 插件：

```bash
./mvnw spring-boot:run -pl {project-name}-bootstrap
```

## 6. 开发规范 (Development Guidelines)

生成的代码遵循以下规范：

### 6.1 命名规范

- **PO**: 持久化对象，对应数据库表
- **VO**: 值对象，用于数据展示
- **CMD**: 命令对象，用于数据修改
- **Query**: 查询对象，用于查询条件

### 6.2 分层规范

- Domain 层不依赖任何其他层
- Application 层依赖 Domain 层
- Infrastructure 层依赖 Domain 层
- Adapter 层依赖 Application 层
- Bootstrap 层依赖所有层

### 6.3 调用链路

```
Controller -> Service -> Gateway -> Repository -> Database
     ↓         ↓         ↓          ↓
   DTO/VO <- DTO/VO <- Domain <- PO
```

## 7. 扩展开发 (Extension)

### 7.1 添加新实体

1. 在 Domain 层创建 DTO（Cmd、Query、VO）
2. 在 Domain 层创建 Gateway 接口
3. 在 Application 层创建 Service 接口和实现
4. 在 Infrastructure 层创建 PO、Repository、Gateway 实现
5. 在 Adapter 层创建 Controller

### 7.2 添加新适配器

在 `{project-name}-adapter` 下创建新模块：

- `{project-name}-job`: 任务调度适配器
- `{project-name}-mq`: 消息队列适配器
- `{project-name}-rpc`: RPC 适配器

## 8. 常见问题 (FAQ)

### 8.1 如何修改数据库类型？

修改 `application.yml` 中的数据源配置，并在 POM 中添加对应的数据库驱动依赖。

### 8.2 如何添加缓存支持？

在 Infrastructure 层添加缓存配置，并在 Service 层使用 `@Cacheable` 注解。

### 8.3 如何集成 Swagger？

在 Bootstrap 模块添加 Swagger 依赖和配置类。

## 9. 参考资料 (References)

- [YSS 后端开发规范](./references//yss-backend-scaffold-parent/SKILL.md)
- [Domain 层开发指南](./references/yss-backend-scaffold-domain/SKILL.md)
- [Application 层开发指南](./references/yss-backend-scaffold-application/SKILL.md)
- [Infrastructure 层开发指南](./references/yss-backend-scaffold-infrastructure/SKILL.md)
- [Web Adapter 开发指南](./references/yss-backend-scaffold-web/SKILL.md)

## 10. 更新日志 (Changelog)

### v1.0 (2024-01-15)

- 初始版本发布
- 支持基础四层架构生成
- 包含完整的 User CRUD 示例
- 支持 MySQL 数据库
