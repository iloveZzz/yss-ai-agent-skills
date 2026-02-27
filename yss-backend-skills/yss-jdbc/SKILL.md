---
name: "yss-jdbc"
description: "yss-component-jdbc 框架专家指南。当用户询问有关 Hutool-db 封装、多数据源 JDBC 操作、动态数据源连接或批量数据处理时调用。"
---

# yss-jdbc

本技能提供关于 `yss-component-jdbc` 组件的专家级知识。该组件基于 Hutool-db 进行了封装，提供了在 Spring 环境下更便捷的多数据源和动态数据源 JDBC 操作能力。

## 概述

`yss-component-jdbc` 旨在解决复杂的 JDBC 操作场景，特别是涉及多数据源切换、动态构建连接以及大批量数据处理的场景。它与 `yss-component-persistence-common` 集成，复用了多数据源配置。

## 核心特性

- **Hutool 集成**: 封装了 Hutool 的 `Db` 和 `Session` 对象，简化 JDBC 操作。
- **多数据源支持**: 能够识别并操作 `MultiDataSourceHolder` 中管理的所有数据源。
- **动态连接**: 支持通过参数（URL, User, Password）即时创建数据库连接，无需预先配置 Bean。
- **批量增强**: 提供了针对 `List<Entity>` 和 `List<Map>` 的高效批量插入工具方法。

## 核心组件

### 1. DefaultHutoolDbHolder
用于获取已配置数据源的 `Db` 或 `Session` 对象。

```java
// 获取名为 "slave" 的数据源对应的 Db 对象
Db db = DefaultHutoolDbHolder.getDb("slave");
List<Entity> list = db.findAll("user");
```

### 2. JdbcSqlUtil
工具类，提供动态连接和批量操作能力。

```java
// 动态连接
DsParam param = new DsParam("com.mysql.cj.jdbc.Driver", "jdbc:mysql://...", "root", "123456");
Db db = JdbcSqlUtil.getDb(param);

// 批量插入
JdbcSqlUtil.batchAddMapData("user_log", logList, (sql, params) -> {
    // 执行回调，如调用 db.executeBatch(sql, params)
});
```

## 使用指南

### 1. 引入依赖
```xml
<dependency>
    <groupId>com.yss.cloud</groupId>
    <artifactId>yss-component-jdbc</artifactId>
</dependency>
```

### 2. 操作多数据源
确保项目中已配置多数据源（通过 `yss-component-persistence-common`）。

```java
@Service
public class DataService {
    public void syncData() {
        // 从主库读取
        Db masterDb = DefaultHutoolDbHolder.getDb("primary");
        // 写入从库
        Db slaveDb = DefaultHutoolDbHolder.getDb("slave");
        // ...
    }
}
```

## 常见问题

- **Q: 什么时候用 `DefaultHutoolDbHolder`，什么时候用 `JdbcSqlUtil`？**
  - A: 如果数据源已经在 Spring 配置文件中定义，使用 `DefaultHutoolDbHolder`；如果需要连接运行时才确定的外部数据库，使用 `JdbcSqlUtil`。
- **Q: 批量插入的性能如何？**
  - A: `JdbcSqlUtil` 提供了拼装 SQL 的能力，结合 JDBC 的 `executeBatch` 可以获得极高的性能。

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
- 核心代码资产：[assets](./assets/)
