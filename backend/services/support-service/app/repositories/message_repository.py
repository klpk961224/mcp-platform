"""
绔欏唴淇epository

鎻愪緵绔欏唴淇℃暟鎹闂眰
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from common.database.models.message import Message, MessageRead


class MessageRepository:
    """绔欏唴淇epository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, message_id: str) -> Optional[Message]:
        """鏍规嵁ID鑾峰彇绔欏唴淇?""
        return self.db.query(Message).filter(Message.id == message_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Message]:
        """鑾峰彇鎵€鏈夌珯鍐呬俊"""
        return self.db.query(Message).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def get_by_sender(self, sender_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """鏍规嵁鍙戦€佽€呰幏鍙栫珯鍐呬俊"""
        return self.db.query(Message).filter(
            Message.sender_id == sender_id
        ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def get_by_receiver(self, receiver_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """鏍规嵁鎺ユ敹鑰呰幏鍙栫珯鍐呬俊"""
        return self.db.query(Message).filter(
            Message.receiver_id == receiver_id
        ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def get_unread_by_receiver(self, receiver_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """鏍规嵁鎺ユ敹鑰呰幏鍙栨湭璇荤珯鍐呬俊"""
        return self.db.query(Message).filter(
            Message.receiver_id == receiver_id,
            Message.status == "unread"
        ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """鎼滅储绔欏唴淇?""
        query = self.db.query(Message)

        # 绉熸埛ID杩囨护
        if query_params.get("tenant_id"):
            query = query.filter(Message.tenant_id == query_params["tenant_id"])

        # 绫诲瀷杩囨护
        if query_params.get("type"):
            query = query.filter(Message.type == query_params["type"])

        # 鍙戦€佽€呰繃婊?        if query_params.get("sender_id"):
            query = query.filter(Message.sender_id == query_params["sender_id"])

        # 鎺ユ敹鑰呰繃婊?        if query_params.get("receiver_id"):
            query = query.filter(Message.receiver_id == query_params["receiver_id"])

        # 鐘舵€佽繃婊?        if query_params.get("status"):
            query = query.filter(Message.status == query_params["status"])

        # 鏍囬鎼滅储
        if query_params.get("title"):
            query = query.filter(Message.title.like(f"%{query_params['title']}%"))

        # 鍐呭鎼滅储
        if query_params.get("content"):
            query = query.filter(Message.content.like(f"%{query_params['content']}%"))

        # 缁熻鎬绘暟
        total = query.count()

        # 鍒嗛〉
        messages = query.order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

        return messages, total

    def create(self, message: Message) -> Message:
        """鍒涘缓绔欏唴淇?""
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def update(self, message: Message) -> Message:
        """鏇存柊绔欏唴淇?""
        self.db.commit()
        self.db.refresh(message)
        return message

    def delete(self, message_id: str) -> bool:
        """鍒犻櫎绔欏唴淇?""
        message = self.get_by_id(message_id)
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False

    def mark_as_read(self, message_id: str, user_id: str) -> bool:
        """鏍囪绔欏唴淇′负宸茶"""
        message = self.get_by_id(message_id)
        if message and message.receiver_id == user_id:
            message.status = "read"
            message.read_at = datetime.now()
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """缁熻绔欏唴淇℃暟閲?""
        return self.db.query(Message).count()

    def count_by_receiver(self, receiver_id: str) -> int:
        """鏍规嵁鎺ユ敹鑰呯粺璁＄珯鍐呬俊鏁伴噺"""
        return self.db.query(Message).filter(Message.receiver_id == receiver_id).count()

    def count_unread_by_receiver(self, receiver_id: str) -> int:
        """鏍规嵁鎺ユ敹鑰呯粺璁℃湭璇荤珯鍐呬俊鏁伴噺"""
        return self.db.query(Message).filter(
            Message.receiver_id == receiver_id,
            Message.status == "unread"
        ).count()

    def count_by_sender(self, sender_id: str) -> int:
        """鏍规嵁鍙戦€佽€呯粺璁＄珯鍐呬俊鏁伴噺"""
        return self.db.query(Message).filter(Message.sender_id == sender_id).count()

    def create_read_record(self, message_id: str, user_id: str) -> MessageRead:
        """鍒涘缓闃呰璁板綍"""
        read_record = MessageRead(
            message_id=message_id,
            user_id=user_id,
            read_at=datetime.now()
        )
        self.db.add(read_record)
        self.db.commit()
        self.db.refresh(read_record)
        return read_record
