"""
宀椾綅妯″瀷

鍔熻兘璇存槑锛?1. 宀椾綅鍩烘湰淇℃伅
2. 宀椾綅涓庣敤鎴峰叧鑱?3. 宀椾綅涓庨儴闂ㄥ叧鑱?
浣跨敤绀轰緥锛?    from common.database.models.position import Position
    
    # 创建宀椾綅
    position = Position(
        name="寮€鍙戝伐绋嬪笀",
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
    宀椾綅妯″瀷

    鍔熻兘锛?    - 宀椾綅鍩烘湰淇℃伅
    - 宀椾綅涓庣敤鎴峰叧鑱?    - 宀椾綅涓庨儴闂ㄥ叧鑱?
    灞炴€ц鏄庯細
    - id: 岗位ID锛堜富閿級
    - tenant_id: 租户ID
    - name: 宀椾綅名称
    - code: 宀椾綅编码
    - level: 宀椾綅级别
    - description: 描述
    - status: 状态?    - created_at: 创建时间
    - updated_at: 更新鏃堕棿
    """

    __tablename__ = "positions"

    # 鍩烘湰淇℃伅
    tenant_id = Column(String(64), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="宀椾綅名称")
    code = Column(String(50), nullable=False, comment="宀椾綅编码")
    level = Column(Integer, nullable=False, default=1, comment="宀椾綅级别")
    description = Column(Text, nullable=True, comment="描述")

    # 状态?    status = Column(String(20), nullable=False, default="active", comment="状态?)

    def __repr__(self):
        return f"<Position(id={self.id}, name={self.name}, code={self.code})>"

    def to_dict(self):
        """杞崲涓哄瓧鍏?""
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
        """妫€鏌ュ矖浣嶆槸鍚︽縺娲?""
        return self.status == "active"
