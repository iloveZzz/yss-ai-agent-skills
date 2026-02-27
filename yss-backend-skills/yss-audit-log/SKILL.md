---
name: "yss-audit-log"
description: "yss-component-audit-log 审计日志组件专家指南。当用户询问如何记录操作审计、配置 AuditLog 注解、SpEL 日志解析或日志分发机制时调用。"
---

# yss-audit-log

本技能提供关于 `yss-component-audit-log` 审计日志组件的专家级知识。该组件支持基于注解的非侵入式日志收集，并提供异步的日志发布和订阅处理机制。

## 概述

`yss-component-audit-log` 通过 AOP 切面技术拦截带有 `@AuditLog` 注解的方法，自动收集操作上下文信息（用户信息、IP、请求参数、返回结果等），并异步发送至指定的订阅者（如系统管理服务）。

## 核心特性

- **非侵入式**: 使用 `@AuditLog` 注解即可开启审计，无需修改业务逻辑。
- **动态描述**: 支持 SpEL 表达式（如 `#{参数名.字段}`），动态生成审计日志摘要。
- **异步处理**: 内部使用阻塞队列和线程池，确保审计日志收集不影响主业务性能。
- **多订阅支持**: 内置控制台打印和系统管理服务发送两种模式，支持自定义扩展。

## 核心组件

### 1. 关键注解
- **@EnableAuditLog**: 开启审计日志功能。可配置是否发送至系统管理、是否打印控制台日志。
- **@AuditLog**: 核心注解，用于标记审计方法。包含 `operation` (类型), `summary` (描述), `resource` (资源类型) 等属性。

### 2. 基础设施类
- **AuditLogAspect**: 审计切面，负责拦截、信息收集及 SpEL 表达式解析。
- **YssAuditPublishService**: 异步发布服务，负责将日志消息入队并分发给订阅者。
- **YssAuditSubscriber**: 订阅者接口，实现此接口可自定义日志处理逻辑。

## 使用指南

### 1. 开启审计功能
在启动类添加注解：
```java
@EnableAuditLog(sendSysManageEnabled = true)
public class Application {}
```

### 2. 在业务方法上添加注解
```java
@Service
public class UserServiceImpl implements UserService {

    @AuditLog(
        operation = AuditOperationType.UPDATE,
        summary = "更新用户: #{user.userName}", // 使用 SpEL
        resource = AuditResourceType.USER
    )
    public void updateUser(User user) {
        // ...
    }
}
```

### 3. 配置说明
**application.yml**:
```yaml
yss:
  audit:
    enabled: true                # 是否开启审计总开关
    sendSysManageEnabled: true   # 是否发送至系统管理
    auditLogPrintEnabled: false  # 是否打印到控制台
```

## 常见问题

- **Q: 为什么 SpEL 表达式不解析？**
  - A: 确保表达式格式为 `#{...}`，且变量名与方法参数名一致。注意：需要开启编译参数 `-parameters` 以保留参数名。
- **Q: 审计日志收集是实时的吗？**
  - A: 收集是切面实时触发的，但分发和处理是异步的，不会阻塞主流程。
- **Q: 如何增加新的日志处理方式？**
  - A: 实现 `YssAuditSubscriber` 接口并将其注册为 Spring Bean，`YssAuditPublishService` 会自动发现并调用。

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
- 核心代码资产：[assets](./assets/)
