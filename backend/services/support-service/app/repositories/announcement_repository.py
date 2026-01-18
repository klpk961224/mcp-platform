"""
閫氱煡鍏憡Repository

鎻愪緵閫氱煡鍏憡鏁版嵁璁块棶灞?"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from common.database.models.announcement import Announcement, AnnouncementRead


class AnnouncementRepository:
    """閫氱煡鍏憡Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, announcement_id: str) -> Optional[Announcement]:
        """鏍规嵁ID鑾峰彇閫氱煡鍏憡"""
        return self.db.query(Announcement).filter(Announcement.id == announcement_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """鑾峰彇鎵€鏈夐€氱煡鍏憡"""
        return self.db.query(Announcement).order_by(desc(Announcement.is_top), desc(Announcement.publish_at)).offset(skip).limit(limit).all()

    def get_published(self, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """鑾峰彇宸插彂甯冪殑閫氱煡鍏憡"""
        return self.db.query(Announcement).filter(
            Announcement.status == "published"
        ).order_by(desc(Announcement.is_top), desc(Announcement.publish_at)).offset(skip).limit(limit).all()

    def get_by_publisher(self, publisher_id: str, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """鏍规嵁鍙戝竷鑰呰幏鍙栭€氱煡鍏憡"""
        return self.db.query(Announcement).filter(
            Announcement.publisher_id == publisher_id
        ).order_by(desc(Announcement.created_at)).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """鎼滅储閫氱煡鍏憡"""
        query = self.db.query(Announcement)

        # 绉熸埛ID杩囨护
        if query_params.get("tenant_id"):
            query = query.filter(Announcement.tenant_id == query_params["tenant_id"])

        # 绫诲瀷杩囨护
        if query_params.get("type"):
            query = query.filter(Announcement.type == query_params["type"])

        # 鍙戝竷鑰呰繃婊?        if query_params.get("publisher_id"):
            query = query.filter(Announcement.publisher_id == query_params["publisher_id"])

        # 鐘舵€佽繃婊?        if query_params.get("status"):
            query = query.filter(Announcement.status == query_params["status"])

        # 鏍囬鎼滅储
        if query_params.get("title"):
            query = query.filter(Announcement.title.like(f"%{query_params['title']}%"))

        # 鍐呭鎼滅储
        if query_params.get("content"):
            query = query.filter(Announcement.content.like(f"%{query_params['content']}%"))

        # 缃《杩囨护
        if query_params.get("is_top") is not None:
            query = query.filter(Announcement.is_top == query_params["is_top"])

        # 缁熻鎬绘暟
        total = query.count()

        # 鍒嗛〉
        announcements = query.order_by(desc(Announcement.is_top), desc(Announcement.publish_at)).offset(skip).limit(limit).all()

        return announcements, total

    def create(self, announcement: Announcement) -> Announcement:
        """鍒涘缓閫氱煡鍏憡"""
        self.db.add(announcement)
        self.db.commit()
        self.db.refresh(announcement)
        return announcement

    def update(self, announcement: Announcement) -> Announcement:
        """鏇存柊閫氱煡鍏憡"""
        self.db.commit()
        self.db.refresh(announcement)
        return announcement

    def delete(self, announcement_id: str) -> bool:
        """鍒犻櫎閫氱煡鍏憡"""
        announcement = self.get_by_id(announcement_id)
        if announcement:
            self.db.delete(announcement)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """缁熻閫氱煡鍏憡鏁伴噺"""
        return self.db.query(Announcement).count()

    def count_by_publisher(self, publisher_id: str) -> int:
        """鏍规嵁鍙戝竷鑰呯粺璁￠€氱煡鍏憡鏁伴噺"""
        return self.db.query(Announcement).filter(Announcement.publisher_id == publisher_id).count()

    def count_published(self) -> int:
        """缁熻宸插彂甯冮€氱煡鍏憡鏁伴噺"""
        return self.db.query(Announcement).filter(Announcement.status == "published").count()

    def create_read_record(self, announcement_id: str, user_id: str) -> AnnouncementRead:
        """鍒涘缓闃呰璁板綍"""
        read_record = AnnouncementRead(
            announcement_id=announcement_id,
            user_id=user_id,
            read_at=datetime.now()
        )
        self.db.add(read_record)
        self.db.commit()
        self.db.refresh(read_record)
        return read_record

    def get_read_record(self, announcement_id: str, user_id: str) -> Optional[AnnouncementRead]:
        """鑾峰彇闃呰璁板綍"""
        return self.db.query(AnnouncementRead).filter(
            AnnouncementRead.announcement_id == announcement_id,
            AnnouncementRead.user_id == user_id
        ).first()

    def count_reads(self, announcement_id: str) -> int:
        """缁熻闃呰鏁伴噺"""
        return self.db.query(AnnouncementRead).filter(
            AnnouncementRead.announcement_id == announcement_id
        ).count()
