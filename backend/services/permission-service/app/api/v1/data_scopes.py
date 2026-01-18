"""
鏁版嵁鑼冨洿鏉冮檺API璺敱
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

router = APIRouter(prefix="/data-scopes", tags=["鏁版嵁鑼冨洿鏉冮檺"])


@router.get("", summary="鑾峰彇鏁版嵁鑼冨洿鍒楄〃")
async def get_data_scopes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """鑾峰彇鏁版嵁鑼冨洿鍒楄〃"""
    logger.info(f"鑾峰彇鏁版嵁鑼冨洿鍒楄〃: page={page}")
    
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
        logger.error(f"鑾峰彇鏁版嵁鑼冨洿鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鏁版嵁鑼冨洿鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/user/{user_id}", summary="鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺")
async def get_user_data_scope(
    user_id: str,
    module: str = Query(..., description="妯″潡"),
    db: Session = Depends(get_db)
):
    """鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺"""
    logger.info(f"鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺: user_id={user_id}, module={module}")
    
    try:
        data_scope_service = DataScopeService(db)
        user_data_scope = data_scope_service.get_user_data_scope(user_id, module)
        
        if not user_data_scope:
            return {
                "user_id": user_id,
                "module": module,
                "data_scope": None,
                "message": "鏈厤缃暟鎹寖鍥存潈闄愶紝榛樿涓轰粎鏈汉鏁版嵁"
            }
        
        return user_data_scope.to_dict()
    except Exception as e:
        logger.error(f"鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺澶辫触锛岃绋嶅悗閲嶈瘯")


@router.post("/user/{user_id}", summary="璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺")
async def set_user_data_scope(
    user_id: str,
    module: str = Query(..., description="妯″潡"),
    data_scope_code: str = Query(..., description="鏁版嵁鑼冨洿缂栫爜"),
    db: Session = Depends(get_db)
):
    """璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺"""
    logger.info(f"璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺: user_id={user_id}, module={module}, data_scope_code={data_scope_code}")
    
    try:
        data_scope_service = DataScopeService(db)
        user_data_scope = data_scope_service.set_user_data_scope(user_id, module, data_scope_code)
        
        logger.info(f"璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺鎴愬姛: user_id={user_id}, module={module}")
        
        return user_data_scope.to_dict()
    except ValueError as e:
        logger.warning(f"璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺澶辫触: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺澶辫触锛岃绋嶅悗閲嶈瘯")


@router.post("/check", summary="妫€鏌ユ暟鎹寖鍥存潈闄?)
async def check_data_scope(
    user_id: str = Query(..., description="鐢ㄦ埛ID"),
    module: str = Query(..., description="妯″潡"),
    target_id: str = Query(..., description="鐩爣鏁版嵁ID"),
    db: Session = Depends(get_db)
):
    """妫€鏌ユ暟鎹寖鍥存潈闄?""
    logger.info(f"妫€鏌ユ暟鎹寖鍥存潈闄? user_id={user_id}, module={module}, target_id={target_id}")
    
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
        logger.error(f"妫€鏌ユ暟鎹寖鍥存潈闄愬紓甯? error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="妫€鏌ユ暟鎹寖鍥存潈闄愬け璐ワ紝璇风◢鍚庨噸璇?)
