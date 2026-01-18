"""
鍦板尯鐩稿叧妯″瀷

鍖呭惈锛?- Region: 鍦板尯琛?"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel, TimestampMixin


class Region(BaseModel, TimestampMixin):
    """
    鍦板尯琛?
    鍔熻兘锛?    - 鍦板尯鍩烘湰淇℃伅
    - 鍦板尯灞傜骇鍏崇郴锛堢渷/甯?鍖?琛楅亾锛?    - 鍦板尯缂栫爜
    """

    __tablename__ = "regions"

    name = Column(String(100), nullable=False, comment="鍦板尯鍚嶇О")
    code = Column(String(20), unique=True, nullable=False, index=True, comment="鍦板尯缂栫爜")
    level = Column(String(20), nullable=False, comment="鍦板尯绾у埆")
    parent_id = Column(String(50), ForeignKey("regions.id", ondelete="CASCADE"), nullable=True, comment="鐖剁骇ID")
    sort_order = Column(Integer, nullable=False, default=0, comment="鎺掑簭")
    status = Column(String(20), nullable=False, default="active", comment="鐘舵€?)

    # 鑷紩鐢ㄥ叧绯?    parent = relationship("Region", remote_side="Region.id", back_populates="children")
    children = relationship("Region", back_populates="parent", cascade="all, delete-orphan")
