"""
字典管理API路由
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

router = APIRouter(prefix="/dictionaries", tags=["字典管理"])


@router.post("", summary="创建字典")
async def create_dict(
    type: str = Query(..., description="字典类型"),
    name: str = Query(..., description="字典名称"),
    tenant_id: str = Query(..., description="租户ID"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """创建字典"""
    logger.info(f"创建字典: type={type}, name={name}")
    
    try:
        dict_service = DictService(db)
        
        dict_data = {
            "type": type,
            "name": name,
            "tenant_id": tenant_id,
            "description": description
        }
        
        new_dict = dict_service.create_dict(dict_data)
        
        logger.info(f"创建字典成功: type={type}, dict_id={new_dict.id}")
        
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
        logger.warning(f"创建字典失败: type={type}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建字典异常: type={type}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建字典失败，请稍后重试")


@router.get("", summary="获取字典列表")
async def get_dictionaries(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取字典列表"""
    logger.info(f"获取字典列表: page={page}")
    
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
        logger.error(f"获取字典列表异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取字典列表失败，请稍后重试")


@router.get("/{dict_id}", summary="获取字典详情")
async def get_dictionary(
    dict_id: str,
    db: Session = Depends(get_db)
):
    """获取字典详情"""
    logger.info(f"获取字典详情: dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        dict_obj = dict_service.get_dict(dict_id)
        
        if not dict_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典不存在")
        
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
        logger.error(f"获取字典详情异常: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取字典详情失败，请稍后重试")


@router.put("/{dict_id}", summary="更新字典")
async def update_dictionary(
    dict_id: str,
    name: Optional[str] = Query(None, description="字典名称"),
    description: Optional[str] = Query(None, description="描述"),
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
):
    """更新字典"""
    logger.info(f"更新字典: dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        
        existing_dict = dict_service.get_dict(dict_id)
        if not existing_dict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典不存在")
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if status is not None:
            update_data["status"] = status
        
        updated_dict = dict_service.update_dict(dict_id, update_data)
        
        logger.info(f"更新字典成功: dict_id={dict_id}")
        
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
        logger.error(f"更新字典异常: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新字典失败，请稍后重试")


@router.delete("/{dict_id}", summary="删除字典")
async def delete_dictionary(
    dict_id: str,
    db: Session = Depends(get_db)
):
    """删除字典"""
    logger.info(f"删除字典: dict_id={dict_id}")
    
    try:
        dict_service = DictService(db)
        
        existing_dict = dict_service.get_dict(dict_id)
        if not existing_dict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典不存在")
        
        dict_service.delete_dict(dict_id)
        
        logger.info(f"删除字典成功: dict_id={dict_id}")
        
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除字典异常: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除字典失败，请稍后重试")


@router.post("/{dict_id}/items", summary="创建字典项")
async def create_dict_item(
    dict_id: str,
    label: str = Query(..., description="字典项标签"),
    value: str = Query(..., description="字典项值"),
    sort_order: int = Query(0, description="排序"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """创建字典项"""
    logger.info(f"创建字典项: dict_id={dict_id}, label={label}")
    
    try:
        dict_service = DictService(db)
        
        dict_item_data = {
            "label": label,
            "value": value,
            "sort_order": sort_order,
            "description": description
        }
        
        new_dict_item = dict_service.create_dict_item(dict_id, dict_item_data)
        
        logger.info(f"创建字典项成功: dict_id={dict_id}, dict_item_id={new_dict_item.id}")
        
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
        logger.warning(f"创建字典项失败: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建字典项异常: dict_id={dict_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建字典项失败，请稍后重试")


@router.get("/{dict_id}/items", summary="获取字典项列表")
async def get_dict_items(
    dict_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取字典项列表"""
    logger.info(f"获取字典项列表: dict_id={dict_id}")
    
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
        logger.error(f"获取字典项列表异常: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取字典项列表失败，请稍后重试")