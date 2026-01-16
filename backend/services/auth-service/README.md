# 认证域服务 (auth-service)

## 服务说明

认证域服务负责处理用户认证、Token管理和用户登录登出等核心认证功能。

## 功能特性

- ✅ 用户登录/登出
- ✅ JWT Token生成和验证
- ✅ Token刷新机制
- ✅ 密码加密和验证
- ✅ 用户状态管理
- ✅ 多租户支持
- ✅ API Key认证

## 技术栈

- **框架**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: MySQL 8.0+
- **缓存**: Redis 7.0+
- **日志**: loguru 0.7+

## 项目结构

```
auth-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── api/                  # API路由
│   │   └── v1/
│   │       └── auth.py      # 认证API
│   ├── core/                 # 核心配置
│   │   ├── config.py        # 配置类
│   │   └── deps.py          # 依赖注入
│   ├── models/               # SQLAlchemy模型
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   └── token.py         # Token模型
│   ├── schemas/              # Pydantic模型
│   │   ├── __init__.py
│   │   └── auth.py          # 认证Schema
│   ├── services/             # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py  # 认证服务
│   │   └── token_service.py # Token服务
│   └── repositories/         # 数据访问层
│       ├── __init__.py
│       ├── user_repository.py    # 用户数据访问
│       └── token_repository.py   # Token数据访问
├── tests/                     # 测试目录
│   ├── unit/               # 单元测试
│   └── integration/        # 集成测试
├── alembic/                   # 数据库迁移
│   ├── env.py              # 迁移环境配置
│   ├── script.py.mako      # 迁移脚本模板
│   └── versions/           # 迁移版本
├── scripts/                   # 脚本工具
├── .env.development          # 开发环境配置
├── .env.production           # 生产环境配置
├── Dockerfile                # Docker配置
├── docker-compose.yml        # Docker编排
├── requirements.txt          # Python依赖
└── README.md                 # 本文件
```

## 快速开始

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.development .env

# 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Docker部署

```bash
# 构建镜像
docker build -t auth-service:latest .

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f auth-service
```

## API接口

### 健康检查

- `GET /health` - 健康检查接口

### 认证接口

- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新Token
- `POST /api/v1/auth/logout` - 用户登出

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| APP_NAME | 应用名称 | 认证域服务 |
| APP_ENV | 环境类型 | development |
| APP_DEBUG | 调试模式 | True |
| APP_PORT | 服务端口 | 8001 |
| DATABASE_URL | 数据库连接URL | - |
| REDIS_HOST | Redis主机 | 127.0.0.1 |
| REDIS_PORT | Redis端口 | 6379 |
| JWT_SECRET | JWT密钥 | - |
| JWT_EXPIRE_MINUTES | Token过期时间（分钟） | 1440 |
| REFRESH_TOKEN_EXPIRE_DAYS | 刷新Token过期时间（天） | 30 |

## 数据库迁移

```bash
# 生成迁移脚本
alembic revision --autogenerate -m "创建用户表"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit

# 运行集成测试
pytest tests/integration

# 生成测试报告
pytest --html=reports/test-report.html
```

## 开发规范

- 遵循 PEP 8 代码规范
- 使用类型注解
- 编写单元测试
- 添加日志记录
- 编写文档注释

## 常见问题

### 数据库连接失败

检查 MySQL 服务是否启动，数据库配置是否正确。

### Token验证失败

检查 JWT_SECRET 配置是否正确，Token是否过期。

### 依赖安装失败

尝试使用虚拟环境，或者升级 pip 版本。

## 联系方式

- 项目地址: https://github.com/klpk961224/mcp-platform
- 问题反馈: 提交 Issue

---

**最后更新**: 2026-01-15