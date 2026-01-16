# -*- coding: utf-8 -*-
"""
Auth API集成测试

测试内容：
1. 用户登录API
2. 刷新Token API
3. 用户登出API
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
        "username": "testuser",
        "email": "test@example.com",
        "status": "active",
        "tenant_id": "default"
    }


class TestAuthAPI:
    """Auth API测试类"""
    
    def test_login_success(self, client, mock_user):
        """测试登录成功"""
        # 模拟AuthService
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.login.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "token_type": "bearer",
                "expires_in": 86400,
                "user_info": mock_user
            }
            MockAuthService.return_value = mock_service
            
            # 发送登录请求
            response = client.post("/api/v1/auth/login", json={
                "username": "testuser",
                "password": "password"
            })
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "test_access_token"
            assert data["refresh_token"] == "test_refresh_token"
            assert data["user_info"]["username"] == "testuser"
    
    def test_login_wrong_password(self, client):
        """测试登录失败（密码错误）"""
        # 模拟AuthService抛出异常
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.login.side_effect = ValueError("用户名或密码错误")
            MockAuthService.return_value = mock_service
            
            # 发送登录请求
            response = client.post("/api/v1/auth/login", json={
                "username": "testuser",
                "password": "wrong_password"
            })
            
            # 验证响应
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_login_user_disabled(self, client):
        """测试登录失败（用户已禁用）"""
        # 模拟AuthService抛出异常
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.login.side_effect = ValueError("用户已被禁用")
            MockAuthService.return_value = mock_service
            
            # 发送登录请求
            response = client.post("/api/v1/auth/login", json={
                "username": "testuser",
                "password": "password"
            })
            
            # 验证响应
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_refresh_token_success(self, client):
        """测试刷新Token成功"""
        # 模拟AuthService
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.refresh_token.return_value = {
                "access_token": "new_access_token",
                "token_type": "bearer",
                "expires_in": 86400
            }
            MockAuthService.return_value = mock_service
            
            # 发送刷新Token请求
            response = client.post("/api/v1/auth/refresh", json={
                "refresh_token": "test_refresh_token"
            })
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "new_access_token"
    
    def test_refresh_token_invalid(self, client):
        """测试刷新Token失败（Token无效）"""
        # 模拟AuthService抛出异常
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.refresh_token.side_effect = ValueError("Token无效或已过期")
            MockAuthService.return_value = mock_service
            
            # 发送刷新Token请求
            response = client.post("/api/v1/auth/refresh", json={
                "refresh_token": "invalid_token"
            })
            
            # 验证响应
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_logout_success(self, client):
        """测试登出成功"""
        # 模拟AuthService
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.logout.return_value = True
            MockAuthService.return_value = mock_service
            
            # 模拟Token验证
            with patch('app.api.v1.auth.verify_token', return_value={"user_id": "test_user_id"}):
                # 发送登出请求
                response = client.post("/api/v1/auth/logout", json={
                    "refresh_token": "test_refresh_token"
                })
                
                # 验证响应
                assert response.status_code == 200
                data = response.json()
                assert data["message"] == "登出成功"
    
    def test_logout_invalid_token(self, client):
        """测试登出失败（Token无效）"""
        # 模拟Token验证失败
        with patch('app.api.v1.auth.verify_token', return_value=None):
            # 发送登出请求
            response = client.post("/api/v1/auth/logout", json={
                "refresh_token": "invalid_token"
            })
            
            # 验证响应
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_login_missing_username(self, client):
        """测试登录失败（缺少用户名）"""
        # 发送登录请求（缺少用户名）
        response = client.post("/api/v1/auth/login", json={
            "password": "password"
        })
        
        # 验证响应
        assert response.status_code == 422  # Validation Error
    
    def test_login_missing_password(self, client):
        """测试登录失败（缺少密码）"""
        # 发送登录请求（缺少密码）
        response = client.post("/api/v1/auth/login", json={
            "username": "testuser"
        })
        
        # 验证响应
        assert response.status_code == 422  # Validation Error
    
    def test_refresh_token_missing_token(self, client):
        """测试刷新Token失败（缺少Token）"""
        # 发送刷新Token请求（缺少Token）
        response = client.post("/api/v1/auth/refresh", json={})
        
        # 验证响应
        assert response.status_code == 422  # Validation Error