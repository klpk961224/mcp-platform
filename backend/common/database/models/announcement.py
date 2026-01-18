"""
通知公告相关模型

包含：
- Announcement: 通知公告表
- AnnouncementRead: 通知公告阅读记录表
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from ..base import BaseModel, TimestampMixin


class Announcement(BaseModel, TimestampMixin):
    """
    通知公告表

    功能：
    - 通知公告基本信息
    - 通知公告类型（系统公告、活动通知、维护通知等）
    - 通知公告状态
    """

    __tablename__ = "announcements"

    tenant_id: Mapped[str] = mapped_column(String(64), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, comment="租户ID")
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="类型")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="内容")
    publisher_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="发布者ID")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="优先级")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft", comment="状态")
    publish_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="发布时间")
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="过期时间")
    is_top: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="是否置顶")

    # 关系
    publisher = relationship("User", backref="announcements")


class AnnouncementRead(BaseModel, TimestampMixin):
    """
    通知公告阅读记录表

    功能：
    - 记录通知公告的阅读情况
    """

    announcement_id: Mapped[str] = mapped_column(String(50), ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, comment="通知公告ID")
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="阅读时间")

    # 关系
    announcement = relationship("Announcement", backref="read_records")
    user = relationship("User", backref="announcement_reads")