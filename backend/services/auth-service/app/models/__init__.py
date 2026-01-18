# -*- coding: utf-8 -*-
"""
数据模型模块

功能说明：
1. SQLAlchemy ORM模型定义
2. 数据库表结构映射
3. 模型关系定义

使用示例：
    from app.models.token import Token
"""

from .token import Token
from common.database.models.user import User

__all__ = ["User", "Token"]