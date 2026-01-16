# -*- coding: utf-8 -*-
"""
部门模型

功能说明：
1. 部门基本信息
2. 部门树形结构
3. 部门租户关联

使用示例：
    from app.models.department import Department
    
    # 创建部门
    dept = Department(
        name="技术部",
        code="tech",
        tenant_id="tenant_001"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class Department(BaseModel):
    """
    部门模型
    
    功能：
    - 部门基本信息
    - 部门树形结构
    - 部门租户关联
    
    属性说明：
    - id: 部门ID（主键）
    - tenant_id: 租户ID（外键）
    - parent_id: 父部门ID
    - name: 部门名称
    - code: 部门编码
    - level: 部门层级
    - sort_order: 排序
    - description: 描述
    """
    
    __tablename__ = "departments"
    
    # 基本信息
    tenant_id = Column(String(64), ForeignKey("tenants.id"), nullable=False, index=True, comment="租户ID")
    parent_id = Column(String(64), ForeignKey("departments.id"), nullable=True, comment="父部门ID")
    name = Column(String(100), nullable=False, comment="部门名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="部门编码")
    
    # 层级信息
    level = Column(Integer, nullable=False, default=1, comment="部门层级")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序")
    
    # 扩展信息
    description = Column(Text, nullable=True, comment="描述")
    leader_id = Column(String(64), nullable=True, comment="负责人ID")
    phone = Column(String(20), nullable=True, comment="联系电话")
    email = Column(String(100), nullable=True, comment="联系邮箱")
    
    # 关系
    parent = relationship("Department", remote_side='Department.id', backref="children")
    users = relationship("User", back_populates="department")
    tenant = relationship("Tenant", back_populates="departments")
    
    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "code": self.code,
            "level": self.level,
            "sort_order": self.sort_order,
            "description": self.description,
            "leader_id": self.leader_id,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def to_tree_dict(self):
        """转换为树形字典"""
        data = self.to_dict()
        data["children"] = [child.to_tree_dict() for child in self.children]
        return data