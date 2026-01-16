# -*- coding: utf-8 -*-
"""
API v1模块

包含所有v1版本的API路由
"""

from fastapi import APIRouter
from app.api.v1.routers import todos

# 创建v1路由器
router = APIRouter(prefix="/api/v1")

# 注册所有路由
router.include_router(todos.router, prefix="/todos", tags=["待办任务"])

__all__ = ["router"]