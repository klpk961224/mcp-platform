"""
宀椾綅绠＄悊API璺敱
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
from app.services.position_service import PositionService

router = APIRouter(prefix="/positions", tags=["宀椾綅绠＄悊"])


@router.post("", summary="创建宀椾綅")
async def create_position(
    name: str = Query(..., description="宀椾綅名称"),
    code: str = Query(..., description="宀椾綅编码"),
    tenant_id: str = Query(..., description="租户ID"),
    level: int = Query(1, description="宀椾綅级别"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """创建宀椾綅"""
    logger.info(f"创建宀椾綅: name={name}, code={code}")
    
    try:
        position_service = PositionService(db)
        
        position_data = {
            "name": name,
            "code": code,
            "tenant_id": tenant_id,
            "level": level,
            "description": description
        }
        
        new_position = position_service.create_position(position_data)
        
        logger.info(f"创建宀椾綅鎴愬姛: name={name}, position_id={new_position.id}")
        
        return new_position.to_dict()
    except ValueError as e:
        logger.warning(f"创建宀椾綅澶辫触: name={name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"创建宀椾綅寮傚父: name={name}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建宀椾綅澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("", summary="鑾峰彇宀椾綅鍒楄〃")
async def get_positions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    keyword: Optional[str] = Query(None, description="鎼滅储鍏抽敭璇?),
    db: Session = Depends(get_db)
):
    """鑾峰彇宀椾綅鍒楄〃"""
    logger.info(f"鑾峰彇宀椾綅鍒楄〃: page={page}")
    
    try:
        position_service = PositionService(db)
        
        positions = position_service.list_positions(
            tenant_id=tenant_id,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        
        total = position_service.count_positions(tenant_id=tenant_id)
        items = [position.to_dict() for position in positions]
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"鑾峰彇宀椾綅鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇宀椾綅鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/{position_id}", summary="鑾峰彇宀椾綅璇︽儏")
async def get_position(
    position_id: str,
    db: Session = Depends(get_db)
):
    """鑾峰彇宀椾綅璇︽儏"""
    logger.info(f"鑾峰彇宀椾綅璇︽儏: position_id={position_id}")
    
    try:
        position_service = PositionService(db)
        position = position_service.get_position(position_id)
        
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宀椾綅涓嶅瓨鍦?)
        
        return position.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇宀椾綅璇︽儏寮傚父: position_id={position_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇宀椾綅璇︽儏澶辫触锛岃绋嶅悗閲嶈瘯")


@router.put("/{position_id}", summary="更新宀椾綅")
async def update_position(
    position_id: str,
    name: Optional[str] = Query(None, description="宀椾綅名称"),
    level: Optional[int] = Query(None, description="宀椾綅级别"),
    description: Optional[str] = Query(None, description="描述"),
    status: Optional[str] = Query(None, description="状态?),
    db: Session = Depends(get_db)
):
    """更新宀椾綅"""
    logger.info(f"更新宀椾綅: position_id={position_id}")
    
    try:
        position_service = PositionService(db)
        
        existing_position = position_service.get_position(position_id)
        if not existing_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宀椾綅涓嶅瓨鍦?)
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if level is not None:
            update_data["level"] = level
        if description is not None:
            update_data["description"] = description
        if status is not None:
            update_data["status"] = status
        
        updated_position = position_service.update_position(position_id, update_data)
        
        logger.info(f"更新宀椾綅鎴愬姛: position_id={position_id}")
        
        return updated_position.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新宀椾綅寮傚父: position_id={position_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新宀椾綅澶辫触锛岃绋嶅悗閲嶈瘯")


@router.delete("/{position_id}", summary="删除宀椾綅")
async def delete_position(
    position_id: str,
    db: Session = Depends(get_db)
):
    """删除宀椾綅"""
    logger.info(f"删除宀椾綅: position_id={position_id}")
    
    try:
        position_service = PositionService(db)
        
        existing_position = position_service.get_position(position_id)
        if not existing_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宀椾綅涓嶅瓨鍦?)
        
        position_service.delete_position(position_id)
        
        logger.info(f"删除宀椾綅鎴愬姛: position_id={position_id}")
        
        return {"message": "删除鎴愬姛"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除宀椾綅寮傚父: position_id={position_id}, error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除宀椾綅澶辫触锛岃绋嶅悗閲嶈瘯")
