# YSS DDD 脚手架生成器

## 📁 目录结构

```
yss-ddd-scaffold-generator/
├── SKILL.md                          # 主技能文档
├── README.md                         # 本文件
├── scripts/                          # Python 生成脚本
│   └── generate_scaffold.py         # 主生成脚本
├── assets/                           # 资源文件
│   └── templates/                    # 代码模板
│       ├── domain/                   # Domain 层模板
│       │   ├── UserAddCmd.java.template
│       │   ├── UserUpdateCmd.java.template
│       │   ├── UserPageQuery.java.template
│       │   ├── UserVO.java.template
│       │   ├── UserGateway.java.template
│       │   └── User.java.template
│       ├── application/              # Application 层模板
│       │   ├── UserService.java.template
│       │   ├── UserServiceImpl.java.template
│       │   └── UserConvertor.java.template
│       ├── infrastructure/           # Infrastructure 层模板
│       │   ├── UserPO.java.template
│       │   ├── UserRepository.java.template
│       │   ├── UserGatewayImpl.java.template
│       │   ├── UserConvertor.java.template
│       │   └── PageUtil.java.template
│       ├── adapter/                  # Adapter 层模板
│       │   └── UserController.java.template
│       ├── bootstrap/                # Bootstrap 层模板
│       │   └── Application.java.template
│       ├── pom/                      # Maven POM 模板
│       │   ├── parent-pom.xml.template
│       │   ├── domain-pom.xml.template
│       │   ├── application-pom.xml.template
│       │   ├── infrastructure-pom.xml.template
│       │   ├── adapter-pom.xml.template
│       │   ├── web-pom.xml.template
│       │   └── bootstrap-pom.xml.template
│       └── config/                   # 配置文件模板
│           ├── parent-pom.xml.template
│           ├── application.yml.template
│           ├── logback-spring.xml.template
│           ├── schema.sql.template
│           └── data.sql.template
└── references/                       # 参考文档
    ├── ARCHITECTURE.md               # 架构设计文档
    ├── USAGE_EXAMPLES.md             # 使用示例
    └── BEST_PRACTICES.md             # 最佳实践
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python 3.7+
python --version

# 无需额外依赖，使用标准库即可
```

### 2. 生成项目

```bash
cd yss-datamiddle-scaffold

python .trae/skills/yss-ddd-scaffold-generator/scripts/generate_scaffold.py \
  --project-name my-service \
  --base-package com.yss.datamiddle.myservice \
  --output-dir ./output
```

### 3. 编译运行

```bash
cd output/my-service
./mvnw clean compile
./mvnw spring-boot:run -pl my-service-bootstrap
```

## 📚 文档说明

### SKILL.md
主技能文档，包含：
- 功能概述
- 使用方法
- 参数说明
- 生成的项目结构
- 配置说明
- 构建和运行指南

### references/ARCHITECTURE.md
架构设计文档，包含：
- 架构概述
- 各层职责详解
- 依赖关系
- 调用链路
- 命名规范
- 最佳实践

### references/USAGE_EXAMPLES.md
使用示例文档，包含：
- 快速开始
- 编译和运行
- 添加新实体的完整示例
- 集成其他功能（Redis、Swagger）
- 常见问题解答
- 性能优化建议

## 🎯 核心特性

### 1. 完整的四层架构
- ✅ Domain 层：核心业务逻辑
- ✅ Application 层：业务用例编排
- ✅ Infrastructure 层：技术实现
- ✅ Adapter 层：外部接口适配

### 2. 开箱即用的示例
- ✅ User CRUD 完整示例
- ✅ 包含所有层的代码
- ✅ 数据库脚本
- ✅ 配置文件

### 3. 符合规范
- ✅ 遵循 YSS 开发规范
- ✅ 使用标准命名约定
- ✅ 包含完整注释
- ✅ 支持参数校验

### 4. 易于扩展
- ✅ 清晰的模块划分
- ✅ 标准的接口定义
- ✅ 灵活的配置
- ✅ 完善的文档

## 🛠️ 模板说明

### Domain 层模板
- **UserAddCmd**: 新增命令对象，包含 JSR-303 校验
- **UserUpdateCmd**: 更新命令对象
- **UserPageQuery**: 分页查询对象
- **UserVO**: 值对象，用于返回数据
- **UserGateway**: 网关接口，定义 CRUD 方法

### Application 层模板
- **UserService**: 服务接口
- **UserServiceImpl**: 服务实现，包含事务管理
- **UserConvertor**: MapStruct 转换器

### Infrastructure 层模板
- **UserPO**: 持久化对象，继承 AuditableEntity
- **UserRepository**: 仓储接口，继承 BasePlusRepository
- **UserGatewayImpl**: 网关实现，使用 MyBatis Plus
- **UserConvertor**: PO/VO 转换器

### Adapter 层模板
- **UserController**: REST 控制器，包含完整的 CRUD 接口

### 配置模板
- **parent-pom.xml**: 父级 POM，定义依赖管理
- **application.yml**: 应用配置，包含数据源、MyBatis Plus 配置
- **logback-spring.xml**: 日志配置
- **schema.sql**: 数据库建表脚本

## 📝 变量说明

模板中使用的变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{project_name}}` | 项目名称 | `user-service` |
| `{{base_package}}` | 基础包名 | `com.yss.datamiddle.user` |
| `{{group_id}}` | Maven GroupId | `com.yss.datamiddle` |
| `{{author}}` | 作者 | `YSS Team` |
| `{{date}}` | 日期 | `2024-01-15` |
| `{{database}}` | 数据库类型 | `mysql` |
| `{{driver_class}}` | 驱动类名 | `com.mysql.cj.jdbc.Driver` |
| `{{db_name}}` | 数据库名 | `user_db` |

## 🔧 自定义扩展

### 添加新的模板

1. 在 `assets/templates/` 对应目录下创建模板文件
2. 使用 `{{variable}}` 语法定义变量
3. 在生成脚本中添加模板处理逻辑

### 修改现有模板

1. 编辑 `assets/templates/` 下的模板文件
2. 保持变量命名一致
3. 测试生成结果

## 📖 参考资料

- [YSS 后端开发规范](../yss-backend-scaffold-parent/SKILL.md)
- [Domain 层开发指南](../yss-backend-scaffold-domain/SKILL.md)
- [Application 层开发指南](../yss-backend-scaffold-application/SKILL.md)
- [Infrastructure 层开发指南](../yss-backend-scaffold-infrastructure/SKILL.md)
- [Web Adapter 开发指南](../yss-backend-scaffold-web/SKILL.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个脚手架生成器。

## 📄 许可证

Copyright © 2024 YSS Data Team
