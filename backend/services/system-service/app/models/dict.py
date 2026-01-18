# -*- coding: utf-8 -*-
"""
瀛楀吀妯″瀷

鍔熻兘璇存槑锛?1. 瀛楀吀鍒嗙被绠＄悊
2. 瀛楀吀椤圭鐞?3. 瀛楀吀缂撳瓨

浣跨敤绀轰緥锛?    from app.models.dict import Dict, DictItem
    
    # 鍒涘缓瀛楀吀
    dict = Dict(
        name="鐢ㄦ埛鐘舵€?,
        code="user_status",
        description="鐢ㄦ埛鐘舵€佸瓧鍏?
    )
    
    # 鍒涘缓瀛楀吀椤?    item = DictItem(
        dict_id=dict.id,
        label="婵€娲?,
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
    瀛楀吀妯″瀷
    
    鍔熻兘锛?    - 瀛楀吀鍒嗙被绠＄悊
    - 瀛楀瓧鍏搁」绠＄悊
    
    灞炴€ц鏄庯細
    - id: 瀛楀吀ID锛堜富閿級
    - tenant_id: 绉熸埛ID
    - name: 瀛楀吀鍚嶇О
    - code: 瀛楀吀缂栫爜锛堝敮涓€锛?    - description: 瀛楀吀鎻忚堪
    - is_system: 鏄惁绯荤粺瀛楀吀锛堜笉鍙垹闄わ級
    - status: 鐘舵€侊紙active/inactive锛?    - created_at: 鍒涘缓鏃堕棿
    - updated_at: 鏇存柊鏃堕棿
    """
    
    __tablename__ = "dicts"
    
    # 鍩烘湰淇℃伅
    tenant_id = Column(String(64), nullable=False, index=True, comment="绉熸埛ID")
    name = Column(String(100), nullable=False, comment="瀛楀吀鍚嶇О")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="瀛楀吀缂栫爜")
    description = Column(Text, nullable=True, comment="瀛楀吀鎻忚堪")
    
    # 鐘舵€佷俊鎭?    is_system = Column(Boolean, nullable=False, default=False, comment="鏄惁绯荤粺瀛楀吀")
    status = Column(String(20), nullable=False, default="active", comment="鐘舵€?)
    
    # 鍏崇郴
    items = relationship("DictItem", back_populates="dict", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Dict(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """杞崲涓哄瓧鍏?""
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
    瀛楀吀椤规ā鍨?    
    鍔熻兘锛?    - 瀛楀吀椤圭鐞?    
    灞炴€ц鏄庯細
    - id: 瀛楀吀椤笽D锛堜富閿級
    - dict_id: 瀛楀吀ID锛堝閿級
    - label: 瀛楀吀椤规爣绛?    - value: 瀛楀吀椤瑰€?    - description: 瀛楀吀椤规弿杩?    - sort_order: 鎺掑簭
    - is_default: 鏄惁榛樿鍊?    - status: 鐘舵€侊紙active/inactive锛?    - created_at: 鍒涘缓鏃堕棿
    - updated_at: 鏇存柊鏃堕棿
    """
    
    __tablename__ = "dict_items"
    
    # 鍩烘湰淇℃伅
    dict_id = Column(String(64), ForeignKey("dicts.id"), nullable=False, index=True, comment="瀛楀吀ID")
    label = Column(String(100), nullable=False, comment="瀛楀吀椤规爣绛?)
    value = Column(String(100), nullable=False, comment="瀛楀吀椤瑰€?)
    description = Column(Text, nullable=True, comment="瀛楀吀椤规弿杩?)
    
    # 鎺掑簭鍜岀姸鎬?    sort_order = Column(Integer, nullable=False, default=0, comment="鎺掑簭")
    is_default = Column(Boolean, nullable=False, default=False, comment="鏄惁榛樿鍊?)
    status = Column(String(20), nullable=False, default="active", comment="鐘舵€?)
    
    # 鍏崇郴
    dict = relationship("Dict", back_populates="items")
    
    def __repr__(self):
        return f"<DictItem(id={self.id}, label={self.label}, value={self.value})>"
    
    def to_dict(self):
        """杞崲涓哄瓧鍏?""
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
