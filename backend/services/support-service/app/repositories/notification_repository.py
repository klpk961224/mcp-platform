# -*- coding: utf-8 -*-
"""
通知数据访问层

功能说明：
1. 通知CRUD操作
2. 通知阅读记录管理
3. 通知查询和统计

使用示例：
    from app.repositories.notification_repository import NotificationRepository
    
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
    通知数据访问层
    
    功能：
    - 通知CRUD操作
    - 通知阅读记录管理
    - 通知查询和统计
    
    使用方法：
        notification_repo = NotificationRepository(db)
        notifications = notification_repo.get_user_notifications(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        初始化通知数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create_notification(self, notification: Notification) -> Notification:
        """
        创建通知
        
        Args:
            notification: 通知对象
        
        Returns:
            Notification: 创建的通知对象
        """
        logger.info(f"创建通知: title={notification.title}, type={notification.notification_type}")
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def get_notification_by_id(self, notification_id: str) -> Optional[Notification]:
        """
        根据ID获取通知
        
        Args:
            notification_id: 通知ID
        
        Returns:
            Optional[Notification]: 通知对象，不存在返回None
        """
        return self.db.query(Notification).filter(Notification.id == notification_id).first()
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False,
                              page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        获取用户通知
        
        Args:
            user_id: 用户ID
            unread_only: 是否只获取未读通知
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Notification]: 通知列表
        """
        offset = (page - 1) * page_size
        
        if unread_only:
            # 获取未读通知
            return self.db.query(Notification).join(NotificationRead).filter(
                and_(
                    NotificationRead.user_id == user_id,
                    NotificationRead.is_read == False
                )
            ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
        else:
            # 获取所有通知
            return self.db.query(Notification).join(NotificationRead).filter(
                NotificationRead.user_id == user_id
            ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_notifications(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        获取租户通知
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Notification]: 通知列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Notification).filter(
            Notification.tenant_id == tenant_id
        ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def get_system_notifications(self, page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        获取系统通知
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Notification]: 系统通知列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Notification).filter(
            Notification.is_system == True
        ).order_by(Notification.send_time.desc()).offset(offset).limit(page_size).all()
    
    def search_notifications(self, keyword: str, tenant_id: Optional[str] = None,
                             page: int = 1, page_size: int = 10) -> List[Notification]:
        """
        搜索通知
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Notification]: 通知列表
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
        更新通知
        
        Args:
            notification: 通知对象
        
        Returns:
            Notification: 更新后的通知对象
        """
        logger.info(f"更新通知: notification_id={notification.id}")
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        删除通知
        
        Args:
            notification_id: 通知ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除通知: notification_id={notification_id}")
        notification = self.get_notification_by_id(notification_id)
        if not notification:
            return False
        
        self.db.delete(notification)
        self.db.commit()
        return True
    
    # 通知阅读记录相关方法
    def create_notification_read(self, notification_read: NotificationRead) -> NotificationRead:
        """
        创建通知阅读记录
        
        Args:
            notification_read: 通知阅读记录对象
        
        Returns:
            NotificationRead: 创建的通知阅读记录对象
        """
        self.db.add(notification_read)
        self.db.commit()
        self.db.refresh(notification_read)
        return notification_read
    
    def get_notification_read(self, notification_id: str, user_id: str) -> Optional[NotificationRead]:
        """
        获取通知阅读记录
        
        Args:
            notification_id: 通知ID
            user_id: 用户ID
        
        Returns:
            Optional[NotificationRead]: 通知阅读记录对象，不存在返回None
        """
        return self.db.query(NotificationRead).filter(
            and_(
                NotificationRead.notification_id == notification_id,
                NotificationRead.user_id == user_id
            )
        ).first()
    
    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """
        标记通知为已读
        
        Args:
            notification_id: 通知ID
            user_id: 用户ID
        
        Returns:
            bool: 是否成功
        """
        notification_read = self.get_notification_read(notification_id, user_id)
        if notification_read:
            notification_read.mark_as_read()
            self.db.commit()
            
            # 更新通知的已读数量
            notification = self.get_notification_by_id(notification_id)
            if notification:
                notification.read_count += 1
                self.db.commit()
            
            return True
        return False
    
    def mark_all_as_read(self, user_id: str) -> int:
        """
        标记所有通知为已读
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 标记的通知数量
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
        获取用户未读通知数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 未读通知数量
        """
        return self.db.query(NotificationRead).filter(
            and_(
                NotificationRead.user_id == user_id,
                NotificationRead.is_read == False
            )
        ).count()
    
    # 统计方法
    def count_notifications_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户通知数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 通知数量
        """
        return self.db.query(Notification).filter(Notification.tenant_id == tenant_id).count()
    
    def count_all_notifications(self) -> int:
        """
        统计所有通知数量
        
        Returns:
            int: 通知数量
        """
        return self.db.query(Notification).count()