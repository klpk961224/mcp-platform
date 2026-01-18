# 企业级AI综合管理平台 - 项目结构说明

## 📋 文档信息

- **项目名称**：企业级AI综合管理平台
- **文档版本**：v1.1
- **创建日期**：2026-01-15
- **最后更新**：2026-01-18
- **文档类型**：项目结构说明文档

---

## 1. 概述

本项目采用**企业级FastAPI微服务框架**，遵循标准的分层架构设计，确保代码的可维护性、可扩展性和可测试性。

### 1.1 架构特点

- ✅ **微服务架构**：6个独立的微服务，每个服务负责特定的业务功能
- ✅ **分层架构**：API路由层、业务逻辑层、数据访问层、数据模型层
- ✅ **Repository模式**：封装数据访问逻辑，提高代码复用性
- ✅ **Service模式**：封装业务逻辑，提高代码可维护性
- ✅ **依赖注入**：使用FastAPI的依赖注入系统，提高代码可测试性
- ✅ **统一配置**：使用Pydantic进行配置管理，支持多环境配置
- ✅ **数据库迁移**：使用Alembic进行数据库版本管理
- ✅ **容器化部署**：支持Docker和Docker Compose部署

### 1.2 技术栈

| 技术组件 | 版本 | 用途 |
|---------|------|------|
| **Python** | 3.13+ | 编程语言 |
| **FastAPI** | 0.104+ | Web框架 |
| **SQLAlchemy** | 2.0+ | ORM框架 |
| **Pydantic** | 2.0+ | 数据验证 |
| **Alembic** | 1.12+ | 数据库迁移 |
| **MySQL** | 8.0+ | 主数据库 |
| **Redis** | 7.0+ | 缓存 |
| **RabbitMQ** | 3.12+ | 消息队列 |
| **Docker** | 24.0+ | 容器化 |

---

## 2. 整体目录结构

```
backend/
├── common/                          # 共享代码库（所有服务共用）
│   ├── cache/                       # 缓存模块
│   ├── config/                      # 配置模块
│   ├── database/                    # 数据库模块
│   ├── decorators/                  # 装饰器
│   ├── exceptions/                  # 异常类
│   ├── middleware/                  # 中间件
│   ├── responses/                   # 响应模块
│   ├── security/                    # 安全模块
│   └── utils/                       # 工具模块
│
├── services/                        # 微服务目录
│   ├── auth-service/                # 认证域服务（8001）
│   ├── user-service/                # 用户域服务（8002）
│   ├── permission-service/          # 权限域服务（8003）
│   ├── system-service/              # 系统域服务（8004）
│   ├── support-service/             # 支撑域服务（8005）
│   └── business-service/            # 业务域服务（8006）
│
├── tests/                           # 集成测试
├── scripts/                         # 工具脚本
│   ├── init_db.sql                 # 数据库表结构初始化脚本
│   ├── execute_init_db.py          # 执行数据库表结构初始化
│   ├── init_data.py                # 初始化默认数据（超级管理员、角色权限等）
│   └── ...                         # 其他工具脚本
├── alembic.ini                      # Alembic全局配置
├── docker-compose.yml               # Docker编排配置（6个微服务）
├── start_services.bat               # 启动所有服务
├── stop_services.bat                # 停止所有服务
├── run_tests.bat                    # 运行测试
└── __init__.py                      # 包初始化文件
```

---

## 3. 共享代码库（common/）

共享代码库包含所有微服务共用的代码，避免重复开发，提高代码复用性。

### 3.1 目录结构

```
common/
├── cache/                           # 缓存模块
│   ├── local.py                     # 本地缓存实现
│   └── redis.py                     # Redis缓存实现
│
├── config/                          # 配置模块
│   ├── __init__.py
│   ├── constants.py                 # 常量定义
│   └── settings.py                  # 配置类（Pydantic）
│
├── database/                        # 数据库模块
│   ├── __init__.py
│   ├── base.py                      # 基础模型类（BaseModel）
│   ├── connection.py                # 多数据源管理器
│   ├── pandas_helper.py             # Pandas数据分析助手
│   ├── session.py                   # 数据库会话管理
│   ├── transaction.py               # 跨数据源事务管理（Saga模式）
│   └── models/                      # 共享数据模型
│       ├── __init__.py
│       ├── permission.py            # 权限相关模型
│       ├── system.py                # 系统相关模型
│       ├── tenant.py                # 租户相关模型
│       ├── todo.py                  # 待办任务模型
│       ├── user.py                  # 用户相关模型
│       └── workflow.py              # 工作流相关模型
│
├── decorators/                      # 装饰器
│   ├── __init__.py
│   ├── cache.py                     # 缓存装饰器
│   └── permission.py                # 权限装饰器
│
├── exceptions/                      # 异常类
│   ├── __init__.py
│   └── base.py                      # 基础异常类
│
├── middleware/                      # 中间件
│   ├── __init__.py
│   ├── auth.py                      # 认证中间件
│   ├── exception.py                 # 异常处理中间件
│   └── logging.py                   # 日志中间件
│
├── responses/                       # 响应模块
│   ├── __init__.py
│   └── base.py                      # 统一响应格式
│
├── security/                        # 安全模块
│   ├── __init__.py
│   ├── api_key.py                   # API Key管理
│   ├── jwt.py                       # JWT工具
│   └── password.py                  # 密码加密
│
└── utils/                           # 工具模块
    ├── __init__.py
    ├── datetime.py                  # 日期时间工具
    ├── helpers.py                   # 辅助函数
    └── validators.py                # 验证器
```

### 3.2 核心模块说明

#### 3.2.1 数据库模块（database/）

**base.py** - 基础模型类
```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

BaseModel = declarative_base()

class BaseModel(BaseModel):
    """所有数据模型的基类"""
    
    __abstract__ = True
    
    id = Column(String(64), primary_key=True, comment="主键ID")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
```

**connection.py** - 多数据源管理器
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Dict, Optional

class DatasourceManager:
    """多数据源管理器"""
    
    def __init__(self):
        self.engines: Dict[str, Any] = {}
        self.session_makers: Dict[str, Any] = {}
    
    def register_datasource(
        self,
        name: str,
        db_type: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        pool_size: int = 10,
        max_overflow: int = 20,
        echo: bool = False
    ):
        """注册数据源"""
        # 创建数据库连接URL
        if db_type == "mysql":
            url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "postgresql":
            url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "oracle":
            url = f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        # 创建引擎
        engine = create_engine(
            url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo
        )
        
        # 创建会话工厂
        session_maker = sessionmaker(bind=engine)
        
        # 保存
        self.engines[name] = engine
        self.session_makers[name] = session_maker
    
    def get_session(self, name: str) -> Session:
        """获取数据库会话"""
        if name not in self.session_makers:
            raise ValueError(f"未找到数据源: {name}")
        return self.session_makers[name]()
    
    def close_all(self):
        """关闭所有连接"""
        for engine in self.engines.values():
            engine.dispose()

# 全局数据源管理器实例
datasource_manager = DatasourceManager()
```

#### 3.2.2 配置模块（config/）

**settings.py** - 配置类
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用配置
    APP_NAME: str = "MCP Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/mcp_platform"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_ENABLED: bool = False
    CACHE_TYPE: str = "local"  # local or redis
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # RabbitMQ配置
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    USE_RABBITMQ: bool = False
    
    # Nacos配置
    NACOS_SERVER: str = "localhost:8848"
    USE_NACOS: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 全局配置实例
settings = Settings()
```

#### 3.2.3 安全模块（security/）

**jwt.py** - JWT工具
```python
from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
from common.config.settings import settings

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
```

---

## 4. 微服务结构

每个微服务都遵循统一的目录结构，确保代码的一致性和可维护性。

### 4.1 标准目录结构

```
{service-name}/
├── app/                             # 应用主目录
│   ├── api/                         # API路由层
│   │   └── v1/                      # API版本1
│   │       └── {module}.py          # 模块API
│   ├── core/                        # 核心配置
│   │   ├── config.py                # 服务配置
│   │   ├── deps.py                  # 依赖注入
│   │   └── security.py              # 安全配置
│   ├── models/                      # 数据模型层（SQLAlchemy ORM）
│   │   ├── __init__.py
│   │   └── {module}.py              # 模块模型
│   ├── repositories/                # 数据访问层
│   │   ├── __init__.py
│   │   └── {module}_repository.py   # 模块数据访问
│   ├── schemas/                     # Pydantic模型（请求/响应验证）
│   │   ├── __init__.py
│   │   └── {module}.py              # 模块Schema
│   ├── services/                    # 业务逻辑层
│   │   ├── __init__.py
│   │   └── {module}_service.py      # 模块业务逻辑
│   └── main.py                      # FastAPI应用入口
│
├── alembic/                         # 数据库迁移
│   ├── env.py                       # 迁移环境配置
│   ├── script.py.mako               # 迁移模板
│   └── versions/                    # 迁移版本文件
│
├── scripts/                         # 工具脚本
├── tests/                           # 测试目录
│   ├── unit/                        # 单元测试
│   │   └── __init__.py
│   └── integration/                 # 集成测试
│       └── __init__.py
│
├── .env.development                 # 开发环境配置
├── .env.production                  # 生产环境配置
├── docker-compose.yml               # Docker编排
├── Dockerfile                       # Docker镜像构建
├── requirements.txt                 # Python依赖
└── README.md                        # 服务文档
```

### 4.2 分层架构详解

#### 4.2.1 API路由层（api/）

**职责**：
- 接收HTTP请求
- 参数验证（Pydantic Schema）
- 调用业务逻辑层
- 返回HTTP响应

**示例代码**：
```python
# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.core.deps import get_db

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/", response_model=UserResponse, summary="创建用户")
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """创建新用户"""
    user_service = UserService(db)
    user = user_service.create(user_data)
    return user

@router.get("/{user_id}", response_model=UserResponse, summary="获取用户")
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取用户详情"""
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

#### 4.2.2 业务逻辑层（services/）

**职责**：
- 实现业务逻辑
- 协调多个Repository
- 实现事务管理
- 业务规则验证

**示例代码**：
```python
# app/services/user_service.py
from typing import Optional, List
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.schemas.user import UserCreate

class UserService:
    """用户业务逻辑服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
    
    def create(self, user_data: UserCreate) -> User:
        """创建用户
        
        业务逻辑：
        1. 验证部门是否存在
        2. 创建用户
        3. 分配默认角色
        """
        # 验证部门
        if user_data.department_id:
            dept = self.dept_repo.get_by_id(user_data.department_id)
            if not dept:
                raise ValueError("部门不存在")
        
        # 创建用户
        user = self.user_repo.create(user_data)
        
        # 分配默认角色（可选）
        # self.role_repo.assign_default_role(user.id)
        
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        return self.user_repo.get_by_id(user_id)
```

#### 4.2.3 数据访问层（repositories/）

**职责**：
- 封装数据库操作
- 提供CRUD方法
- 实现查询逻辑
- 数据缓存（可选）

**示例代码**：
```python
# app/repositories/user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    """用户数据访问层"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    def create(self, user_data: dict) -> User:
        """创建用户"""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: str, user_data: dict) -> Optional[User]:
        """更新用户"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str) -> bool:
        """删除用户"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return self.db.query(User).offset(skip).limit(limit).all()
```

#### 4.2.4 数据模型层（models/）

**职责**：
- 定义数据库表结构
- 实现ORM映射
- 定义表关系
- 数据验证

**示例代码**：
```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from common.database.base import BaseModel

class User(BaseModel):
    """用户模型"""
    
    __tablename__ = "users"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    username = Column(String(50), nullable=False, unique=True, index=True, comment="用户名")
    email = Column(String(100), nullable=False, index=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    
    # 用户信息
    full_name = Column(String(100), nullable=True, comment="全名")
    phone = Column(String(20), nullable=True, comment="手机号")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="active", comment="状态（active/disabled）")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    
    # 部门和岗位
    department_id = Column(String(64), nullable=True, comment="部门ID")
    position_id = Column(String(64), nullable=True, comment="岗位ID")
    
    # 扩展信息
    bio = Column(Text, nullable=True, comment="个人简介")
    preferences = Column(Text, nullable=True, comment="用户偏好设置（JSON）")
    
    # 关系
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
```

### 4.3 依赖注入（deps.py）

**职责**：
- 提供数据库会话
- 提供认证信息
- 提供其他依赖项

**示例代码**：
```python
# app/core/deps.py
from typing import Optional, Generator
from sqlalchemy.orm import Session
from common.database.connection import datasource_manager
from app.core.security import verify_token

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    session = None
    try:
        session = datasource_manager.get_session('mysql')
        yield session
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user
```

### 4.4 应用入口（main.py）

**职责**：
- 创建FastAPI应用
- 注册路由
- 配置中间件
- 配置事件处理

**示例代码**：
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from common.config.settings import settings
from common.database.connection import datasource_manager
from app.api.v1 import auth

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="企业级AI综合管理平台 - 认证域服务"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # 注册数据源
    try:
        db_url = settings.DATABASE_URL
        if db_url.startswith("mysql+pymysql://"):
            # 解析连接字符串
            url_without_prefix = db_url.replace("mysql+pymysql://", "")
            auth_part, host_port_db = url_without_prefix.split("@")
            username, password = auth_part.split(":")
            host_port, database = host_port_db.split("/")
            host, port = host_port.split(":")
            
            datasource_manager.register_datasource(
                name='mysql',
                db_type='mysql',
                host=host,
                port=int(port),
                username=username,
                password=password,
                database=database,
                pool_size=10,
                max_overflow=20,
                echo=False
            )
            logger.info("数据源注册成功")
    except Exception as e:
        logger.error(f"数据源注册失败: {e}")
        raise

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("关闭应用")
    datasource_manager.close_all()

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "auth-service"}
```

---

## 5. 微服务列表

| 服务名称 | 端口 | 职责 | 主要功能 |
|---------|------|------|---------|
| **auth-service** | 8001 | 认证域服务 | JWT认证、API Key认证、权限校验、Token管理 |
| **user-service** | 8002 | 用户域服务 | 用户CRUD、部门管理、租户管理、用户与部门/角色关联 |
| **permission-service** | 8003 | 权限域服务 | 角色管理、权限分配、菜单管理、动态菜单加载 |
| **system-service** | 8004 | 系统域服务 | MCP工具注册/调用、多数据源管理、字典管理、系统配置 |
| **support-service** | 8005 | 支撑域服务 | 登录日志、操作日志、站内信、通知公告、待办任务管理 |
| **business-service** | 8006 | 业务域服务 | 工作流管理（审批流程、可视化设计器、审批任务管理） |

---

## 6. 数据库迁移（Alembic）

### 6.1 Alembic配置

**alembic/env.py** - 迁移环境配置
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from common.database.base import BaseModel
from app.models import *  # 导入所有模型

# Alembic Config对象
config = context.config

# 设置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据
target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    """离线运行迁移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """在线运行迁移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 6.2 创建迁移

```bash
# 创建迁移脚本
alembic revision --autogenerate -m "create users table"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

---

## 7. 测试

### 7.1 测试目录结构

```
tests/
├── unit/                           # 单元测试
│   ├── __init__.py
│   ├── test_user_service.py
│   └── test_user_repository.py
│
└── integration/                    # 集成测试
    ├── __init__.py
    ├── test_user_api.py
    └── test_auth_api.py
```

### 7.2 测试示例

**单元测试**：
```python
# tests/unit/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.schemas.user import UserCreate

def test_create_user(db_session):
    """测试创建用户"""
    user_service = UserService(db_session)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )
    
    user = user_service.create(user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.id is not None
```

**集成测试**：
```python
# tests/integration/test_user_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """测试创建用户API"""
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
```

---

## 8. 部署

### 8.1 Docker部署

**Dockerfile**：
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8001

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**docker-compose.yml**：
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: mcp_platform
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7.0
    ports:
      - "6379:6379"

  auth-service:
    build: ./services/auth-service
    ports:
      - "8001:8001"
    depends_on:
      - mysql
      - redis
    environment:
      - DATABASE_URL=mysql+pymysql://root:root@mysql:3306/mcp_platform
      - REDIS_URL=redis://redis:6379/0

volumes:
  mysql_data:
```

### 8.2 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 9. 最佳实践

### 9.1 代码规范

- ✅ 遵循PEP 8规范
- ✅ 使用类型提示（Type Hints）
- ✅ 编写文档字符串（Docstrings）
- ✅ 使用有意义的变量名和函数名
- ✅ 避免过度嵌套

### 9.2 错误处理

- ✅ 使用自定义异常类
- ✅ 统一的异常处理中间件
- ✅ 详细的错误日志
- ✅ 友好的错误消息

### 9.3 性能优化

- ✅ 使用数据库连接池
- ✅ 使用缓存（Redis）
- ✅ 异步处理（RabbitMQ）
- ✅ 数据库索引优化

### 9.4 安全性

- ✅ 使用JWT认证
- ✅ 密码加密存储
- ✅ SQL注入防护
- ✅ XSS防护
- ✅ CSRF防护

### 9.5 日志记录

- ✅ 使用结构化日志（loguru）
- ✅ 记录关键操作
- ✅ 记录异常信息
- ✅ 日志分级管理

---

## 10. 常见问题

### Q1: 如何添加新的微服务？

1. 在 `backend/services/` 下创建新的服务目录
2. 按照标准目录结构创建子目录和文件
3. 实现 `app/main.py` 作为应用入口
4. 创建 `requirements.txt` 和配置文件
5. 创建 `Dockerfile` 和 `docker-compose.yml`
6. 编写测试用例

### Q2: 如何添加新的API接口？

1. 在 `app/api/v1/` 下创建或修改路由文件
2. 使用FastAPI Router定义路由
3. 使用Pydantic Schema定义请求/响应模型
4. 在Service层实现业务逻辑
5. 在Repository层实现数据访问
6. 编写测试用例

### Q3: 如何添加新的数据库表？

1. 在 `app/models/` 下创建新的模型文件
2. 继承 `BaseModel` 类
3. 定义表结构和字段
4. 创建Alembic迁移脚本
5. 执行迁移
6. 编写测试用例

### Q4: 如何调试代码？

1. 使用 `print()` 或 `logger.info()` 输出调试信息
2. 使用IDE的调试功能（断点调试）
3. 查看日志文件
4. 使用FastAPI的自动文档（Swagger UI）
5. 使用Postman或curl测试API

---

## 🔗 相关文档

- [技术架构设计文档](../doc/2-技术架构设计文档.md)
- [数据库设计文档](../doc/3-数据库设计文档.md)
- [API接口设计文档](../doc/4-API接口设计文档.md)
- [开发规范文档](../doc/6-开发规范文档.md)
- [环境配置文档](../doc/7-环境配置文档.md)

---

## 💡 注意事项

1. **代码复用**：优先使用 `common/` 中的共享代码，避免重复开发
2. **分层清晰**：严格遵守分层架构，不要跨层调用
3. **依赖注入**：使用FastAPI的依赖注入系统，提高代码可测试性
4. **数据库会话**：使用 `get_db()` 依赖注入获取数据库会话，不要手动创建
5. **事务管理**：在Service层管理事务，不要在Repository层管理
6. **异常处理**：使用自定义异常类，统一异常处理
7. **日志记录**：使用 `loguru` 记录日志，不要使用 `print()`
8. **测试覆盖**：编写单元测试和集成测试，保证代码质量
9. **文档更新**：代码变更时及时更新文档，保持文档与代码同步
10. **版本控制**：使用Git进行版本控制，遵循Git Flow工作流

---

**文档版本历史**：

| 版本 | 日期 | 作者 | 变更说明 |
|-----|------|------|---------|
| v1.0 | 2026-01-15 | AI助手 | 初始版本，记录企业级项目结构 |
| v1.1 | 2026-01-18 | AI助手 | 更新Docker配置，添加数据初始化脚本说明 |

---

**最后更新时间**：2026-01-18
**下次更新时间**：项目结构变更时