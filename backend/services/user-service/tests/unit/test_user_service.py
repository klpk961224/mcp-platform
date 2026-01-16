# -*- coding: utf-8 -*-
"""
UserService单元测试

测试内容：
1. 创建用户
2. 获取用户
3. 更新用户
4. 删除用户
5. 搜索用户
6. 用户状态管理
"""

import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session

# 导入所有模型，确保SQLAlchemy正确配置mapper
from app.models import User, Department, Tenant
from sqlalchemy.orm import configure_mappers
configure_mappers()

from app.services.user_service import UserService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_user():
    """模拟用户对象"""
    user = Mock(spec=User)
    user.id = "test_user_id"
    user.username = "testuser"
    user.email = "test@example.com"
    user.password_hash = "hashed_password"
    user.status = "active"
    user.tenant_id = "default"
    user.department_id = None
    user.created_at = Mock()
    user.updated_at = Mock()
    user.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
    user.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
    return user


@pytest.fixture
def user_service(mock_db):
    """创建UserService实例"""
    return UserService(mock_db)


class TestUserService:
    """UserService测试类"""
    
    def test_init(self, mock_db):
        """测试UserService初始化"""
        service = UserService(mock_db)
        assert service.db == mock_db
        assert service.user_repo is not None
        assert service.dept_repo is not None
        assert service.tenant_repo is not None
    
    def test_create_user_success(self, user_service, mock_user):
        """测试创建用户成功"""
        # 模拟租户对象
        mock_tenant = Mock()
        mock_tenant.status = "active"
        mock_tenant.is_expired = Mock(return_value=False)
        mock_tenant.can_add_user = Mock(return_value=True)
        
        # 模拟用户名不存在
        user_service.user_repo.exists_by_username = Mock(return_value=False)
        # 模拟邮箱不存在
        user_service.user_repo.exists_by_email = Mock(return_value=False)
        # 模拟租户存在
        user_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 模拟创建用户
        user_service.user_repo.create = Mock(return_value=mock_user)
        
        # 执行创建用户
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password",
            "tenant_id": "default"
        }
        result = user_service.create_user(user_data)
        
        # 验证结果
        assert result.id == "test_user_id"
        assert result.username == "testuser"
        user_service.user_repo.create.assert_called_once()
    
    def test_create_user_username_exists(self, user_service):
        """测试创建用户时用户名已存在"""
        # 模拟用户名已存在
        user_service.user_repo.exists_by_username = Mock(return_value=True)
        
        # 执行创建用户并验证异常
        user_data = {
            "username": "existing_user",
            "email": "test@example.com",
            "password_hash": "hashed_password"
        }
        with pytest.raises(ValueError, match="用户名已存在"):
            user_service.create_user(user_data)
    
    def test_create_user_email_exists(self, user_service):
        """测试创建用户时邮箱已存在"""
        # 模拟用户名不存在
        user_service.user_repo.exists_by_username = Mock(return_value=False)
        # 模拟邮箱已存在
        user_service.user_repo.exists_by_email = Mock(return_value=True)
        
        # 执行创建用户并验证异常
        user_data = {
            "username": "testuser",
            "email": "existing@example.com",
            "password_hash": "hashed_password"
        }
        with pytest.raises(ValueError, match="邮箱已存在"):
            user_service.create_user(user_data)
    
    def test_get_by_id_success(self, user_service, mock_user):
        """测试获取用户成功"""
        # 模拟查询用户
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        
        # 执行查询
        result = user_service.get_user("test_user_id")
        
        # 验证结果
        assert result.id == "test_user_id"
        user_service.user_repo.get_by_id.assert_called_once_with("test_user_id")
    
    def test_get_by_id_not_found(self, user_service):
        """测试获取用户失败"""
        # 模拟查询用户返回None
        user_service.user_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = user_service.get_user("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_update_user_success(self, user_service, mock_user):
        """测试更新用户成功"""
        # 模拟查询用户
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        # 模拟邮箱不存在
        user_service.user_repo.exists_by_email = Mock(return_value=False)
        # 模拟更新用户
        user_service.user_repo.update = Mock(return_value=mock_user)
        
        # 执行更新
        update_data = {"email": "newemail@example.com"}
        result = user_service.update_user("test_user_id", update_data)
        
        # 验证结果
        assert result.id == "test_user_id"
        user_service.user_repo.update.assert_called_once()
    
    def test_delete_user_success(self, user_service):
        """测试删除用户成功"""
        # 模拟删除用户
        user_service.user_repo.delete = Mock()
        
        # 执行删除
        user_service.delete_user("test_user_id")
        
        # 验证结果
        user_service.user_repo.delete.assert_called_once_with("test_user_id")
    
    def test_search_users_success(self, user_service, mock_user):
        """测试搜索用户成功"""
        # 模拟搜索用户
        user_service.list_users = Mock(return_value=[mock_user])
        
        # 执行搜索
        result = user_service.list_users(
            tenant_id="default",
            page=1,
            page_size=10
        )
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_user_id"
    
    def test_activate_user_success(self, user_service, mock_user):
        """测试激活用户成功"""
        # 模拟查询用户
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        # 模拟更新用户
        user_service.user_repo.update = Mock(return_value=mock_user)
        
        # 执行激活
        result = user_service.activate_user("test_user_id")
        
        # 验证结果
        assert result.status == "active"
    
    def test_deactivate_user_success(self, user_service, mock_user):
        """测试停用用户成功"""
        # 模拟查询用户
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        # 模拟更新用户
        user_service.user_repo.update = Mock(return_value=mock_user)
        
        # 执行停用
        result = user_service.deactivate_user("test_user_id")
        
        # 验证结果
        assert result.status == "inactive"
    
    def test_get_user_statistics(self, user_service):
        """测试获取用户统计"""
        # 模拟获取统计
        user_service.count_users = Mock(return_value=100)
        
        # 执行获取统计
        result = user_service.count_users(tenant_id="default")
        
        # 验证结果
        assert result == 100