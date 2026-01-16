# -*- coding: utf-8 -*-
"""
权限模型

功能说明：
1. 权限基本信息
2. 权限类型管理
3. 权限资源关联

使用示例：
    from app.models.permission import Permission
    
    # 创建权限
    permission = Permission(
        name="用户管理",
        code="user:manage",
        resource="user",
        action="manage"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel
from app.models.association_tables import role_permissions


class Permission(BaseModel):
    """
    权限模型
    
    功能：
    - 权限基本信息
    - 权限类型管理
    - 权限资源关联
    
    属性说明：
    - id: 权限ID（主键）
    - tenant_id: 租户ID
    - name: 权限名称
    - code: 权限编码
    - resource: 资源类型
    - action: 操作类型
    - type: 权限类型
    - description: 描述
    """
    
    __tablename__ = "permissions"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="权限名称")
    code = Column(String(100), nullable=False, unique=True, index=True, comment="权限编码")
    
    # 权限信息
    resource = Column(String(50), nullable=False, comment="资源类型")
    action = Column(String(50), nullable=False, comment="操作类型")
    type = Column(String(20), nullable=False, default="menu", comment="权限类型")
    
    # 层级信息
    level = Column(Integer, nullable=False, default=1, comment="权限级别")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序")
    
    # 扩展信息
    description = Column(Text, nullable=True, comment="描述")
    
    # 关系
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "resource": self.resource,
            "action": self.action,
            "type": self.type,
            "level": self.level,
            "sort_order": self.sort_order,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }