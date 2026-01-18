# -*- coding: utf-8 -*-
"""
MessageService单元测试

测试内容：
1. 创建站内信
2. 获取站内信
3. 更新站内信
4. 删除站内信
5. 标记已读
6. 获取未读数量
7. 获取统计信息
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.message_service import MessageService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_message():
    """模拟站内信对象"""
    message = Mock()
    message.id = "test_message_id"
    message.tenant_id = "default"
    message.type = "private"
    message.title = "测试消息"
    message.content = "测试内容"
    message.sender_id = "user_001"
    message.receiver_id = "user_002"
    message.receiver_type = "user"
    message.priority = 1
    message.status = "unread"
    message.read_at = None
    message.extra_data = None
    message.created_at = datetime(2026, 1, 15)
    message.updated_at = datetime(2026, 1, 15)
    return message


@pytest.fixture
def message_service(mock_db):
    """创建MessageService实例"""
    return MessageService(mock_db)


class TestMessageService:
    """MessageService测试类"""
    
    def test_init(self, mock_db):
        """测试MessageService初始化"""
        service = MessageService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_message_by_id_success(self, message_service, mock_message):
        """测试根据ID获取站内信成功"""
        # 模拟查询站内信
        message_service.repository.get_by_id = Mock(return_value=mock_message)
        
        # 执行查询
        result = message_service.get_message_by_id("test_message_id")
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_message_id"
        assert result["title"] == "测试消息"
    
    def test_get_message_by_id_not_found(self, message_service):
        """测试根据ID获取站内信失败"""
        # 模拟查询站内信返回None
        message_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = message_service.get_message_by_id("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_all_messages_success(self, message_service, mock_message):
        """测试获取所有站内信成功"""
        # 模拟查询站内信列表
        message_service.repository.get_all = Mock(return_value=[mock_message])
        message_service.repository.count = Mock(return_value=1)
        
        # 执行查询
        result = message_service.get_all_messages()
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["title"] == "测试消息"
    
    def test_get_messages_by_sender_success(self, message_service, mock_message):
        """测试根据发送者获取站内信成功"""
        # 模拟查询站内信列表
        message_service.repository.get_by_sender = Mock(return_value=[mock_message])
        message_service.repository.count_by_sender = Mock(return_value=1)
        
        # 执行查询
        result = message_service.get_messages_by_sender("user_001")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["sender_id"] == "user_001"
    
    def test_get_messages_by_receiver_success(self, message_service, mock_message):
        """测试根据接收者获取站内信成功"""
        # 模拟查询站内信列表
        message_service.repository.get_by_receiver = Mock(return_value=[mock_message])
        message_service.repository.count_by_receiver = Mock(return_value=1)
        
        # 执行查询
        result = message_service.get_messages_by_receiver("user_002")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["receiver_id"] == "user_002"
    
    def test_get_unread_messages_by_receiver_success(self, message_service, mock_message):
        """测试根据接收者获取未读站内信成功"""
        # 模拟查询未读站内信列表
        message_service.repository.get_unread_by_receiver = Mock(return_value=[mock_message])
        message_service.repository.count_unread_by_receiver = Mock(return_value=1)
        
        # 执行查询
        result = message_service.get_unread_messages_by_receiver("user_002")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["status"] == "unread"
    
    def test_search_messages_success(self, message_service, mock_message):
        """测试搜索站内信成功"""
        # 模拟搜索站内信
        message_service.repository.search = Mock(return_value=([mock_message], 1))
        
        # 执行搜索
        result = message_service.search_messages({"title": "测试"})
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_message_success(self, message_service, mock_message):
        """测试创建站内信成功"""
        # 模拟创建站内信
        message_service.repository.create = Mock(return_value=mock_message)
        
        # 执行创建站内信
        result = message_service.create_message(
            tenant_id="default",
            type="private",
            title="测试消息",
            content="测试内容",
            sender_id="user_001",
            receiver_id="user_002"
        )
        
        # 验证结果
        assert result["title"] == "测试消息"
        assert result["type"] == "private"
        assert result["status"] == "unread"
        message_service.repository.create.assert_called_once()
    
    def test_update_message_success(self, message_service, mock_message):
        """测试更新站内信成功"""
        # 模拟查询站内信
        message_service.repository.get_by_id = Mock(return_value=mock_message)
        # 模拟更新站内信
        message_service.repository.update = Mock(return_value=mock_message)
        
        # 执行更新
        result = message_service.update_message(
            "test_message_id",
            title="更新后的标题"
        )
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_message_id"
        message_service.repository.update.assert_called_once()
    
    def test_update_message_not_found(self, message_service):
        """测试更新站内信失败（站内信不存在）"""
        # 模拟查询站内信返回None
        message_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行更新
        result = message_service.update_message(
            "nonexistent_id",
            title="更新后的标题"
        )
        
        # 验证结果
        assert result is None
    
    def test_delete_message_success(self, message_service):
        """测试删除站内信成功"""
        # 模拟删除站内信
        message_service.repository.delete = Mock(return_value=True)
        
        # 执行删除
        result = message_service.delete_message("test_message_id")
        
        # 验证结果
        assert result is True
        message_service.repository.delete.assert_called_once_with("test_message_id")
    
    def test_mark_as_read_success(self, message_service):
        """测试标记站内信为已读成功"""
        # 模拟标记已读
        message_service.repository.mark_as_read = Mock(return_value=True)
        # 模拟创建阅读记录
        message_service.repository.create_read_record = Mock()
        
        # 执行标记已读
        result = message_service.mark_as_read("test_message_id", "user_002")
        
        # 验证结果
        assert result is True
        message_service.repository.mark_as_read.assert_called_once()
        message_service.repository.create_read_record.assert_called_once()
    
    def test_get_unread_count_success(self, message_service):
        """测试获取未读站内信数量成功"""
        # 模拟统计未读数量
        message_service.repository.count_unread_by_receiver = Mock(return_value=5)
        
        # 执行获取未读数量
        result = message_service.get_unread_count("user_002")
        
        # 验证结果
        assert result == 5
    
    def test_get_statistics_success(self, message_service):
        """测试获取统计信息成功"""
        # 模拟统计
        message_service.repository.count_by_receiver = Mock(return_value=10)
        message_service.repository.count_unread_by_receiver = Mock(return_value=3)
        
        # 执行获取统计
        result = message_service.get_statistics("user_002")
        
        # 验证结果
        assert result["total"] == 10
        assert result["unread"] == 3
        assert result["read"] == 7