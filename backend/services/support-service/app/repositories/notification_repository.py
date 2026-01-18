# -*- coding: utf-8 -*-
"""
閫氱煡鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 閫氱煡CRUD鎿嶄綔
2. 閫氱煡闃呰璁板綍绠＄悊
3. 閫氱煡查询鍜岀粺璁?
浣跨敤绀轰緥锛?    from app.repositories.notification_repository import NotificationRepository
    
    notification_repo = NotificationRepository(db)
    notifications = notification_repo.get_user_notifications(user_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from app.models.notification import Notification, NotificationRead


class NotificationRepository:
    """
    閫氱煡鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 閫氱煡CRUD鎿嶄綔
    - 閫氱煡闃呰璁板綍绠＄悊
    - 閫氱煡查询鍜岀粺璁?    
    浣跨敤鏂规硶锛?        notification_repo = NotificationRepository(db)
        notifications = notification_repo.get_user_notifications(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栭€氱煡鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create_notification(self, notification: Notification) -> Notification:
        """
        创建閫氱煡
        
        Args:
            notification: 閫氱煡瀵硅薄
        
        Returns:
            Notification: 创建鐨勯€氱煡瀵硅薄
        """
        logger.info(f"创建閫氱煡: title={notification.title}, type={notification.notification_type}")
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def get_notification_by_id(self, notification_id: str) -> Optional[Notification]:
        """
        根据ID鑾峰彇閫氱煡
        
        Args:
            notification_id: 閫氱煡ID
        
        Returns:
            Optional[Notification]: 閫氱煡瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Notification).filter(Notification.id == notification_id).first()
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False,
                              page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        鑾峰彇鐢ㄦ埛閫氱煡
        
        Args:
            user_id: 用户ID
            unread_only: 鏄惁鍙幏鍙栨湭璇婚€氱煡
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Notification]: 閫氱煡鍒楄〃
        """
        offset = (page - 1) * page_size
        
        if unread_only:
            # 鑾峰彇鏈閫氱煡
            return self.db.query(Notification).join(NotificationRead).filter(
                and_(
                    NotificationRead.user_id == user_id,
                    NotificationRead.is_read == False
                )
            ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
        else:
            # 鑾峰彇鎵€鏈夐€氱煡
            return self.db.query(Notification).join(NotificationRead).filter(
                NotificationRead.user_id == user_id
            ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_notifications(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        鑾峰彇绉熸埛閫氱煡
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Notification]: 閫氱煡鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Notification).filter(
            Notification.tenant_id == tenant_id
        ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def get_system_notifications(self, page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        鑾峰彇绯荤粺閫氱煡
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Notification]: 绯荤粺閫氱煡鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Notification).filter(
            Notification.is_system == True
        ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def search_notifications(self, keyword: str, tenant_id: Optional[str] = None,
                             page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        鎼滅储閫氱煡
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Notification]: 閫氱煡鍒楄〃
        """
        offset = (page - 1) * page_size
        query = self.db.query(Notification).filter(
            or_(
                Notification.title.like(f"%{keyword}%"),
                Notification.content.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Notification.tenant_id == tenant_id)
        
        return query.order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def update_notification(self, notification: Notification) -> Notification:
        """
        更新閫氱煡
        
        Args:
            notification: 閫氱煡瀵硅薄
        
        Returns:
            Notification: 更新鍚庣殑閫氱煡瀵硅薄
        """
        logger.info(f"更新閫氱煡: notification_id={notification.id}")
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        删除閫氱煡
        
        Args:
            notification_id: 閫氱煡ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除閫氱煡: notification_id={notification_id}")
        notification = self.get_notification_by_id(notification_id)
        if not notification:
            return False
        
        self.db.delete(notification)
        self.db.commit()
        return True
    
    # 閫氱煡闃呰璁板綍鐩稿叧鏂规硶
    def create_notification_read(self, notification_read: NotificationRead) -> NotificationRead:
        """
        创建閫氱煡闃呰璁板綍
        
        Args:
            notification_read: 閫氱煡闃呰璁板綍瀵硅薄
        
        Returns:
            NotificationRead: 创建鐨勯€氱煡闃呰璁板綍瀵硅薄
        """
        self.db.add(notification_read)
        self.db.commit()
        self.db.refresh(notification_read)
        return notification_read
    
    def get_notification_read(self, notification_id: str, user_id: str) -> Optional[NotificationRead]:
        """
        鑾峰彇閫氱煡闃呰璁板綍
        
        Args:
            notification_id: 閫氱煡ID
            user_id: 用户ID
        
        Returns:
            Optional[NotificationRead]: 閫氱煡闃呰璁板綍瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(NotificationRead).filter(
            and_(
                NotificationRead.notification_id == notification_id,
                NotificationRead.user_id == user_id
            )
        ).first()
    
    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """
        鏍囪閫氱煡涓哄凡璇?        
        Args:
            notification_id: 閫氱煡ID
            user_id: 用户ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        notification_read = self.get_notification_read(notification_id, user_id)
        if notification_read:
            notification_read.mark_as_read()
            self.db.commit()
            
            # 更新閫氱煡鐨勫凡璇绘暟閲?            notification = self.get_notification_by_id(notification_id)
            if notification:
                notification.read_count += 1
                self.db.commit()
            
            return True
        return False
    
    def mark_all_as_read(self, user_id: str) -> int:
        """
        鏍囪鎵€鏈夐€氱煡涓哄凡璇?        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 鏍囪鐨勯€氱煡数量
        """
        count = self.db.query(NotificationRead).filter(
            and_(
                NotificationRead.user_id == user_id,
                NotificationRead.is_read == False
            )
        ).update({"is_read": True, "read_time": datetime.now()})
        
        self.db.commit()
        return count
    
    def get_unread_count(self, user_id: str) -> int:
        """
        鑾峰彇鐢ㄦ埛鏈閫氱煡数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 鏈閫氱煡数量
        """
        return self.db.query(NotificationRead).filter(
            and_(
                NotificationRead.user_id == user_id,
                NotificationRead.is_read == False
            )
        ).count()
    
    # 缁熻鏂规硶
    def count_notifications_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛閫氱煡数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 閫氱煡数量
        """
        return self.db.query(Notification).filter(Notification.tenant_id == tenant_id).count()
    
    def count_all_notifications(self) -> int:
        """
        缁熻鎵€鏈夐€氱煡数量
        
        Returns:
            int: 閫氱煡数量
        """
        return self.db.query(Notification).count()
