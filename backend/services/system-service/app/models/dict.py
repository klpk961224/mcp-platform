# -*- coding: utf-8 -*-
"""
字典模型

功能说明：
1. 字典分类管理
2. 字典项管理
3. 字典缓存

使用示例：
    from app.models.dict import Dict, DictItem
    
    # 创建字典
    dict = Dict(
        name="用户状态",
        code="user_status",
        description="用户状态字典"
    )
    
    # 创建字典项
    item = DictItem(
        dict_id=dict.id,
        label="激活",
        value="active",
        sort_order=1
    )
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class Dict(BaseModel):
    """
    字典模型
    
    功能：
    - 字典分类管理
    - 字字典项管理
    
    属性说明：
    - id: 字典ID（主键）
    - tenant_id: 租户ID
    - name: 字典名称
    - code: 字典编码（唯一）
    - description: 字典描述
    - is_system: 是否系统字典（不可删除）
    - status: 状态（active/inactive）
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "dicts"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="字典名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="字典编码")
    description = Column(Text, nullable=True, comment="字典描述")
    
    # 状态信息
    is_system = Column(Boolean, nullable=False, default=False, comment="是否系统字典")
    status = Column(String(20), nullable=False, default="active", comment="状态")
    
    # 关系
    items = relationship("DictItem", back_populates="dict", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Dict(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "is_system": self.is_system,
            "status": self.status,
            "item_count": len(self.items),
            "items": [item.to_dict() for item in self.items] if self.items else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DictItem(BaseModel):
    """
    字典项模型
    
    功能：
    - 字典项管理
    
    属性说明：
    - id: 字典项ID（主键）
    - dict_id: 字典ID（外键）
    - label: 字典项标签
    - value: 字典项值
    - description: 字典项描述
    - sort_order: 排序
    - is_default: 是否默认值
    - status: 状态（active/inactive）
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "dict_items"
    
    # 基本信息
    dict_id = Column(String(64), ForeignKey("dicts.id"), nullable=False, index=True, comment="字典ID")
    label = Column(String(100), nullable=False, comment="字典项标签")
    value = Column(String(100), nullable=False, comment="字典项值")
    description = Column(Text, nullable=True, comment="字典项描述")
    
    # 排序和状态
    sort_order = Column(Integer, nullable=False, default=0, comment="排序")
    is_default = Column(Boolean, nullable=False, default=False, comment="是否默认值")
    status = Column(String(20), nullable=False, default="active", comment="状态")
    
    # 关系
    dict = relationship("Dict", back_populates="items")
    
    def __repr__(self):
        return f"<DictItem(id={self.id}, label={self.label}, value={self.value})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "dict_id": self.dict_id,
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "sort_order": self.sort_order,
            "is_default": self.is_default,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }