---
name: "yss-cache"
description: "yss-component-cache-parent 框架专家指南。当用户询问有关缓存配置、实现原理或最佳实践时调用。"
---

# yss-cache

本技能提供关于 `yss-component-cache-parent` 框架的专家级知识，该框架是 YSS Cloud 微服务平台的统一缓存管理解决方案。

## 概述

`yss-component-cache-parent` 对底层缓存实现（Spring Cache, JetCache）进行了抽象，并提供了统一的多级缓存接口（L1 本地 + L2 远程）。

### 核心特性

- **多级缓存**：支持 L1 (Caffeine/Local) 和 L2 (Redis) 缓存。
- **动态路由**：通过配置 (`yss.cache.activeType`) 在 Redis 和 Caffeine 之间切换。
- **高可用性**：内置 Redis 健康检查机制，支持自动降级。
- **统一注解**：扩展了 Spring Cache 的自定义注解（`@QueryCache`, `@UpdateCache`, `@ClearCache`）。

## 核心组件

### 1. 注解

- **@EnableYssCloudRedisCache**：开启缓存框架。引入 Redis 和 Caffeine 的配置。
- **@QueryCache**：等同于 `@Cacheable`。支持 `cacheNames` (使用 `CacheKeyCode`)、`key`、`condition` 等属性。
- **@ClearCache**：等同于 `@CacheEvict`。
- **@UpdateCache**：等同于 `@CachePut`。

### 2. 基础设施类

- **CacheManagerCompose**：管理 `CaffeineCacheManager` 和 `RedisCacheManager`。实现了降级逻辑和健康检查。
- **CacheComposeResolver**：实现 `CacheResolver` 接口。根据 `yss.cache.activeType` 动态选择激活的 `CacheManager`。
- **YssCacheAnnotationParser**：解析自定义注解，将其注册到 Spring 的缓存基础设施中。

## 配置

### application.yml / bootstrap.yml

```yaml
yss:
  cache:
    activeType: redis # 选项: redis, caffeine. 默认值: redis

spring:
  redis:
    host: localhost
    port: 6379
    password: ...
```

### JetCache 配置 (如果使用 `yss-component-jetcache`)

```yaml
jetcache:
  statIntervalMinutes: 1
  areaInCacheName: false
  local:
    default:
      type: linkedhashmap
      keyConvertor: jackson
  remote:
    default:
      type: redis
      keyConvertor: jackson
      broadcastChannel: yss:datamiddle
      keyPrefix: yss:datamiddle
```

## 实现细节

### 缓存路由

框架不强制使用单一的缓存实现。相反，`CacheComposeResolver` 在运行时检查 `yss.cache.activeType`，决定是从 `RedisCacheManager` 还是 `CaffeineCacheManager` 获取缓存实例。

### Redis 健康检查

`CacheManagerCompose` 启动一个定时任务（每20秒），检查 Redis 连接性。如果 Redis 宕机，`redisHealthCheck` 标志将被设置为 `false`，从而阻止后续的 Redis 调用，避免应用阻塞。

### JetCache 集成

当使用 `yss-component-jetcache` 时，`CacheManagerCompose` (JetCache 版本) 使用 `QuickConfig` 动态创建缓存实例。它支持 `local` 和 `remote` 缓存类型，通过 Redis Pub/Sub 实现两级缓存的自动同步。

## 使用指南

1. **添加依赖**：
   - 标准用法：`yss-component-cache-starter`
   - 高级特性 (JetCache)：`yss-component-jetcache`

2. **开启缓存**：
   在 Spring Boot 应用启动类上添加 `@EnableYssCloudRedisCache`。

3. **使用注解**：
   ```java
   @Service
   public class MyService {
       @QueryCache(cacheNames = CacheKeyCode.DATA_MIDDLE_CACHE_DEFAULT, key = "#id")
       public User getUser(String id) {
           // ...
       }
   }
   ```

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
