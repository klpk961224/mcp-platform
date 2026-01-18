# -*- coding: utf-8 -*-
"""
AuthService单元测试

测试内容：
1. 用户登录
2. 用户登出
3. 刷新Token
4. 密码验证
5. 用户状态检查
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session

from app.services import auth_service as auth_service_module
from app.services.auth_service import AuthService
from app.models.user import User
from app.models.token import Token


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
    user.to_dict = Mock(return_value={
        "id": "test_user_id",
        "username": "testuser",
        "email": "test@example.com",
        "status": "active",
        "tenant_id": "default"
    })
    return user


@pytest.fixture
def auth_service(mock_db):
    """创建AuthService实例"""
    return AuthService(mock_db)


class TestAuthService:
    """AuthService测试类"""
    
    def test_init(self, mock_db):
        """测试AuthService初始化"""
        service = AuthService(mock_db)
        assert service.db == mock_db
        assert service.user_repo is not None
        assert service.token_repo is not None
    
    def test_login_success(self, auth_service, mock_user):
        """测试登录成功"""
        # 模拟用户查询
        auth_service.user_repo.get_by_username = Mock(return_value=mock_user)
        # 模拟Token创建
        auth_service.token_repo.create_token = Mock()
        # 模拟用户更新
        auth_service.user_repo.update = Mock()
        # 模拟密码验证
        with patch('app.services.auth_service.verify_password', return_value=True):
            # 模拟Token生成
            with patch('app.services.auth_service.create_access_token', return_value='access_token'):
                with patch('app.services.auth_service.create_refresh_token', return_value='refresh_token'):
                    # 执行登录
                    result = auth_service.login(username="testuser", password="password")
                    
                    # 验证结果
                    assert result["access_token"] == "access_token"
                    assert result["refresh_token"] == "refresh_token"
                    assert result["user_info"]["username"] == "testuser"
    
    def test_login_user_not_found(self, auth_service):
        """测试用户不存在"""
        # 模拟用户查询返回None
        auth_service.user_repo.get_by_username = Mock(return_value=None)
        
        # 执行登录并验证异常
        with pytest.raises(ValueError, match="用户名或密码错误"):
            auth_service.login(username="nonexistent", password="password")
    
    def test_login_wrong_password(self, auth_service, mock_user):
        """测试密码错误"""
        # 模拟用户查询
        auth_service.user_repo.get_by_username = Mock(return_value=mock_user)
        # 模拟密码验证失败
        with patch('app.services.auth_service.verify_password', return_value=False):
            # 执行登录并验证异常
            with pytest.raises(ValueError, match="用户名或密码错误"):
                auth_service.login(username="testuser", password="wrong_password")
    
    def test_login_user_disabled(self, auth_service, mock_user):
        """测试用户已被禁用"""
        # 设置用户状态为inactive
        mock_user.status = "inactive"
        # 模拟用户查询
        auth_service.user_repo.get_by_username = Mock(return_value=mock_user)
        # 模拟密码验证成功
        with patch('app.services.auth_service.verify_password', return_value=True):
            # 执行登录并验证异常
            with pytest.raises(ValueError, match="用户已被禁用"):
                auth_service.login(username="testuser", password="password")
    
    def test_logout_success(self, auth_service):
        """测试登出成功"""
        # 模拟吊销Token
        auth_service.token_repo.revoke_all_tokens = Mock()
        
        # 执行登出
        result = auth_service.logout(user_id="test_user_id")
        
        # 验证结果
        assert result is True
        auth_service.token_repo.revoke_all_tokens.assert_called_once_with("test_user_id")
    
    def test_refresh_token_success(self, auth_service):
        """测试刷新Token成功"""
        # 保存原始函数
        original_verify_token = auth_service_module.verify_token
        
        try:
            # 替换为mock函数
            auth_service_module.verify_token = Mock(return_value={"user_id": "test_user_id"})
            
            # 模拟Token生成
            with patch('app.services.auth_service.create_access_token', return_value='new_access_token'):
                # 执行刷新Token
                result = auth_service.refresh_token("refresh_token")
                
                # 验证结果
                assert result["access_token"] == "new_access_token"
                assert result["token_type"] == "bearer"
        finally:
            # 恢复原始函数
            auth_service_module.verify_token = original_verify_token
    
    def test_refresh_token_invalid(self, auth_service):
        """测试刷新Token无效"""
        # 保存原始函数
        original_verify_token = auth_service_module.verify_token
        
        try:
            # 替换为mock函数
            auth_service_module.verify_token = Mock(return_value=None)
            
            # 执行刷新Token并验证异常
            with pytest.raises(ValueError, match="Token无效或已过期"):
                auth_service.refresh_token("invalid_token")
        finally:
            # 恢复原始函数
            auth_service_module.verify_token = original_verify_token

