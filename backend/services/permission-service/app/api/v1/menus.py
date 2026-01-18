"""
菜单管理API路由
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
from app.schemas.menu import (
    MenuCreate,
    MenuUpdate,
    MenuResponse,
    MenuListResponse,
    MenuTreeResponse
)
from app.services.menu_service import MenuService

router = APIRouter(prefix="/menus", tags=["菜单管理"])


@router.post("", response_model=MenuResponse, summary="创建菜单")
async def create_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db)
):
    """创建菜单"""
    logger.info(f"创建菜单: name={menu.name}")
    
    try:
        menu_service = MenuService(db)
        new_menu = menu_service.create_menu(menu.model_dump())
        
        logger.info(f"创建菜单成功: name={menu.name}, menu_id={new_menu.id}")
        
        return MenuResponse(
            id=new_menu.id,
            tenant_id=new_menu.tenant_id,
            name=new_menu.name,
            path=new_menu.path,
            icon=new_menu.icon,
            parent_id=new_menu.parent_id,
            sort_order=new_menu.sort_order,
            is_visible=new_menu.is_visible == "1",
            status=new_menu.status,
            created_at=new_menu.created_at,
            updated_at=new_menu.updated_at
        )
    except ValueError as e:
        logger.warning(f"创建菜单失败: name={menu.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建菜单异常: name={menu.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建菜单失败，请稍后重试")


@router.get("", response_model=MenuListResponse, summary="获取菜单列表")
async def get_menus(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取菜单列表"""
    logger.info(f"获取菜单列表: page={page}")
    
    try:
        menu_service = MenuService(db)
        
        menus = menu_service.list_menus(
            tenant_id=tenant_id,
            page=page,
            page_size=page_size
        )
        
        # 统计总数
        total = menu_service.count_menus(tenant_id=tenant_id)
        
        items = [
            MenuResponse(
                id=menu.id,
                tenant_id=menu.tenant_id,
                name=menu.name,
                path=menu.path,
                icon=menu.icon,
                parent_id=menu.parent_id,
                sort_order=menu.sort_order,
                is_visible=menu.is_visible == "1",
                status=menu.status,
                created_at=menu.created_at,
                updated_at=menu.updated_at
            )
            for menu in menus
        ]
        
        return MenuListResponse(total=total, items=items, page=page, page_size=page_size)
    except Exception as e:
        logger.error(f"获取菜单列表异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取菜单列表失败，请稍后重试")


@router.get("/tree", response_model=list[MenuTreeResponse], summary="获取菜单树")
async def get_menu_tree(
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    db: Session = Depends(get_db)
):
    """获取菜单树"""
    logger.info(f"获取菜单树: tenant_id={tenant_id}")
    
    try:
        menu_service = MenuService(db)
        menu_tree = menu_service.get_menu_tree(tenant_id=tenant_id)
        
        # 转换为树形结构
        def build_tree(menus: list) -> list:
            result = []
            for menu in menus:
                result.append(
                    MenuTreeResponse(
                        id=menu.id,
                        tenant_id=menu.tenant_id,
                        name=menu.name,
                        path=menu.path,
                        icon=menu.icon,
                        parent_id=menu.parent_id,
                        sort_order=menu.sort_order,
                        is_visible=menu.is_visible == "1",
                        status=menu.status,
                        created_at=menu.created_at,
                        updated_at=menu.updated_at,
                        children=build_tree(menu.children)
                    )
                )
            return result
        
        return build_tree(menu_tree)
    except Exception as e:
        logger.error(f"获取菜单树异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取菜单树失败，请稍后重试")


@router.get("/{menu_id}", response_model=MenuResponse, summary="获取菜单详情")
async def get_menu(
    menu_id: str,
    db: Session = Depends(get_db)
):
    """获取菜单详情"""
    logger.info(f"获取菜单详情: menu_id={menu_id}")
    
    try:
        menu_service = MenuService(db)
        menu = menu_service.get_menu(menu_id)
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
        
        return MenuResponse(
            id=menu.id,
            tenant_id=menu.tenant_id,
            name=menu.name,
            path=menu.path,
            icon=menu.icon,
            parent_id=menu.parent_id,
            sort_order=menu.sort_order,
            is_visible=menu.is_visible == "1",
            status=menu.status,
            created_at=menu.created_at,
            updated_at=menu.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取菜单详情异常: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取菜单详情失败，请稍后重试")


@router.put("/{menu_id}", response_model=MenuResponse, summary="更新菜单")
async def update_menu(
    menu_id: str,
    menu: MenuUpdate,
    db: Session = Depends(get_db)
):
    """更新菜单"""
    logger.info(f"更新菜单: menu_id={menu_id}")
    
    try:
        menu_service = MenuService(db)
        
        existing_menu = menu_service.get_menu(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
        
        update_data = menu.model_dump(exclude_unset=True)
        updated_menu = menu_service.update_menu(menu_id, update_data)
        
        logger.info(f"更新菜单成功: menu_id={menu_id}")
        
        return MenuResponse(
            id=updated_menu.id,
            tenant_id=updated_menu.tenant_id,
            name=updated_menu.name,
            path=updated_menu.path,
            icon=updated_menu.icon,
            parent_id=updated_menu.parent_id,
            sort_order=updated_menu.sort_order,
            is_visible=updated_menu.is_visible == "1",
            status=updated_menu.status,
            created_at=updated_menu.created_at,
            updated_at=updated_menu.updated_at
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"更新菜单失败: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"更新菜单异常: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新菜单失败，请稍后重试")


@router.delete("/{menu_id}", summary="删除菜单")
async def delete_menu(
    menu_id: str,
    db: Session = Depends(get_db)
):
    """删除菜单"""
    logger.info(f"删除菜单: menu_id={menu_id}")
    
    try:
        menu_service = MenuService(db)
        
        existing_menu = menu_service.get_menu(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
        
        menu_service.delete_menu(menu_id)
        
        logger.info(f"删除菜单成功: menu_id={menu_id}")
        
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除菜单异常: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除菜单失败，请稍后重试")