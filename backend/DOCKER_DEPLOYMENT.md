# Docker部署指南

## 前置要求
- Docker 24.0+
- Docker Compose 2.0+

## 快速开始

### 1. 启动所有服务
cd backend
start_all_services.bat

### 2. 停止所有服务
stop_all_services.bat

### 3. 查看服务日志
docker-compose logs -f

## 服务列表
- MySQL: 3306
- Redis: 6379
- auth-service: 8001
- user-service: 8002
- permission-service: 8003
- system-service: 8004
- support-service: 8005
- business-service: 8006
