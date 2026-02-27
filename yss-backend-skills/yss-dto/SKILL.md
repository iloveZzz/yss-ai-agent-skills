---
name: "yss-dto"
description: "yss-component-dto 核心组件专家指南。当用户询问有关统一响应格式 (Result)、分页查询 (PageQuery)、DTO 继承规范或基础命令/查询对象时调用。"
---

# yss-dto

本技能提供关于 `yss-component-dto` 组件的专家级知识。该组件定义了微服务架构中通用的数据传输对象规范，包括统一响应、分页查询基础类、命令/查询对象基类等。

## 概述

`yss-component-dto` 是所有微服务项目的核心依赖之一，旨在规范服务间及前后端的数据交互格式。

## 核心组件

### 1. 统一响应 (Result)

用于封装 API 接口的返回结果。

- **Result**: 通用返回对象，包含 `success`, `code`, `message`, `data` 等字段。
- **常用方法**: `Result.buildSuccess()`, `Result.buildFailure(msg)`。

### 2. 分页查询 (PageQuery)

所有分页查询参数类的基类。

- **属性**: `pageIndex` (页码), `pageSize` (条数), `orderBy` (排序)。
- **集成**: 与 `yss-component-mybatis-starter` 配合，自动触发分页插件。

### 3. DTO 基类

- **CommandDTO**: 所有写操作（增删改）参数的基类。
- **QueryDTO**: 所有读操作（查询）参数的基类，继承自 `CommandDTO`。

## 使用指南

### 1. 定义 Controller 接口

```java
@PostMapping("/list")
public Result<List<User>> list(@RequestBody UserPageQuery query) {
    return Result.buildSuccess(userService.list(query));
}
```

### 2. 定义查询参数

```java
public class UserPageQuery extends PageQuery {
    private String username;
    // getter/setter
}
```

### 3. 构建响应

```java
// 成功
return Result.buildSuccess("操作成功");

// 失败
return Result.buildFailure("参数错误");
```

## 常见问题

- **Q: `PageQuery` 中的 `tempTotalCount` 是什么？**
  - A: 这是一个内部字段，由分页插件在执行查询后自动回填总记录数，通常不需要手动设置。
- **Q: 为什么要继承 `CommandDTO` / `QueryDTO`？**
  - A: 为了保持代码规范和语义清晰，同时也为未来可能的统一处理（如序列化、审计）预留扩展点。

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
- 核心代码资产：[assets](./assets/)
