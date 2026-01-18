# -*- coding: utf-8 -*-
"""
閫氱煡妯″瀷

鍔熻兘璇存槑锛?
1. 绔欏唴淇＄鐞?
2. 閫氱煡鍏憡绠＄悊
3. 娑堟伅闃呰鐘舵€?

浣跨敤绀轰緥锛?
    from app.models.notification import Notification, NotificationRead
    
    # 鍒涘缓閫氱煡
    notification = Notification(
        title="绯荤粺閫氱煡",
        content="绯荤粺灏嗕簬浠婃櫄缁存姢",
        notification_type="system"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional

from common.database.base import BaseModel


class Notification(BaseModel):
    """
    閫氱煡妯″瀷
    
    鍔熻兘锛?
    - 绔欏唴淇＄鐞?
    - 閫氱煡鍏憡绠＄悊
    
    灞炴€ц鏄庯細
    - id: 閫氱煡ID锛堜富閿級
    - tenant_id: 绉熸埛ID
    - sender_id: 鍙戦€佽€匢D
    - sender_name: 鍙戦€佽€呭悕绉?
    - title: 鏍囬
    - content: 鍐呭
    - notification_type: 閫氱煡绫诲瀷
    - priority: 浼樺厛绾?
    - status: 鐘舵€?
    - send_time: 鍙戦€佹椂闂?
    - is_system: 鏄惁绯荤粺閫氱煡
    - target_type: 鐩爣绫诲瀷
    - target_ids: 鐩爣ID鍒楄〃锛圝SON锛?
    - attachment: 闄勪欢URL
    - read_count: 宸茶鏁伴噺
    - total_count: 鎬绘暟閲?
    - created_at: 鍒涘缓鏃堕棿
    """
    
    # 鍩烘湰淇℃伅
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="绉熸埛ID")
    sender_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="鍙戦€佽€匢D")
    sender_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="鍙戦€佽€呭悕绉?)
    
    # 鍐呭淇℃伅
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="鏍囬")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="鍐呭")
    
    # 绫诲瀷淇℃伅
    notification_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="閫氱煡绫诲瀷")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="normal", comment="浼樺厛绾?)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="sent", comment="鐘舵€?)
    
    # 鏃堕棿淇℃伅
    send_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="鍙戦€佹椂闂?)
    
    # 鐩爣淇℃伅
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="鏄惁绯荤粺閫氱煡")
    target_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="鐩爣绫诲瀷")
    target_ids: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="鐩爣ID鍒楄〃锛圝SON锛?)
    
    # 鎵╁睍淇℃伅
    attachment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="闄勪欢URL")
    
    # 缁熻淇℃伅
    read_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="宸茶鏁伴噺")
    total_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="鎬绘暟閲?)
    
    # 鍏崇郴
    reads = relationship("NotificationRead", back_populates="notification", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title={self.title}, type={self.notification_type})>"
    
    def to_dict(self):
        """杞崲涓哄瓧鍏?""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "title": self.title,
            "content": self.content,
            "notification_type": self.notification_type,
            "priority": self.priority,
            "status": self.status,
            "send_time": self.send_time.isoformat() if self.send_time else None,
            "is_system": self.is_system,
            "target_type": self.target_type,
            "target_ids": self.target_ids,
            "attachment": self.attachment,
            "read_count": self.read_count,
            "total_count": self.total_count,
            "read_rate": self.get_read_rate(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def get_read_rate(self) -> float:
        """鑾峰彇宸茶鐜?""
        if self.total_count == 0:
            return 0.0
        return round(self.read_count / self.total_count * 100, 2)
    
    def is_unread(self) -> bool:
        """妫€鏌ユ槸鍚︽湁鏈"""
        return self.read_count < self.total_count


class NotificationRead(BaseModel):
    """
    閫氱煡闃呰璁板綍妯″瀷
    
    鍔熻兘锛?
    - 閫氱煡闃呰鐘舵€?
    - 闃呰鏃堕棿璁板綍
    
    灞炴€ц鏄庯細
    - id: 闃呰璁板綍ID锛堜富閿級
    - notification_id: 閫氱煡ID锛堝閿級
    - user_id: 鐢ㄦ埛ID
    - username: 鐢ㄦ埛鍚?
    - is_read: 鏄惁宸茶
    - read_time: 闃呰鏃堕棿
    - created_at: 鍒涘缓鏃堕棿
    """
    
    # 鍩烘湰淇℃伅
    notification_id: Mapped[str] = mapped_column(String(64), ForeignKey("notification.id"), nullable=False, index=True, comment="閫氱煡ID")
    user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="鐢ㄦ埛ID")
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment="鐢ㄦ埛鍚?)
    
    # 闃呰鐘舵€?
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="鏄惁宸茶")
    read_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="闃呰鏃堕棿")
    
    # 鍏崇郴
    notification = relationship("Notification", back_populates="reads")
    
    def __repr__(self):
        return f"<NotificationRead(id={self.id}, user_id={self.user_id}, is_read={self.is_read})>"
    
    def to_dict(self):
        """杞崲涓哄瓧鍏?""
        return {
            "id": self.id,
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "username": self.username,
            "is_read": self.is_read,
            "read_time": self.read_time.isoformat() if self.read_time else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def mark_as_read(self):
        """鏍囪涓哄凡璇?""
        self.is_read = True
        self.read_time = datetime.now()
