# -*- coding: utf-8 -*-
"""
TokenService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建Token
2. 鍚婇攢Token
3. 鍚婇攢鐢ㄦ埛鎵€鏈塗oken
4. 娓呯悊杩囨湡Token
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.token_service import TokenService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_token():
    """妯℃嫙Token瀵硅薄"""
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
    """创建TokenService瀹炰緥"""
    return TokenService(mock_db)


class TestTokenService:
    """TokenService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯TokenService鍒濆鍖?""
        service = TokenService(mock_db)
        assert service.db == mock_db
        assert service.token_repo is not None
    
    def test_create_token_success(self, token_service, mock_token):
        """娴嬭瘯创建Token鎴愬姛"""
        # 妯℃嫙创建Token
        token_service.token_repo.create_token = Mock(return_value=mock_token)
        
        # 鎵ц创建Token
        result = token_service.create_token(
            user_id="test_user_id",
            token_type="access",
            token_hash="hashed_token"
        )
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_token_id"
        assert result.user_id == "test_user_id"
        token_service.token_repo.create_token.assert_called_once()
    
    def test_revoke_token_success(self, token_service, mock_token):
        """娴嬭瘯鍚婇攢Token鎴愬姛"""
        # 妯℃嫙查询Token
        token_service.token_repo.get_by_token_hash = Mock(return_value=mock_token)
        # 妯℃嫙更新Token
        token_service.token_repo.update = Mock()
        
        # 鎵ц鍚婇攢Token
        result = token_service.revoke_token("hashed_token")
        
        # 楠岃瘉缁撴灉
        assert result is True
        mock_token.revoke.assert_called_once()
        token_service.token_repo.update.assert_called_once()
    
    def test_revoke_token_not_found(self, token_service):
        """娴嬭瘯鍚婇攢Token澶辫触锛圱oken涓嶅瓨鍦級"""
        # 妯℃嫙查询Token杩斿洖None
        token_service.token_repo.get_by_token_hash = Mock(return_value=None)
        
        # 鎵ц鍚婇攢Token
        result = token_service.revoke_token("nonexistent_token")
        
        # 楠岃瘉缁撴灉
        assert result is False
    
    def test_revoke_all_tokens_success(self, token_service, mock_token):
        """娴嬭瘯鍚婇攢鐢ㄦ埛鎵€鏈塗oken鎴愬姛"""
        # 妯℃嫙查询鐢ㄦ埛Token
        token_service.token_repo.get_by_user_id = Mock(return_value=[mock_token])
        # 妯℃嫙更新Token
        token_service.token_repo.update = Mock()
        
        # 鎵ц鍚婇攢鎵€鏈塗oken
        result = token_service.revoke_all_tokens("test_user_id")
        
        # 楠岃瘉缁撴灉
        assert result == 1
        mock_token.revoke.assert_called_once()
        token_service.token_repo.update.assert_called_once()
    
    def test_revoke_all_tokens_empty(self, token_service):
        """娴嬭瘯鍚婇攢鐢ㄦ埛鎵€鏈塗oken锛堟棤Token锛?""
        # 妯℃嫙查询鐢ㄦ埛Token杩斿洖绌哄垪琛?        token_service.token_repo.get_by_user_id = Mock(return_value=[])
        
        # 鎵ц鍚婇攢鎵€鏈塗oken
        result = token_service.revoke_all_tokens("test_user_id")
        
        # 楠岃瘉缁撴灉
        assert result == 0
    
    def test_clean_expired_tokens_success(self, token_service, mock_token):
        """娴嬭瘯娓呯悊杩囨湡Token鎴愬姛"""
        # 妯℃嫙查询杩囨湡Token
        token_service.token_repo.get_expired_tokens = Mock(return_value=[mock_token])
        # 妯℃嫙删除Token
        token_service.token_repo.delete = Mock()
        
        # 鎵ц娓呯悊杩囨湡Token
        result = token_service.clean_expired_tokens()
        
        # 楠岃瘉缁撴灉
        assert result == 1
        token_service.token_repo.delete.assert_called_once_with("test_token_id")
    
    def test_clean_expired_tokens_empty(self, token_service):
        """娴嬭瘯娓呯悊杩囨湡Token锛堟棤杩囨湡Token锛?""
        # 妯℃嫙查询杩囨湡Token杩斿洖绌哄垪琛?        token_service.token_repo.get_expired_tokens = Mock(return_value=[])
        
        # 鎵ц娓呯悊杩囨湡Token
        result = token_service.clean_expired_tokens()
        
        # 楠岃瘉缁撴灉
        assert result == 0
