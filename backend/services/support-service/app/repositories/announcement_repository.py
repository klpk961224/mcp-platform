"""
通知公告Repository

提供通知公告数据访问层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from common.database.models.announcement import Announcement, AnnouncementRead


class AnnouncementRepository:
    """通知公告Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, announcement_id: str) -> Optional[Announcement]:
        """根据ID获取通知公告"""
        return self.db.query(Announcement).filter(Announcement.id == announcement_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """获取所有通知公告"""
        return self.db.query(Announcement).order_by(desc(Announcement.is_top), desc(Announcement.publish_at)).offset(skip).limit(limit).all()

    def get_published(self, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """获取已发布的通知公告"""
        return self.db.query(Announcement).filter(
            Announcement.status == "published"
        ).order_by(desc(Announcement.is_top), desc(Announcement.publish_at)).offset(skip).limit(limit).all()

    def get_by_publisher(self, publisher_id: str, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """根据发布者获取通知公告"""
        return self.db.query(Announcement).filter(
            Announcement.publisher_id == publisher_id
        ).order_by(desc(Announcement.created_at)).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """搜索通知公告"""
        query = self.db.query(Announcement)

        # 租户ID过滤
        if query_params.get("tenant_id"):
            query = query.filter(Announcement.tenant_id == query_params["tenant_id"])

        # 类型过滤
        if query_params.get("type"):
            query = query.filter(Announcement.type == query_params["type"])

        # 发布者过滤
        if query_params.get("publisher_id"):
            query = query.filter(Announcement.publisher_id == query_params["publisher_id"])

        # 状态过滤
        if query_params.get("status"):
            query = query.filter(Announcement.status == query_params["status"])

        # 标题搜索
        if query_params.get("title"):
            query = query.filter(Announcement.title.like(f"%{query_params['title']}%"))

        # 内容搜索
        if query_params.get("content"):
            query = query.filter(Announcement.content.like(f"%{query_params['content']}%"))

        # 置顶过滤
        if query_params.get("is_top") is not None:
            query = query.filter(Announcement.is_top == query_params["is_top"])

        # 统计总数
        total = query.count()

        # 分页
        announcements = query.order_by(desc(Announcement.is_top), desc(Announcement.publish_at)).offset(skip).limit(limit).all()

        return announcements, total

    def create(self, announcement: Announcement) -> Announcement:
        """创建通知公告"""
        self.db.add(announcement)
        self.db.commit()
        self.db.refresh(announcement)
        return announcement

    def update(self, announcement: Announcement) -> Announcement:
        """更新通知公告"""
        self.db.commit()
        self.db.refresh(announcement)
        return announcement

    def delete(self, announcement_id: str) -> bool:
        """删除通知公告"""
        announcement = self.get_by_id(announcement_id)
        if announcement:
            self.db.delete(announcement)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """统计通知公告数量"""
        return self.db.query(Announcement).count()

    def count_by_publisher(self, publisher_id: str) -> int:
        """根据发布者统计通知公告数量"""
        return self.db.query(Announcement).filter(Announcement.publisher_id == publisher_id).count()

    def count_published(self) -> int:
        """统计已发布通知公告数量"""
        return self.db.query(Announcement).filter(Announcement.status == "published").count()

    def create_read_record(self, announcement_id: str, user_id: str) -> AnnouncementRead:
        """创建阅读记录"""
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
        """获取阅读记录"""
        return self.db.query(AnnouncementRead).filter(
            AnnouncementRead.announcement_id == announcement_id,
            AnnouncementRead.user_id == user_id
        ).first()

    def count_reads(self, announcement_id: str) -> int:
        """统计阅读数量"""
        return self.db.query(AnnouncementRead).filter(
            AnnouncementRead.announcement_id == announcement_id
        ).count()