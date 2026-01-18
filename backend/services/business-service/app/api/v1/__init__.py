# -*- coding: utf-8 -*-
"""
API v1妯″潡

鍖呭惈鎵€鏈塿1鐗堟湰鐨凙PI璺敱
"""

from fastapi import APIRouter

# 鍒涘缓v1璺敱鍣?router = APIRouter(prefix="/api/v1")

# 瀵煎叆璺敱
from app.api.v1.routers import workflows

# 娉ㄥ唽璺敱
router.include_router(workflows.router, tags=["宸ヤ綔娴?])

__all__ = ["router"]
