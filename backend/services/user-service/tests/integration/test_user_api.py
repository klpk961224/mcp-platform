# -*- coding: utf-8 -*-
"""
User API闆嗘垚娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建鐢ㄦ埛API
2. 鑾峰彇鐢ㄦ埛鍒楄〃API
3. 鑾峰彇鐢ㄦ埛璇︽儏API
4. 更新鐢ㄦ埛API
5. 删除鐢ㄦ埛API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


@pytest.fixture
def client():
    """创建娴嬭瘯瀹㈡埛绔?""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_user():
    """妯℃嫙鐢ㄦ埛鏁版嵁"""
    return {
        "id": "test_user_id",
        "tenant_id": "default",
        "username": "testuser",
        "email": "test@example.com",
        "phone": "132800138000",
        "dept_id": None,
        "position_id": None,
        "status": "active",
        "created_at": "2026-01-15T00:00:00",
        "updated_at": "2026-01-15T00:00:00"
    }


class TestUserAPI:
    """User API娴嬭瘯绫?""
    
    def test_create_user_success(self, client, mock_user):
        """娴嬭瘯创建鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_user_obj.id = "test_user_id"
            mock_user_obj.username = "testuser"
            mock_user_obj.email = "test@example.com"
            mock_user_obj.phone = "132800138000"
            mock_user_obj.department_id = None
            mock_user_obj.status = "active"
            mock_user_obj.created_at = Mock()
            mock_user_obj.updated_at = Mock()
            mock_user_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_user_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.create_user.return_value = mock_user_obj
            MockUserService.return_value = mock_service
            
            # 鍙戦€佸垱寤虹敤鎴疯姹?            response = client.post("/api/v1/users", json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "tenant_id": "default"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "testuser"
            assert data["email"] == "test@example.com"
    
    def test_create_user_username_exists(self, client):
        """娴嬭瘯创建鐢ㄦ埛澶辫触锛堢敤鎴峰悕宸插瓨鍦級"""
        # 妯℃嫙UserService鎶涘嚭寮傚父
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.create_user.side_effect = ValueError("用户名嶅凡瀛樺湪")
            MockUserService.return_value = mock_service
            
            # 鍙戦€佸垱寤虹敤鎴疯姹?            response = client.post("/api/v1/users", json={
                "username": "existing_user",
                "email": "test@example.com",
                "password": "password123",
                "tenant_id": "default"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
    
    def test_get_users_success(self, client, mock_user):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鍒楄〃鎴愬姛"""
        # 妯℃嫙UserService
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
            
            # 鍙戦€佽幏鍙栫敤鎴峰垪琛ㄨ姹?            response = client.get("/api/v1/users?page=1&page_size=10")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert len(data["items"]) == 1
            assert data["items"][0]["username"] == "testuser"
    
    def test_get_users_with_filters(self, client):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鍒楄〃锛堝甫绛涢€夋潯浠讹級"""
        # 妯℃嫙UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.search_users.return_value = ([], 0)
            MockUserService.return_value = mock_service
            
            # 鍙戦€佽幏鍙栫敤鎴峰垪琛ㄨ姹傦紙甯︾瓫閫夋潯浠讹級
            response = client.get("/api/v1/users?page=1&page_size=10&tenant_id=default&status=active&keyword=test")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["items"]) == 0
    
    def test_get_user_success(self, client, mock_user):
        """娴嬭瘯鑾峰彇鐢ㄦ埛璇︽儏鎴愬姛"""
        # 妯℃嫙UserService
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
            
            # 鍙戦€佽幏鍙栫敤鎴疯鎯呰姹?            response = client.get("/api/v1/users/test_user_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_user_id"
            assert data["username"] == "testuser"
    
    def test_get_user_not_found(self, client):
        """娴嬭瘯鑾峰彇鐢ㄦ埛璇︽儏澶辫触锛堢敤鎴蜂笉瀛樺湪锛?""
        # 妯℃嫙UserService杩斿洖None
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockUserService.return_value = mock_service
            
            # 鍙戦€佽幏鍙栫敤鎴疯鎯呰姹?            response = client.get("/api/v1/users/nonexistent_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_update_user_success(self, client):
        """娴嬭瘯更新鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙UserService
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
            
            # 鍙戦€佹洿鏂扮敤鎴疯姹?            response = client.put("/api/v1/users/test_user_id", json={
                "email": "newemail@example.com"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "newemail@example.com"
    
    def test_update_user_not_found(self, client):
        """娴嬭瘯更新鐢ㄦ埛澶辫触锛堢敤鎴蜂笉瀛樺湪锛?""
        # 妯℃嫙UserService杩斿洖None
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockUserService.return_value = mock_service
            
            # 鍙戦€佹洿鏂扮敤鎴疯姹?            response = client.put("/api/v1/users/nonexistent_id", json={
                "email": "newemail@example.com"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_delete_user_success(self, client):
        """娴嬭瘯删除鐢ㄦ埛鎴愬姛"""
        # 妯℃嫙UserService
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_user_obj = Mock()
            mock_service.get_by_id.return_value = mock_user_obj
            mock_service.delete_user = Mock()
            MockUserService.return_value = mock_service
            
            # 鍙戦€佸垹闄ょ敤鎴疯姹?            response = client.delete("/api/v1/users/test_user_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "删除鎴愬姛"
    
    def test_delete_user_not_found(self, client):
        """娴嬭瘯删除鐢ㄦ埛澶辫触锛堢敤鎴蜂笉瀛樺湪锛?""
        # 妯℃嫙UserService杩斿洖None
        with patch('app.api.v1.users.UserService') as MockUserService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockUserService.return_value = mock_service
            
            # 鍙戦€佸垹闄ょ敤鎴疯姹?            response = client.delete("/api/v1/users/nonexistent_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_create_user_missing_username(self, client):
        """娴嬭瘯创建鐢ㄦ埛澶辫触锛堢己灏戠敤鎴峰悕锛?""
        # 鍙戦€佸垱寤虹敤鎴疯姹傦紙缂哄皯用户名嶏級
        response = client.post("/api/v1/users", json={
            "email": "test@example.com",
            "password": "password123",
            "tenant_id": "default"
        })
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
    
    def test_create_user_missing_email(self, client):
        """娴嬭瘯创建鐢ㄦ埛澶辫触锛堢己灏戦偖绠憋級"""
        # 鍙戦€佸垱寤虹敤鎴疯姹傦紙缂哄皯邮箱锛?        response = client.post("/api/v1/users", json={
            "username": "testuser",
            "password": "password123",
            "tenant_id": "default"
        })
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
