# YSS DDD 脚手架生成器 - 快速参考

## 🚀 一分钟快速开始

```bash
# 1. 生成项目
python .trae/skills/yss-ddd-scaffold-generator/scripts/generate_scaffold.py \
  --project-name my-service \
  --base-package com.yss.datamiddle.myservice

# 2. 编译项目
cd output/my-service && ./mvnw clean compile

# 3. 运行项目
./mvnw spring-boot:run -pl my-service-bootstrap

# 4. 测试接口
curl http://localhost:8080/actuator/health
```

## 📁 项目结构速查

```
my-service/
├── my-service-domain/          # 领域层：DTO、Gateway、Model
├── my-service-application/     # 应用层：Service、Convertor
├── my-service-infrastructure/  # 基础设施层：PO、Repository、Gateway Impl
├── my-service-adapter/         # 适配器层：Controller
│   └── my-service-web/
└── my-service-bootstrap/       # 启动层：Application、配置文件
```

## 🎯 核心概念速查

| 概念 | 说明 | 位置 | 示例 |
|------|------|------|------|
| **CMD** | 命令对象（写操作） | domain/client/dto/cmd | UserAddCmd |
| **Query** | 查询对象（读操作） | domain/client/dto/query | UserPageQuery |
| **VO** | 值对象（返回结果） | domain/client/vo | UserVO |
| **Gateway** | 网关接口 | domain/domain/gateway | UserGateway |
| **Service** | 应用服务 | application/core/service | UserService |
| **PO** | 持久化对象 | infrastructure/repository/entity | UserPO |
| **Repository** | 仓储接口 | infrastructure/repository | UserRepository |
| **Controller** | REST 控制器 | adapter/rest | UserController |

## 📝 命名规范速查

| 类型 | 格式 | 示例 |
|------|------|------|
| 项目名 | kebab-case | user-service |
| 包名 | lowercase.dot | com.yss.datamiddle.user |
| 类名 | PascalCase | UserService |
| 方法名 | camelCase | getUserById |
| 常量 | UPPER_SNAKE_CASE | MAX_SIZE |

## 🔧 常用命令速查

### Maven 命令
```bash
# 编译
./mvnw clean compile

# 打包
./mvnw clean package -DskipTests

# 运行
./mvnw spring-boot:run -pl {module}-bootstrap

# 测试
./mvnw test

# 安装到本地仓库
./mvnw clean install
```

### API 测试命令
```bash
# 分页查询
curl -X POST http://localhost:8080/api/users/page \
  -H "Content-Type: application/json" \
  -d '{"pageNum":1,"pageSize":10}'

# 新增
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com"}'

# 查询详情
curl http://localhost:8080/api/users/1

# 更新
curl -X PUT http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"id":1,"username":"test","status":1}'

# 删除
curl -X DELETE http://localhost:8080/api/users/1
```

## 📚 文档导航速查

| 文档 | 用途 | 路径 |
|------|------|------|
| **SKILL.md** | 主文档 | ./SKILL.md |
| **README.md** | 使用说明 | ./README.md |
| **ARCHITECTURE.md** | 架构设计 | ./references/ARCHITECTURE.md |
| **USAGE_EXAMPLES.md** | 使用示例 | ./references/USAGE_EXAMPLES.md |
| **SUMMARY.md** | 完成总结 | ./SUMMARY.md |

## 🎨 代码模板速查

### Domain 层
```java
// Command
@Data
public class UserAddCmd extends CommandDTO {
    @NotBlank(message = "用户名不能为空")
    private String username;
}

// VO
@Data
public class UserVO implements Serializable {
    private Long id;
    private String username;
}

// Gateway
public interface UserGateway {
    PageResult<UserVO> pageUser(UserPageQuery query);
    Long addUser(UserAddCmd cmd);
}
```

### Application 层
```java
// Service
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserGateway userGateway;
    
    @Transactional(rollbackFor = Exception.class)
    public Long addUser(UserAddCmd cmd) {
        return userGateway.addUser(cmd);
    }
}
```

### Infrastructure 层
```java
// PO
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("t_user")
public class UserPO extends AuditableEntity {
    @TableId(value = "id", type = IdType.ASSIGN_ID)
    private Long id;
    
    @TableField("username")
    private String username;
}

// Repository
public interface UserRepository extends BasePlusRepository<UserPO> {
}
```

### Adapter 层
```java
// Controller
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;
    
    @PostMapping
    public SingleResult<Long> add(@Valid @RequestBody UserAddCmd cmd) {
        return SingleResult.of(userService.addUser(cmd));
    }
}
```

## ⚙️ 配置速查

### application.yml
```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/db_name
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver

mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true
  global-config:
    db-config:
      id-type: assign_id
```

### pom.xml 关键依赖
```xml
<!-- YSS Components -->
<dependency>
    <groupId>com.yss.cloud</groupId>
    <artifactId>yss-component-mybatis-starter</artifactId>
</dependency>

<!-- MapStruct -->
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
</dependency>

<!-- Lombok -->
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

## 🔍 故障排查速查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 编译失败 | 依赖缺失 | 检查 pom.xml，执行 `./mvnw clean install` |
| 启动失败 | 数据库连接失败 | 检查 application.yml 数据源配置 |
| 接口404 | 路径错误 | 检查 @RequestMapping 路径 |
| 参数校验失败 | 缺少 @Valid | 在 Controller 参数前添加 @Valid |
| 事务不生效 | 缺少 @Transactional | 在 Service 方法上添加注解 |

## 📞 快速联系

- **文档**: [SKILL.md](./SKILL.md)
- **示例**: [USAGE_EXAMPLES.md](./references/USAGE_EXAMPLES.md)
- **架构**: [ARCHITECTURE.md](./references/ARCHITECTURE.md)
- **邮箱**: data-team@yss.com.cn

---

**提示**: 这是一个快速参考文档，详细信息请查看完整文档。
