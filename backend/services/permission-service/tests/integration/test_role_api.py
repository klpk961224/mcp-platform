# -*- coding: utf-8 -*-
"""
Role API闆嗘垚娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓瑙掕壊API
2. 鑾峰彇瑙掕壊鍒楄〃API
3. 鑾峰彇瑙掕壊璇︽儏API
4. 鏇存柊瑙掕壊API
5. 鍒犻櫎瑙掕壊API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


@pytest.fixture
def client():
    """鍒涘缓娴嬭瘯瀹㈡埛绔?""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_role():
    """妯℃嫙瑙掕壊鏁版嵁"""
    return {
        "id": "test_role_id",
        "tenant_id": "default",
        "name": "娴嬭瘯瑙掕壊",
        "code": "test_role",
        "description": "娴嬭瘯瑙掕壊鎻忚堪",
        "is_system": False,
        "status": "active",
        "created_at": "2026-01-15T00:00:00",
        "updated_at": "2026-01-15T00:00:00"
    }


class TestRoleAPI:
    """Role API娴嬭瘯绫?""
    
    def test_create_role_success(self, client, mock_role):
        """娴嬭瘯鍒涘缓瑙掕壊鎴愬姛"""
        # 妯℃嫙RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "娴嬭瘯瑙掕壊"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "娴嬭瘯瑙掕壊鎻忚堪"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.create_role.return_value = mock_role_obj
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佸垱寤鸿鑹茶姹?            response = client.post("/api/v1/roles", json={
                "name": "娴嬭瘯瑙掕壊",
                "code": "test_role",
                "tenant_id": "default",
                "description": "娴嬭瘯瑙掕壊鎻忚堪"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "娴嬭瘯瑙掕壊"
            assert data["code"] == "test_role"
    
    def test_create_role_code_exists(self, client):
        """娴嬭瘯鍒涘缓瑙掕壊澶辫触锛堣鑹蹭唬鐮佸凡瀛樺湪锛?""
        # 妯℃嫙RoleService鎶涘嚭寮傚父
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.create_role.side_effect = ValueError("瑙掕壊浠ｇ爜宸插瓨鍦?)
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佸垱寤鸿鑹茶姹?            response = client.post("/api/v1/roles", json={
                "name": "娴嬭瘯瑙掕壊",
                "code": "existing_role",
                "tenant_id": "default"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
    
    def test_get_roles_success(self, client, mock_role):
        """娴嬭瘯鑾峰彇瑙掕壊鍒楄〃鎴愬姛"""
        # 妯℃嫙RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "娴嬭瘯瑙掕壊"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "娴嬭瘯瑙掕壊鎻忚堪"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.search_roles.return_value = ([mock_role_obj], 1)
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佽幏鍙栬鑹插垪琛ㄨ姹?            response = client.get("/api/v1/roles?page=1&page_size=10")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert len(data["items"]) == 1
            assert data["items"][0]["name"] == "娴嬭瘯瑙掕壊"
    
    def test_get_roles_with_filters(self, client):
        """娴嬭瘯鑾峰彇瑙掕壊鍒楄〃锛堝甫绛涢€夋潯浠讹級"""
        # 妯℃嫙RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.search_roles.return_value = ([], 0)
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佽幏鍙栬鑹插垪琛ㄨ姹傦紙甯︾瓫閫夋潯浠讹級
            response = client.get("/api/v1/roles?page=1&page_size=10&tenant_id=default&status=active&keyword=娴嬭瘯")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["items"]) == 0
    
    def test_get_role_success(self, client, mock_role):
        """娴嬭瘯鑾峰彇瑙掕壊璇︽儏鎴愬姛"""
        # 妯℃嫙RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "娴嬭瘯瑙掕壊"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "娴嬭瘯瑙掕壊鎻忚堪"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.get_by_id.return_value = mock_role_obj
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佽幏鍙栬鑹茶鎯呰姹?            response = client.get("/api/v1/roles/test_role_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_role_id"
            assert data["name"] == "娴嬭瘯瑙掕壊"
    
    def test_get_role_not_found(self, client):
        """娴嬭瘯鑾峰彇瑙掕壊璇︽儏澶辫触锛堣鑹蹭笉瀛樺湪锛?""
        # 妯℃嫙RoleService杩斿洖None
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佽幏鍙栬鑹茶鎯呰姹?            response = client.get("/api/v1/roles/nonexistent_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_update_role_success(self, client):
        """娴嬭瘯鏇存柊瑙掕壊鎴愬姛"""
        # 妯℃嫙RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "鏇存柊鍚庣殑瑙掕壊"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "鏇存柊鍚庣殑鎻忚堪"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.get_by_id.return_value = mock_role_obj
            mock_service.update_role.return_value = mock_role_obj
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佹洿鏂拌鑹茶姹?            response = client.put("/api/v1/roles/test_role_id", json={
                "name": "鏇存柊鍚庣殑瑙掕壊",
                "description": "鏇存柊鍚庣殑鎻忚堪"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "鏇存柊鍚庣殑瑙掕壊"
    
    def test_update_role_not_found(self, client):
        """娴嬭瘯鏇存柊瑙掕壊澶辫触锛堣鑹蹭笉瀛樺湪锛?""
        # 妯℃嫙RoleService杩斿洖None
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佹洿鏂拌鑹茶姹?            response = client.put("/api/v1/roles/nonexistent_id", json={
                "name": "鏇存柊鍚庣殑瑙掕壊"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_delete_role_success(self, client):
        """娴嬭瘯鍒犻櫎瑙掕壊鎴愬姛"""
        # 妯℃嫙RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_service.get_by_id.return_value = mock_role_obj
            mock_service.delete_role = Mock()
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佸垹闄よ鑹茶姹?            response = client.delete("/api/v1/roles/test_role_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "鍒犻櫎鎴愬姛"
    
    def test_delete_role_not_found(self, client):
        """娴嬭瘯鍒犻櫎瑙掕壊澶辫触锛堣鑹蹭笉瀛樺湪锛?""
        # 妯℃嫙RoleService杩斿洖None
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockRoleService.return_value = mock_service
            
            # 鍙戦€佸垹闄よ鑹茶姹?            response = client.delete("/api/v1/roles/nonexistent_id")
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_create_role_missing_name(self, client):
        """娴嬭瘯鍒涘缓瑙掕壊澶辫触锛堢己灏戣鑹插悕绉帮級"""
        # 鍙戦€佸垱寤鸿鑹茶姹傦紙缂哄皯瑙掕壊鍚嶇О锛?        response = client.post("/api/v1/roles", json={
            "code": "test_role",
            "tenant_id": "default"
        })
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
    
    def test_create_role_missing_code(self, client):
        """娴嬭瘯鍒涘缓瑙掕壊澶辫触锛堢己灏戣鑹蹭唬鐮侊級"""
        # 鍙戦€佸垱寤鸿鑹茶姹傦紙缂哄皯瑙掕壊浠ｇ爜锛?        response = client.post("/api/v1/roles", json={
            "name": "娴嬭瘯瑙掕壊",
            "tenant_id": "default"
        })
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
