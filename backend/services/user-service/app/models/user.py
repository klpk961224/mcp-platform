# -*- coding: utf-8 -*-
"""
用户模型

功能说明：
1. 用户基本信息
2. 用户部门关联
3. 用户租户关联

使用示例：
    from app.models.user import User
    
    # 创建用户
    user = User(
        username="admin",
        email="admin@example.com",
        tenant_id="tenant_001"
    )
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel, TimestampMixin


class User(BaseModel, TimestampMixin):
    """
    用户模型
    
    功能：
    - 用户基本信息
    - 用户部门关联
    - 用户租户关联
    
    属性说明：
    - id: 用户ID（主键）
    - tenant_id: 租户ID（外键）
    - department_id: 部门ID（外键）
    - username: 用户名
    - email: 邮箱
    - phone: 手机号
    - full_name: 全名
    - avatar: 头像URL
    - status: 状态
    - is_active: 是否激活
    """
    
    __tablename__ = "users"
    
    # 基本信息
    tenant_id = Column(String(64), ForeignKey("tenants.id"), nullable=False, index=True, comment="租户ID")
    department_id = Column(String(64), ForeignKey("departments.id"), nullable=True, comment="部门ID")
    username = Column(String(50), nullable=False, unique=True, index=True, comment="用户名")
    email = Column(String(100), nullable=False, index=True, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    password_hash = Column(String(255), nullable=True, comment="密码哈希")
    
    # 用户信息
    full_name = Column(String(100), nullable=True, comment="全名")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    nickname = Column(String(50), nullable=True, comment="昵称")
    bio = Column(Text, nullable=True, comment="个人简介")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="active", comment="状态")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否激活")
    
    # 关系
    department = relationship("Department", back_populates="users")
    tenant = relationship("Tenant", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "department_id": self.department_id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "avatar": self.avatar,
            "nickname": self.nickname,
            "bio": self.bio,
            "status": self.status,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }