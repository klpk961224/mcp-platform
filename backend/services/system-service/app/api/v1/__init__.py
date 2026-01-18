# -*- coding: utf-8 -*-
"""
API v1妯″潡

鍖呭惈鎵€鏈塿1鐗堟湰鐨凙PI璺敱
"""

from fastapi import APIRouter
from app.api.v1.routers import mcp_tools, datasources, dictionaries, error_codes, regions, sensitive_words

# 鍒涘缓v1璺敱鍣?router = APIRouter(prefix="/api/v1")

# 娉ㄥ唽鎵€鏈夎矾鐢?router.include_router(mcp_tools.router, prefix="/mcp-tools", tags=["MCP宸ュ叿"])
router.include_router(datasources.router, prefix="/datasources", tags=["鏁版嵁婧?])
router.include_router(dictionaries.router, tags=["瀛楀吀"])
router.include_router(error_codes.router, prefix="/error-codes", tags=["閿欒鐮?])
router.include_router(regions.router, prefix="/regions", tags=["鍦板尯"])
router.include_router(sensitive_words.router, prefix="/sensitive-words", tags=["鏁忔劅璇?])

__all__ = ["router"]
