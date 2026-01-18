"""
租户相关模型

包含：
- Tenant: 租户表
"""

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel, TimestampMixin, FullModelMixin


class Tenant(BaseModel, FullModelMixin):
    """租户表"""
    
    __tablename__ = 'tenants'
    
    name = Column(String(100), nullable=False, comment='租户名称')
    code = Column(String(50), nullable=False, unique=True, comment='租户编码')
    status = Column(String(20), nullable=False, default='active', comment='状态')
    description = Column(Text, comment='描述')
    
    # 关系
    users = relationship('User', back_populates='tenant', cascade='all, delete-orphan')
    departments = relationship('Department', back_populates='tenant', cascade='all, delete-orphan')
    roles = relationship('Role', back_populates='tenant', cascade='all, delete-orphan')
    menus = relationship('Menu', back_populates='tenant', cascade='all, delete-orphan')
    mcp_tools = relationship('MCPTool', back_populates='tenant', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.name}, code={self.code})>"