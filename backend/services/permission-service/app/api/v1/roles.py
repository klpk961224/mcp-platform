"""
角色管理API路由
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
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    RoleListResponse
)
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["角色管理"])


@router.post("", response_model=RoleResponse, summary="创建角色")
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    """创建角色"""
    logger.info(f"创建角色: name={role.name}")
    
    try:
        role_service = RoleService(db)
        new_role = role_service.create_role(role.dict())
        
        logger.info(f"创建角色成功: name={role.name}, role_id={new_role.id}")
        
        return RoleResponse(
            id=new_role.id,
            tenant_id=new_role.tenant_id,
            name=new_role.name,
            code=new_role.code,
            description=new_role.description,
            is_system=new_role.is_system,
            status=new_role.status,
            created_at=new_role.created_at.isoformat() if new_role.created_at else None,
            updated_at=new_role.updated_at.isoformat() if new_role.updated_at else None
        )
    except ValueError as e:
        logger.warning(f"创建角色失败: name={role.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建角色异常: name={role.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建角色失败，请稍后重试")


@router.get("", response_model=RoleListResponse, summary="获取角色列表")
async def get_roles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取角色列表"""
    logger.info(f"获取角色列表: page={page}, tenant_id={tenant_id}")
    
    try:
        role_service = RoleService(db)
        
        query_params = {
            "tenant_id": tenant_id,
            "status": status,
            "keyword": keyword
        }
        
        roles, total = role_service.search_roles(
            query_params=query_params,
            offset=(page - 1) * page_size,
            limit=page_size
        )
        
        items = [
            RoleResponse(
                id=role.id,
                tenant_id=role.tenant_id,
                name=role.name,
                code=role.code,
                description=role.description,
                is_system=role.is_system,
                status=role.status,
                created_at=role.created_at.isoformat() if role.created_at else None,
                updated_at=role.updated_at.isoformat() if role.updated_at else None
            )
            for role in roles
        ]
        
        return RoleListResponse(total=total, items=items, page=page, page_size=page_size)
    except Exception as e:
        logger.error(f"获取角色列表异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取角色列表失败，请稍后重试")


@router.get("/{role_id}", response_model=RoleResponse, summary="获取角色详情")
async def get_role(
    role_id: str,
    db: Session = Depends(get_db)
):
    """获取角色详情"""
    logger.info(f"获取角色详情: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        role = role_service.get_by_id(role_id)
        
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
        
        return RoleResponse(
            id=role.id,
            tenant_id=role.tenant_id,
            name=role.name,
            code=role.code,
            description=role.description,
            is_system=role.is_system,
            status=role.status,
            created_at=role.created_at.isoformat() if role.created_at else None,
            updated_at=role.updated_at.isoformat() if role.updated_at else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取角色详情异常: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取角色详情失败，请稍后重试")


@router.put("/{role_id}", response_model=RoleResponse, summary="更新角色")
async def update_role(
    role_id: str,
    role: RoleUpdate,
    db: Session = Depends(get_db)
):
    """更新角色"""
    logger.info(f"更新角色: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
        
        update_data = role.dict(exclude_unset=True)
        updated_role = role_service.update_role(role_id, update_data)
        
        logger.info(f"更新角色成功: role_id={role_id}")
        
        return RoleResponse(
            id=updated_role.id,
            tenant_id=updated_role.tenant_id,
            name=updated_role.name,
            code=updated_role.code,
            description=updated_role.description,
            is_system=updated_role.is_system,
            status=updated_role.status,
            created_at=updated_role.created_at.isoformat() if updated_role.created_at else None,
            updated_at=updated_role.updated_at.isoformat() if updated_role.updated_at else None
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"更新角色失败: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"更新角色异常: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新角色失败，请稍后重试")


@router.delete("/{role_id}", summary="删除角色")
async def delete_role(
    role_id: str,
    db: Session = Depends(get_db)
):
    """删除角色"""
    logger.info(f"删除角色: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
        
        role_service.delete_role(role_id)
        
        logger.info(f"删除角色成功: role_id={role_id}")
        
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除角色异常: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除角色失败，请稍后重试")