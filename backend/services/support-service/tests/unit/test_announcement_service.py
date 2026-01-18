# -*- coding: utf-8 -*-
"""
AnnouncementService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓閫氱煡鍏憡
2. 鑾峰彇閫氱煡鍏憡
3. 鏇存柊閫氱煡鍏憡
4. 鍒犻櫎閫氱煡鍏憡
5. 鍙戝竷閫氱煡鍏憡
6. 褰掓。閫氱煡鍏憡
7. 鏍囪宸茶
8. 鑾峰彇闃呰鏁伴噺
9. 鑾峰彇鐢ㄦ埛鏈鏁伴噺
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.announcement_service import AnnouncementService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_announcement():
    """妯℃嫙閫氱煡鍏憡瀵硅薄"""
    announcement = Mock()
    announcement.id = "test_announcement_id"
    announcement.tenant_id = "default"
    announcement.type = "system"
    announcement.title = "娴嬭瘯鍏憡"
    announcement.content = "娴嬭瘯鍐呭"
    announcement.publisher_id = "user_001"
    announcement.priority = 1
    announcement.status = "draft"
    announcement.publish_at = None
    announcement.expire_at = None
    announcement.is_top = 0
    announcement.created_at = datetime(2026, 1, 15)
    announcement.updated_at = datetime(2026, 1, 15)
    return announcement


@pytest.fixture
def announcement_service(mock_db):
    """鍒涘缓AnnouncementService瀹炰緥"""
    return AnnouncementService(mock_db)


class TestAnnouncementService:
    """AnnouncementService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯AnnouncementService鍒濆鍖?""
        service = AnnouncementService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_announcement_by_id_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鏍规嵁ID鑾峰彇閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        
        # 鎵ц鏌ヨ
        result = announcement_service.get_announcement_by_id("test_announcement_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_announcement_id"
        assert result["title"] == "娴嬭瘯鍏憡"
    
    def test_get_announcement_by_id_not_found(self, announcement_service):
        """娴嬭瘯鏍规嵁ID鑾峰彇閫氱煡鍏憡澶辫触"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡杩斿洖None
        announcement_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = announcement_service.get_announcement_by_id("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_all_announcements_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鑾峰彇鎵€鏈夐€氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡鍒楄〃
        announcement_service.repository.get_all = Mock(return_value=[mock_announcement])
        announcement_service.repository.count = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = announcement_service.get_all_announcements()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["title"] == "娴嬭瘯鍏憡"
    
    def test_get_published_announcements_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鑾峰彇宸插彂甯冪殑閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ宸插彂甯冪殑閫氱煡鍏憡鍒楄〃
        announcement_service.repository.get_published = Mock(return_value=[mock_announcement])
        announcement_service.repository.count_published = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = announcement_service.get_published_announcements()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["status"] == "draft"
    
    def test_get_announcements_by_publisher_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鏍规嵁鍙戝竷鑰呰幏鍙栭€氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡鍒楄〃
        announcement_service.repository.get_by_publisher = Mock(return_value=[mock_announcement])
        announcement_service.repository.count_by_publisher = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = announcement_service.get_announcements_by_publisher("user_001")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["publisher_id"] == "user_001"
    
    def test_search_announcements_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鎼滅储閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鎼滅储閫氱煡鍏憡
        announcement_service.repository.search = Mock(return_value=([mock_announcement], 1))
        
        # 鎵ц鎼滅储
        result = announcement_service.search_announcements({"title": "娴嬭瘯"})
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_announcement_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鍒涘缓閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鍒涘缓閫氱煡鍏憡
        announcement_service.repository.create = Mock(return_value=mock_announcement)
        
        # 鎵ц鍒涘缓閫氱煡鍏憡
        result = announcement_service.create_announcement(
            tenant_id="default",
            type="system",
            title="娴嬭瘯鍏憡",
            content="娴嬭瘯鍐呭",
            publisher_id="user_001"
        )
        
        # 楠岃瘉缁撴灉
        assert result["title"] == "娴嬭瘯鍏憡"
        assert result["type"] == "system"
        assert result["status"] == "draft"
        announcement_service.repository.create.assert_called_once()
    
    def test_update_announcement_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鏇存柊閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        # 妯℃嫙鏇存柊閫氱煡鍏憡
        announcement_service.repository.update = Mock(return_value=mock_announcement)
        
        # 鎵ц鏇存柊
        result = announcement_service.update_announcement(
            "test_announcement_id",
            title="鏇存柊鍚庣殑鏍囬"
        )
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_announcement_id"
        announcement_service.repository.update.assert_called_once()
    
    def test_update_announcement_not_found(self, announcement_service):
        """娴嬭瘯鏇存柊閫氱煡鍏憡澶辫触锛堥€氱煡鍏憡涓嶅瓨鍦級"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡杩斿洖None
        announcement_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏇存柊
        result = announcement_service.update_announcement(
            "nonexistent_id",
            title="鏇存柊鍚庣殑鏍囬"
        )
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_announcement_success(self, announcement_service):
        """娴嬭瘯鍒犻櫎閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鍒犻櫎閫氱煡鍏憡
        announcement_service.repository.delete = Mock(return_value=True)
        
        # 鎵ц鍒犻櫎
        result = announcement_service.delete_announcement("test_announcement_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        announcement_service.repository.delete.assert_called_once_with("test_announcement_id")
    
    def test_publish_announcement_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鍙戝竷閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        # 妯℃嫙鏇存柊閫氱煡鍏憡
        announcement_service.repository.update = Mock(return_value=mock_announcement)
        
        # 鎵ц鍙戝竷
        result = announcement_service.publish_announcement("test_announcement_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        announcement_service.repository.update.assert_called_once()
    
    def test_archive_announcement_success(self, announcement_service, mock_announcement):
        """娴嬭瘯褰掓。閫氱煡鍏憡鎴愬姛"""
        # 妯℃嫙鏌ヨ閫氱煡鍏憡
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        # 妯℃嫙鏇存柊閫氱煡鍏憡
        announcement_service.repository.update = Mock(return_value=mock_announcement)
        
        # 鎵ц褰掓。
        result = announcement_service.archive_announcement("test_announcement_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        announcement_service.repository.update.assert_called_once()
    
    def test_mark_as_read_success(self, announcement_service):
        """娴嬭瘯鏍囪閫氱煡鍏憡涓哄凡璇绘垚鍔?""
        # 妯℃嫙妫€鏌ユ槸鍚﹀凡璇昏繃
        announcement_service.repository.get_read_record = Mock(return_value=None)
        # 妯℃嫙鍒涘缓闃呰璁板綍
        announcement_service.repository.create_read_record = Mock()
        
        # 鎵ц鏍囪宸茶
        result = announcement_service.mark_as_read("test_announcement_id", "user_002")
        
        # 楠岃瘉缁撴灉
        assert result is True
        announcement_service.repository.create_read_record.assert_called_once()
    
    def test_mark_as_read_already_read(self, announcement_service):
        """娴嬭瘯鏍囪閫氱煡鍏憡涓哄凡璇伙紙宸茶杩囷級"""
        # 妯℃嫙妫€鏌ユ槸鍚﹀凡璇昏繃锛堝凡璇昏繃锛?        announcement_service.repository.get_read_record = Mock(return_value=Mock())
        # 鍒涘缓涓€涓狹ock瀵硅薄鏉ユā鎷焎reate_read_record
        mock_create = Mock()
        announcement_service.repository.create_read_record = mock_create
        
        # 鎵ц鏍囪宸茶
        result = announcement_service.mark_as_read("test_announcement_id", "user_002")
        
        # 楠岃瘉缁撴灉
        assert result is True
        # 涓嶅簲璇ュ垱寤烘柊鐨勯槄璇昏褰?        mock_create.assert_not_called()
    
    def test_get_read_count_success(self, announcement_service):
        """娴嬭瘯鑾峰彇闃呰鏁伴噺鎴愬姛"""
        # 妯℃嫙缁熻闃呰鏁伴噺
        announcement_service.repository.count_reads = Mock(return_value=5)
        
        # 鎵ц鑾峰彇闃呰鏁伴噺
        result = announcement_service.get_read_count("test_announcement_id")
        
        # 楠岃瘉缁撴灉
        assert result == 5
    
    def test_get_user_unread_count_success(self, announcement_service, mock_announcement):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鏈閫氱煡鍏憡鏁伴噺鎴愬姛"""
        # 妯℃嫙鑾峰彇宸插彂甯冪殑閫氱煡鍏憡
        announcement_service.repository.get_published = Mock(return_value=[mock_announcement])
        # 妯℃嫙妫€鏌ラ槄璇昏褰?        announcement_service.repository.get_read_record = Mock(return_value=None)
        
        # 鎵ц鑾峰彇鐢ㄦ埛鏈鏁伴噺
        result = announcement_service.get_user_unread_count("user_002")
        
        # 楠岃瘉缁撴灉
        assert result == 1
