# -*- coding: utf-8 -*-
"""
Alembic鐜閰嶇疆

鍔熻兘璇存槑锛?1. 鏁版嵁搴撹縼绉荤幆澧冮厤缃?2. 鑷姩鐢熸垚杩佺Щ鑴氭湰
3. 鏁版嵁搴撹繛鎺ョ鐞?
浣跨敤绀轰緥锛?    alembic revision --autogenerate -m "鍒涘缓鐢ㄦ埛琛?
    alembic upgrade head
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 瀵煎叆妯″瀷锛堢敤浜庤嚜鍔ㄧ敓鎴愯縼绉伙級
from app.models import Base
from app.core.config import settings

# 瀵煎叆鏁版嵁搴撹繛鎺?from common.database import datasource_manager

# Alembic閰嶇疆瀵硅薄
config = context.config

# 璁剧疆鏃ュ織
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 娣诲姞妯″瀷鐨凪etaData
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    绂荤嚎妯″紡杩愯杩佺Щ
    
    浣跨敤鏂规硶锛?        alembic upgrade head --sql
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
    鍦ㄧ嚎妯″紡杩愯杩佺Щ
    
    浣跨敤鏂规硶锛?        alembic upgrade head
    """
    # 浣跨敤鏁版嵁婧愮鐞嗗櫒鐨勫紩鎿?    engine = datasource_manager.get_engine('mysql')

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
