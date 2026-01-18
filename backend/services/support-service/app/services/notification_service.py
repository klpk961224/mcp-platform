# -*- coding: utf-8 -*-
"""
通知服务

功能说明：
1. 通知管理
2. 通知发送
3. 通知阅读管理

使用示例：
    from app.services.notification_service import NotificationService
    
    notification_service = NotificationService(db)
    notification = notification_service.create_notification(title="系统通知", content="...")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.notification import Notification, NotificationRead
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    """
    通知服务
    
    功能：
    - 通知管理
    - 通知发送
    - 通知阅读管理
    
    使用方法：
        notification_service = NotificationService(db)
        notification = notification_service.create_notification(title="系统通知", content="...")
    """
    
    def __init__(self, db: Session):
        """
        初始化通知服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.notification_repo = NotificationRepository(db)
    
    def create_notification(self, title: str, content: str, tenant_id: str,
                           notification_type: str = "system", priority: str = "normal",
                           sender_id: Optional[str] = None, sender_name: Optional[str] = None,
                           target_type: Optional[str] = None, target_ids: Optional[List[str]] = None,
                           attachment: Optional[str] = None) -> Notification:
        """
        创建通知
        
        Args:
            title: 标题
            content: 内容
            tenant_id: 租户ID
            notification_type: 通知类型
            priority: 优先级
            sender_id: 发送者ID（可选）
            sender_name: 发送者名称（可选）
            target_type: 目标类型（可选）
            target_ids: 目标ID列表（可选）
            attachment: 附件URL（可选）
        
        Returns:
            Notification: 创建的通知对象
        """
        logger.info(f"创建通知: title={title}, type={notification_type}")
        
        import json
        notification = Notification(
            tenant_id=tenant_id,
            sender_id=sender_id,
            sender_name=sender_name,
            title=title,
            content=content,
            notification_type=notification_type,
            priority=priority,
            status="sent",
            send_time=datetime.now(),
            target_type=target_type,
            target_ids=json.dumps(target_ids) if target_ids else None,
            attachment=attachment,
            is_system=(sender_id is None),
            total_count=len(target_ids) if target_ids else 0
        )
        
        notification = self.notification_repo.create_notification(notification)
        
        # 为每个目标用户创建阅读记录
        if target_ids:
            for user_id in target_ids:
                # 这里需要获取用户名，实际应用中可能需要调用user-service
                notification_read = NotificationRead(
                    notification_id=notification.id,
                    user_id=user_id,
                    username=f"User_{user_id}",
                    is_read=False
                )
                self.notification_repo.create_notification_read(notification_read)
        
        return notification
    
    def send_system_notification(self, title: str, content: str, tenant_id: str,
                                  target_ids: List[str], priority: str = "normal") -> Notification:
        """
        发送系统通知
        
        Args:
            title: 标题
            content: 内容
            tenant_id: 租户ID
            target_ids: 目标ID列表
            priority: 优先级
        
        Returns:
            Notification: 创建的通知对象
        """
        return self.create_notification(
            title=title,
            content=content,
            tenant_id=tenant_id,
            notification_type="system",
            priority=priority,
            target_type="user",
            target_ids=target_ids,
            is_system=True
        )
    
    def send_announcement(self, title: str, content: str, tenant_id: str,
                          target_ids: List[str]) -> Notification:
        """
        发送公告
        
        Args:
            title: 标题
            content: 内容
            tenant_id: 租户ID
            target_ids: 目标ID列表
        
        Returns:
            Notification: 创建的通知对象
        """
        return self.create_notification(
            title=title,
            content=content,
            tenant_id=tenant_id,
            notification_type="announcement",
            priority="high",
            target_type="user",
            target_ids=target_ids,
            is_system=True
        )
    
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
        return self.notification_repo.get_user_notifications(user_id, unread_only, page, page_size)
    
    def get_unread_count(self, user_id: str) -> int:
        """
        获取用户未读通知数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 未读通知数量
        """
        return self.notification_repo.get_unread_count(user_id)
    
    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """
        标记通知为已读
        
        Args:
            notification_id: 通知ID
            user_id: 用户ID
        
        Returns:
            bool: 是否成功
        """
        logger.info(f"标记通知为已读: notification_id={notification_id}, user_id={user_id}")
        return self.notification_repo.mark_as_read(notification_id, user_id)
    
    def mark_all_as_read(self, user_id: str) -> int:
        """
        标记所有通知为已读
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 标记的通知数量
        """
        logger.info(f"标记所有通知为已读: user_id={user_id}")
        return self.notification_repo.mark_all_as_read(user_id)
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        删除通知
        
        Args:
            notification_id: 通知ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除通知: notification_id={notification_id}")
        return self.notification_repo.delete_notification(notification_id)
    
    def count_notifications(self, tenant_id: Optional[str] = None) -> int:
        """
        统计通知数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 通知数量
        """
        if tenant_id:
            return self.notification_repo.count_notifications_by_tenant(tenant_id)
        else:
            return self.notification_repo.count_all_notifications()