"""
站内信相关模型

包含：
- Message: 站内信表
- MessageRead: 站内信阅读记录表
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from ..base import BaseModel


class Message(BaseModel):
    """
    站内信表

    功能：
    - 站内信基本信息
    - 站内信类型（系统通知、私信、公告等）
    - 站内信状态
    """

    __tablename__ = "messages"

    tenant_id = Column(String(64), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, comment="租户ID")
    type = Column(String(50), nullable=False, comment="类型")
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, nullable=True, comment="内容")
    sender_id = Column(String(50), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="发送者ID")
    receiver_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, comment="接收者ID")
    receiver_type = Column(String(20), nullable=False, default="user", comment="接收者类型")
    priority = Column(Integer, nullable=False, default=0, comment="优先级")
    status = Column(String(20), nullable=False, default="unread", comment="状态")
    read_at = Column(DateTime, nullable=True, comment="阅读时间")
    extra_data = Column(JSON, nullable=True, comment="额外数据")

    # 关系
    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_messages")


class MessageRead(BaseModel):
    """
    站内信阅读记录表

    功能：
    - 记录站内信的阅读情况
    - 支持批量发送的阅读记录
    """

    __tablename__ = "message_reads"

    message_id = Column(String(50), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, comment="站内信ID")
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    read_at = Column(DateTime, nullable=False, comment="阅读时间")

    # 关系
    message = relationship("Message", backref="read_records")
    user = relationship("User", backref="message_reads")