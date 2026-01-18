# -*- coding: utf-8 -*-
"""
TodoService单元测试

测试内容：
1. 创建待办任务
2. 获取待办任务
3. 完成待办任务
4. 取消完成待办任务
5. 删除待办任务
6. 获取逾期任务
7. 创建每日计划
8. 获取每日计划
9. 获取统计信息
10. 发送逾期提醒
11. 发送即将到期提醒
12. 统计待办任务数量
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.services.todo_service import TodoService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_todo():
    """模拟待办任务对象"""
    todo = Mock()
    todo.id = "test_todo_id"
    todo.tenant_id = "default"
    todo.user_id = "user_001"
    todo.username = "User_001"
    todo.title = "测试任务"
    todo.description = "测试描述"
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
    
    # 模拟方法
    todo.mark_completed = Mock()
    todo.mark_pending = Mock()
    todo.update_overdue_status = Mock()
    
    return todo


@pytest.fixture
def mock_daily_plan():
    """模拟每日计划对象"""
    daily_plan = Mock()
    daily_plan.id = "test_daily_plan_id"
    daily_plan.tenant_id = "default"
    daily_plan.user_id = "user_001"
    daily_plan.username = "User_001"
    daily_plan.plan_date = datetime(2026, 1, 16)
    daily_plan.tasks = '[{"title": "任务1", "completed": false}]'
    daily_plan.notes = "备注"
    daily_plan.total_tasks = 1
    daily_plan.completed_tasks = 0
    daily_plan.completion_rate = 0
    daily_plan.created_at = datetime(2026, 1, 16)
    daily_plan.updated_at = datetime(2026, 1, 16)
    return daily_plan


@pytest.fixture
def todo_service(mock_db):
    """创建TodoService实例"""
    return TodoService(mock_db)


class TestTodoService:
    """TodoService测试类"""
    
    def test_init(self, mock_db):
        """测试TodoService初始化"""
        service = TodoService(mock_db)
        assert service.db == mock_db
        assert service.todo_repo is not None
        assert service.notification_service is not None
    
    def test_create_todo_success(self, todo_service, mock_todo):
        """测试创建待办任务成功"""
        # 模拟创建待办任务
        todo_service.todo_repo.create_todo = Mock(return_value=mock_todo)
        
        # 执行创建待办任务
        result = todo_service.create_todo(
            title="测试任务",
            user_id="user_001",
            tenant_id="default",
            description="测试描述"
        )
        
        # 验证结果
        assert result.id == "test_todo_id"
        assert result.title == "测试任务"
        assert result.status == "pending"
        todo_service.todo_repo.create_todo.assert_called_once()
    
    def test_get_user_todos_success(self, todo_service, mock_todo):
        """测试获取用户待办任务成功"""
        # 模拟查询待办任务列表
        todo_service.todo_repo.get_user_todos = Mock(return_value=[mock_todo])
        
        # 执行查询
        result = todo_service.get_user_todos("user_001")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].user_id == "user_001"
        todo_service.todo_repo.get_user_todos.assert_called_once()
    
    def test_complete_todo_success(self, todo_service, mock_todo):
        """测试完成待办任务成功"""
        # 模拟查询待办任务
        todo_service.todo_repo.get_todo_by_id = Mock(return_value=mock_todo)
        # 模拟更新待办任务
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        
        # 执行完成
        result = todo_service.complete_todo("test_todo_id")
        
        # 验证结果
        assert result is not None
        assert result.id == "test_todo_id"
        mock_todo.mark_completed.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_complete_todo_not_found(self, todo_service):
        """测试完成待办任务失败（待办任务不存在）"""
        # 模拟查询待办任务返回None
        todo_service.todo_repo.get_todo_by_id = Mock(return_value=None)
        
        # 执行完成
        result = todo_service.complete_todo("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_uncomplete_todo_success(self, todo_service, mock_todo):
        """测试取消完成待办任务成功"""
        # 模拟查询待办任务
        todo_service.todo_repo.get_todo_by_id = Mock(return_value=mock_todo)
        # 模拟更新待办任务
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        
        # 执行取消完成
        result = todo_service.uncomplete_todo("test_todo_id")
        
        # 验证结果
        assert result is not None
        assert result.id == "test_todo_id"
        mock_todo.mark_pending.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_delete_todo_success(self, todo_service):
        """测试删除待办任务成功"""
        # 模拟删除待办任务
        todo_service.todo_repo.delete_todo = Mock(return_value=True)
        
        # 执行删除
        result = todo_service.delete_todo("test_todo_id")
        
        # 验证结果
        assert result is True
        todo_service.todo_repo.delete_todo.assert_called_once_with("test_todo_id")
    
    def test_get_overdue_todos_success(self, todo_service, mock_todo):
        """测试获取逾期任务成功"""
        # 模拟查询逾期任务
        todo_service.todo_repo.get_overdue_todos = Mock(return_value=[mock_todo])
        
        # 执行查询
        result = todo_service.get_overdue_todos()
        
        # 验证结果
        assert len(result) == 1
        todo_service.todo_repo.get_overdue_todos.assert_called_once()
    
    def test_update_overdue_status_success(self, todo_service, mock_todo):
        """测试更新所有任务的逾期状态成功"""
        # 模拟查询所有任务
        todo_service.todo_repo.get_tenant_todos = Mock(return_value=[mock_todo])
        # 模拟更新任务
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        
        # 执行更新逾期状态
        todo_service.update_overdue_status()
        
        # 验证结果
        mock_todo.update_overdue_status.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_create_daily_plan_success(self, todo_service, mock_daily_plan):
        """测试创建每日计划成功"""
        # 模拟创建每日计划
        todo_service.todo_repo.create_daily_plan = Mock(return_value=mock_daily_plan)
        
        # 执行创建每日计划
        result = todo_service.create_daily_plan(
            user_id="user_001",
            tenant_id="default",
            plan_date=date(2026, 1, 16),
            tasks=[{"title": "任务1"}]
        )
        
        # 验证结果
        assert result.id == "test_daily_plan_id"
        assert result.total_tasks == 1
        todo_service.todo_repo.create_daily_plan.assert_called_once()
    
    def test_get_user_daily_plan_success(self, todo_service, mock_daily_plan):
        """测试获取用户指定日期的每日计划成功"""
        # 模拟查询每日计划
        todo_service.todo_repo.get_user_daily_plan = Mock(return_value=mock_daily_plan)
        
        # 执行查询
        result = todo_service.get_user_daily_plan("user_001", date(2026, 1, 16))
        
        # 验证结果
        assert result is not None
        assert result.user_id == "user_001"
        todo_service.todo_repo.get_user_daily_plan.assert_called_once()
    
    def test_get_user_daily_plan_not_found(self, todo_service):
        """测试获取用户指定日期的每日计划失败"""
        # 模拟查询每日计划返回None
        todo_service.todo_repo.get_user_daily_plan = Mock(return_value=None)
        
        # 执行查询
        result = todo_service.get_user_daily_plan("user_001", date(2026, 1, 16))
        
        # 验证结果
        assert result is None
    
    def test_get_todo_statistics_success(self, todo_service):
        """测试获取用户待办任务统计信息成功"""
        # 模拟获取统计信息
        stats = {
            "total": 10,
            "pending": 5,
            "completed": 3,
            "overdue": 2
        }
        todo_service.todo_repo.get_todo_statistics = Mock(return_value=stats)
        
        # 执行获取统计
        result = todo_service.get_todo_statistics("user_001")
        
        # 验证结果
        assert result["total"] == 10
        assert result["pending"] == 5
        todo_service.todo_repo.get_todo_statistics.assert_called_once()
    
    def test_send_overdue_reminders_success(self, todo_service, mock_todo):
        """测试发送逾期任务提醒成功"""
        # 模拟查询逾期任务
        todo_service.todo_repo.get_overdue_todos = Mock(return_value=[mock_todo])
        # 模拟更新任务
        todo_service.todo_repo.update_todo = Mock(return_value=mock_todo)
        # 模拟发送通知
        todo_service.notification_service.send_system_notification = Mock()
        
        # 执行发送逾期提醒
        todo_service.send_overdue_reminders()
        
        # 验证结果
        todo_service.notification_service.send_system_notification.assert_called_once()
        todo_service.todo_repo.update_todo.assert_called_once()
    
    def test_send_due_date_reminders_success(self, todo_service, mock_todo):
        """测试发送即将到期任务提醒成功"""
        # 模拟查询所有任务
        todo_service.todo_repo.get_tenant_todos = Mock(return_value=[mock_todo])
        # 模拟发送通知
        todo_service.notification_service.send_system_notification = Mock()
        
        # 执行发送即将到期提醒
        todo_service.send_due_date_reminders(hours_before=24)
        
        # 验证结果
        todo_service.todo_repo.get_tenant_todos.assert_called_once()
    
    def test_count_todos_success(self, todo_service):
        """测试统计待办任务数量成功"""
        # 模拟统计
        todo_service.todo_repo.count_todos_by_user = Mock(return_value=10)
        
        # 执行统计
        result = todo_service.count_todos(user_id="user_001")
        
        # 验证结果
        assert result == 10
        todo_service.todo_repo.count_todos_by_user.assert_called_once()
    
    def test_count_todos_all_success(self, todo_service):
        """测试统计所有待办任务数量成功"""
        # 模拟统计
        todo_service.todo_repo.count_all_todos = Mock(return_value=100)
        
        # 执行统计
        result = todo_service.count_todos()
        
        # 验证结果
        assert result == 100
        todo_service.todo_repo.count_all_todos.assert_called_once()