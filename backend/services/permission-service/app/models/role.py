# -*- coding: utf-8 -*-
"""
角色模型

功能说明：
1. 角色基本信息
2. 角色权限关联
3. 角色菜单关联

使用示例：
    from app.models.role import Role
    
    # 创建角色
    role = Role(
        name="管理员",
        code="admin",
        tenant_id="tenant_001"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel
from app.models.association_tables import role_permissions, role_menus


class Role(BaseModel):
    """
    角色模型
    
    功能：
    - 角色基本信息
    - 角色权限关联
    - 角色菜单关联
    
    属性说明：
    - id: 角色ID（主键）
    - tenant_id: 租户ID
    - name: 角色名称
    - code: 角色编码（唯一）
    - description: 描述
    - is_system: 是否系统角色
    - status: 状态（active/inactive）
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "roles"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="角色名称")
    code = Column(String(50), nullable=False, comment="角色编码")
    description = Column(Text, nullable=True, comment="描述")
    
    # 系统标识
    is_system = Column(Boolean, nullable=False, default=False, comment="是否系统角色")
    
    # 状态
    status = Column(String(20), nullable=False, default="active", comment="状态")
    
    # 关系
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    menus = relationship("Menu", secondary=role_menus, back_populates="roles")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, code={self.code})>"
    
    def is_active(self):
        """检查角色是否激活"""
        return self.status == "active"
    
    def is_system_role(self):
        """检查是否为系统角色"""
        return self.is_system
    
    def has_permission(self, permission_code):
        """检查是否有指定权限"""
        return any(p.code == permission_code for p in self.permissions)
    
    def has_menu(self, menu_id):
        """检查是否有指定菜单"""
        return any(m.id == menu_id for m in self.menus)
