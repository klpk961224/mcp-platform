"""
数据范围权限模型

功能说明：
1. 数据范围类型定义
2. 数据范围权限配置
3. 用户数据范围权限关联

使用示例：
    from common.database.models.data_scope import DataScope, UserDataScope
    
    # 创建数据范围
    data_scope = DataScope(
        name="本部门数据",
        code="department",
        description="只能查看本部门的数据"
    )
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel


class DataScope(BaseModel):
    """
    数据范围类型表
    
    功能：
    - 定义数据范围类型（全部、本部门、本部门及以下、仅本人等）
    - 配置数据范围的描述和说明
    
    属性说明：
    - id: 数据范围ID（主键）
    - name: 数据范围名称
    - code: 数据范围编码（all/department/department_and_below/self）
    - description: 描述
    - level: 权限级别（数字越大权限越高）
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "data_scopes"
    
    # 基本信息
    name = Column(String(100), nullable=False, comment="数据范围名称")
    code = Column(String(50), nullable=False, unique=True, comment="数据范围编码")
    description = Column(Text, nullable=True, comment="描述")
    
    # 权限级别
    level = Column(Integer, nullable=False, default=0, comment="权限级别")
    
    def __repr__(self):
        return f"<DataScope(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "level": self.level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserDataScope(BaseModel):
    """
    用户数据范围权限表
    
    功能：
    - 定义用户的数据范围权限
    - 支持按模块配置不同的数据范围
    
    属性说明：
    - id: 用户数据范围ID（主键）
    - user_id: 用户ID
    - module: 模块（user/department/tenant等）
    - data_scope_id: 数据范围ID
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "user_data_scopes"
    
    # 基本信息
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    module = Column(String(50), nullable=False, comment="模块")
    data_scope_id = Column(String(50), ForeignKey("data_scopes.id", ondelete="CASCADE"), nullable=False, comment="数据范围ID")
    
    # 关系
    user = relationship("User", backref="data_scopes")
    data_scope = relationship("DataScope", backref="user_data_scopes")
    
    def __repr__(self):
        return f"<UserDataScope(id={self.id}, user_id={self.user_id}, module={self.module}, data_scope_id={self.data_scope_id})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "module": self.module,
            "data_scope_id": self.data_scope_id,
            "data_scope_name": self.data_scope.name if self.data_scope else None,
            "data_scope_code": self.data_scope.code if self.data_scope else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }