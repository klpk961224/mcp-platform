# -*- coding: utf-8 -*-
"""
用户模型

功能说明：
1. 用户基本信息
2. 用户认证信息
3. 用户状态管理

使用示例：
    from app.models.user import User
    
    # 创建用户
    user = User(
        username="admin",
        email="admin@example.com",
        password_hash="hashed_password"
    )
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class User(BaseModel):
    """
    用户模型
    
    功能：
    - 用户基本信息（用户名、邮箱、手机）
    - 用户认证信息（密码哈希）
    - 用户状态管理（激活、禁用）
    - 租户隔离
    
    属性说明：
    - id: 用户ID（主键）
    - tenant_id: 租户ID（多租户隔离）
    - username: 用户名（唯一）
    - email: 邮箱
    - phone: 手机号
    - password_hash: 密码哈希
    - status: 状态（active/inactive）
    - is_superuser: 是否超级管理员
    - last_login_at: 最后登录时间
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "users"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    username = Column(String(50), nullable=False, unique=True, index=True, comment="用户名")
    email = Column(String(100), nullable=False, index=True, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    
    # 认证信息
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="active", comment="状态")
    is_superuser = Column(Boolean, nullable=False, default=False, comment="是否超级管理员")
    
    # 登录信息
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    
    # 扩展信息
    avatar = Column(String(255), nullable=True, comment="头像URL")
    nickname = Column(String(50), nullable=True, comment="昵称")
    bio = Column(Text, nullable=True, comment="个人简介")
    
    # 关系
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "is_superuser": self.is_superuser,
            "avatar": self.avatar,
            "nickname": self.nickname,
            "bio": self.bio,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }