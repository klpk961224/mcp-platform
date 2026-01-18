# -*- coding: utf-8 -*-
"""
API v1模块

包含所有v1版本的API路由
"""

from fastapi import APIRouter

# 创建v1路由器
router = APIRouter(prefix="/api/v1")

# 导入路由
from app.api.v1.routers import workflows

# 注册路由
router.include_router(workflows.router, tags=["工作流"])

__all__ = ["router"]