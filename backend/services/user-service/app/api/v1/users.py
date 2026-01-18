"""
鐢ㄦ埛绠＄悊API璺敱
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings
from app.core.deps import get_db
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse
)
from app.services.user_service import UserService
from common.security.password import hash_password

router = APIRouter(prefix="/users", tags=["鐢ㄦ埛绠＄悊"])


@router.post("", response_model=UserResponse, summary="创建鐢ㄦ埛")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """创建鐢ㄦ埛"""
    logger.info(f"创建鐢ㄦ埛璇锋眰: username={user.username}")
    
    try:
        user_service = UserService(db)
        
        # 鍝堝笇瀵嗙爜
        password_hash = hash_password(user.password)
        
        # 杞崲涓哄瓧鍏?        user_data = user.dict()
        user_data["password_hash"] = password_hash
        del user_data["password"]
        
        # 创建鐢ㄦ埛
        new_user = user_service.create_user(user_data)
        
        logger.info(f"创建鐢ㄦ埛鎴愬姛: username={user.username}, user_id={new_user.id}")
        
        return UserResponse(
            id=new_user.id,
            tenant_id=new_user.tenant_id,
            username=new_user.username,
            email=new_user.email,
            phone=new_user.phone,
            dept_id=new_user.department_id,
            position_id=getattr(new_user, 'position_id', None),
            status=new_user.status,
            created_at=new_user.created_at.isoformat() if new_user.created_at else None,
            updated_at=new_user.updated_at.isoformat() if new_user.updated_at else None
        )
    except ValueError as e:
        logger.warning(f"创建鐢ㄦ埛澶辫触: username={user.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"创建鐢ㄦ埛寮傚父: username={user.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建鐢ㄦ埛澶辫触锛岃绋嶅悗閲嶈瘯"
        )


@router.get("", response_model=UserListResponse, summary="鑾峰彇鐢ㄦ埛鍒楄〃")
async def get_users(
    page: int = Query(1, ge=1, description="椤电爜"),
    page_size: int = Query(10, ge=1, le=100, description="姣忛〉数量"),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    status: Optional[str] = Query(None, description="状态?),
    keyword: Optional[str] = Query(None, description="鍏抽敭璇?),
    db: Session = Depends(get_db)
):
    """鑾峰彇鐢ㄦ埛鍒楄〃"""
    logger.info(f"鑾峰彇鐢ㄦ埛鍒楄〃: page={page}, page_size={page_size}, tenant_id={tenant_id}")
    
    try:
        user_service = UserService(db)
        
        # 查询鐢ㄦ埛鍒楄〃
        users = user_service.list_users(
            tenant_id=tenant_id,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        
        # 缁熻鎬绘暟
        total = user_service.count_users(tenant_id=tenant_id)
        
        # 杞崲涓哄搷搴旀牸寮?        items = [
            UserResponse(
                id=user.id,
                tenant_id=user.tenant_id,
                username=user.username,
                email=user.email,
                phone=user.phone,
                dept_id=user.dept_id,
                position_id=user.position_id,
                status=user.status,
                created_at=user.created_at.isoformat() if user.created_at else None,
                updated_at=user.updated_at.isoformat() if user.updated_at else None
            )
            for user in users
        ]
        
        return UserListResponse(
            total=total,
            items=items,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"鑾峰彇鐢ㄦ埛鍒楄〃寮傚父: error={str(e)}", exc_info=True)
        import traceback
        raise HTTPException(
            status_code=500,
            detail=f"鑾峰彇鐢ㄦ埛鍒楄〃澶辫触: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse, summary="鑾峰彇鐢ㄦ埛璇︽儏")
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """鑾峰彇鐢ㄦ埛璇︽儏"""
    logger.info(f"鑾峰彇鐢ㄦ埛璇︽儏: user_id={user_id}")
    
    try:
        user_service = UserService(db)
        user = user_service.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="鐢ㄦ埛涓嶅瓨鍦?
            )
        
        return UserResponse(
            id=user.id,
            tenant_id=user.tenant_id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            dept_id=user.department_id,
            position_id=getattr(user, 'position_id', None),
            status=user.status,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇鐢ㄦ埛璇︽儏寮傚父: user_id={user_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="鑾峰彇鐢ㄦ埛璇︽儏澶辫触锛岃绋嶅悗閲嶈瘯"
        )


@router.put("/{user_id}", response_model=UserResponse, summary="更新鐢ㄦ埛")
async def update_user(
    user_id: str,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新鐢ㄦ埛"""
    logger.info(f"更新鐢ㄦ埛: user_id={user_id}")
    
    try:
        user_service = UserService(db)
        
        # 鑾峰彇鐜版湁鐢ㄦ埛
        existing_user = user_service.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="鐢ㄦ埛涓嶅瓨鍦?
            )
        
        # 更新鐢ㄦ埛淇℃伅
        update_data = user.dict(exclude_unset=True)
        if "dept_id" in update_data:
            update_data["department_id"] = update_data.pop("dept_id")
        
        updated_user = user_service.update_user(user_id, update_data)
        
        logger.info(f"更新鐢ㄦ埛鎴愬姛: user_id={user_id}")
        
        return UserResponse(
            id=updated_user.id,
            tenant_id=updated_user.tenant_id,
            username=updated_user.username,
            email=updated_user.email,
            phone=updated_user.phone,
            dept_id=updated_user.department_id,
            position_id=getattr(updated_user, 'position_id', None),
            status=updated_user.status,
            created_at=updated_user.created_at.isoformat() if updated_user.created_at else None,
            updated_at=updated_user.updated_at.isoformat() if updated_user.updated_at else None
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"更新鐢ㄦ埛澶辫触: user_id={user_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"更新鐢ㄦ埛寮傚父: user_id={user_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新鐢ㄦ埛澶辫触锛岃绋嶅悗閲嶈瘯"
        )


@router.delete("/{user_id}", summary="删除鐢ㄦ埛")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """删除鐢ㄦ埛"""
    logger.info(f"删除鐢ㄦ埛: user_id={user_id}")
    
    try:
        user_service = UserService(db)
        
        # 妫€鏌ョ敤鎴锋槸鍚﹀瓨鍦?        existing_user = user_service.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="鐢ㄦ埛涓嶅瓨鍦?
            )
        
        # 删除鐢ㄦ埛
        user_service.delete_user(user_id)
        
        logger.info(f"删除鐢ㄦ埛鎴愬姛: user_id={user_id}")
        
        return {"message": "删除鎴愬姛"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除鐢ㄦ埛寮傚父: user_id={user_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除鐢ㄦ埛澶辫触锛岃绋嶅悗閲嶈瘯"
        )
