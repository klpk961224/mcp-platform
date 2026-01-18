"""
绔欏唴淇＄浉鍏虫ā鍨?
鍖呭惈锛?- Message: 绔欏唴淇¤〃
- MessageRead: 绔欏唴淇￠槄璇昏褰曡〃
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from ..base import BaseModel, TimestampMixin


class Message(BaseModel, TimestampMixin):
    """
    绔欏唴淇¤〃

    鍔熻兘锛?    - 绔欏唴淇″熀鏈俊鎭?    - 绔欏唴淇＄被鍨嬶紙绯荤粺閫氱煡銆佺淇°€佸叕鍛婄瓑锛?    - 绔欏唴淇＄姸鎬?    """

    tenant_id: Mapped[str] = mapped_column(String(64), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, comment="租户ID")
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="类型")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="鏍囬")
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="鍐呭")
    sender_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="鍙戦€佽€匢D")
    receiver_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, comment="鎺ユ敹鑰匢D")
    receiver_type: Mapped[str] = mapped_column(String(20), nullable=False, default="user", comment="鎺ユ敹鑰呯被鍨?)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="浼樺厛绾?)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="unread", comment="状态?)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="闃呰鏃堕棿")
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="棰濆鏁版嵁")

    # 鍏崇郴
    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_messages")


class MessageRead(BaseModel, TimestampMixin):
    """
    绔欏唴淇￠槄璇昏褰曡〃

    鍔熻兘锛?    - 璁板綍绔欏唴淇＄殑闃呰鎯呭喌
    - 鏀寔鎵归噺鍙戦€佺殑闃呰璁板綍
    """

    message_id: Mapped[str] = mapped_column(String(50), ForeignKey("message.id", ondelete="CASCADE"), nullable=False, comment="绔欏唴淇D")
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="闃呰鏃堕棿")

    # 鍏崇郴
    message = relationship("Message", backref="read_records")
    user = relationship("User", backref="message_reads")
