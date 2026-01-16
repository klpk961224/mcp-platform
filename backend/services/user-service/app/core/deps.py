"""
依赖注入模块

功能说明：
1. 提供数据库会话依赖
2. 提供当前用户依赖
3. 提供权限校验依赖

使用示例：
    from app.core.deps import get_db

    @router.get("/users")
    async def get_users(db: Session = Depends(get_db)):
        return db.query(User).all()
"""

from sqlalchemy.orm import Session
from typing import Generator
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from common.database.connection import datasource_manager


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话（生成器函数，用于FastAPI依赖注入）

    Returns:
        Generator[Session, None, None]: 数据库会话生成器

    使用示例：
        @router.get("/users")
        async def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
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