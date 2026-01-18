"""
权限管理API路由
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
from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
    PermissionListResponse
)
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/permissions", tags=["权限管理"])


@router.post("", response_model=PermissionResponse, summary="创建权限")
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db)
):
    """创建权限"""
    logger.info(f"创建权限: name={permission.name}")
    
    try:
        perm_service = PermissionService(db)
        new_perm = perm_service.create_permission(permission.dict())
        
        logger.info(f"创建权限成功: name={permission.name}, permission_id={new_perm.id}")
        
        return PermissionResponse(
            id=new_perm.id,
            name=new_perm.name,
            code=new_perm.code,
            type=new_perm.type,
            description=new_perm.description,
            created_at=new_perm.created_at.isoformat() if new_perm.created_at else None,
            updated_at=new_perm.updated_at.isoformat() if new_perm.updated_at else None
        )
    except ValueError as e:
        logger.warning(f"创建权限失败: name={permission.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建权限异常: name={permission.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建权限失败，请稍后重试")


@router.get("", response_model=PermissionListResponse, summary="获取权限列表")
async def get_permissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    type: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取权限列表"""
    logger.info(f"获取权限列表: page={page}")
    
    try:
        perm_service = PermissionService(db)
        
        # 查询权限列表
        permissions = perm_service.list_permissions(
            permission_type=type,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        
        # 统计总数
        total = perm_service.count_permissions()
        
        items = [
            PermissionResponse(
                id=perm.id,
                name=perm.name,
                code=perm.code,
                type=perm.type,
                description=perm.description,
                created_at=perm.created_at.isoformat() if perm.created_at else None,
                updated_at=perm.updated_at.isoformat() if perm.updated_at else None
            )
            for perm in permissions
        ]
        
        return PermissionListResponse(total=total, items=items, page=page, page_size=page_size)
    except Exception as e:
        logger.error(f"获取权限列表异常: error={str(e)}")
        raise HTTPException(status_code=500, detail="获取权限列表失败，请稍后重试")


@router.get("/{permission_id}", response_model=PermissionResponse, summary="获取权限详情")
async def get_permission(
    permission_id: str,
    db: Session = Depends(get_db)
):
    """获取权限详情"""
    logger.info(f"获取权限详情: permission_id={permission_id}")
    
    try:
        perm_service = PermissionService(db)
        perm = perm_service.get_by_id(permission_id)
        
        if not perm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="权限不存在")
        
        return PermissionResponse(
            id=perm.id,
            name=perm.name,
            code=perm.code,
            type=perm.type,
            description=perm.description,
            created_at=perm.created_at.isoformat() if perm.created_at else None,
            updated_at=perm.updated_at.isoformat() if perm.updated_at else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取权限详情异常: permission_id={permission_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取权限详情失败，请稍后重试")


@router.put("/{permission_id}", response_model=PermissionResponse, summary="更新权限")
async def update_permission(
    permission_id: str,
    permission: PermissionUpdate,
    db: Session = Depends(get_db)
):
    """更新权限"""
    logger.info(f"更新权限: permission_id={permission_id}")
    
    try:
        perm_service = PermissionService(db)
        
        existing_perm = perm_service.get_by_id(permission_id)
        if not existing_perm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="权限不存在")
        
        update_data = permission.dict(exclude_unset=True)
        updated_perm = perm_service.update_permission(permission_id, update_data)
        
        logger.info(f"更新权限成功: permission_id={permission_id}")
        
        return PermissionResponse(
            id=updated_perm.id,
            name=updated_perm.name,
            code=updated_perm.code,
            type=updated_perm.type,
            description=updated_perm.description,
            created_at=updated_perm.created_at.isoformat() if updated_perm.created_at else None,
            updated_at=updated_perm.updated_at.isoformat() if updated_perm.updated_at else None
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"更新权限失败: permission_id={permission_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"更新权限异常: permission_id={permission_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新权限失败，请稍后重试")


@router.delete("/{permission_id}", summary="删除权限")
async def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db)
):
    """删除权限"""
    logger.info(f"删除权限: permission_id={permission_id}")
    
    try:
        perm_service = PermissionService(db)
        
        existing_perm = perm_service.get_by_id(permission_id)
        if not existing_perm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="权限不存在")
        
        perm_service.delete_permission(permission_id)
        
        logger.info(f"删除权限成功: permission_id={permission_id}")
        
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除权限异常: permission_id={permission_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除权限失败，请稍后重试")