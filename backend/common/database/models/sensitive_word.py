"""
敏感词相关模型

包含：
- SensitiveWord: 敏感词表
"""

from sqlalchemy import Column, String, Integer, Text
from ..base import BaseModel, TimestampMixin


class SensitiveWord(BaseModel, TimestampMixin):
    """
    敏感词表

    功能：
    - 敏感词基本信息
    - 敏感词分类
    - 敏感词状态
    """

    __tablename__ = "sensitive_words"

    word = Column(String(200), nullable=False, comment="敏感词")
    category = Column(String(50), nullable=False, comment="分类")
    level = Column(Integer, nullable=False, default=1, comment="敏感级别")
    replacement = Column(String(200), nullable=True, comment="替换词")
    description = Column(Text, nullable=True, comment="描述")
    status = Column(String(20), nullable=False, default="active", comment="状态")