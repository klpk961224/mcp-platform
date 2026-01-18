# -*- coding: utf-8 -*-
"""
API v1妯″潡

鍖呭惈鎵€鏈塿1鐗堟湰鐨凙PI璺敱
"""

from fastapi import APIRouter
from app.api.v1.routers import todos, logs, messages, announcements

# 创建v1璺敱鍣?router = APIRouter(prefix="/api/v1")

# 娉ㄥ唽鎵€鏈夎矾鐢?router.include_router(todos.router, prefix="/todos", tags=["寰呭姙浠诲姟"])
router.include_router(logs.router, tags=["鏃ュ織瀹¤"])
router.include_router(messages.router, prefix="/messages", tags=["绔欏唴淇?])
router.include_router(announcements.router, prefix="/announcements", tags=["閫氱煡鍏憡"])

__all__ = ["router"]
