"""
鏁忔劅璇嶇浉鍏虫ā鍨?
鍖呭惈锛?- SensitiveWord: 鏁忔劅璇嶈〃
"""

from sqlalchemy import Column, String, Integer, Text
from ..base import BaseModel, TimestampMixin


class SensitiveWord(BaseModel, TimestampMixin):
    """
    鏁忔劅璇嶈〃

    鍔熻兘锛?    - 鏁忔劅璇嶅熀鏈俊鎭?    - 鏁忔劅璇嶅垎绫?    - 鏁忔劅璇嶇姸鎬?    """

    __tablename__ = "sensitive_words"

    word = Column(String(200), nullable=False, comment="鏁忔劅璇?)
    category = Column(String(50), nullable=False, comment="鍒嗙被")
    level = Column(Integer, nullable=False, default=1, comment="鏁忔劅级别")
    replacement = Column(String(200), nullable=True, comment="鏇挎崲璇?)
    description = Column(Text, nullable=True, comment="描述")
    status = Column(String(20), nullable=False, default="active", comment="状态?)
