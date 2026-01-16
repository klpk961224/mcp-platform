# -*- coding: utf-8 -*-
"""
菜单模型

功能说明：
1. 菜单基本信息
2. 菜单树形结构
3. 菜单类型管理

使用示例：
    from app.models.menu import Menu
    
    # 创建菜单
    menu = Menu(
        name="用户管理",
        code="user_manage",
        path="/users",
        menu_type="menu"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel
from app.models.association_tables import role_menus


class Menu(BaseModel):
    """
    菜单模型
    
    功能：
    - 菜单基本信息
    - 菜单树形结构
    - 菜单类型管理
    
    属性说明：
    - id: 菜单ID（主键）
    - tenant_id: 租户ID
    - parent_id: 父菜单ID
    - name: 菜单名称
    - code: 菜单编码
    - path: 路由路径
    - component: 组件路径
    - icon: 图标
    - menu_type: 菜单类型
    - level: 菜单层级
    - sort_order: 排序
    - is_visible: 是否可见
    - is_cache: 是否缓存
    """
    
    __tablename__ = "menus"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    parent_id = Column(String(64), ForeignKey("menus.id"), nullable=True, comment="父菜单ID")
    name = Column(String(100), nullable=False, comment="菜单名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="菜单编码")
    
    # 路由信息
    path = Column(String(255), nullable=True, comment="路由路径")
    component = Column(String(255), nullable=True, comment="组件路径")
    redirect = Column(String(255), nullable=True, comment="重定向路径")
    
    # 显示信息
    icon = Column(String(100), nullable=True, comment="图标")
    title = Column(String(100), nullable=True, comment="菜单标题")
    
    # 菜单信息
    menu_type = Column(String(20), nullable=False, default="menu", comment="菜单类型")
    level = Column(Integer, nullable=False, default=1, comment="菜单层级")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序")
    
    # 状态信息
    is_visible = Column(String(1), nullable=False, default="1", comment="是否可见")
    is_cache = Column(String(1), nullable=False, default="0", comment="是否缓存")
    is_affix = Column(String(1), nullable=False, default="0", comment="是否固定")
    
    # 扩展信息
    description = Column(Text, nullable=True, comment="描述")
    
    # 关系
    parent = relationship("Menu", remote_side='Menu.id', backref="children")
    roles = relationship("Role", secondary="role_menus", back_populates="menus")
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "code": self.code,
            "path": self.path,
            "component": self.component,
            "redirect": self.redirect,
            "icon": self.icon,
            "title": self.title,
            "menu_type": self.menu_type,
            "level": self.level,
            "sort_order": self.sort_order,
            "is_visible": self.is_visible,
            "is_cache": self.is_cache,
            "is_affix": self.is_affix,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def to_tree_dict(self):
        """转换为树形字典"""
        data = self.to_dict()
        data["children"] = [child.to_tree_dict() for child in self.children]
        return data
    
    def is_visible_menu(self):
        """检查是否为可见菜单"""
        return self.is_visible == "1" and self.menu_type == "menu"