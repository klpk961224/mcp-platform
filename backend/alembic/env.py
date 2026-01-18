"""
Alembic鐜閰嶇疆
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 瀵煎叆閰嶇疆鍜屾ā鍨?from common.config import settings
from common.database.base import BaseModel

# 瀵煎叆鎵€鏈夋ā鍨嬩互纭繚瀹冧滑琚敞鍐?from common.database.models import *

# Alembic閰嶇疆瀵硅薄
config = context.config

# 璁剧疆鏁版嵁搴揢RL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 瑙ｉ噴閰嶇疆鏂囦欢涓殑鏃ュ織閰嶇疆
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 娣诲姞妯″瀷鐨凪etaData瀵硅薄
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """绂荤嚎妯″紡杩愯杩佺Щ"""
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
    """鍦ㄧ嚎妯″紡杩愯杩佺Щ"""
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
