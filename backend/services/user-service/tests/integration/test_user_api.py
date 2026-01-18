# -*- coding: utf-8 -*-
"""
User API集成测试

测试内容：
1. 创建用户API
2. 获取用户列表API
3. 获取用户详情API
4. 更新用户API
5. 删除用户API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


@pytest.fixture
def client():
    """创建测试客户端"""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_user():
    """模拟用户数据"""
    return {
        "id": "test_user_id",
        "tenant_id": "default",
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13800138000",
        "dept_id": None,
        "position_id": None,
        "status": "active",
        "created_at": "2026-01-15T00:00:00",
        "updated_at": "2026-01-15T00:00:00"
    }


class TestUserAPI:
    """User API测试类"""
    
    def test_create_user_success(self, client, mock_user):
        """测试创建用户成功"""
        # 模拟UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_user_obj.id = "test_user_id"
            mock_user_obj.username = "testuser"
            mock_user_obj.email = "test@example.com"
            mock_user_obj.phone = "13800138000"
            mock_user_obj.department_id = None
            mock_user_obj.status = "active"
            mock_user_obj.created_at = Mock()
            mock_user_obj.updated_at = Mock()
            mock_user_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_user_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.create_user.return_value = mock_user_obj
            MockUserService.return_value = mock_service
            
            # 发送创建用户请求
            response = client.post("/api/v1/users", json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "tenant_id": "default"
            })
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "testuser"
            assert data["email"] == "test@example.com"
    
    def test_create_user_username_exists(self, client):
        """测试创建用户失败（用户名已存在）"""
        # 模拟UserService抛出异常
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.create_user.side_effect = ValueError("用户名已存在")
            MockUserService.return_value = mock_service
            
            # 发送创建用户请求
            response = client.post("/api/v1/users", json={
                "username": "existing_user",
                "email": "test@example.com",
                "password": "password123",
                "tenant_id": "default"
            })
            
            # 验证响应
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
    
    def test_get_users_success(self, client, mock_user):
        """测试获取用户列表成功"""
        # 模拟UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_user_obj.id = "test_user_id"
            mock_user_obj.username = "testuser"
            mock_user_obj.email = "test@example.com"
            mock_user_obj.department_id = None
            mock_user_obj.status = "active"
            mock_user_obj.created_at = Mock()
            mock_user_obj.updated_at = Mock()
            mock_user_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_user_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.search_users.return_value = ([mock_user_obj], 1)
            MockUserService.return_value = mock_service
            
            # 发送获取用户列表请求
            response = client.get("/api/v1/users?page=1&page_size=10")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert len(data["items"]) == 1
            assert data["items"][0]["username"] == "testuser"
    
    def test_get_users_with_filters(self, client):
        """测试获取用户列表（带筛选条件）"""
        # 模拟UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.search_users.return_value = ([], 0)
            MockUserService.return_value = mock_service
            
            # 发送获取用户列表请求（带筛选条件）
            response = client.get("/api/v1/users?page=1&page_size=10&tenant_id=default&status=active&keyword=test")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["items"]) == 0
    
    def test_get_user_success(self, client, mock_user):
        """测试获取用户详情成功"""
        # 模拟UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_user_obj.id = "test_user_id"
            mock_user_obj.username = "testuser"
            mock_user_obj.email = "test@example.com"
            mock_user_obj.department_id = None
            mock_user_obj.status = "active"
            mock_user_obj.created_at = Mock()
            mock_user_obj.updated_at = Mock()
            mock_user_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_user_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.get_by_id.return_value = mock_user_obj
            MockUserService.return_value = mock_service
            
            # 发送获取用户详情请求
            response = client.get("/api/v1/users/test_user_id")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_user_id"
            assert data["username"] == "testuser"
    
    def test_get_user_not_found(self, client):
        """测试获取用户详情失败（用户不存在）"""
        # 模拟UserService返回None
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockUserService.return_value = mock_service
            
            # 发送获取用户详情请求
            response = client.get("/api/v1/users/nonexistent_id")
            
            # 验证响应
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_update_user_success(self, client):
        """测试更新用户成功"""
        # 模拟UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_user_obj.id = "test_user_id"
            mock_user_obj.username = "testuser"
            mock_user_obj.email = "newemail@example.com"
            mock_user_obj.department_id = None
            mock_user_obj.status = "active"
            mock_user_obj.created_at = Mock()
            mock_user_obj.updated_at = Mock()
            mock_user_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_user_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.get_by_id.return_value = mock_user_obj
            mock_service.update_user.return_value = mock_user_obj
            MockUserService.return_value = mock_service
            
            # 发送更新用户请求
            response = client.put("/api/v1/users/test_user_id", json={
                "email": "newemail@example.com"
            })
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "newemail@example.com"
    
    def test_update_user_not_found(self, client):
        """测试更新用户失败（用户不存在）"""
        # 模拟UserService返回None
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockUserService.return_value = mock_service
            
            # 发送更新用户请求
            response = client.put("/api/v1/users/nonexistent_id", json={
                "email": "newemail@example.com"
            })
            
            # 验证响应
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_delete_user_success(self, client):
        """测试删除用户成功"""
        # 模拟UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_service.get_by_id.return_value = mock_user_obj
            mock_service.delete_user = Mock()
            MockUserService.return_value = mock_service
            
            # 发送删除用户请求
            response = client.delete("/api/v1/users/test_user_id")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "删除成功"
    
    def test_delete_user_not_found(self, client):
        """测试删除用户失败（用户不存在）"""
        # 模拟UserService返回None
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockUserService.return_value = mock_service
            
            # 发送删除用户请求
            response = client.delete("/api/v1/users/nonexistent_id")
            
            # 验证响应
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_create_user_missing_username(self, client):
        """测试创建用户失败（缺少用户名）"""
        # 发送创建用户请求（缺少用户名）
        response = client.post("/api/v1/users", json={
            "email": "test@example.com",
            "password": "password123",
            "tenant_id": "default"
        })
        
        # 验证响应
        assert response.status_code == 422  # Validation Error
    
    def test_create_user_missing_email(self, client):
        """测试创建用户失败（缺少邮箱）"""
        # 发送创建用户请求（缺少邮箱）
        response = client.post("/api/v1/users", json={
            "username": "testuser",
            "password": "password123",
            "tenant_id": "default"
        })
        
        # 验证响应
        assert response.status_code == 422  # Validation Error