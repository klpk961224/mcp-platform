# Docker本地部署指南

## 部署架构

本部署方案适用于MySQL和Redis已部署在宿主机上的场景。

### 服务配置

- **网络模式**: host（所有服务共享宿主机IP）
- **数据库**: 使用宿主机的MySQL（localhost:3306）
- **缓存**: 使用宿主机的Redis（localhost:6379）
- **服务IP**: 所有服务都在宿主机IP上，端口为28001-28006

### 服务列表

| 服务名称 | 端口 | 说明 |
|---------|------|------|
| 认证服务 | 28001 | JWT认证、API Key认证 |
| 用户服务 | 28002 | 用户CRUD、部门管理 |
| 权限服务 | 28003 | 角色管理、权限分配 |
| 系统服务 | 28004 | MCP工具注册、数据源管理 |
| 支撑服务 | 28005 | 待办任务、日志管理 |
| 业务服务 | 28006 | 工作流管理、审批流程 |

## 前置条件

### 1. 安装Docker
确保已安装Docker Desktop或Docker Engine：
```bash
docker --version
```

### 2. 启动MySQL和Redis
确保宿主机的MySQL和Redis服务已启动：
```bash
# 检查MySQL
mysql -h localhost -u root -p

# 检查Redis
redis-cli ping
```

### 3. 创建数据库
```sql
CREATE DATABASE mcp_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 快速部署

### 启动所有服务
```bash
cd backend
start_all_services.bat
```

### 查看服务状态
```bash
docker-compose ps
```

### 查看服务日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f auth-service
docker-compose logs -f user-service
```

### 停止所有服务
```bash
stop_all_services.bat
```

## 服务访问

所有服务都在宿主机IP上访问：

### 健康检查
```bash
# 认证服务
http://localhost:28001/health

# 用户服务
http://localhost:28002/health

# 权限服务
http://localhost:28003/health

# 系统服务
http://localhost:28004/health

# 支撑服务
http://localhost:28005/health

# 业务服务
http://localhost:28006/health
```

### API文档
```bash
# 认证服务
http://localhost:28001/docs

# 用户服务
http://localhost:28002/docs

# 权限服务
http://localhost:28003/docs

# 系统服务
http://localhost:28004/docs

# 支撑服务
http://localhost:28005/docs

# 业务服务
http://localhost:28006/docs
```

## 环境变量配置

### 认证服务
```bash
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/mcp_platform
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 用户服务
```bash
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/mcp_platform
REDIS_HOST=localhost
REDIS_PORT=6379
AUTH_SERVICE_URL=http://localhost:28001/api/v1
```

### 权限服务
```bash
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/mcp_platform
REDIS_HOST=localhost
REDIS_PORT=6379
AUTH_SERVICE_URL=http://localhost:28001/api/v1
```

### 系统服务
```bash
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/mcp_platform
REDIS_HOST=localhost
REDIS_PORT=6379
AUTH_SERVICE_URL=http://localhost:28001/api/v1
```

### 支撑服务
```bash
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/mcp_platform
REDIS_HOST=localhost
REDIS_PORT=6379
AUTH_SERVICE_URL=http://localhost:28001/api/v1
```

### 业务服务
```bash
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/mcp_platform
REDIS_HOST=localhost
REDIS_PORT=6379
AUTH_SERVICE_URL=http://localhost:28001/api/v1
```

## 常见问题

### 1. 服务无法连接MySQL
**原因**: MySQL未启动或防火墙阻止连接

**解决方案**:
```bash
# 检查MySQL是否启动
netstat -ano | findstr "3306"

# 检查MySQL连接
mysql -h localhost -u root -p
```

### 2. 服务无法连接Redis
**原因**: Redis未启动或防火墙阻止连接

**解决方案**:
```bash
# 检查Redis是否启动
netstat -ano | findstr "6379"

# 检查Redis连接
redis-cli ping
```

### 3. 服务启动失败
**原因**: 端口被占用

**解决方案**:
```bash
# 检查端口占用
netstat -ano | findstr "28001 28002 28003 28004 28005 28006"

# 停止占用端口的进程
taskkill /F /PID <进程ID>
```

### 4. 服务间无法通信
**原因**: 使用host网络模式，服务间通过localhost通信

**解决方案**: 确保所有服务都使用`network_mode: host`配置，并且依赖服务已启动

## 网络说明

### Host网络模式
- 所有服务共享宿主机的网络栈
- 服务直接使用宿主机的IP和端口
- 服务间通过localhost相互访问
- 优势：性能最好，无网络转换开销
- 注意：端口不能冲突

### 服务间通信
```
用户服务 → 认证服务: http://localhost:28001/api/v1
权限服务 → 认证服务: http://localhost:28001/api/v1
系统服务 → 认证服务: http://localhost:28001/api/v1
支撑服务 → 认证服务: http://localhost:28001/api/v1
业务服务 → 认证服务: http://localhost:28001/api/v1
```

## 防火墙配置

如果需要从外部访问服务，需要开放防火墙端口：

```bash
# Windows防火墙
netsh advfirewall firewall add rule name="MCP Platform" dir=in action=allow protocol=TCP localport=28001,28002,28003,28004,28005,28006
```

## 监控和日志

### 查看容器资源使用
```bash
docker stats
```

### 查看容器日志
```bash
# 实时查看
docker-compose logs -f

# 查看最近100行
docker-compose logs --tail=100

# 查看特定时间段的日志
docker-compose logs --since 2024-01-01T00:00:00
```

### 进入容器调试
```bash
# 认证服务
docker exec -it mcp-auth-service bash

# 用户服务
docker exec -it mcp-user-service bash
```

## 更新和重启

### 更新服务代码
```bash
# 1. 停止服务
docker-compose down

# 2. 重新构建并启动
docker-compose up -d --build

# 3. 查看日志确认启动成功
docker-compose logs -f
```

### 重启单个服务
```bash
# 重启认证服务
docker-compose restart auth-service

# 重启用户服务
docker-compose restart user-service
```

## 备份和恢复

### 备份数据库
```bash
# 备份MySQL数据库
mysqldump -h localhost -u root -p mcp_platform > backup_$(date +%Y%m%d).sql
```

### 恢复数据库
```bash
# 恢复MySQL数据库
mysql -h localhost -u root -p mcp_platform < backup_20240101.sql
```

## 性能优化

### 调整容器资源限制
在docker-compose.yml中添加资源限制：
```yaml
services:
  auth-service:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### 启用日志轮转
```yaml
services:
  auth-service:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 安全建议

1. **修改默认密码**: 修改MySQL root密码
2. **使用环境变量**: 敏感信息使用环境变量配置
3. **限制网络访问**: 使用防火墙限制外部访问
4. **定期更新**: 定期更新Docker镜像和依赖
5. **监控日志**: 定期检查服务日志，发现异常及时处理