"""
绔欏唴淇ervice

鎻愪緵绔欏唴淇′笟鍔￠€昏緫灞?"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from common.database.models.message import Message, MessageRead
from app.repositories.message_repository import MessageRepository


class MessageService:
    """绔欏唴淇ervice"""

    # 绔欏唴淇＄被鍨嬪父閲?    TYPE_SYSTEM = "system"  # 绯荤粺閫氱煡
    TYPE_PRIVATE = "private"  # 绉佷俊
    TYPE_ANNOUNCEMENT = "announcement"  # 鍏憡
    TYPE_REMINDER = "reminder"  # 鎻愰啋

    # 鐘舵€佸父閲?    STATUS_UNREAD = "unread"
    STATUS_READ = "read"
    STATUS_DELETED = "deleted"

    # 浼樺厛绾у父閲?    PRIORITY_LOW = 0
    PRIORITY_NORMAL = 1
    PRIORITY_HIGH = 2
    PRIORITY_URGENT = 3

    def __init__(self, db: Session):
        self.db = db
        self.repository = MessageRepository(db)

    def get_message_by_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """鏍规嵁ID鑾峰彇绔欏唴淇?""
        message = self.repository.get_by_id(message_id)
        if not message:
            return None
        return self._to_dict(message)

    def get_all_messages(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鑾峰彇鎵€鏈夌珯鍐呬俊"""
        messages = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {
            "items": [self._to_dict(m) for m in messages],
            "total": total
        }

    def get_messages_by_sender(self, sender_id: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鏍规嵁鍙戦€佽€呰幏鍙栫珯鍐呬俊"""
        messages = self.repository.get_by_sender(sender_id, skip=skip, limit=limit)
        total = self.repository.count_by_sender(sender_id)
        return {
            "items": [self._to_dict(m) for m in messages],
            "total": total
        }

    def get_messages_by_receiver(self, receiver_id: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鏍规嵁鎺ユ敹鑰呰幏鍙栫珯鍐呬俊"""
        messages = self.repository.get_by_receiver(receiver_id, skip=skip, limit=limit)
        total = self.repository.count_by_receiver(receiver_id)
        return {
            "items": [self._to_dict(m) for m in messages],
            "total": total
        }

    def get_unread_messages_by_receiver(self, receiver_id: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鏍规嵁鎺ユ敹鑰呰幏鍙栨湭璇荤珯鍐呬俊"""
        messages = self.repository.get_unread_by_receiver(receiver_id, skip=skip, limit=limit)
        total = self.repository.count_unread_by_receiver(receiver_id)
        return {
            "items": [self._to_dict(m) for m in messages],
            "total": total
        }

    def search_messages(
        self,
        query_params: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """鎼滅储绔欏唴淇?""
        messages, total = self.repository.search(query_params, skip=skip, limit=limit)
        return {
            "items": [self._to_dict(m) for m in messages],
            "total": total
        }

    def create_message(
        self,
        tenant_id: str,
        type: str,
        title: str,
        content: Optional[str] = None,
        sender_id: Optional[str] = None,
        receiver_id: Optional[str] = None,
        receiver_type: str = "user",
        priority: int = PRIORITY_NORMAL,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """鍒涘缓绔欏唴淇?""
        # 鍒涘缓绔欏唴淇?        message = Message(
            tenant_id=tenant_id,
            type=type,
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            priority=priority,
            status=self.STATUS_UNREAD,
            extra_data=extra_data
        )

        message = self.repository.create(message)
        return self._to_dict(message)

    def update_message(
        self,
        message_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """鏇存柊绔欏唴淇?""
        message = self.repository.get_by_id(message_id)
        if not message:
            return None

        # 鏇存柊瀛楁
        if title is not None:
            message.title = title
        if content is not None:
            message.content = content
        if status is not None:
            message.status = status
        if extra_data is not None:
            message.extra_data = extra_data

        message = self.repository.update(message)
        return self._to_dict(message)

    def delete_message(self, message_id: str) -> bool:
        """鍒犻櫎绔欏唴淇?""
        return self.repository.delete(message_id)

    def mark_as_read(self, message_id: str, user_id: str) -> bool:
        """鏍囪绔欏唴淇′负宸茶"""
        success = self.repository.mark_as_read(message_id, user_id)
        if success:
            # 鍒涘缓闃呰璁板綍
            self.repository.create_read_record(message_id, user_id)
        return success

    def get_unread_count(self, user_id: str) -> int:
        """鑾峰彇鏈绔欏唴淇℃暟閲?""
        return self.repository.count_unread_by_receiver(user_id)

    def get_statistics(self, user_id: str) -> Dict[str, Any]:
        """鑾峰彇绔欏唴淇＄粺璁′俊鎭?""
        total = self.repository.count_by_receiver(user_id)
        unread = self.repository.count_unread_by_receiver(user_id)
        read = total - unread

        return {
            "total": total,
            "unread": unread,
            "read": read
        }

    def _to_dict(self, message: Message) -> Dict[str, Any]:
        """杞崲涓哄瓧鍏?""
        return {
            "id": message.id,
            "tenant_id": message.tenant_id,
            "type": message.type,
            "title": message.title,
            "content": message.content,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "receiver_type": message.receiver_type,
            "priority": message.priority,
            "status": message.status,
            "read_at": message.read_at.isoformat() if message.read_at else None,
            "extra_data": message.extra_data,
            "created_at": message.created_at.isoformat() if message.created_at else None,
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }
