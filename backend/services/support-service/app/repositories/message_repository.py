"""
站内信Repository

提供站内信数据访问层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from common.database.models.message import Message, MessageRead


class MessageRepository:
    """站内信Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, message_id: str) -> Optional[Message]:
        """根据ID获取站内信"""
        return self.db.query(Message).filter(Message.id == message_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Message]:
        """获取所有站内信"""
        return self.db.query(Message).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def get_by_sender(self, sender_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """根据发送者获取站内信"""
        return self.db.query(Message).filter(
            Message.sender_id == sender_id
        ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def get_by_receiver(self, receiver_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """根据接收者获取站内信"""
        return self.db.query(Message).filter(
            Message.receiver_id == receiver_id
        ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def get_unread_by_receiver(self, receiver_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """根据接收者获取未读站内信"""
        return self.db.query(Message).filter(
            Message.receiver_id == receiver_id,
            Message.status == "unread"
        ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """搜索站内信"""
        query = self.db.query(Message)

        # 租户ID过滤
        if query_params.get("tenant_id"):
            query = query.filter(Message.tenant_id == query_params["tenant_id"])

        # 类型过滤
        if query_params.get("type"):
            query = query.filter(Message.type == query_params["type"])

        # 发送者过滤
        if query_params.get("sender_id"):
            query = query.filter(Message.sender_id == query_params["sender_id"])

        # 接收者过滤
        if query_params.get("receiver_id"):
            query = query.filter(Message.receiver_id == query_params["receiver_id"])

        # 状态过滤
        if query_params.get("status"):
            query = query.filter(Message.status == query_params["status"])

        # 标题搜索
        if query_params.get("title"):
            query = query.filter(Message.title.like(f"%{query_params['title']}%"))

        # 内容搜索
        if query_params.get("content"):
            query = query.filter(Message.content.like(f"%{query_params['content']}%"))

        # 统计总数
        total = query.count()

        # 分页
        messages = query.order_by(desc(Message.created_at)).offset(skip).limit(limit).all()

        return messages, total

    def create(self, message: Message) -> Message:
        """创建站内信"""
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def update(self, message: Message) -> Message:
        """更新站内信"""
        self.db.commit()
        self.db.refresh(message)
        return message

    def delete(self, message_id: str) -> bool:
        """删除站内信"""
        message = self.get_by_id(message_id)
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False

    def mark_as_read(self, message_id: str, user_id: str) -> bool:
        """标记站内信为已读"""
        message = self.get_by_id(message_id)
        if message and message.receiver_id == user_id:
            message.status = "read"
            message.read_at = datetime.now()
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """统计站内信数量"""
        return self.db.query(Message).count()

    def count_by_receiver(self, receiver_id: str) -> int:
        """根据接收者统计站内信数量"""
        return self.db.query(Message).filter(Message.receiver_id == receiver_id).count()

    def count_unread_by_receiver(self, receiver_id: str) -> int:
        """根据接收者统计未读站内信数量"""
        return self.db.query(Message).filter(
            Message.receiver_id == receiver_id,
            Message.status == "unread"
        ).count()

    def count_by_sender(self, sender_id: str) -> int:
        """根据发送者统计站内信数量"""
        return self.db.query(Message).filter(Message.sender_id == sender_id).count()

    def create_read_record(self, message_id: str, user_id: str) -> MessageRead:
        """创建阅读记录"""
        read_record = MessageRead(
            message_id=message_id,
            user_id=user_id,
            read_at=datetime.now()
        )
        self.db.add(read_record)
        self.db.commit()
        self.db.refresh(read_record)
        return read_record