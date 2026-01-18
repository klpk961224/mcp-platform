"""
数据范围权限API路由
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings
from app.core.deps import get_db
from app.services.data_scope_service import DataScopeService

router = APIRouter(prefix="/data-scopes", tags=["数据范围权限"])


@router.get("", summary="获取数据范围列表")
async def get_data_scopes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取数据范围列表"""
    logger.info(f"获取数据范围列表: page={page}")
    
    try:
        data_scope_service = DataScopeService(db)
        data_scopes = data_scope_service.list_data_scopes(page=page, page_size=page_size)
        
        items = [data_scope.to_dict() for data_scope in data_scopes]
        total = data_scope_service.data_scope_repo.count_all()
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"获取数据范围列表异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取数据范围列表失败，请稍后重试")


@router.get("/user/{user_id}", summary="获取用户数据范围权限")
async def get_user_data_scope(
    user_id: str,
    module: str = Query(..., description="模块"),
    db: Session = Depends(get_db)
):
    """获取用户数据范围权限"""
    logger.info(f"获取用户数据范围权限: user_id={user_id}, module={module}")
    
    try:
        data_scope_service = DataScopeService(db)
        user_data_scope = data_scope_service.get_user_data_scope(user_id, module)
        
        if not user_data_scope:
            return {
                "user_id": user_id,
                "module": module,
                "data_scope": None,
                "message": "未配置数据范围权限，默认为仅本人数据"
            }
        
        return user_data_scope.to_dict()
    except Exception as e:
        logger.error(f"获取用户数据范围权限异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取用户数据范围权限失败，请稍后重试")


@router.post("/user/{user_id}", summary="设置用户数据范围权限")
async def set_user_data_scope(
    user_id: str,
    module: str = Query(..., description="模块"),
    data_scope_code: str = Query(..., description="数据范围编码"),
    db: Session = Depends(get_db)
):
    """设置用户数据范围权限"""
    logger.info(f"设置用户数据范围权限: user_id={user_id}, module={module}, data_scope_code={data_scope_code}")
    
    try:
        data_scope_service = DataScopeService(db)
        user_data_scope = data_scope_service.set_user_data_scope(user_id, module, data_scope_code)
        
        logger.info(f"设置用户数据范围权限成功: user_id={user_id}, module={module}")
        
        return user_data_scope.to_dict()
    except ValueError as e:
        logger.warning(f"设置用户数据范围权限失败: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"设置用户数据范围权限异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="设置用户数据范围权限失败，请稍后重试")


@router.post("/check", summary="检查数据范围权限")
async def check_data_scope(
    user_id: str = Query(..., description="用户ID"),
    module: str = Query(..., description="模块"),
    target_id: str = Query(..., description="目标数据ID"),
    db: Session = Depends(get_db)
):
    """检查数据范围权限"""
    logger.info(f"检查数据范围权限: user_id={user_id}, module={module}, target_id={target_id}")
    
    try:
        data_scope_service = DataScopeService(db)
        has_access = data_scope_service.check_data_scope(user_id, module, target_id)
        
        return {
            "user_id": user_id,
            "module": module,
            "target_id": target_id,
            "has_access": has_access
        }
    except Exception as e:
        logger.error(f"检查数据范围权限异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="检查数据范围权限失败，请稍后重试")