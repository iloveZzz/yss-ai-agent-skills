---
name: "yss-distributed-id"
description: "yss-component-distributed-id 框架专家指南。当用户询问有关分布式 ID 生成、号段模式、雪花算法或 MyBatis 自动 ID 注入时调用。"
---

# yss-distributed-id

本技能提供关于 `yss-component-distributed-id` 框架的专家级知识。该框架集成了 Leaf 和 CosId，支持 MyBatis/MP 自动注入分布式 ID。

## 核心功能

### 1. 多种 ID 策略
- **Leaf Segment** (推荐): 数据库号段模式，高可用，ID 趋势递增。
- **Leaf Snowflake**: Zookeeper 雪花算法，高性能，无 DB 依赖。
- **CosId Segment**: CosId 号段模式。
- **UUID**: 标准 UUID。

### 2. 自动注入
- **AutoIdInterceptor**: MyBatis 拦截器，拦截 `INSERT` 语句。
- **兼容性**: 支持 JPA (`@GeneratedValue`) 和 MyBatis-Plus (`@TableId`) 注解。
- **批量支持**: 自动处理 `List` 和 `Array` 类型的批量插入。

## 使用指南

### 1. 开启功能
在启动类添加注解：
```java
@EnableDistributedId
public class Application {}
```

### 2. 配置号段模式 (Leaf Segment)
**application.yml**:
```yaml
spring:
  leaf:
    leaf-segment-enable: true
```

**DB 初始化**:
```sql
CREATE TABLE `leaf_alloc` (
  `biz_tag` varchar(128)  NOT NULL DEFAULT '', -- 业务标识 (如表名)
  `max_id` bigint(20) NOT NULL DEFAULT '1',    -- 当前最大ID
  `step` int(11) NOT NULL,                     -- 步长
  PRIMARY KEY (`biz_tag`)
) ENGINE=InnoDB;
```

### 3. 实体类注解
**JPA 方式**:
```java
@Entity
public class User {
    @Id
    @GeneratedValue(generator = "segment") // 策略: segment, snowflake
    private Long id;
}
```

**MyBatis-Plus 方式**:
```java
@TableName("user")
public class User {
    @TableId(type = IdType.ASSIGN_ID) // 对应 segment 策略
    private Long id;
}
```

## 常见问题

- **Q: ID 重复怎么办？**
  - A: 检查 `leaf_alloc` 表的 `max_id` 是否被手动修改过，或者是否有多个应用实例使用了相同的 `biz_tag` 但连接了不同的数据库。
- **Q: 批量插入时 ID 不连续？**
  - A: 号段模式下，为了性能，ID 是从内存号段中获取的，不保证严格连续，只保证趋势递增。
- **Q: 支持 String 类型的 ID 吗？**
  - A: 支持。如果字段类型是 String，框架会自动将生成的 Long ID 转换为 String；也可以使用 UUID 策略。

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
- 核心代码资产：[assets](./assets/)
