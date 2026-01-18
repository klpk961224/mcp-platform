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
    - 鍦板尯灞傜骇鍏崇郴锛堢渷/甯?鍖?琛楅亾锛?    - 鍦板尯编码
    """

    __tablename__ = "regions"

    name = Column(String(100), nullable=False, comment="鍦板尯名称")
    code = Column(String(20), unique=True, nullable=False, index=True, comment="鍦板尯编码")
    level = Column(String(20), nullable=False, comment="鍦板尯级别")
    parent_id = Column(String(50), ForeignKey("regions.id", ondelete="CASCADE"), nullable=True, comment="父级ID")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序")
    status = Column(String(20), nullable=False, default="active", comment="状态?)

    # 鑷紩鐢ㄥ叧绯?    parent = relationship("Region", remote_side="Region.id", back_populates="children")
    children = relationship("Region", back_populates="parent", cascade="all, delete-orphan")
