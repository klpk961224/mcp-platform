"""
权限相关模型

包含：
- Permission: 权限表
- Menu: 菜单表
- RolePermission: 角色权限关联表
- RoleMenu: 角色菜单关联表
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel


# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True, comment='关联ID'),
    Column('role_id', String(50), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='角色ID'),
    Column('permission_id', String(50), ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False, comment='权限ID'),
    Column('created_at', DateTime, nullable=False, default=datetime.now, comment='创建时间')
)


# 角色菜单关联表
role_menus = Table(
    'role_menus',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True, comment='关联ID'),
    Column('role_id', String(50), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='角色ID'),
    Column('menu_id', String(50), ForeignKey('menus.id', ondelete='CASCADE'), nullable=False, comment='菜单ID'),
    Column('created_at', DateTime, nullable=False, default=datetime.now, comment='创建时间')
)


class Permission(BaseModel):
    """权限表"""
    
    __tablename__ = 'permissions'
    
    name = Column(String(100), nullable=False, comment='权限名称')
    code = Column(String(100), nullable=False, unique=True, comment='权限编码')
    type = Column(String(20), nullable=False, comment='类型')
    description = Column(Text, comment='描述')
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name}, code={self.code})>"


class Menu(BaseModel):
    """菜单表"""
    
    __tablename__ = 'menus'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='租户ID')
    name = Column(String(100), nullable=False, comment='菜单名称')
    path = Column(String(255), comment='菜单路径')
    icon = Column(String(100), comment='菜单图标')
    parent_id = Column(String(50), ForeignKey('menus.id', ondelete='CASCADE'), comment='父菜单ID')
    sort_order = Column(Integer, nullable=False, default=0, comment='排序')
    is_visible = Column(Boolean, nullable=False, default=True, comment='是否可见')
    status = Column(String(20), nullable=False, default='active', comment='状态')
    
    # 关系
    tenant = relationship('Tenant', back_populates='menus')
    parent = relationship('Menu', remote_side='Menu.id', backref='children')
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name={self.name}, path={self.path})>"