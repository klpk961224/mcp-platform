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
- auth-service: 28001
- user-service: 28002
- permission-service: 28003
- system-service: 28004
- support-service: 28005
- business-service: 28006

