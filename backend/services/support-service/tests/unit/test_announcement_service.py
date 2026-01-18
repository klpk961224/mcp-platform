# -*- coding: utf-8 -*-
"""
AnnouncementService单元测试

测试内容：
1. 创建通知公告
2. 获取通知公告
3. 更新通知公告
4. 删除通知公告
5. 发布通知公告
6. 归档通知公告
7. 标记已读
8. 获取阅读数量
9. 获取用户未读数量
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.announcement_service import AnnouncementService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_announcement():
    """模拟通知公告对象"""
    announcement = Mock()
    announcement.id = "test_announcement_id"
    announcement.tenant_id = "default"
    announcement.type = "system"
    announcement.title = "测试公告"
    announcement.content = "测试内容"
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
    """创建AnnouncementService实例"""
    return AnnouncementService(mock_db)


class TestAnnouncementService:
    """AnnouncementService测试类"""
    
    def test_init(self, mock_db):
        """测试AnnouncementService初始化"""
        service = AnnouncementService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_announcement_by_id_success(self, announcement_service, mock_announcement):
        """测试根据ID获取通知公告成功"""
        # 模拟查询通知公告
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        
        # 执行查询
        result = announcement_service.get_announcement_by_id("test_announcement_id")
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_announcement_id"
        assert result["title"] == "测试公告"
    
    def test_get_announcement_by_id_not_found(self, announcement_service):
        """测试根据ID获取通知公告失败"""
        # 模拟查询通知公告返回None
        announcement_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = announcement_service.get_announcement_by_id("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_all_announcements_success(self, announcement_service, mock_announcement):
        """测试获取所有通知公告成功"""
        # 模拟查询通知公告列表
        announcement_service.repository.get_all = Mock(return_value=[mock_announcement])
        announcement_service.repository.count = Mock(return_value=1)
        
        # 执行查询
        result = announcement_service.get_all_announcements()
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["title"] == "测试公告"
    
    def test_get_published_announcements_success(self, announcement_service, mock_announcement):
        """测试获取已发布的通知公告成功"""
        # 模拟查询已发布的通知公告列表
        announcement_service.repository.get_published = Mock(return_value=[mock_announcement])
        announcement_service.repository.count_published = Mock(return_value=1)
        
        # 执行查询
        result = announcement_service.get_published_announcements()
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["status"] == "draft"
    
    def test_get_announcements_by_publisher_success(self, announcement_service, mock_announcement):
        """测试根据发布者获取通知公告成功"""
        # 模拟查询通知公告列表
        announcement_service.repository.get_by_publisher = Mock(return_value=[mock_announcement])
        announcement_service.repository.count_by_publisher = Mock(return_value=1)
        
        # 执行查询
        result = announcement_service.get_announcements_by_publisher("user_001")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["publisher_id"] == "user_001"
    
    def test_search_announcements_success(self, announcement_service, mock_announcement):
        """测试搜索通知公告成功"""
        # 模拟搜索通知公告
        announcement_service.repository.search = Mock(return_value=([mock_announcement], 1))
        
        # 执行搜索
        result = announcement_service.search_announcements({"title": "测试"})
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_announcement_success(self, announcement_service, mock_announcement):
        """测试创建通知公告成功"""
        # 模拟创建通知公告
        announcement_service.repository.create = Mock(return_value=mock_announcement)
        
        # 执行创建通知公告
        result = announcement_service.create_announcement(
            tenant_id="default",
            type="system",
            title="测试公告",
            content="测试内容",
            publisher_id="user_001"
        )
        
        # 验证结果
        assert result["title"] == "测试公告"
        assert result["type"] == "system"
        assert result["status"] == "draft"
        announcement_service.repository.create.assert_called_once()
    
    def test_update_announcement_success(self, announcement_service, mock_announcement):
        """测试更新通知公告成功"""
        # 模拟查询通知公告
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        # 模拟更新通知公告
        announcement_service.repository.update = Mock(return_value=mock_announcement)
        
        # 执行更新
        result = announcement_service.update_announcement(
            "test_announcement_id",
            title="更新后的标题"
        )
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_announcement_id"
        announcement_service.repository.update.assert_called_once()
    
    def test_update_announcement_not_found(self, announcement_service):
        """测试更新通知公告失败（通知公告不存在）"""
        # 模拟查询通知公告返回None
        announcement_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行更新
        result = announcement_service.update_announcement(
            "nonexistent_id",
            title="更新后的标题"
        )
        
        # 验证结果
        assert result is None
    
    def test_delete_announcement_success(self, announcement_service):
        """测试删除通知公告成功"""
        # 模拟删除通知公告
        announcement_service.repository.delete = Mock(return_value=True)
        
        # 执行删除
        result = announcement_service.delete_announcement("test_announcement_id")
        
        # 验证结果
        assert result is True
        announcement_service.repository.delete.assert_called_once_with("test_announcement_id")
    
    def test_publish_announcement_success(self, announcement_service, mock_announcement):
        """测试发布通知公告成功"""
        # 模拟查询通知公告
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        # 模拟更新通知公告
        announcement_service.repository.update = Mock(return_value=mock_announcement)
        
        # 执行发布
        result = announcement_service.publish_announcement("test_announcement_id")
        
        # 验证结果
        assert result is not None
        announcement_service.repository.update.assert_called_once()
    
    def test_archive_announcement_success(self, announcement_service, mock_announcement):
        """测试归档通知公告成功"""
        # 模拟查询通知公告
        announcement_service.repository.get_by_id = Mock(return_value=mock_announcement)
        # 模拟更新通知公告
        announcement_service.repository.update = Mock(return_value=mock_announcement)
        
        # 执行归档
        result = announcement_service.archive_announcement("test_announcement_id")
        
        # 验证结果
        assert result is not None
        announcement_service.repository.update.assert_called_once()
    
    def test_mark_as_read_success(self, announcement_service):
        """测试标记通知公告为已读成功"""
        # 模拟检查是否已读过
        announcement_service.repository.get_read_record = Mock(return_value=None)
        # 模拟创建阅读记录
        announcement_service.repository.create_read_record = Mock()
        
        # 执行标记已读
        result = announcement_service.mark_as_read("test_announcement_id", "user_002")
        
        # 验证结果
        assert result is True
        announcement_service.repository.create_read_record.assert_called_once()
    
    def test_mark_as_read_already_read(self, announcement_service):
        """测试标记通知公告为已读（已读过）"""
        # 模拟检查是否已读过（已读过）
        announcement_service.repository.get_read_record = Mock(return_value=Mock())
        # 创建一个Mock对象来模拟create_read_record
        mock_create = Mock()
        announcement_service.repository.create_read_record = mock_create
        
        # 执行标记已读
        result = announcement_service.mark_as_read("test_announcement_id", "user_002")
        
        # 验证结果
        assert result is True
        # 不应该创建新的阅读记录
        mock_create.assert_not_called()
    
    def test_get_read_count_success(self, announcement_service):
        """测试获取阅读数量成功"""
        # 模拟统计阅读数量
        announcement_service.repository.count_reads = Mock(return_value=5)
        
        # 执行获取阅读数量
        result = announcement_service.get_read_count("test_announcement_id")
        
        # 验证结果
        assert result == 5
    
    def test_get_user_unread_count_success(self, announcement_service, mock_announcement):
        """测试获取用户未读通知公告数量成功"""
        # 模拟获取已发布的通知公告
        announcement_service.repository.get_published = Mock(return_value=[mock_announcement])
        # 模拟检查阅读记录
        announcement_service.repository.get_read_record = Mock(return_value=None)
        
        # 执行获取用户未读数量
        result = announcement_service.get_user_unread_count("user_002")
        
        # 验证结果
        assert result == 1