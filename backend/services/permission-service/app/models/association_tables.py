# -*- coding: utf-8 -*-
"""
权限域服务关联表

包含：
- role_permissions: 角色权限关联表
- role_menus: 角色菜单关联表
"""

from sqlalchemy import Column, String, ForeignKey, Table
from common.database.base import Base

# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', String(64), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', String(64), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
    comment='角色权限关联表'
)

# 角色菜单关联表
role_menus = Table(
    'role_menus',
    Base.metadata,
    Column('role_id', String(64), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('menu_id', String(64), ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True),
    comment='角色菜单关联表'
)

__all__ = ["role_permissions", "role_menus"]