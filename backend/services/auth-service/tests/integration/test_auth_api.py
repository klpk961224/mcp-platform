# -*- coding: utf-8 -*-
"""
Auth API闆嗘垚娴嬭瘯

娴嬭瘯鍐呭锛?1. 鐢ㄦ埛鐧诲綍API
2. 鍒锋柊Token API
3. 鐢ㄦ埛鐧诲嚭API
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
def mock_user():
    """妯℃嫙鐢ㄦ埛鏁版嵁"""
    return {
        "id": "test_user_id",
        "username": "testuser",
        "email": "test@example.com",
        "status": "active",
        "tenant_id": "default"
    }


class TestAuthAPI:
    """Auth API娴嬭瘯绫?""
    
    def test_login_success(self, client, mock_user):
        """娴嬭瘯鐧诲綍鎴愬姛"""
        # 妯℃嫙AuthService
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
            
            # 鍙戦€佺櫥褰曡姹?            response = client.post("/api/v1/auth/login", json={
                "username": "testuser",
                "password": "password"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "test_access_token"
            assert data["refresh_token"] == "test_refresh_token"
            assert data["user_info"]["username"] == "testuser"
    
    def test_login_wrong_password(self, client):
        """娴嬭瘯鐧诲綍澶辫触锛堝瘑鐮侀敊璇級"""
        # 妯℃嫙AuthService鎶涘嚭寮傚父
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.login.side_effect = ValueError("鐢ㄦ埛鍚嶆垨瀵嗙爜閿欒")
            MockAuthService.return_value = mock_service
            
            # 鍙戦€佺櫥褰曡姹?            response = client.post("/api/v1/auth/login", json={
                "username": "testuser",
                "password": "wrong_password"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_login_user_disabled(self, client):
        """娴嬭瘯鐧诲綍澶辫触锛堢敤鎴峰凡绂佺敤锛?""
        # 妯℃嫙AuthService鎶涘嚭寮傚父
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.login.side_effect = ValueError("鐢ㄦ埛宸茶绂佺敤")
            MockAuthService.return_value = mock_service
            
            # 鍙戦€佺櫥褰曡姹?            response = client.post("/api/v1/auth/login", json={
                "username": "testuser",
                "password": "password"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_refresh_token_success(self, client):
        """娴嬭瘯鍒锋柊Token鎴愬姛"""
        # 妯℃嫙AuthService
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.refresh_token.return_value = {
                "access_token": "new_access_token",
                "token_type": "bearer",
                "expires_in": 86400
            }
            MockAuthService.return_value = mock_service
            
            # 鍙戦€佸埛鏂癟oken璇锋眰
            response = client.post("/api/v1/auth/refresh", json={
                "refresh_token": "test_refresh_token"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "new_access_token"
    
    def test_refresh_token_invalid(self, client):
        """娴嬭瘯鍒锋柊Token澶辫触锛圱oken鏃犳晥锛?""
        # 妯℃嫙AuthService鎶涘嚭寮傚父
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.refresh_token.side_effect = ValueError("Token鏃犳晥鎴栧凡杩囨湡")
            MockAuthService.return_value = mock_service
            
            # 鍙戦€佸埛鏂癟oken璇锋眰
            response = client.post("/api/v1/auth/refresh", json={
                "refresh_token": "invalid_token"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_logout_success(self, client):
        """娴嬭瘯鐧诲嚭鎴愬姛"""
        # 妯℃嫙AuthService
        with patch('app.api.v1.auth.AuthService') as MockAuthService:
            mock_service = Mock()
            mock_service.logout.return_value = True
            MockAuthService.return_value = mock_service
            
            # 妯℃嫙Token楠岃瘉
            with patch('app.api.v1.auth.verify_token', return_value={"user_id": "test_user_id"}):
                # 鍙戦€佺櫥鍑鸿姹?                response = client.post("/api/v1/auth/logout", json={
                    "refresh_token": "test_refresh_token"
                })
                
                # 楠岃瘉鍝嶅簲
                assert response.status_code == 200
                data = response.json()
                assert data["message"] == "鐧诲嚭鎴愬姛"
    
    def test_logout_invalid_token(self, client):
        """娴嬭瘯鐧诲嚭澶辫触锛圱oken鏃犳晥锛?""
        # 妯℃嫙Token楠岃瘉澶辫触
        with patch('app.api.v1.auth.verify_token', return_value=None):
            # 鍙戦€佺櫥鍑鸿姹?            response = client.post("/api/v1/auth/logout", json={
                "refresh_token": "invalid_token"
            })
            
            # 楠岃瘉鍝嶅簲
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_login_missing_username(self, client):
        """娴嬭瘯鐧诲綍澶辫触锛堢己灏戠敤鎴峰悕锛?""
        # 鍙戦€佺櫥褰曡姹傦紙缂哄皯鐢ㄦ埛鍚嶏級
        response = client.post("/api/v1/auth/login", json={
            "password": "password"
        })
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
    
    def test_login_missing_password(self, client):
        """娴嬭瘯鐧诲綍澶辫触锛堢己灏戝瘑鐮侊級"""
        # 鍙戦€佺櫥褰曡姹傦紙缂哄皯瀵嗙爜锛?        response = client.post("/api/v1/auth/login", json={
            "username": "testuser"
        })
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
    
    def test_refresh_token_missing_token(self, client):
        """娴嬭瘯鍒锋柊Token澶辫触锛堢己灏慣oken锛?""
        # 鍙戦€佸埛鏂癟oken璇锋眰锛堢己灏慣oken锛?        response = client.post("/api/v1/auth/refresh", json={})
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 422  # Validation Error
