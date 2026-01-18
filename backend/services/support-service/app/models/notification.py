# -*- coding: utf-8 -*-
"""
通知模型

功能说明：
1. 站内信管理
2. 通知公告管理
3. 消息阅读状态

使用示例：
    from app.models.notification import Notification, NotificationRead
    
    # 创建通知
    notification = Notification(
        title="系统通知",
        content="系统将于今晚维护",
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
    通知模型
    
    功能：
    - 站内信管理
    - 通知公告管理
    
    属性说明：
    - id: 通知ID（主键）
    - tenant_id: 租户ID
    - sender_id: 发送者ID
    - sender_name: 发送者名称
    - title: 标题
    - content: 内容
    - notification_type: 通知类型
    - priority: 优先级
    - status: 状态
    - send_time: 发送时间
    - is_system: 是否系统通知
    - target_type: 目标类型
    - target_ids: 目标ID列表（JSON）
    - attachment: 附件URL
    - read_count: 已读数量
    - total_count: 总数量
    - created_at: 创建时间
    """
    
    # 基本信息
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="租户ID")
    sender_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="发送者ID")
    sender_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="发送者名称")
    
    # 内容信息
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")
    
    # 类型信息
    notification_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="通知类型")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="normal", comment="优先级")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="sent", comment="状态")
    
    # 时间信息
    send_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="发送时间")
    
    # 目标信息
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否系统通知")
    target_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="目标类型")
    target_ids: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="目标ID列表（JSON）")
    
    # 扩展信息
    attachment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="附件URL")
    
    # 统计信息
    read_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="已读数量")
    total_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="总数量")
    
    # 关系
    reads = relationship("NotificationRead", back_populates="notification", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title={self.title}, type={self.notification_type})>"
    
    def to_dict(self):
        """转换为字典"""
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
        """获取已读率"""
        if self.total_count == 0:
            return 0.0
        return round(self.read_count / self.total_count * 100, 2)
    
    def is_unread(self) -> bool:
        """检查是否有未读"""
        return self.read_count < self.total_count


class NotificationRead(BaseModel):
    """
    通知阅读记录模型
    
    功能：
    - 通知阅读状态
    - 阅读时间记录
    
    属性说明：
    - id: 阅读记录ID（主键）
    - notification_id: 通知ID（外键）
    - user_id: 用户ID
    - username: 用户名
    - is_read: 是否已读
    - read_time: 阅读时间
    - created_at: 创建时间
    """
    
    # 基本信息
    notification_id: Mapped[str] = mapped_column(String(64), ForeignKey("notification.id"), nullable=False, index=True, comment="通知ID")
    user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment="用户名")
    
    # 阅读状态
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否已读")
    read_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="阅读时间")
    
    # 关系
    notification = relationship("Notification", back_populates="reads")
    
    def __repr__(self):
        return f"<NotificationRead(id={self.id}, user_id={self.user_id}, is_read={self.is_read})>"
    
    def to_dict(self):
        """转换为字典"""
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
        """标记为已读"""
        self.is_read = True
        self.read_time = datetime.now()