# -*- coding: utf-8 -*-
"""
API v1模块

包含所有v1版本的API路由
"""

from fastapi import APIRouter
from app.api.v1.routers import mcp_tools, datasources, dictionaries, error_codes, regions, sensitive_words

# 创建v1路由器
router = APIRouter(prefix="/api/v1")

# 注册所有路由
router.include_router(mcp_tools.router, prefix="/mcp-tools", tags=["MCP工具"])
router.include_router(datasources.router, prefix="/datasources", tags=["数据源"])
router.include_router(dictionaries.router, tags=["字典"])
router.include_router(error_codes.router, prefix="/error-codes", tags=["错误码"])
router.include_router(regions.router, prefix="/regions", tags=["地区"])
router.include_router(sensitive_words.router, prefix="/sensitive-words", tags=["敏感词"])

__all__ = ["router"]