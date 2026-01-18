"""
瑙掕壊绠＄悊API璺敱
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

router = APIRouter(prefix="/roles", tags=["瑙掕壊绠＄悊"])


@router.post("", response_model=RoleResponse, summary="创建瑙掕壊")
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    """创建瑙掕壊"""
    logger.info(f"创建瑙掕壊: name={role.name}")
    
    try:
        role_service = RoleService(db)
        new_role = role_service.create_role(role.dict())
        
        logger.info(f"创建瑙掕壊鎴愬姛: name={role.name}, role_id={new_role.id}")
        
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
        logger.warning(f"创建瑙掕壊澶辫触: name={role.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建瑙掕壊寮傚父: name={role.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建瑙掕壊澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("", response_model=RoleListResponse, summary="鑾峰彇瑙掕壊鍒楄〃")
async def get_roles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """鑾峰彇瑙掕壊鍒楄〃"""
    logger.info(f"鑾峰彇瑙掕壊鍒楄〃: page={page}, tenant_id={tenant_id}")
    
    try:
        role_service = RoleService(db)
        
        # 查询瑙掕壊鍒楄〃
        roles = role_service.list_roles(
            tenant_id=tenant_id,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        
        # 缁熻鎬绘暟
        total = role_service.count_roles(tenant_id=tenant_id)
        
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
        logger.error(f"鑾峰彇瑙掕壊鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇瑙掕壊鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/{role_id}", response_model=RoleResponse, summary="鑾峰彇瑙掕壊璇︽儏")
async def get_role(
    role_id: str,
    db: Session = Depends(get_db)
):
    """鑾峰彇瑙掕壊璇︽儏"""
    logger.info(f"鑾峰彇瑙掕壊璇︽儏: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        role = role_service.get_by_id(role_id)
        
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
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
        logger.error(f"鑾峰彇瑙掕壊璇︽儏寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇瑙掕壊璇︽儏澶辫触锛岃绋嶅悗閲嶈瘯")


@router.put("/{role_id}", response_model=RoleResponse, summary="更新瑙掕壊")
async def update_role(
    role_id: str,
    role: RoleUpdate,
    db: Session = Depends(get_db)
):
    """更新瑙掕壊"""
    logger.info(f"更新瑙掕壊: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        update_data = role.dict(exclude_unset=True)
        updated_role = role_service.update_role(role_id, update_data)
        
        logger.info(f"更新瑙掕壊鎴愬姛: role_id={role_id}")
        
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
        logger.warning(f"更新瑙掕壊澶辫触: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"更新瑙掕壊寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新瑙掕壊澶辫触锛岃绋嶅悗閲嶈瘯")


@router.delete("/{role_id}", summary="删除瑙掕壊")
async def delete_role(
    role_id: str,
    db: Session = Depends(get_db)
):
    """删除瑙掕壊"""
    logger.info(f"删除瑙掕壊: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        role_service.delete_role(role_id)
        
        logger.info(f"删除瑙掕壊鎴愬姛: role_id={role_id}")
        
        return {"message": "删除鎴愬姛"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除瑙掕壊寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除瑙掕壊澶辫触锛岃绋嶅悗閲嶈瘯")


@router.post("/{role_id}/permissions", response_model=RoleResponse, summary="鍒嗛厤鏉冮檺")
async def assign_permissions(
    role_id: str,
    permission_ids: list[str],
    db: Session = Depends(get_db)
):
    """
    鍒嗛厤鏉冮檺缁欒鑹?    
    鍔熻兘锛?    - 娓呯┖瑙掕壊鐜版湁鏉冮檺
    - 娣诲姞鏂扮殑鏉冮檺鍒楄〃
    
    Args:
        role_id: 角色ID
        permission_ids: 鏉冮檺ID鍒楄〃
    
    Returns:
        RoleResponse: 更新鍚庣殑瑙掕壊淇℃伅
    
    Raises:
        HTTPException: 瑙掕壊涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"鍒嗛厤鏉冮檺: role_id={role_id}, permission_count={len(permission_ids)}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        updated_role = role_service.assign_permissions(role_id, permission_ids)
        
        logger.info(f"鍒嗛厤鏉冮檺鎴愬姛: role_id={role_id}, permission_count={len(permission_ids)}")
        
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
    except Exception as e:
        logger.error(f"鍒嗛厤鏉冮檺寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鍒嗛厤鏉冮檺澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/{role_id}/permissions", summary="鑾峰彇瑙掕壊鏉冮檺")
async def get_role_permissions(
    role_id: str,
    db: Session = Depends(get_db)
):
    """
    鑾峰彇瑙掕壊鏉冮檺鍒楄〃
    
    Args:
        role_id: 角色ID
    
    Returns:
        list: 鏉冮檺鍒楄〃
    
    Raises:
        HTTPException: 瑙掕壊涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"鑾峰彇瑙掕壊鏉冮檺: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        permissions = role_service.get_role_permissions(role_id)
        
        return [
            {
                "id": perm.id,
                "name": perm.name,
                "code": perm.code,
                "resource": perm.resource,
                "action": perm.action,
                "description": perm.description
            }
            for perm in permissions
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇瑙掕壊鏉冮檺寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇瑙掕壊鏉冮檺澶辫触锛岃绋嶅悗閲嶈瘯")


@router.post("/{role_id}/menus", response_model=RoleResponse, summary="鍒嗛厤鑿滃崟")
async def assign_menus(
    role_id: str,
    menu_ids: list[str],
    db: Session = Depends(get_db)
):
    """
    鍒嗛厤鑿滃崟缁欒鑹?    
    鍔熻兘锛?    - 娓呯┖瑙掕壊鐜版湁鑿滃崟
    - 娣诲姞鏂扮殑鑿滃崟鍒楄〃
    
    Args:
        role_id: 角色ID
        menu_ids: 鑿滃崟ID鍒楄〃
    
    Returns:
        RoleResponse: 更新鍚庣殑瑙掕壊淇℃伅
    
    Raises:
        HTTPException: 瑙掕壊涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"鍒嗛厤鑿滃崟: role_id={role_id}, menu_count={len(menu_ids)}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        updated_role = role_service.assign_menus(role_id, menu_ids)
        
        logger.info(f"鍒嗛厤鑿滃崟鎴愬姛: role_id={role_id}, menu_count={len(menu_ids)}")
        
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
    except Exception as e:
        logger.error(f"鍒嗛厤鑿滃崟寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鍒嗛厤鑿滃崟澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/{role_id}/menus", summary="鑾峰彇瑙掕壊鑿滃崟")
async def get_role_menus(
    role_id: str,
    db: Session = Depends(get_db)
):
    """
    鑾峰彇瑙掕壊鑿滃崟鍒楄〃
    
    Args:
        role_id: 角色ID
    
    Returns:
        list: 鑿滃崟鍒楄〃
    
    Raises:
        HTTPException: 瑙掕壊涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"鑾峰彇瑙掕壊鑿滃崟: role_id={role_id}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        menus = role_service.get_role_menus(role_id)
        
        return [
            {
                "id": menu.id,
                "name": menu.name,
                "code": menu.code,
                "path": menu.path,
                "icon": menu.icon,
                "parent_id": menu.parent_id,
                "level": menu.level,
                "sort_order": menu.sort_order,
                "description": menu.description
            }
            for menu in menus
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇瑙掕壊鑿滃崟寮傚父: role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇瑙掕壊鑿滃崟澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/{role_id}/check-permission/{permission_code}", summary="妫€查询鑹叉潈闄?)
async def check_role_permission(
    role_id: str,
    permission_code: str,
    db: Session = Depends(get_db)
):
    """
    妫€查询鑹叉槸鍚︽嫢鏈夋寚瀹氭潈闄?    
    Args:
        role_id: 角色ID
        permission_code: 鏉冮檺编码
    
    Returns:
        dict: 妫€鏌ョ粨鏋?    
    Raises:
        HTTPException: 瑙掕壊涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"妫€查询鑹叉潈闄? role_id={role_id}, permission_code={permission_code}")
    
    try:
        role_service = RoleService(db)
        
        existing_role = role_service.get_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瑙掕壊涓嶅瓨鍦?)
        
        has_permission = role_service.check_permission(role_id, permission_code)
        
        return {
            "role_id": role_id,
            "permission_code": permission_code,
            "has_permission": has_permission
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"妫€查询鑹叉潈闄愬紓甯? role_id={role_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="妫€查询鑹叉潈闄愬け璐ワ紝璇风◢鍚庨噸璇?)
