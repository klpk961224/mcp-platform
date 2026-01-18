"""
閫氱煡鍏憡Service

鎻愪緵閫氱煡鍏憡涓氬姟閫昏緫灞?"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from common.database.models.announcement import Announcement, AnnouncementRead
from app.repositories.announcement_repository import AnnouncementRepository


class AnnouncementService:
    """閫氱煡鍏憡Service"""

    # 閫氱煡鍏憡绫诲瀷甯搁噺
    TYPE_SYSTEM = "system"  # 绯荤粺鍏憡
    TYPE_ACTIVITY = "activity"  # 娲诲姩閫氱煡
    TYPE_MAINTENANCE = "maintenance"  # 缁存姢閫氱煡
    TYPE_UPDATE = "update"  # 鏇存柊閫氱煡
    TYPE_OTHER = "other"  # 鍏朵粬

    # 鐘舵€佸父閲?    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"

    # 浼樺厛绾у父閲?    PRIORITY_LOW = 0
    PRIORITY_NORMAL = 1
    PRIORITY_HIGH = 2
    PRIORITY_URGENT = 3

    def __init__(self, db: Session):
        self.db = db
        self.repository = AnnouncementRepository(db)

    def get_announcement_by_id(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """鏍规嵁ID鑾峰彇閫氱煡鍏憡"""
        announcement = self.repository.get_by_id(announcement_id)
        if not announcement:
            return None
        return self._to_dict(announcement)

    def get_all_announcements(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鑾峰彇鎵€鏈夐€氱煡鍏憡"""
        announcements = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {
            "items": [self._to_dict(a) for a in announcements],
            "total": total
        }

    def get_published_announcements(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鑾峰彇宸插彂甯冪殑閫氱煡鍏憡"""
        announcements = self.repository.get_published(skip=skip, limit=limit)
        total = self.repository.count_published()
        return {
            "items": [self._to_dict(a) for a in announcements],
            "total": total
        }

    def get_announcements_by_publisher(self, publisher_id: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鏍规嵁鍙戝竷鑰呰幏鍙栭€氱煡鍏憡"""
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
        """鎼滅储閫氱煡鍏憡"""
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
        """鍒涘缓閫氱煡鍏憡"""
        # 鍒涘缓閫氱煡鍏憡
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
        """鏇存柊閫氱煡鍏憡"""
        announcement = self.repository.get_by_id(announcement_id)
        if not announcement:
            return None

        # 鏇存柊瀛楁
        if title is not None:
            announcement.title = title
        if content is not None:
            announcement.content = content
        if priority is not None:
            announcement.priority = priority
        if status is not None:
            announcement.status = status
            # 濡傛灉鐘舵€佹敼涓哄凡鍙戝竷锛屼笖娌℃湁鍙戝竷鏃堕棿锛屽垯璁剧疆鍙戝竷鏃堕棿
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
        """鍒犻櫎閫氱煡鍏憡"""
        return self.repository.delete(announcement_id)

    def publish_announcement(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """鍙戝竷閫氱煡鍏憡"""
        return self.update_announcement(
            announcement_id=announcement_id,
            status=self.STATUS_PUBLISHED,
            publish_at=datetime.now()
        )

    def archive_announcement(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """褰掓。閫氱煡鍏憡"""
        return self.update_announcement(
            announcement_id=announcement_id,
            status=self.STATUS_ARCHIVED
        )

    def mark_as_read(self, announcement_id: str, user_id: str) -> bool:
        """鏍囪閫氱煡鍏憡涓哄凡璇?""
        # 妫€鏌ユ槸鍚﹀凡缁忚杩?        existing = self.repository.get_read_record(announcement_id, user_id)
        if existing:
            return True

        # 鍒涘缓闃呰璁板綍
        self.repository.create_read_record(announcement_id, user_id)
        return True

    def get_read_count(self, announcement_id: str) -> int:
        """鑾峰彇闃呰鏁伴噺"""
        return self.repository.count_reads(announcement_id)

    def get_user_unread_count(self, user_id: str) -> int:
        """鑾峰彇鐢ㄦ埛鏈閫氱煡鍏憡鏁伴噺"""
        # 鑾峰彇鎵€鏈夊凡鍙戝竷鐨勯€氱煡鍏憡
        published = self.repository.get_published(skip=0, limit=999999)
        unread_count = 0

        for announcement in published:
            read_record = self.repository.get_read_record(announcement.id, user_id)
            if not read_record:
                unread_count += 1

        return unread_count

    def _to_dict(self, announcement: Announcement) -> Dict[str, Any]:
        """杞崲涓哄瓧鍏?""
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
