# -*- coding: utf-8 -*-
"""
用户服务模型

包含：
- User: 用户模型
- Department: 部门模型（从common导入）
- Tenant: 租户模型（从common导入）
"""

from .user import User
from common.database.models import Department, Tenant

__all__ = ["User", "Department", "Tenant"]