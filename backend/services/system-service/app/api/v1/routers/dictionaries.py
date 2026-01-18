"""
瀛楀吀绠＄悊API璺敱
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
from app.services.dict_service import DictService

router = APIRouter(prefix="/dictionaries", tags=["瀛楀吀绠＄悊"])


@router.post("", summary="创建瀛楀吀")
async def create_dict(
    type: str = Query(..., description="瀛楀吀类型"),
    name: str = Query(..., description="瀛楀吀名称"),
    tenant_id: str = Query(..., description="租户ID"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """创建瀛楀吀"""
    logger.info(f"创建瀛楀吀: type={type}, name={name}")
    
    try:
        dict_service = DictService(db)
        
        dict_data = {
            "type": type,
            "name": name,
            "tenant_id": tenant_id,
            "description": description
        }
        
        new_dict = dict_service.create_dict(dict_data)
        
        logger.info(f"创建瀛楀吀鎴愬姛: type={type}, dict_id={new_dict.id}")
        
        return {
            "id": new_dict.id,
            "type": new_dict.type,
            "name": new_dict.name,
            "tenant_id": new_dict.tenant_id,
            "description": new_dict.description,
            "status": new_dict.status,
            "created_at": new_dict.created_at.isoformat() if new_dict.created_at else None,
            "updated_at": new_dict.updated_at.isoformat() if new_dict.updated_at else None,
        }
    except ValueError as e:
        logger.warning(f"创建瀛楀吀澶辫触: type={type}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建瀛楀吀寮傚父: type={type}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建瀛楀吀澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("", summary="鑾峰彇瀛楀吀鍒楄〃")
async def get_dictionaries(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    keyword: Optional[str] = Query(None, description="鎼滅储鍏抽敭璇?),
    db: Session = Depends(get_db)
):
    """鑾峰彇瀛楀吀鍒楄〃"""
    logger.info(f"鑾峰彇瀛楀吀鍒楄〃: page={page}")
    
    try:
        dict_service = DictService(db)
        
        dicts = dict_service.list_dicts(
            tenant_id=tenant_id,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        
        total = dict_service.count_dicts(tenant_id=tenant_id)
        items = [
            {
                "id": d.id,
                "type": d.type,
                "name": d.name,
                "tenant_id": d.tenant_id,
                "description": d.description,
                "status": d.status,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "updated_at": d.updated_at.isoformat() if d.updated_at else None,
            }
            for d in dicts
        ]
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"鑾峰彇瀛楀吀鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇瀛楀吀鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/{dict_id}", summary="鑾峰彇瀛楀吀璇︽儏")
async def get_dictionary(
    dict_id: str,
    db: Session = Depends(get_db)
):
    """鑾峰彇瀛楀吀璇︽儏"""
    logger.info(f"鑾峰彇瀛楀吀璇︽儏: dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        dict_obj = dict_service.get_dict(dict_id)
        
        if not dict_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瀛楀吀涓嶅瓨鍦?)
        
        return {
            "id": dict_obj.id,
            "type": dict_obj.type,
            "name": dict_obj.name,
            "tenant_id": dict_obj.tenant_id,
            "description": dict_obj.description,
            "status": dict_obj.status,
            "created_at": dict_obj.created_at.isoformat() if dict_obj.created_at else None,
            "updated_at": dict_obj.updated_at.isoformat() if dict_obj.updated_at else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇瀛楀吀璇︽儏寮傚父: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇瀛楀吀璇︽儏澶辫触锛岃绋嶅悗閲嶈瘯")


@router.put("/{dict_id}", summary="更新瀛楀吀")
async def update_dictionary(
    dict_id: str,
    name: Optional[str] = Query(None, description="瀛楀吀名称"),
    description: Optional[str] = Query(None, description="描述"),
    status: Optional[str] = Query(None, description="状态?),
    db: Session = Depends(get_db)
):
    """更新瀛楀吀"""
    logger.info(f"更新瀛楀吀: dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        
        existing_dict = dict_service.get_dict(dict_id)
        if not existing_dict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瀛楀吀涓嶅瓨鍦?)
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if status is not None:
            update_data["status"] = status
        
        updated_dict = dict_service.update_dict(dict_id, update_data)
        
        logger.info(f"更新瀛楀吀鎴愬姛: dict_id={dict_id}")
        
        return {
            "id": updated_dict.id,
            "type": updated_dict.type,
            "name": updated_dict.name,
            "tenant_id": updated_dict.tenant_id,
            "description": updated_dict.description,
            "status": updated_dict.status,
            "created_at": updated_dict.created_at.isoformat() if updated_dict.created_at else None,
            "updated_at": updated_dict.updated_at.isoformat() if updated_dict.updated_at else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新瀛楀吀寮傚父: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新瀛楀吀澶辫触锛岃绋嶅悗閲嶈瘯")


@router.delete("/{dict_id}", summary="删除瀛楀吀")
async def delete_dictionary(
    dict_id: str,
    db: Session = Depends(get_db)
):
    """删除瀛楀吀"""
    logger.info(f"删除瀛楀吀: dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        
        existing_dict = dict_service.get_dict(dict_id)
        if not existing_dict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="瀛楀吀涓嶅瓨鍦?)
        
        dict_service.delete_dict(dict_id)
        
        logger.info(f"删除瀛楀吀鎴愬姛: dict_id={dict_id}")
        
        return {"message": "删除鎴愬姛"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除瀛楀吀寮傚父: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除瀛楀吀澶辫触锛岃绋嶅悗閲嶈瘯")


@router.post("/{dict_id}/items", summary="创建瀛楀吀椤?)
async def create_dict_item(
    dict_id: str,
    label: str = Query(..., description="瀛楀吀椤规爣绛?),
    value: str = Query(..., description="瀛楀吀椤瑰€?),
    sort_order: int = Query(0, description="排序"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """创建瀛楀吀椤?""
    logger.info(f"创建瀛楀吀椤? dict_id={dict_id}, label={label}")
    
    try:
        dict_service = DictService(db)
        
        dict_item_data = {
            "label": label,
            "value": value,
            "sort_order": sort_order,
            "description": description
        }
        
        new_dict_item = dict_service.create_dict_item(dict_id, dict_item_data)
        
        logger.info(f"创建瀛楀吀椤规垚鍔? dict_id={dict_id}, dict_item_id={new_dict_item.id}")
        
        return {
            "id": new_dict_item.id,
            "dict_id": new_dict_item.dict_id,
            "label": new_dict_item.label,
            "value": new_dict_item.value,
            "sort_order": new_dict_item.sort_order,
            "description": new_dict_item.description,
            "status": new_dict_item.status,
            "created_at": new_dict_item.created_at.isoformat() if new_dict_item.created_at else None,
            "updated_at": new_dict_item.updated_at.isoformat() if new_dict_item.updated_at else None,
        }
    except ValueError as e:
        logger.warning(f"创建瀛楀吀椤瑰け璐? dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建瀛楀吀椤瑰紓甯? dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建瀛楀吀椤瑰け璐ワ紝璇风◢鍚庨噸璇?)


@router.get("/{dict_id}/items", summary="鑾峰彇瀛楀吀椤瑰垪琛?)
async def get_dict_items(
    dict_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """鑾峰彇瀛楀吀椤瑰垪琛?""
    logger.info(f"鑾峰彇瀛楀吀椤瑰垪琛? dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        
        dict_items = dict_service.get_dict_items(dict_id, page, page_size)
        
        total = dict_service.count_dict_items(dict_id)
        items = [
            {
                "id": item.id,
                "dict_id": item.dict_id,
                "label": item.label,
                "value": item.value,
                "sort_order": item.sort_order,
                "description": item.description,
                "status": item.status,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            }
            for item in dict_items
        ]
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"鑾峰彇瀛楀吀椤瑰垪琛ㄥ紓甯? error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇瀛楀吀椤瑰垪琛ㄥけ璐ワ紝璇风◢鍚庨噸璇?)
