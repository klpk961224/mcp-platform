# -*- coding: utf-8 -*-
"""
璁よ瘉鏈嶅姟闆嗘垚娴嬭瘯

娴嬭瘯璁よ瘉鏈嶅姟涓庡叾浠栨湇鍔＄殑浜や簰:
1. 鐢ㄦ埛娉ㄥ唽娴佺▼锛堟暟鎹簱鎿嶄綔锛?2. 鐢ㄦ埛鐧诲綍娴佺▼锛圝WT鐢熸垚锛?3. Token鍒锋柊娴佺▼锛圱oken绠＄悊锛?4. API Key璁よ瘉锛圓PI Key楠岃瘉锛?"""

import pytest
import requests
import time
from typing import Dict, Any
from datetime import datetime


class TestAuthIntegration:
    """璁よ瘉鏈嶅姟闆嗘垚娴嬭瘯"""
    
    def __init__(self):
        self.base_url = "http://localhost:228001/api/v1"
        self.user_service_url = "http://localhost:228002/api/v1"
        self.session = requests.Session()
        self.test_user_id = None
        self.test_tenant_id = None
        self.access_token = None
        self.refresh_token = None
        self.api_key = None
    
    def setup_method(self):
        """娴嬭瘯鍓嶅噯澶?""
        print("\n" + "=" * 60)
        print("寮€濮嬭璇佹湇鍔￠泦鎴愭祴璇?)
        print("=" * 60)
        
        # 绛夊緟鏈嶅姟鍚姩
        self._wait_for_service()
        
        # 鍑嗗娴嬭瘯鏁版嵁
        self._prepare_test_data()
    
    def teardown_method(self):
        """娴嬭瘯鍚庢竻鐞?""
        print("\n" + "=" * 60)
        print("娓呯悊娴嬭瘯鏁版嵁")
        print("=" * 60)
        
        # 娓呯悊娴嬭瘯鏁版嵁
        self._cleanup_test_data()
    
    def _wait_for_service(self, max_retries: int = 30):
        """绛夊緟鏈嶅姟鍚姩"""
        print("绛夊緟璁よ瘉鏈嶅姟鍚姩...")
        
        for i in range(max_retries):
            try:
                response = self.session.get(f"http://localhost:228001/health", timeout=2)
                if response.status_code == 200:
                    print("鉁?璁よ瘉鏈嶅姟宸插惎鍔?)
                    return
            except:
                pass
            
            time.sleep(1)
        
        raise Exception("璁よ瘉鏈嶅姟鍚姩瓒呮椂")
    
    def _prepare_test_data(self):
        """鍑嗗娴嬭瘯鏁版嵁"""
        print("鍑嗗娴嬭瘯鏁版嵁...")
        
        # 鍒涘缓娴嬭瘯绉熸埛
        try:
            response = self.session.post(
                f"{self.user_service_url}/tenants",
                json={
                    "name": "娴嬭瘯绉熸埛_闆嗘垚娴嬭瘯",
                    "code": f"test_tenant_{int(time.time())}",
                    "status": 1
                },
                timeout=5
            )
            
            if response.status_code == 200:
                self.test_tenant_id = response.json().get("data", {}).get("id")
                print(f"鉁?鍒涘缓娴嬭瘯绉熸埛: {self.test_tenant_id}")
        except Exception as e:
            print(f"鈿?鍒涘缓娴嬭瘯绉熸埛澶辫触: {str(e)}")
    
    def _cleanup_test_data(self):
        """娓呯悊娴嬭瘯鏁版嵁"""
        print("娓呯悊娴嬭瘯鏁版嵁...")
        
        # 娓呯悊娴嬭瘯鐢ㄦ埛
        if self.test_user_id:
            try:
                self.session.delete(
                    f"{self.user_service_url}/users/{self.test_user_id}",
                    timeout=5
                )
                print(f"鉁?鍒犻櫎娴嬭瘯鐢ㄦ埛: {self.test_user_id}")
            except Exception as e:
                print(f"鈿?鍒犻櫎娴嬭瘯鐢ㄦ埛澶辫触: {str(e)}")
        
        # 娓呯悊娴嬭瘯绉熸埛
        if self.test_tenant_id:
            try:
                self.session.delete(
                    f"{self.user_service_url}/tenants/{self.test_tenant_id}",
                    timeout=5
                )
                print(f"鉁?鍒犻櫎娴嬭瘯绉熸埛: {self.test_tenant_id}")
            except Exception as e:
                print(f"鈿?鍒犻櫎娴嬭瘯绉熸埛澶辫触: {str(e)}")
    
    def test_01_user_registration(self):
        """娴嬭瘯鐢ㄦ埛娉ㄥ唽娴佺▼"""
        print("\n" + "-" * 50)
        print("娴嬭瘯鐢ㄤ緥 1: 鐢ㄦ埛娉ㄥ唽娴佺▼")
        print("-" * 50)
        
        # 鍑嗗娉ㄥ唽鏁版嵁
        username = f"testuser_{int(time.time())}"
        email = f"test_{int(time.time())}@example.com"
        
        registration_data = {
            "username": username,
            "password": "Test@123456",
            "email": email,
            "phone": "132800138000",
            "tenant_id": self.test_tenant_id or "default"
        }
        
        print(f"娉ㄥ唽鏁版嵁: {registration_data}")
        
        # 鍙戦€佹敞鍐岃姹?        response = self.session.post(
            f"{self.base_url}/auth/register",
            json=registration_data,
            timeout=10
        )
        
        print(f"鍝嶅簲鐘舵€佺爜: {response.status_code}")
        print(f"鍝嶅簲鍐呭: {response.text[:500]}")
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 200, f"娉ㄥ唽澶辫触: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"娉ㄥ唽澶辫触: {result}"
        
        data = result.get("data", {})
        assert "user_id" in data, "鍝嶅簲涓己灏憉ser_id"
        assert "access_token" in data, "鍝嶅簲涓己灏慳ccess_token"
        
        # 淇濆瓨娴嬭瘯鏁版嵁
        self.test_user_id = data.get("user_id")
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        
        print(f"鉁?鐢ㄦ埛娉ㄥ唽鎴愬姛")
        print(f"  鐢ㄦ埛ID: {self.test_user_id}")
        print(f"  Access Token: {self.access_token[:50]}...")
        
        return True
    
    def test_02_user_login(self):
        """娴嬭瘯鐢ㄦ埛鐧诲綍娴佺▼"""
        print("\n" + "-" * 50)
        print("娴嬭瘯鐢ㄤ緥 2: 鐢ㄦ埛鐧诲綍娴佺▼")
        print("-" * 50)
        
        # 鍑嗗鐧诲綍鏁版嵁
        login_data = {
            "username": "admin",
            "password": "123456"
        }
        
        print(f"鐧诲綍鏁版嵁: {login_data}")
        
        # 鍙戦€佺櫥褰曡姹?        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"鍝嶅簲鐘舵€佺爜: {response.status_code}")
        print(f"鍝嶅簲鍐呭: {response.text[:500]}")
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 200, f"鐧诲綍澶辫触: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"鐧诲綍澶辫触: {result}"
        
        data = result.get("data", {})
        assert "access_token" in data, "鍝嶅簲涓己灏慳ccess_token"
        assert "refresh_token" in data, "鍝嶅簲涓己灏憆efresh_token"
        
        # 淇濆瓨Token
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        
        print(f"鉁?鐢ㄦ埛鐧诲綍鎴愬姛")
        print(f"  Access Token: {self.access_token[:50]}...")
        print(f"  Refresh Token: {self.refresh_token[:50]}...")
        
        return True
    
    def test_03_token_refresh(self):
        """娴嬭瘯Token鍒锋柊娴佺▼"""
        print("\n" + "-" * 50)
        print("娴嬭瘯鐢ㄤ緥 3: Token鍒锋柊娴佺▼")
        print("-" * 50)
        
        # 鍏堢櫥褰曡幏鍙朤oken
        if not self.access_token:
            self.test_02_user_login()
        
        # 鍑嗗鍒锋柊Token鏁版嵁
        refresh_data = {
            "refresh_token": self.refresh_token
        }
        
        print(f"鍒锋柊Token鏁版嵁: refresh_token={self.refresh_token[:50]}...")
        
        # 鍙戦€佸埛鏂癟oken璇锋眰
        response = self.session.post(
            f"{self.base_url}/auth/refresh",
            json=refresh_data,
            timeout=10
        )
        
        print(f"鍝嶅簲鐘舵€佺爜: {response.status_code}")
        print(f"鍝嶅簲鍐呭: {response.text[:500]}")
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 200, f"鍒锋柊Token澶辫触: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"鍒锋柊Token澶辫触: {result}"
        
        data = result.get("data", {})
        assert "access_token" in data, "鍝嶅簲涓己灏慳ccess_token"
        assert "refresh_token" in data, "鍝嶅簲涓己灏憆efresh_token"
        
        # 楠岃瘉鏂癟oken涓庢棫Token涓嶅悓
        new_access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token")
        
        assert new_access_token != self.access_token, "鏂癮ccess_token搴旇涓庢棫token涓嶅悓"
        assert new_refresh_token != self.refresh_token, "鏂皉efresh_token搴旇涓庢棫token涓嶅悓"
        
        # 鏇存柊Token
        self.access_token = new_access_token
        self.refresh_token = new_refresh_token
        
        print(f"鉁?Token鍒锋柊鎴愬姛")
        print(f"  鏂癆ccess Token: {self.access_token[:50]}...")
        print(f"  鏂癛efresh Token: {self.refresh_token[:50]}...")
        
        return True
    
    def test_04_api_key_authentication(self):
        """娴嬭瘯API Key璁よ瘉"""
        print("\n" + "-" * 50)
        print("娴嬭瘯鐢ㄤ緥 4: API Key璁よ瘉")
        print("-" * 50)
        
        # 鍏堢櫥褰曡幏鍙朤oken
        if not self.access_token:
            self.test_02_user_login()
        
        # 鍒涘缓API Key
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        create_api_key_data = {
            "name": "娴嬭瘯API Key",
            "description": "闆嗘垚娴嬭瘯API Key"
        }
        
        print(f"鍒涘缓API Key鏁版嵁: {create_api_key_data}")
        
        # 鍙戦€佸垱寤篈PI Key璇锋眰
        response = self.session.post(
            f"{self.base_url}/auth/api-keys",
            json=create_api_key_data,
            headers=headers,
            timeout=10
        )
        
        print(f"鍝嶅簲鐘舵€佺爜: {response.status_code}")
        print(f"鍝嶅簲鍐呭: {response.text[:500]}")
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 200, f"鍒涘缓API Key澶辫触: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"鍒涘缓API Key澶辫触: {result}"
        
        data = result.get("data", {})
        assert "api_key" in data, "鍝嶅簲涓己灏慳pi_key"
        
        self.api_key = data.get("api_key")
        
        print(f"鉁?API Key鍒涘缓鎴愬姛")
        print(f"  API Key: {self.api_key[:50]}...")
        
        # 浣跨敤API Key杩涜璁よ瘉
        api_key_headers = {
            "X-API-Key": self.api_key
        }
        
        # 娴嬭瘯API Key璁よ瘉
        test_response = self.session.get(
            f"{self.base_url}/auth/me",
            headers=api_key_headers,
            timeout=10
        )
        
        print(f"API Key璁よ瘉鍝嶅簲鐘舵€佺爜: {test_response.status_code}")
        print(f"API Key璁よ瘉鍝嶅簲鍐呭: {test_response.text[:500]}")
        
        # 楠岃瘉API Key璁よ瘉鎴愬姛
        assert test_response.status_code == 200, f"API Key璁よ瘉澶辫触: {test_response.text}"
        
        print(f"鉁?API Key璁よ瘉鎴愬姛")
        
        return True
    
    def test_05_user_logout(self):
        """娴嬭瘯鐢ㄦ埛鐧诲嚭娴佺▼"""
        print("\n" + "-" * 50)
        print("娴嬭瘯鐢ㄤ緥 5: 鐢ㄦ埛鐧诲嚭娴佺▼")
        print("-" * 50)
        
        # 鍏堢櫥褰曡幏鍙朤oken
        if not self.access_token:
            self.test_02_user_login()
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        # 鍙戦€佺櫥鍑鸿姹?        response = self.session.post(
            f"{self.base_url}/auth/logout",
            headers=headers,
            timeout=10
        )
        
        print(f"鍝嶅簲鐘舵€佺爜: {response.status_code}")
        print(f"鍝嶅簲鍐呭: {response.text[:500]}")
        
        # 楠岃瘉鍝嶅簲
        assert response.status_code == 200, f"鐧诲嚭澶辫触: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"鐧诲嚭澶辫触: {result}"
        
        print(f"鉁?鐢ㄦ埛鐧诲嚭鎴愬姛")
        
        # 楠岃瘉Token宸插け鏁?        test_response = self.session.get(
            f"{self.base_url}/auth/me",
            headers=headers,
            timeout=10
        )
        
        print(f"楠岃瘉Token澶辨晥鍝嶅簲鐘舵€佺爜: {test_response.status_code}")
        
        # Token搴旇澶辨晥
        assert test_response.status_code != 200, "鐧诲嚭鍚嶵oken搴旇澶辨晥"
        
        print(f"鉁?Token宸插け鏁?)
        
        return True


def run_all_tests():
    """杩愯鎵€鏈夋祴璇?""
    tester = TestAuthIntegration()
    
    tests = [
        ("鐢ㄦ埛娉ㄥ唽娴佺▼", tester.test_01_user_registration),
        ("鐢ㄦ埛鐧诲綍娴佺▼", tester.test_02_user_login),
        ("Token鍒锋柊娴佺▼", tester.test_03_token_refresh),
        ("API Key璁よ瘉", tester.test_04_api_key_authentication),
        ("鐢ㄦ埛鐧诲嚭娴佺▼", tester.test_05_user_logout),
    ]
    
    results = {
        "total": len(tests),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for test_name, test_func in tests:
        try:
            test_func()
            results["passed"] += 1
            results["details"].append({
                "test_name": test_name,
                "status": "passed"
            })
            print(f"鉁?{test_name} - 閫氳繃")
        except Exception as e:
            results["failed"] += 1
            results["details"].append({
                "test_name": test_name,
                "status": "failed",
                "error": str(e)
            })
            print(f"鉁?{test_name} - 澶辫触: {str(e)}")
    
    print("\n" + "=" * 60)
    print("璁よ瘉鏈嶅姟闆嗘垚娴嬭瘯瀹屾垚")
    print(f"鎬绘祴璇曟暟: {results['total']}")
    print(f"閫氳繃鏁? {results['passed']}")
    print(f"澶辫触鏁? {results['failed']}")
    print(f"閫氳繃鐜? {(results['passed'] / results['total'] * 100):.2f}%")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    run_all_tests()

