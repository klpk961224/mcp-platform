# -*- coding: utf-8 -*-
"""
閫氱煡鏈嶅姟

鍔熻兘璇存槑锛?1. 閫氱煡绠＄悊
2. 閫氱煡鍙戦€?3. 閫氱煡闃呰绠＄悊

浣跨敤绀轰緥锛?    from app.services.notification_service import NotificationService
    
    notification_service = NotificationService(db)
    notification = notification_service.create_notification(title="绯荤粺閫氱煡", content="...")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.notification import Notification, NotificationRead
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    """
    閫氱煡鏈嶅姟
    
    鍔熻兘锛?    - 閫氱煡绠＄悊
    - 閫氱煡鍙戦€?    - 閫氱煡闃呰绠＄悊
    
    浣跨敤鏂规硶锛?        notification_service = NotificationService(db)
        notification = notification_service.create_notification(title="绯荤粺閫氱煡", content="...")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栭€氱煡鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.notification_repo = NotificationRepository(db)
    
    def create_notification(self, title: str, content: str, tenant_id: str,
                           notification_type: str = "system", priority: str = "normal",
                           sender_id: Optional[str] = None, sender_name: Optional[str] = None,
                           target_type: Optional[str] = None, target_ids: Optional[List[str]] = None,
                           attachment: Optional[str] = None) -> Notification:
        """
        鍒涘缓閫氱煡
        
        Args:
            title: 鏍囬
            content: 鍐呭
            tenant_id: 绉熸埛ID
            notification_type: 閫氱煡绫诲瀷
            priority: 浼樺厛绾?            sender_id: 鍙戦€佽€匢D锛堝彲閫夛級
            sender_name: 鍙戦€佽€呭悕绉帮紙鍙€夛級
            target_type: 鐩爣绫诲瀷锛堝彲閫夛級
            target_ids: 鐩爣ID鍒楄〃锛堝彲閫夛級
            attachment: 闄勪欢URL锛堝彲閫夛級
        
        Returns:
            Notification: 鍒涘缓鐨勯€氱煡瀵硅薄
        """
        logger.info(f"鍒涘缓閫氱煡: title={title}, type={notification_type}")
        
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
        
        # 涓烘瘡涓洰鏍囩敤鎴峰垱寤洪槄璇昏褰?        if target_ids:
            for user_id in target_ids:
                # 杩欓噷闇€瑕佽幏鍙栫敤鎴峰悕锛屽疄闄呭簲鐢ㄤ腑鍙兘闇€瑕佽皟鐢╱ser-service
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
        鍙戦€佺郴缁熼€氱煡
        
        Args:
            title: 鏍囬
            content: 鍐呭
            tenant_id: 绉熸埛ID
            target_ids: 鐩爣ID鍒楄〃
            priority: 浼樺厛绾?        
        Returns:
            Notification: 鍒涘缓鐨勯€氱煡瀵硅薄
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
        鍙戦€佸叕鍛?        
        Args:
            title: 鏍囬
            content: 鍐呭
            tenant_id: 绉熸埛ID
            target_ids: 鐩爣ID鍒楄〃
        
        Returns:
            Notification: 鍒涘缓鐨勯€氱煡瀵硅薄
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
        鑾峰彇鐢ㄦ埛閫氱煡
        
        Args:
            user_id: 鐢ㄦ埛ID
            unread_only: 鏄惁鍙幏鍙栨湭璇婚€氱煡
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Notification]: 閫氱煡鍒楄〃
        """
        return self.notification_repo.get_user_notifications(user_id, unread_only, page, page_size)
    
    def get_unread_count(self, user_id: str) -> int:
        """
        鑾峰彇鐢ㄦ埛鏈閫氱煡鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            int: 鏈閫氱煡鏁伴噺
        """
        return self.notification_repo.get_unread_count(user_id)
    
    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """
        鏍囪閫氱煡涓哄凡璇?        
        Args:
            notification_id: 閫氱煡ID
            user_id: 鐢ㄦ埛ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        logger.info(f"鏍囪閫氱煡涓哄凡璇? notification_id={notification_id}, user_id={user_id}")
        return self.notification_repo.mark_as_read(notification_id, user_id)
    
    def mark_all_as_read(self, user_id: str) -> int:
        """
        鏍囪鎵€鏈夐€氱煡涓哄凡璇?        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            int: 鏍囪鐨勯€氱煡鏁伴噺
        """
        logger.info(f"鏍囪鎵€鏈夐€氱煡涓哄凡璇? user_id={user_id}")
        return self.notification_repo.mark_all_as_read(user_id)
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        鍒犻櫎閫氱煡
        
        Args:
            notification_id: 閫氱煡ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎閫氱煡: notification_id={notification_id}")
        return self.notification_repo.delete_notification(notification_id)
    
    def count_notifications(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻閫氱煡鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 閫氱煡鏁伴噺
        """
        if tenant_id:
            return self.notification_repo.count_notifications_by_tenant(tenant_id)
        else:
            return self.notification_repo.count_all_notifications()
