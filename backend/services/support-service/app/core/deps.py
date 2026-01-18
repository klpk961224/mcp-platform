"""
依赖注入模块

功能说明：
1. 提供数据库会话依赖
2. 提供当前用户依赖
3. 提供权限校验依赖

使用示例：
    from app.core.deps import get_db, get_current_user

    @router.get("/users")
    async def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
        return users
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Generator
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from common.database import get_session
from common.security import verify_token
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


async def get_current_user(
    token: str = Depends(lambda: None),
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    获取当前用户
    
    Args:
        token: JWT Token
        db: 数据库会话
    
    Returns:
        Optional[dict]: 用户信息
    
    使用示例：
        @router.get("/profile")
        async def get_profile(current_user = Depends(get_current_user)):
            return current_user
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证Token"
        )
    
    # 验证Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期"
        )
    
    # 从数据库获取用户信息
    # user = db.query(User).filter(User.id == payload.get("user_id")).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="用户不存在"
    #     )
    
    return payload


async def get_current_active_user(
    current_user = Depends(get_current_user)
) -> dict:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
    
    Returns:
        dict: 用户信息
    
    使用示例：
        @router.get("/profile")
        async def get_profile(current_user = Depends(get_current_active_user)):
            return current_user
    """
    if current_user.get("status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    return current_user