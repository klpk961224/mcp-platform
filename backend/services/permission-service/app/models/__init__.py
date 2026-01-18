# -*- coding: utf-8 -*-
"""
权限域服务模型

包含：
- Role: 角色模型
- Permission: 权限模型
- Menu: 菜单模型
"""

from common.database.models.user import Role
from common.database.models.permission import Permission, Menu

__all__ = ["Role", "Permission", "Menu"]