# -*- coding: utf-8 -*-
"""
Alembic环境配置

功能说明：
1. 数据库迁移环境配置
2. 自动生成迁移脚本
3. 数据库连接管理

使用示例：
    alembic revision --autogenerate -m "创建用户表"
    alembic upgrade head
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 导入模型（用于自动生成迁移）
from app.models import Base
from app.core.config import settings

# 导入数据库连接
from common.database import datasource_manager

# Alembic配置对象
config = context.config

# 设置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 添加模型的MetaData
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    离线模式运行迁移
    
    使用方法：
        alembic upgrade head --sql
    """
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
    """
    在线模式运行迁移
    
    使用方法：
        alembic upgrade head
    """
    # 使用数据源管理器的引擎
    engine = datasource_manager.get_engine('mysql')

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()