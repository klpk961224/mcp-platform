# -*- coding: utf-8 -*-
"""
鏃ュ織瀹¤API璺敱
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
from app.services.log_service import LogService

router = APIRouter(prefix="/logs", tags=["鏃ュ織瀹¤"])


@router.get("/login", summary="鑾峰彇鐧诲綍鏃ュ織鍒楄〃")
async def get_login_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = Query(None, description="鐢ㄦ埛ID"),
    tenant_id: Optional[str] = Query(None, description="绉熸埛ID"),
    db: Session = Depends(get_db)
):
    """鑾峰彇鐧诲綍鏃ュ織鍒楄〃"""
    logger.info(f"鑾峰彇鐧诲綍鏃ュ織鍒楄〃: page={page}")
    
    try:
        log_service = LogService(db)
        
        if user_id:
            logs = log_service.get_user_login_logs(user_id, page, page_size)
            total = log_service.log_repo.count_failed_logins_by_user(user_id, hours=24 * 365) + \
                   len(log_service.log_repo.get_user_login_logs(user_id, 1, 1000))
        else:
            logs = log_service.log_repo.get_tenant_login_logs(
                tenant_id or "default",
                page=page,
                page_size=page_size
            )
            total = log_service.log_repo.count_failed_logins_by_user(user_id or "", hours=24 * 365)
        
        items = [log.to_dict() for log in logs]
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"鑾峰彇鐧诲綍鏃ュ織鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鐧诲綍鏃ュ織鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/login/statistics", summary="鑾峰彇鐧诲綍缁熻淇℃伅")
async def get_login_statistics(
    tenant_id: str = Query(..., description="绉熸埛ID"),
    days: int = Query(7, ge=1, le=30, description="缁熻澶╂暟"),
    db: Session = Depends(get_db)
):
    """鑾峰彇鐧诲綍缁熻淇℃伅"""
    logger.info(f"鑾峰彇鐧诲綍缁熻淇℃伅: tenant_id={tenant_id}, days={days}")
    
    try:
        log_service = LogService(db)
        statistics = log_service.get_login_statistics(tenant_id, days)
        
        return statistics
    except Exception as e:
        logger.error(f"鑾峰彇鐧诲綍缁熻淇℃伅寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鐧诲綍缁熻淇℃伅澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/operation", summary="鑾峰彇鎿嶄綔鏃ュ織鍒楄〃")
async def get_operation_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = Query(None, description="鐢ㄦ埛ID"),
    tenant_id: Optional[str] = Query(None, description="绉熸埛ID"),
    db: Session = Depends(get_db)
):
    """鑾峰彇鎿嶄綔鏃ュ織鍒楄〃"""
    logger.info(f"鑾峰彇鎿嶄綔鏃ュ織鍒楄〃: page={page}")
    
    try:
        log_service = LogService(db)
        
        if user_id:
            logs = log_service.get_user_operation_logs(user_id, page, page_size)
            total = len(log_service.log_repo.get_user_operation_logs(user_id, 1, 1000))
        else:
            logs = log_service.log_repo.get_tenant_operation_logs(
                tenant_id or "default",
                page=page,
                page_size=page_size
            )
            total = len(log_service.log_repo.get_user_operation_logs(tenant_id or "default", 1, 1000))
        
        items = [log.to_dict() for log in logs]
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"鑾峰彇鎿嶄綔鏃ュ織鍒楄〃寮傚父: error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鎿嶄綔鏃ュ織鍒楄〃澶辫触锛岃绋嶅悗閲嶈瘯")


@router.get("/operation/slow", summary="鑾峰彇鎱㈡煡璇㈡棩蹇?)
async def get_slow_queries(
    threshold: int = Query(1000, ge=100, description="闃堝€硷紙姣锛?),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """鑾峰彇鎱㈡煡璇㈡棩蹇?""
    logger.info(f"鑾峰彇鎱㈡煡璇㈡棩蹇? threshold={threshold}")
    
    try:
        log_service = LogService(db)
        logs = log_service.log_repo.get_slow_queries(threshold, page, page_size)
        
        items = [log.to_dict() for log in logs]
        total = len(log_service.log_repo.get_slow_queries(threshold, 1, 1000))
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"鑾峰彇鎱㈡煡璇㈡棩蹇楀紓甯? error={str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="鑾峰彇鎱㈡煡璇㈡棩蹇楀け璐ワ紝璇风◢鍚庨噸璇?)

