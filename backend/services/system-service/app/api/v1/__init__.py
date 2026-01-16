# -*- coding: utf-8 -*-
"""
API v1模块

包含所有v1版本的API路由
"""

from fastapi import APIRouter
from app.api.v1.routers import mcp_tools, datasources, dictionaries

# 创建v1路由器
router = APIRouter(prefix="/api/v1")

# 注册所有路由
router.include_router(mcp_tools.router, prefix="/mcp-tools", tags=["MCP工具"])
router.include_router(datasources.router, prefix="/datasources", tags=["数据源"])
router.include_router(dictionaries.router, prefix="/dictionaries", tags=["字典"])

__all__ = ["router"]