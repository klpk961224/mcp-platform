# -*- coding: utf-8 -*-
"""
MessageService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓绔欏唴淇?2. 鑾峰彇绔欏唴淇?3. 鏇存柊绔欏唴淇?4. 鍒犻櫎绔欏唴淇?5. 鏍囪宸茶
6. 鑾峰彇鏈鏁伴噺
7. 鑾峰彇缁熻淇℃伅
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.message_service import MessageService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_message():
    """妯℃嫙绔欏唴淇″璞?""
    message = Mock()
    message.id = "test_message_id"
    message.tenant_id = "default"
    message.type = "private"
    message.title = "娴嬭瘯娑堟伅"
    message.content = "娴嬭瘯鍐呭"
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
    """鍒涘缓MessageService瀹炰緥"""
    return MessageService(mock_db)


class TestMessageService:
    """MessageService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯MessageService鍒濆鍖?""
        service = MessageService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_message_by_id_success(self, message_service, mock_message):
        """娴嬭瘯鏍规嵁ID鑾峰彇绔欏唴淇℃垚鍔?""
        # 妯℃嫙鏌ヨ绔欏唴淇?        message_service.repository.get_by_id = Mock(return_value=mock_message)
        
        # 鎵ц鏌ヨ
        result = message_service.get_message_by_id("test_message_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_message_id"
        assert result["title"] == "娴嬭瘯娑堟伅"
    
    def test_get_message_by_id_not_found(self, message_service):
        """娴嬭瘯鏍规嵁ID鑾峰彇绔欏唴淇″け璐?""
        # 妯℃嫙鏌ヨ绔欏唴淇¤繑鍥濶one
        message_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = message_service.get_message_by_id("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_all_messages_success(self, message_service, mock_message):
        """娴嬭瘯鑾峰彇鎵€鏈夌珯鍐呬俊鎴愬姛"""
        # 妯℃嫙鏌ヨ绔欏唴淇″垪琛?        message_service.repository.get_all = Mock(return_value=[mock_message])
        message_service.repository.count = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = message_service.get_all_messages()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["title"] == "娴嬭瘯娑堟伅"
    
    def test_get_messages_by_sender_success(self, message_service, mock_message):
        """娴嬭瘯鏍规嵁鍙戦€佽€呰幏鍙栫珯鍐呬俊鎴愬姛"""
        # 妯℃嫙鏌ヨ绔欏唴淇″垪琛?        message_service.repository.get_by_sender = Mock(return_value=[mock_message])
        message_service.repository.count_by_sender = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = message_service.get_messages_by_sender("user_001")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["sender_id"] == "user_001"
    
    def test_get_messages_by_receiver_success(self, message_service, mock_message):
        """娴嬭瘯鏍规嵁鎺ユ敹鑰呰幏鍙栫珯鍐呬俊鎴愬姛"""
        # 妯℃嫙鏌ヨ绔欏唴淇″垪琛?        message_service.repository.get_by_receiver = Mock(return_value=[mock_message])
        message_service.repository.count_by_receiver = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = message_service.get_messages_by_receiver("user_002")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["receiver_id"] == "user_002"
    
    def test_get_unread_messages_by_receiver_success(self, message_service, mock_message):
        """娴嬭瘯鏍规嵁鎺ユ敹鑰呰幏鍙栨湭璇荤珯鍐呬俊鎴愬姛"""
        # 妯℃嫙鏌ヨ鏈绔欏唴淇″垪琛?        message_service.repository.get_unread_by_receiver = Mock(return_value=[mock_message])
        message_service.repository.count_unread_by_receiver = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = message_service.get_unread_messages_by_receiver("user_002")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["status"] == "unread"
    
    def test_search_messages_success(self, message_service, mock_message):
        """娴嬭瘯鎼滅储绔欏唴淇℃垚鍔?""
        # 妯℃嫙鎼滅储绔欏唴淇?        message_service.repository.search = Mock(return_value=([mock_message], 1))
        
        # 鎵ц鎼滅储
        result = message_service.search_messages({"title": "娴嬭瘯"})
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_message_success(self, message_service, mock_message):
        """娴嬭瘯鍒涘缓绔欏唴淇℃垚鍔?""
        # 妯℃嫙鍒涘缓绔欏唴淇?        message_service.repository.create = Mock(return_value=mock_message)
        
        # 鎵ц鍒涘缓绔欏唴淇?        result = message_service.create_message(
            tenant_id="default",
            type="private",
            title="娴嬭瘯娑堟伅",
            content="娴嬭瘯鍐呭",
            sender_id="user_001",
            receiver_id="user_002"
        )
        
        # 楠岃瘉缁撴灉
        assert result["title"] == "娴嬭瘯娑堟伅"
        assert result["type"] == "private"
        assert result["status"] == "unread"
        message_service.repository.create.assert_called_once()
    
    def test_update_message_success(self, message_service, mock_message):
        """娴嬭瘯鏇存柊绔欏唴淇℃垚鍔?""
        # 妯℃嫙鏌ヨ绔欏唴淇?        message_service.repository.get_by_id = Mock(return_value=mock_message)
        # 妯℃嫙鏇存柊绔欏唴淇?        message_service.repository.update = Mock(return_value=mock_message)
        
        # 鎵ц鏇存柊
        result = message_service.update_message(
            "test_message_id",
            title="鏇存柊鍚庣殑鏍囬"
        )
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_message_id"
        message_service.repository.update.assert_called_once()
    
    def test_update_message_not_found(self, message_service):
        """娴嬭瘯鏇存柊绔欏唴淇″け璐ワ紙绔欏唴淇′笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ绔欏唴淇¤繑鍥濶one
        message_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏇存柊
        result = message_service.update_message(
            "nonexistent_id",
            title="鏇存柊鍚庣殑鏍囬"
        )
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_message_success(self, message_service):
        """娴嬭瘯鍒犻櫎绔欏唴淇℃垚鍔?""
        # 妯℃嫙鍒犻櫎绔欏唴淇?        message_service.repository.delete = Mock(return_value=True)
        
        # 鎵ц鍒犻櫎
        result = message_service.delete_message("test_message_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        message_service.repository.delete.assert_called_once_with("test_message_id")
    
    def test_mark_as_read_success(self, message_service):
        """娴嬭瘯鏍囪绔欏唴淇′负宸茶鎴愬姛"""
        # 妯℃嫙鏍囪宸茶
        message_service.repository.mark_as_read = Mock(return_value=True)
        # 妯℃嫙鍒涘缓闃呰璁板綍
        message_service.repository.create_read_record = Mock()
        
        # 鎵ц鏍囪宸茶
        result = message_service.mark_as_read("test_message_id", "user_002")
        
        # 楠岃瘉缁撴灉
        assert result is True
        message_service.repository.mark_as_read.assert_called_once()
        message_service.repository.create_read_record.assert_called_once()
    
    def test_get_unread_count_success(self, message_service):
        """娴嬭瘯鑾峰彇鏈绔欏唴淇℃暟閲忔垚鍔?""
        # 妯℃嫙缁熻鏈鏁伴噺
        message_service.repository.count_unread_by_receiver = Mock(return_value=5)
        
        # 鎵ц鑾峰彇鏈鏁伴噺
        result = message_service.get_unread_count("user_002")
        
        # 楠岃瘉缁撴灉
        assert result == 5
    
    def test_get_statistics_success(self, message_service):
        """娴嬭瘯鑾峰彇缁熻淇℃伅鎴愬姛"""
        # 妯℃嫙缁熻
        message_service.repository.count_by_receiver = Mock(return_value=10)
        message_service.repository.count_unread_by_receiver = Mock(return_value=3)
        
        # 鎵ц鑾峰彇缁熻
        result = message_service.get_statistics("user_002")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 10
        assert result["unread"] == 3
        assert result["read"] == 7
