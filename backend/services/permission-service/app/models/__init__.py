# -*- coding: utf-8 -*-
"""
权限域服务模型

包含：
- Role: 角色模型
- Permission: 权限模型
- Menu: 菜单模型
- role_permissions: 角色权限关联表
- role_menus: 角色菜单关联表
"""

from app.models.role import Role
from app.models.permission import Permission
from app.models.menu import Menu
from app.models.association_tables import role_permissions, role_menus

__all__ = ["Role", "Permission", "Menu", "role_permissions", "role_menus"]