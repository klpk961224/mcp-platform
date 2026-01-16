# -*- coding: utf-8 -*-
"""
TokenService单元测试

测试内容：
1. 创建Token
2. 吊销Token
3. 吊销用户所有Token
4. 清理过期Token
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.token_service import TokenService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_token():
    """模拟Token对象"""
    token = Mock()
    token.id = "test_token_id"
    token.user_id = "test_user_id"
    token.token_type = "access"
    token.token_hash = "hashed_token"
    token.expires_at = datetime(2026, 12, 31)
    token.is_revoked = False
    token.revoke = Mock()
    return token


@pytest.fixture
def token_service(mock_db):
    """创建TokenService实例"""
    return TokenService(mock_db)


class TestTokenService:
    """TokenService测试类"""
    
    def test_init(self, mock_db):
        """测试TokenService初始化"""
        service = TokenService(mock_db)
        assert service.db == mock_db
        assert service.token_repo is not None
    
    def test_create_token_success(self, token_service, mock_token):
        """测试创建Token成功"""
        # 模拟创建Token
        token_service.token_repo.create_token = Mock(return_value=mock_token)
        
        # 执行创建Token
        result = token_service.create_token(
            user_id="test_user_id",
            token_type="access",
            token_hash="hashed_token"
        )
        
        # 验证结果
        assert result.id == "test_token_id"
        assert result.user_id == "test_user_id"
        token_service.token_repo.create_token.assert_called_once()
    
    def test_revoke_token_success(self, token_service, mock_token):
        """测试吊销Token成功"""
        # 模拟查询Token
        token_service.token_repo.get_by_token_hash = Mock(return_value=mock_token)
        # 模拟更新Token
        token_service.token_repo.update = Mock()
        
        # 执行吊销Token
        result = token_service.revoke_token("hashed_token")
        
        # 验证结果
        assert result is True
        mock_token.revoke.assert_called_once()
        token_service.token_repo.update.assert_called_once()
    
    def test_revoke_token_not_found(self, token_service):
        """测试吊销Token失败（Token不存在）"""
        # 模拟查询Token返回None
        token_service.token_repo.get_by_token_hash = Mock(return_value=None)
        
        # 执行吊销Token
        result = token_service.revoke_token("nonexistent_token")
        
        # 验证结果
        assert result is False
    
    def test_revoke_all_tokens_success(self, token_service, mock_token):
        """测试吊销用户所有Token成功"""
        # 模拟查询用户Token
        token_service.token_repo.get_by_user_id = Mock(return_value=[mock_token])
        # 模拟更新Token
        token_service.token_repo.update = Mock()
        
        # 执行吊销所有Token
        result = token_service.revoke_all_tokens("test_user_id")
        
        # 验证结果
        assert result == 1
        mock_token.revoke.assert_called_once()
        token_service.token_repo.update.assert_called_once()
    
    def test_revoke_all_tokens_empty(self, token_service):
        """测试吊销用户所有Token（无Token）"""
        # 模拟查询用户Token返回空列表
        token_service.token_repo.get_by_user_id = Mock(return_value=[])
        
        # 执行吊销所有Token
        result = token_service.revoke_all_tokens("test_user_id")
        
        # 验证结果
        assert result == 0
    
    def test_clean_expired_tokens_success(self, token_service, mock_token):
        """测试清理过期Token成功"""
        # 模拟查询过期Token
        token_service.token_repo.get_expired_tokens = Mock(return_value=[mock_token])
        # 模拟删除Token
        token_service.token_repo.delete = Mock()
        
        # 执行清理过期Token
        result = token_service.clean_expired_tokens()
        
        # 验证结果
        assert result == 1
        token_service.token_repo.delete.assert_called_once_with("test_token_id")
    
    def test_clean_expired_tokens_empty(self, token_service):
        """测试清理过期Token（无过期Token）"""
        # 模拟查询过期Token返回空列表
        token_service.token_repo.get_expired_tokens = Mock(return_value=[])
        
        # 执行清理过期Token
        result = token_service.clean_expired_tokens()
        
        # 验证结果
        assert result == 0