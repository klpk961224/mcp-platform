"""
通知公告Service

提供通知公告业务逻辑层
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from common.database.models.announcement import Announcement, AnnouncementRead
from app.repositories.announcement_repository import AnnouncementRepository


class AnnouncementService:
    """通知公告Service"""

    # 通知公告类型常量
    TYPE_SYSTEM = "system"  # 系统公告
    TYPE_ACTIVITY = "activity"  # 活动通知
    TYPE_MAINTENANCE = "maintenance"  # 维护通知
    TYPE_UPDATE = "update"  # 更新通知
    TYPE_OTHER = "other"  # 其他

    # 状态常量
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"

    # 优先级常量
    PRIORITY_LOW = 0
    PRIORITY_NORMAL = 1
    PRIORITY_HIGH = 2
    PRIORITY_URGENT = 3

    def __init__(self, db: Session):
        self.db = db
        self.repository = AnnouncementRepository(db)

    def get_announcement_by_id(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取通知公告"""
        announcement = self.repository.get_by_id(announcement_id)
        if not announcement:
            return None
        return self._to_dict(announcement)

    def get_all_announcements(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """获取所有通知公告"""
        announcements = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {
            "items": [self._to_dict(a) for a in announcements],
            "total": total
        }

    def get_published_announcements(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """获取已发布的通知公告"""
        announcements = self.repository.get_published(skip=skip, limit=limit)
        total = self.repository.count_published()
        return {
            "items": [self._to_dict(a) for a in announcements],
            "total": total
        }

    def get_announcements_by_publisher(self, publisher_id: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """根据发布者获取通知公告"""
        announcements = self.repository.get_by_publisher(publisher_id, skip=skip, limit=limit)
        total = self.repository.count_by_publisher(publisher_id)
        return {
            "items": [self._to_dict(a) for a in announcements],
            "total": total
        }

    def search_announcements(
        self,
        query_params: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """搜索通知公告"""
        announcements, total = self.repository.search(query_params, skip=skip, limit=limit)
        return {
            "items": [self._to_dict(a) for a in announcements],
            "total": total
        }

    def create_announcement(
        self,
        tenant_id: str,
        type: str,
        title: str,
        content: Optional[str] = None,
        publisher_id: Optional[str] = None,
        priority: int = PRIORITY_NORMAL,
        status: str = STATUS_DRAFT,
        publish_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        is_top: int = 0
    ) -> Dict[str, Any]:
        """创建通知公告"""
        # 创建通知公告
        announcement = Announcement(
            tenant_id=tenant_id,
            type=type,
            title=title,
            content=content,
            publisher_id=publisher_id,
            priority=priority,
            status=status,
            publish_at=publish_at,
            expire_at=expire_at,
            is_top=is_top
        )

        announcement = self.repository.create(announcement)
        return self._to_dict(announcement)

    def update_announcement(
        self,
        announcement_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        priority: Optional[int] = None,
        status: Optional[str] = None,
        publish_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        is_top: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """更新通知公告"""
        announcement = self.repository.get_by_id(announcement_id)
        if not announcement:
            return None

        # 更新字段
        if title is not None:
            announcement.title = title
        if content is not None:
            announcement.content = content
        if priority is not None:
            announcement.priority = priority
        if status is not None:
            announcement.status = status
            # 如果状态改为已发布，且没有发布时间，则设置发布时间
            if status == self.STATUS_PUBLISHED and not announcement.publish_at:
                announcement.publish_at = datetime.now()
        if publish_at is not None:
            announcement.publish_at = publish_at
        if expire_at is not None:
            announcement.expire_at = expire_at
        if is_top is not None:
            announcement.is_top = is_top

        announcement = self.repository.update(announcement)
        return self._to_dict(announcement)

    def delete_announcement(self, announcement_id: str) -> bool:
        """删除通知公告"""
        return self.repository.delete(announcement_id)

    def publish_announcement(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """发布通知公告"""
        return self.update_announcement(
            announcement_id=announcement_id,
            status=self.STATUS_PUBLISHED,
            publish_at=datetime.now()
        )

    def archive_announcement(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """归档通知公告"""
        return self.update_announcement(
            announcement_id=announcement_id,
            status=self.STATUS_ARCHIVED
        )

    def mark_as_read(self, announcement_id: str, user_id: str) -> bool:
        """标记通知公告为已读"""
        # 检查是否已经读过
        existing = self.repository.get_read_record(announcement_id, user_id)
        if existing:
            return True

        # 创建阅读记录
        self.repository.create_read_record(announcement_id, user_id)
        return True

    def get_read_count(self, announcement_id: str) -> int:
        """获取阅读数量"""
        return self.repository.count_reads(announcement_id)

    def get_user_unread_count(self, user_id: str) -> int:
        """获取用户未读通知公告数量"""
        # 获取所有已发布的通知公告
        published = self.repository.get_published(skip=0, limit=999999)
        unread_count = 0

        for announcement in published:
            read_record = self.repository.get_read_record(announcement.id, user_id)
            if not read_record:
                unread_count += 1

        return unread_count

    def _to_dict(self, announcement: Announcement) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": announcement.id,
            "tenant_id": announcement.tenant_id,
            "type": announcement.type,
            "title": announcement.title,
            "content": announcement.content,
            "publisher_id": announcement.publisher_id,
            "priority": announcement.priority,
            "status": announcement.status,
            "publish_at": announcement.publish_at.isoformat() if announcement.publish_at else None,
            "expire_at": announcement.expire_at.isoformat() if announcement.expire_at else None,
            "is_top": announcement.is_top,
            "created_at": announcement.created_at.isoformat() if announcement.created_at else None,
            "updated_at": announcement.updated_at.isoformat() if announcement.updated_at else None
        }