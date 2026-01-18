"""
鑿滃崟绠＄悊API璺敱
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

router = APIRouter(prefix="/menus", tags=["鑿滃崟绠＄悊"])


@router.post("", response_model=MenuResponse, summary="鍒涘缓鑿滃崟")
async def create_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db)
):
    """鍒涘缓鑿滃崟"""
    logger.info(f"鍒涘缓鑿滃崟: name={menu.name}")
    
    try:
        menu_service = MenuService(db)
        new_menu = menu_service.create_menu(menu.model_dump())
        
        logger.info(f"鍒涘缓鑿滃崟鎴愬姛: name={menu.name}, menu_id={new_menu.id}")
        
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
        logger.warning(f"鍒涘缓鑿滃崟澶辫触: name={menu.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"鍒涘缓鑿滃崟寮傚父: name={menu.name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鍒涘缓鑿滃崟澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("", response_model=MenuListResponse, summary="鑾峰彇鑿滃崟鍒楄〃")
async def get_menus(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """鑾峰彇鑿滃崟鍒楄〃"""
    logger.info(f"鑾峰彇鑿滃崟鍒楄〃: page={page}")
    
    try:
        menu_service = MenuService(db)
        
        menus = menu_service.list_menus(
            tenant_id=tenant_id,
            page=page,
            page_size=page_size
        )
        
        # 缁熻鎬绘暟
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
        logger.error(f"鑾峰彇鑿滃崟鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鑿滃崟鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/tree", response_model=list[MenuTreeResponse], summary="鑾峰彇鑿滃崟鏍?)
async def get_menu_tree(
    tenant_id: Optional[str] = Query(None, description="绉熸埛ID"),
    db: Session = Depends(get_db)
):
    """鑾峰彇鑿滃崟鏍?""
    logger.info(f"鑾峰彇鑿滃崟鏍? tenant_id={tenant_id}")
    
    try:
        menu_service = MenuService(db)
        menu_tree = menu_service.get_menu_tree(tenant_id=tenant_id)
        
        # 杞崲涓烘爲褰㈢粨鏋?        def build_tree(menus: list) -> list:
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
        logger.error(f"鑾峰彇鑿滃崟鏍戝紓甯? error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鑿滃崟鏍戝け璐ワ紝璇风◢鍚庨噸璇?)


@router.get("/{menu_id}", response_model=MenuResponse, summary="鑾峰彇鑿滃崟璇︽儏")
async def get_menu(
    menu_id: str,
    db: Session = Depends(get_db)
):
    """鑾峰彇鑿滃崟璇︽儏"""
    logger.info(f"鑾峰彇鑿滃崟璇︽儏: menu_id={menu_id}")
    
    try:
        menu_service = MenuService(db)
        menu = menu_service.get_menu(menu_id)
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="鑿滃崟涓嶅瓨鍦?)
        
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
        logger.error(f"鑾峰彇鑿滃崟璇︽儏寮傚父: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鑿滃崟璇︽儏澶辫触锛岃绋嶅悗閲嶈瘯")


@router.put("/{menu_id}", response_model=MenuResponse, summary="鏇存柊鑿滃崟")
async def update_menu(
    menu_id: str,
    menu: MenuUpdate,
    db: Session = Depends(get_db)
):
    """鏇存柊鑿滃崟"""
    logger.info(f"鏇存柊鑿滃崟: menu_id={menu_id}")
    
    try:
        menu_service = MenuService(db)
        
        existing_menu = menu_service.get_menu(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="鑿滃崟涓嶅瓨鍦?)
        
        update_data = menu.model_dump(exclude_unset=True)
        updated_menu = menu_service.update_menu(menu_id, update_data)
        
        logger.info(f"鏇存柊鑿滃崟鎴愬姛: menu_id={menu_id}")
        
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
        logger.warning(f"鏇存柊鑿滃崟澶辫触: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"鏇存柊鑿滃崟寮傚父: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鏇存柊鑿滃崟澶辫触锛岃绋嶅悗閲嶈瘯")


@router.delete("/{menu_id}", summary="鍒犻櫎鑿滃崟")
async def delete_menu(
    menu_id: str,
    db: Session = Depends(get_db)
):
    """鍒犻櫎鑿滃崟"""
    logger.info(f"鍒犻櫎鑿滃崟: menu_id={menu_id}")
    
    try:
        menu_service = MenuService(db)
        
        existing_menu = menu_service.get_menu(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="鑿滃崟涓嶅瓨鍦?)
        
        menu_service.delete_menu(menu_id)
        
        logger.info(f"鍒犻櫎鑿滃崟鎴愬姛: menu_id={menu_id}")
        
        return {"message": "鍒犻櫎鎴愬姛"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鍒犻櫎鑿滃崟寮傚父: menu_id={menu_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鍒犻櫎鑿滃崟澶辫触锛岃绋嶅悗閲嶈瘯")
