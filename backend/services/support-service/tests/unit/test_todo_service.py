# -*- coding: utf-8 -*-
"""
TodoService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓寰呭姙浠诲姟
2. 鑾峰彇寰呭姙浠诲姟
3. 瀹屾垚寰呭姙浠诲姟
4. 鍙栨秷瀹屾垚寰呭姙浠诲姟
5. 鍒犻櫎寰呭姙浠诲姟
6. 鑾峰彇閫炬湡浠诲姟
7. 鍒涘缓姣忔棩璁″垝
8. 鑾峰彇姣忔棩璁″垝
9. 鑾峰彇缁熻淇℃伅
10. 鍙戦€侀€炬湡鎻愰啋
11. 鍙戦€佸嵆灏嗗埌鏈熸彁閱?12. 缁熻寰呭姙浠诲姟鏁伴噺
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.services.todo_service import TodoService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_todo():
    """妯℃嫙寰呭姙浠诲姟瀵硅薄"""
    todo = Mock()
    todo.id = "test_todo_id"
    todo.tenant_id = "default"
    todo.user_id = "user_001"
    todo.username = "User_001"
    todo.title = "娴嬭瘯浠诲姟"
    todo.description = "娴嬭瘯鎻忚堪"
    todo.task_type = "personal"
    todo.priority = "medium"
    todo.status = "pending"
    todo.due_date = datetime(2026, 1, 20)
    todo.due_time = None
    todo.tags = None
    todo.attachment = None
    todo.is_completed = False
    todo.is_overdue = False
    todo.reminder_sent = False
    todo.created_at = datetime(2026, 1, 15)
    todo.updated_at = datetime(2026, 1, 15)
    
    # 妯℃嫙鏂规硶
    todo.mark_completed = Mock()
    todo.mark_pending = Mock()
    todo.update_overdue_status = Mock()
    
    return todo


@pytest.fixture
def mock_daily_plan():
    """妯℃嫙姣忔棩璁″垝瀵硅薄"""
    daily_plan = Mock()
    daily_plan.id = "test_daily_plan_id"
    daily_plan.tenant_id = "default"
    daily_plan.user_id = "user_001"
    daily_plan.username = "User_001"
    daily_plan.plan_date = datetime(2026, 1, 16)
    daily_plan.tasks = '[{"title": "浠诲姟1", "completed": false}]'
    daily_plan.notes = "澶囨敞"
    daily_plan.total_tasks = 1
    daily_plan.completed_tasks = 0
    daily_plan.completion_rate = 0
    daily_plan.created_at = datetime(2026, 1, 16)
    daily_plan.updated_at = datetime(2026, 1, 16)
    return daily_plan


@pytest.fixture
def todo_service(mock_db):
    """鍒涘缓TodoService瀹炰緥"""
    return TodoService(mock_db)


class TestTodoService:
    """TodoService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯TodoService鍒濆鍖?""
        service = TodoService(mock_db)
        assert service.db == mock_db
        assert service.todo_repo is not None
        assert service.notification_service is not None
    
    def test_create_todo_success(self, todo_service, mock_todo):
        """娴嬭瘯鍒涘缓寰呭姙浠诲姟鎴愬姛"""
        # 妯℃嫙鍒涘缓寰呭姙浠诲姟
        todo_service.todo_repo.create_todo = Mock(return_value=mock_todo)
        
        # 鎵ц鍒涘缓寰呭姙浠诲姟
        result = todo_service.create_todo(
            title="娴嬭瘯浠诲姟",
            user_id="user_001",
            tenant_id="default",
            description="娴嬭瘯鎻忚堪"
        )
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_todo_id"
        assert result.title == "娴嬭瘯浠诲姟"
        assert result.status == "pending"
        todo_service.todo_repo.create_todo.assert_called_once()
    
    def test_get_user_todos_success(self, todo_service, mock_todo):
        """娴嬭瘯鑾峰彇鐢ㄦ埛寰呭姙浠诲姟鎴愬姛"""
        # 妯℃嫙鏌ヨ寰呭姙浠诲姟鍒楄〃
        todo_service.todo_repo.get_user_todos = Mock(return_value=[mock_todo])
        
        # 鎵ц鏌ヨ
        result = todo_service.get_user_todos("user_001")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].user_id == "user_001"
        todo_service.todo_repo.get_user_todos.assert_called_once()
    
    def test_complete_todo_success(self, todo_service, mock_todo):
        """娴嬭瘯瀹屾垚寰呭姙浠诲姟鎴愬姛"""
        # 妯℃嫙鏌ヨ寰呭姙浠诲姟
        todo_service.todo_repo.get_todo_by_id = Mock(return_value=mock_todo)
        # 妯℃嫙鏇存柊寰呭姙浠诲姟
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        
        # 鎵ц瀹屾垚
        result = todo_service.complete_todo("test_todo_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result.id == "test_todo_id"
        mock_todo.mark_completed.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_complete_todo_not_found(self, todo_service):
        """娴嬭瘯瀹屾垚寰呭姙浠诲姟澶辫触锛堝緟鍔炰换鍔′笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ寰呭姙浠诲姟杩斿洖None
        todo_service.todo_repo.get_todo_by_id = Mock(return_value=None)
        
        # 鎵ц瀹屾垚
        result = todo_service.complete_todo("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_uncomplete_todo_success(self, todo_service, mock_todo):
        """娴嬭瘯鍙栨秷瀹屾垚寰呭姙浠诲姟鎴愬姛"""
        # 妯℃嫙鏌ヨ寰呭姙浠诲姟
        todo_service.todo_repo.get_todo_by_id = Mock(return_value=mock_todo)
        # 妯℃嫙鏇存柊寰呭姙浠诲姟
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        
        # 鎵ц鍙栨秷瀹屾垚
        result = todo_service.uncomplete_todo("test_todo_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result.id == "test_todo_id"
        mock_todo.mark_pending.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_delete_todo_success(self, todo_service):
        """娴嬭瘯鍒犻櫎寰呭姙浠诲姟鎴愬姛"""
        # 妯℃嫙鍒犻櫎寰呭姙浠诲姟
        todo_service.todo_repo.delete_todo = Mock(return_value=True)
        
        # 鎵ц鍒犻櫎
        result = todo_service.delete_todo("test_todo_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        todo_service.todo_repo.delete_todo.assert_called_once_with("test_todo_id")
    
    def test_get_overdue_todos_success(self, todo_service, mock_todo):
        """娴嬭瘯鑾峰彇閫炬湡浠诲姟鎴愬姛"""
        # 妯℃嫙鏌ヨ閫炬湡浠诲姟
        todo_service.todo_repo.get_overdue_todos = Mock(return_value=[mock_todo])
        
        # 鎵ц鏌ヨ
        result = todo_service.get_overdue_todos()
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        todo_service.todo_repo.get_overdue_todos.assert_called_once()
    
    def test_update_overdue_status_success(self, todo_service, mock_todo):
        """娴嬭瘯鏇存柊鎵€鏈変换鍔＄殑閫炬湡鐘舵€佹垚鍔?""
        # 妯℃嫙鏌ヨ鎵€鏈変换鍔?        todo_service.todo_repo.get_tenant_todos = Mock(return_value=[mock_todo])
        # 妯℃嫙鏇存柊浠诲姟
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        
        # 鎵ц鏇存柊閫炬湡鐘舵€?        todo_service.update_overdue_status()
        
        # 楠岃瘉缁撴灉
        mock_todo.update_overdue_status.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_create_daily_plan_success(self, todo_service, mock_daily_plan):
        """娴嬭瘯鍒涘缓姣忔棩璁″垝鎴愬姛"""
        # 妯℃嫙鍒涘缓姣忔棩璁″垝
        todo_service.todo_repo.create_daily_plan = Mock(return_value=mock_daily_plan)
        
        # 鎵ц鍒涘缓姣忔棩璁″垝
        result = todo_service.create_daily_plan(
            user_id="user_001",
            tenant_id="default",
            plan_date=date(2026, 1, 16),
            tasks=[{"title": "浠诲姟1"}]
        )
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_daily_plan_id"
        assert result.total_tasks == 1
        todo_service.todo_repo.create_daily_plan.assert_called_once()
    
    def test_get_user_daily_plan_success(self, todo_service, mock_daily_plan):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鎸囧畾鏃ユ湡鐨勬瘡鏃ヨ鍒掓垚鍔?""
        # 妯℃嫙鏌ヨ姣忔棩璁″垝
        todo_service.todo_repo.get_user_daily_plan = Mock(return_value=mock_daily_plan)
        
        # 鎵ц鏌ヨ
        result = todo_service.get_user_daily_plan("user_001", date(2026, 1, 16))
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result.user_id == "user_001"
        todo_service.todo_repo.get_user_daily_plan.assert_called_once()
    
    def test_get_user_daily_plan_not_found(self, todo_service):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鎸囧畾鏃ユ湡鐨勬瘡鏃ヨ鍒掑け璐?""
        # 妯℃嫙鏌ヨ姣忔棩璁″垝杩斿洖None
        todo_service.todo_repo.get_user_daily_plan = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = todo_service.get_user_daily_plan("user_001", date(2026, 1, 16))
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_todo_statistics_success(self, todo_service):
        """娴嬭瘯鑾峰彇鐢ㄦ埛寰呭姙浠诲姟缁熻淇℃伅鎴愬姛"""
        # 妯℃嫙鑾峰彇缁熻淇℃伅
        stats = {
            "total": 10,
            "pending": 5,
            "completed": 3,
            "overdue": 2
        }
        todo_service.todo_repo.get_todo_statistics = Mock(return_value=stats)
        
        # 鎵ц鑾峰彇缁熻
        result = todo_service.get_todo_statistics("user_001")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 10
        assert result["pending"] == 5
        todo_service.todo_repo.get_todo_statistics.assert_called_once()
    
    def test_send_overdue_reminders_success(self, todo_service, mock_todo):
        """娴嬭瘯鍙戦€侀€炬湡浠诲姟鎻愰啋鎴愬姛"""
        # 妯℃嫙鏌ヨ閫炬湡浠诲姟
        todo_service.todo_repo.get_overdue_todos = Mock(return_value=[mock_todo])
        # 妯℃嫙鏇存柊浠诲姟
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        # 妯℃嫙鍙戦€侀€氱煡
        todo_service.notification_service.send_system_notification = Mock()
        
        # 鎵ц鍙戦€侀€炬湡鎻愰啋
        todo_service.send_overdue_reminders()
        
        # 楠岃瘉缁撴灉
        todo_service.notification_service.send_system_notification.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_send_due_date_reminders_success(self, todo_service, mock_todo):
        """娴嬭瘯鍙戦€佸嵆灏嗗埌鏈熶换鍔℃彁閱掓垚鍔?""
        # 妯℃嫙鏌ヨ鎵€鏈変换鍔?        todo_service.todo_repo.get_tenant_todos = Mock(return_value=[mock_todo])
        # 妯℃嫙鍙戦€侀€氱煡
        todo_service.notification_service.send_system_notification = Mock()
        
        # 鎵ц鍙戦€佸嵆灏嗗埌鏈熸彁閱?        todo_service.send_due_date_reminders(hours_before=24)
        
        # 楠岃瘉缁撴灉
        todo_service.todo_repo.get_tenant_todos.assert_called_once()
    
    def test_count_todos_success(self, todo_service):
        """娴嬭瘯缁熻寰呭姙浠诲姟鏁伴噺鎴愬姛"""
        # 妯℃嫙缁熻
        todo_service.todo_repo.count_todos_by_user = Mock(return_value=10)
        
        # 鎵ц缁熻
        result = todo_service.count_todos(user_id="user_001")
        
        # 楠岃瘉缁撴灉
        assert result == 10
        todo_service.todo_repo.count_todos_by_user.assert_called_once()
    
    def test_count_todos_all_success(self, todo_service):
        """娴嬭瘯缁熻鎵€鏈夊緟鍔炰换鍔℃暟閲忔垚鍔?""
        # 妯℃嫙缁熻
        todo_service.todo_repo.count_all_todos = Mock(return_value=100)
        
        # 鎵ц缁熻
        result = todo_service.count_todos()
        
        # 楠岃瘉缁撴灉
        assert result == 100
        todo_service.todo_repo.count_all_todos.assert_called_once()
