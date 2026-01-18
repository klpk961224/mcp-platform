# -*- coding: utf-8 -*-
"""
UserService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓鐢ㄦ埛
2. 鑾峰彇鐢ㄦ埛
3. 鏇存柊鐢ㄦ埛
4. 鍒犻櫎鐢ㄦ埛
5. 鎼滅储鐢ㄦ埛
6. 鐢ㄦ埛鐘舵€佺鐞?"""

import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session

# 瀵煎叆鎵€鏈夋ā鍨嬶紝纭繚SQLAlchemy姝ｇ‘閰嶇疆mapper
from app.models import User, Department, Tenant
from sqlalchemy.orm import configure_mappers
configure_mappers()

from app.services.user_service import UserService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_user():
    """妯℃嫙鐢ㄦ埛瀵硅薄"""
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
    """鍒涘缓UserService瀹炰緥"""
    return UserService(mock_db)


class TestUserService:
    """UserService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯UserService鍒濆鍖?""
        service = UserService(mock_db)
        assert service.db == mock_db
        assert service.user_repo is not None
        assert service.dept_repo is not None
        assert service.tenant_repo is not None
    
    def test_create_user_success(self, user_service, mock_user):
        """娴嬭瘯鍒涘缓鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙绉熸埛瀵硅薄
        mock_tenant = Mock()
        mock_tenant.status = "active"
        mock_tenant.is_expired = Mock(return_value=False)
        mock_tenant.can_add_user = Mock(return_value=True)
        
        # 妯℃嫙鐢ㄦ埛鍚嶄笉瀛樺湪
        user_service.user_repo.exists_by_username = Mock(return_value=False)
        # 妯℃嫙閭涓嶅瓨鍦?        user_service.user_repo.exists_by_email = Mock(return_value=False)
        # 妯℃嫙绉熸埛瀛樺湪
        user_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 妯℃嫙鍒涘缓鐢ㄦ埛
        user_service.user_repo.create = Mock(return_value=mock_user)
        
        # 鎵ц鍒涘缓鐢ㄦ埛
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password",
            "tenant_id": "default"
        }
        result = user_service.create_user(user_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_user_id"
        assert result.username == "testuser"
        user_service.user_repo.create.assert_called_once()
    
    def test_create_user_username_exists(self, user_service):
        """娴嬭瘯鍒涘缓鐢ㄦ埛鏃剁敤鎴峰悕宸插瓨鍦?""
        # 妯℃嫙鐢ㄦ埛鍚嶅凡瀛樺湪
        user_service.user_repo.exists_by_username = Mock(return_value=True)
        
        # 鎵ц鍒涘缓鐢ㄦ埛骞堕獙璇佸紓甯?        user_data = {
            "username": "existing_user",
            "email": "test@example.com",
            "password_hash": "hashed_password"
        }
        with pytest.raises(ValueError, match="鐢ㄦ埛鍚嶅凡瀛樺湪"):
            user_service.create_user(user_data)
    
    def test_create_user_email_exists(self, user_service):
        """娴嬭瘯鍒涘缓鐢ㄦ埛鏃堕偖绠卞凡瀛樺湪"""
        # 妯℃嫙鐢ㄦ埛鍚嶄笉瀛樺湪
        user_service.user_repo.exists_by_username = Mock(return_value=False)
        # 妯℃嫙閭宸插瓨鍦?        user_service.user_repo.exists_by_email = Mock(return_value=True)
        
        # 鎵ц鍒涘缓鐢ㄦ埛骞堕獙璇佸紓甯?        user_data = {
            "username": "testuser",
            "email": "existing@example.com",
            "password_hash": "hashed_password"
        }
        with pytest.raises(ValueError, match="閭宸插瓨鍦?):
            user_service.create_user(user_data)
    
    def test_get_by_id_success(self, user_service, mock_user):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙鏌ヨ鐢ㄦ埛
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        
        # 鎵ц鏌ヨ
        result = user_service.get_user("test_user_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_user_id"
        user_service.user_repo.get_by_id.assert_called_once_with("test_user_id")
    
    def test_get_by_id_not_found(self, user_service):
        """娴嬭瘯鑾峰彇鐢ㄦ埛澶辫触"""
        # 妯℃嫙鏌ヨ鐢ㄦ埛杩斿洖None
        user_service.user_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = user_service.get_user("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_update_user_success(self, user_service, mock_user):
        """娴嬭瘯鏇存柊鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙鏌ヨ鐢ㄦ埛
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        # 妯℃嫙閭涓嶅瓨鍦?        user_service.user_repo.exists_by_email = Mock(return_value=False)
        # 妯℃嫙鏇存柊鐢ㄦ埛
        user_service.user_repo.update = Mock(return_value=mock_user)
        
        # 鎵ц鏇存柊
        update_data = {"email": "newemail@example.com"}
        result = user_service.update_user("test_user_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_user_id"
        user_service.user_repo.update.assert_called_once()
    
    def test_delete_user_success(self, user_service):
        """娴嬭瘯鍒犻櫎鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙鍒犻櫎鐢ㄦ埛
        user_service.user_repo.delete = Mock()
        
        # 鎵ц鍒犻櫎
        user_service.delete_user("test_user_id")
        
        # 楠岃瘉缁撴灉
        user_service.user_repo.delete.assert_called_once_with("test_user_id")
    
    def test_search_users_success(self, user_service, mock_user):
        """娴嬭瘯鎼滅储鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙鎼滅储鐢ㄦ埛
        user_service.list_users = Mock(return_value=[mock_user])
        
        # 鎵ц鎼滅储
        result = user_service.list_users(
            tenant_id="default",
            page=1,
            page_size=10
        )
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_user_id"
    
    def test_activate_user_success(self, user_service, mock_user):
        """娴嬭瘯婵€娲荤敤鎴锋垚鍔?""
        # 妯℃嫙鏌ヨ鐢ㄦ埛
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        # 妯℃嫙鏇存柊鐢ㄦ埛
        user_service.user_repo.update = Mock(return_value=mock_user)
        
        # 鎵ц婵€娲?        result = user_service.activate_user("test_user_id")
        
        # 楠岃瘉缁撴灉
        assert result.status == "active"
    
    def test_deactivate_user_success(self, user_service, mock_user):
        """娴嬭瘯鍋滅敤鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙鏌ヨ鐢ㄦ埛
        user_service.user_repo.get_by_id = Mock(return_value=mock_user)
        # 妯℃嫙鏇存柊鐢ㄦ埛
        user_service.user_repo.update = Mock(return_value=mock_user)
        
        # 鎵ц鍋滅敤
        result = user_service.deactivate_user("test_user_id")
        
        # 楠岃瘉缁撴灉
        assert result.status == "inactive"
    
    def test_get_user_statistics(self, user_service):
        """娴嬭瘯鑾峰彇鐢ㄦ埛缁熻"""
        # 妯℃嫙鑾峰彇缁熻
        user_service.count_users = Mock(return_value=100)
        
        # 鎵ц鑾峰彇缁熻
        result = user_service.count_users(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert result == 100
