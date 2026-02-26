---
name: "yss-mybatis"
description: "yss-component-persistence 持久层框架专家指南。当用户询问有关 MyBatis、MyBatis-Plus、Repository、数据源配置、分页查询或批量操作时调用。"
---

# yss-mybatis

本技能提供关于 `yss-component-persistence` 持久化框架的专家级知识。该框架封装了 MyBatis 和 MyBatis-Plus，支持多数据源、自动分页和高效批量操作。

## 概述

`yss-component-persistence` 提供了两种集成模式，适应不同的开发需求：

1. **通用 MyBatis 模式** (`yss-component-mybatis-starter`): 适用于对 SQL 控制要求高的场景。
2. **MyBatis-Plus 模式** (`yss-component-mybatis-plus-starter`): 适用于追求高效率、使用 Lambda 表达式的场景。

## 核心组件

### 1. Repository 接口

- **BaseRepository<T, D>** (通用模式): 继承自 `io.mybatis.mapper.BaseMapper`，提供标准 CRUD。
- **BasePlusRepository<T>** (MP 模式): 继承自 MP 的 `BaseMapper`，额外扩展了 `insertBatchSomeColumn` 等方法。

### 2. 自动分页

- **机制**: 通过 `EntityQueryAspect` 切面拦截带有 `PageQuery` 参数的方法。
- **实现**: 自动调用 `PageHelper.offsetPage`。
- **双重支持**: 在 MP 模式下，同时支持 `PageHelper` 和 `MybatisPlusInterceptor` (IPage)。

### 3. 多数据源

- **配置**: `yss-component-persistence-common` 模块。
- **属性**: `spring.datasource.primary` (主), `yss.datasource.multi` (多数据源)。

## 配置指南

### MyBatis-Plus 模式配置

```yaml
yss:
  mybatis:
    mapper-scan: com.yss.cloud.**.mapper # 必须配置
    mapper-location: mappers/*.xml # XML文件位置
    page-interceptor:
      helper-dialect: mysql
      reasonable: true
      support-methods-arguments: true
```

### 引入依赖

**MP 模式**:

```xml
<dependency>
    <groupId>com.yss.cloud</groupId>
    <artifactId>yss-component-mybatis-plus-starter</artifactId>
</dependency>
```

**通用模式**:

```xml
<dependency>
    <groupId>com.yss.cloud</groupId>
    <artifactId>yss-component-mybatis-starter</artifactId>
</dependency>
```

## 最佳实践

### 1. 批量插入 (推荐)

在 MP 模式下，**务必使用** `insertBatchSomeColumn` 代替 `saveBatch`。前者是 SQL 级批量插入，性能极高；后者是循环单条插入。

```java
@Autowired
private UserRepository userRepository;

public void importUsers(List<User> users) {
    // 生成: insert into user (...) values (...), (...), (...)
    userRepository.insertBatchSomeColumn(users);
}
```

### 2. 分页查询

推荐在 Controller 层接收 `PageQuery` 对象，直接传递给 Service/Repository。

```java
// Controller
public Result<List<User>> list(PageQuery pageQuery) {
    return Result.success(userService.findList(pageQuery));
}

// Repository
List<User> findList(@Param("query") PageQuery query);
```

### 3. 复杂查询 (MP 模式)

使用 `LambdaQueryWrapper` 构建类型安全的查询。

```java
userRepository.selectList(new LambdaQueryWrapper<User>()
    .eq(User::getStatus, 1)
    .ge(User::getAge, 18));
```

## 常见问题

- **Q: 为什么分页不生效？**
  - A: 确保方法参数中包含 `PageQuery` 对象，且切面 `EntityQueryAspect` 能够扫描到该方法（通常是在 Service 或 Repository 层）。
- **Q: 如何切换数据源？**
  - A: 配置 `MultiDataSourceProperties` 并使用 `MultiDataSourceHolder` 获取对应数据源。

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
- 核心代码资产：[assets](./assets/)
