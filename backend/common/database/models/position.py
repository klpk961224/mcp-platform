"""
岗位模型

功能说明：
1. 岗位基本信息
2. 岗位与用户关联
3. 岗位与部门关联

使用示例：
    from common.database.models.position import Position
    
    # 创建岗位
    position = Position(
        name="开发工程师",
        code="developer",
        tenant_id="tenant_001"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..base import BaseModel, TimestampMixin


class Position(BaseModel, TimestampMixin):
    """
    岗位模型

    功能：
    - 岗位基本信息
    - 岗位与用户关联
    - 岗位与部门关联

    属性说明：
    - id: 岗位ID（主键）
    - tenant_id: 租户ID
    - name: 岗位名称
    - code: 岗位编码
    - level: 岗位级别
    - description: 描述
    - status: 状态
    - created_at: 创建时间
    - updated_at: 更新时间
    """

    __tablename__ = "positions"

    # 基本信息
    tenant_id = Column(String(64), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="岗位名称")
    code = Column(String(50), nullable=False, comment="岗位编码")
    level = Column(Integer, nullable=False, default=1, comment="岗位级别")
    description = Column(Text, nullable=True, comment="描述")

    # 状态
    status = Column(String(20), nullable=False, default="active", comment="状态")

    def __repr__(self):
        return f"<Position(id={self.id}, name={self.name}, code={self.code})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "level": self.level,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def is_active(self):
        """检查岗位是否激活"""
        return self.status == "active"