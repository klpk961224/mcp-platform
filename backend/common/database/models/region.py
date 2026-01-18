"""
地区相关模型

包含：
- Region: 地区表
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel, TimestampMixin


class Region(BaseModel, TimestampMixin):
    """
    地区表

    功能：
    - 地区基本信息
    - 地区层级关系（省/市/区/街道）
    - 地区编码
    """

    __tablename__ = "regions"

    name = Column(String(100), nullable=False, comment="地区名称")
    code = Column(String(20), unique=True, nullable=False, index=True, comment="地区编码")
    level = Column(String(20), nullable=False, comment="地区级别")
    parent_id = Column(String(50), ForeignKey("regions.id", ondelete="CASCADE"), nullable=True, comment="父级ID")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序")
    status = Column(String(20), nullable=False, default="active", comment="状态")

    # 自引用关系
    parent = relationship("Region", remote_side="Region.id", back_populates="children")
    children = relationship("Region", back_populates="parent", cascade="all, delete-orphan")