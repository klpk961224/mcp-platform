"""
閫氱煡鍏憡鐩稿叧妯″瀷

鍖呭惈锛?- Announcement: 閫氱煡鍏憡琛?- AnnouncementRead: 閫氱煡鍏憡闃呰璁板綍琛?"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from ..base import BaseModel, TimestampMixin


class Announcement(BaseModel, TimestampMixin):
    """
    閫氱煡鍏憡琛?
    鍔熻兘锛?    - 閫氱煡鍏憡鍩烘湰淇℃伅
    - 閫氱煡鍏憡类型锛堢郴缁熷叕鍛娿€佹椿鍔ㄩ€氱煡銆佺淮鎶ら€氱煡绛夛級
    - 閫氱煡鍏憡状态?    """

    __tablename__ = "announcements"

    tenant_id: Mapped[str] = mapped_column(String(64), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, comment="租户ID")
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="类型")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="鏍囬")
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="鍐呭")
    publisher_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="鍙戝竷鑰匢D")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="浼樺厛绾?)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft", comment="状态?)
    publish_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="鍙戝竷鏃堕棿")
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="杩囨湡鏃堕棿")
    is_top: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="鏄惁缃《")

    # 鍏崇郴
    publisher = relationship("User", backref="announcements")


class AnnouncementRead(BaseModel, TimestampMixin):
    """
    閫氱煡鍏憡闃呰璁板綍琛?
    鍔熻兘锛?    - 璁板綍閫氱煡鍏憡鐨勯槄璇绘儏鍐?    """

    announcement_id: Mapped[str] = mapped_column(String(50), ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, comment="閫氱煡鍏憡ID")
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="闃呰鏃堕棿")

    # 鍏崇郴
    announcement = relationship("Announcement", backref="read_records")
    user = relationship("User", backref="announcement_reads")
