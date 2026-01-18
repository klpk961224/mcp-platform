# -*- coding: utf-8 -*-
"""
API模块

包含所有API版本的路由
"""

from app.api.v1 import router as v1_router

__all__ = ["v1_router"]