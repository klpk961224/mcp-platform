# -*- coding: utf-8 -*-
"""
租户模型

功能说明：
1. 租户基本信息
2. 租户套餐管理
3. 租户状态管理

使用示例：
    from app.models.tenant import Tenant
    
    # 创建租户
    tenant = Tenant(
        name="示例公司",
        code="example",
        package_id="basic"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class Tenant(BaseModel):
    """
    租户模型
    
    功能：
    - 租户基本信息
    - 租户套餐管理
    - 租户状态管理
    
    属性说明：
    - id: 租户ID（主键）
    - name: 租户名称
    - code: 租户编码（唯一）
    - status: 状态（active/inactive/expired）
    - description: 描述
    - package_id: 套餐ID
    - max_users: 最大用户数
    - max_departments: 最大部门数
    - max_storage: 最大存储空间（MB）
    - expires_at: 过期时间
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "tenants"
    
    # 基本信息
    name = Column(String(100), nullable=False, comment="租户名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="租户编码")
    status = Column(String(20), nullable=False, default="active", comment="状态")
    description = Column(Text, nullable=True, comment="描述")
    
    # 套餐信息
    package_id = Column(String(50), nullable=True, comment="套餐ID")
    max_users = Column(Integer, nullable=False, default=100, comment="最大用户数")
    max_departments = Column(Integer, nullable=False, default=50, comment="最大部门数")
    max_storage = Column(Integer, nullable=False, default=10240, comment="最大存储空间（MB）")
    
    # 过期信息
    expires_at = Column(DateTime, nullable=True, comment="过期时间")
    
    # 关系
    users = relationship("User", back_populates="tenant")
    departments = relationship("Department", back_populates="tenant")
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.name}, code={self.code})>"
    
    def is_active(self):
        """检查租户是否激活"""
        return self.status == "active"
    
    def is_expired(self):
        """检查租户是否已过期"""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at
    
    def is_valid(self):
        """检查租户是否有效"""
        return self.is_active() and not self.is_expired()
    
    def get_user_count(self):
        """获取用户数量"""
        return len(self.users)
    
    def get_department_count(self):
        """获取部门数量"""
        return len(self.departments)
