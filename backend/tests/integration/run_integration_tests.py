# -*- coding: utf-8 -*-
"""
杩愯鍚庣闆嗘垚娴嬭瘯

鍔熻兘璇存槑锛?1. 娴嬭瘯鎵€鏈夋湇鍔＄殑鍋ュ悍妫€鏌?2. 娴嬭瘯鏈嶅姟闂寸殑鍩烘湰浜や簰
3. 鐢熸垚娴嬭瘯鎶ュ憡

浣跨敤鏂规硶锛?    python run_integration_tests.py
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
from loguru import logger


class IntegrationTester:
    """闆嗘垚娴嬭瘯鍣?""
    
    def __init__(self):
        self.services = {
            "auth": "http://localhost:228001",
            "user": "http://localhost:228002",
            "permission": "http://localhost:228003",
            "system": "http://localhost:228004",
            "support": "http://localhost:228005",
            "business": "http://localhost:228006"
        }
        self.results = []
        self.session = requests.Session()
    
    def test_health_check(self, service_name: str) -> bool:
        """娴嬭瘯鍋ュ悍妫€鏌?""
        url = f"{self.services[service_name]}/health"
        logger.info(f"娴嬭瘯鍋ュ悍妫€鏌? {service_name} - {url}")
        
        try:
            response = self.session.get(url, timeout=5)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": f"鍋ュ悍妫€鏌?{service_name}",
                "service": service_name,
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?{service_name} 鍋ュ悍妫€鏌ラ€氳繃")
            else:
                logger.error(f"鉁?{service_name} 鍋ュ悍妫€鏌ュけ璐?)
            
            return success
        except Exception as e:
            logger.error(f"鉁?{service_name} 鍋ュ悍妫€鏌ュ紓甯? {str(e)}")
            self.results.append({
                "test_case": f"鍋ュ悍妫€鏌?{service_name}",
                "service": service_name,
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_auth_login(self) -> bool:
        """娴嬭瘯璁よ瘉鏈嶅姟鐧诲綍"""
        url = f"{self.services['auth']}/api/v1/auth/login"
        logger.info(f"娴嬭瘯璁よ瘉鏈嶅姟鐧诲綍: {url}")
        
        try:
            response = self.session.post(
                url,
                json={
                    "username": "admin",
                    "password": "admin123456"
                },
                timeout=10
            )
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鐢ㄦ埛鐧诲綍",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?璁よ瘉鏈嶅姟鐧诲綍閫氳繃")
                result = response.json()
                if result.get("code") == 0:
                    # 保存token鐢ㄤ簬鍚庣画娴嬭瘯
                    access_token = result.get("data", {}).get("access_token")
                    if access_token:
                        self.session.headers.update({
                            "Authorization": f"Bearer {access_token}"
                        })
                        logger.info("宸蹭繚瀛榓ccess_token")
            else:
                logger.error(f"鉁?璁よ瘉鏈嶅姟鐧诲綍澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?璁よ瘉鏈嶅姟鐧诲綍寮傚父: {str(e)}")
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鐢ㄦ埛鐧诲綍",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_user_list(self) -> bool:
        """娴嬭瘯鐢ㄦ埛鏈嶅姟鑾峰彇鐢ㄦ埛鍒楄〃"""
        url = f"{self.services['user']}/api/v1/users"
        logger.info(f"娴嬭瘯鐢ㄦ埛鏈嶅姟鑾峰彇鐢ㄦ埛鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鐢ㄦ埛鏈嶅姟-鑾峰彇鐢ㄦ埛鍒楄〃",
                "service": "user",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇鐢ㄦ埛鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇鐢ㄦ埛鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇鐢ㄦ埛鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鐢ㄦ埛鏈嶅姟-鑾峰彇鐢ㄦ埛鍒楄〃",
                "service": "user",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_permission_roles(self) -> bool:
        """娴嬭瘯鏉冮檺鏈嶅姟鑾峰彇瑙掕壊鍒楄〃"""
        url = f"{self.services['permission']}/api/v1/roles"
        logger.info(f"娴嬭瘯鏉冮檺鏈嶅姟鑾峰彇瑙掕壊鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鏉冮檺鏈嶅姟-鑾峰彇瑙掕壊鍒楄〃",
                "service": "permission",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鏉冮檺鏈嶅姟鑾峰彇瑙掕壊鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鏉冮檺鏈嶅姟鑾峰彇瑙掕壊鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鏉冮檺鏈嶅姟鑾峰彇瑙掕壊鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鏉冮檺鏈嶅姟-鑾峰彇瑙掕壊鍒楄〃",
                "service": "permission",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_auth_register(self) -> bool:
        """娴嬭瘯璁よ瘉鏈嶅姟鐢ㄦ埛娉ㄥ唽"""
        url = f"{self.services['auth']}/api/v1/auth/register"
        logger.info(f"娴嬭瘯璁よ瘉鏈嶅姟鐢ㄦ埛娉ㄥ唽: {url}")
        
        import time
        username = f"testuser_{int(time.time())}"
        
        try:
            response = self.session.post(
                url,
                json={
                    "username": username,
                    "password": "Test@123456",
                    "email": f"{username}@example.com",
                    "phone": "132800138000"
                },
                timeout=10
            )
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鐢ㄦ埛娉ㄥ唽",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?璁よ瘉鏈嶅姟鐢ㄦ埛娉ㄥ唽閫氳繃")
            else:
                logger.error(f"鉁?璁よ瘉鏈嶅姟鐢ㄦ埛娉ㄥ唽澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?璁よ瘉鏈嶅姟鐢ㄦ埛娉ㄥ唽寮傚父: {str(e)}")
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鐢ㄦ埛娉ㄥ唽",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_auth_refresh_token(self) -> bool:
        """娴嬭瘯璁よ瘉鏈嶅姟鍒锋柊Token"""
        url = f"{self.services['auth']}/api/v1/auth/refresh"
        logger.info(f"娴嬭瘯璁よ瘉鏈嶅姟鍒锋柊Token: {url}")
        
        try:
            # 鍏堢櫥褰曡幏鍙杛efresh_token
            login_url = f"{self.services['auth']}/api/v1/auth/login"
            login_response = self.session.post(
                login_url,
                json={
                    "username": "admin",
                    "password": "123456"
                },
                timeout=10
            )
            
            if login_response.status_code != 200:
                logger.error(f"鉁?璁よ瘉鏈嶅姟鍒锋柊Token澶辫触锛氱櫥褰曞け璐?)
                return False
            
            refresh_token = login_response.json().get("refresh_token")
            if not refresh_token:
                logger.error(f"鉁?璁よ瘉鏈嶅姟鍒锋柊Token澶辫触锛氭湭鑾峰彇鍒皉efresh_token")
                return False
            
            response = self.session.post(
                url,
                json={
                    "refresh_token": refresh_token
                },
                timeout=10
            )
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鍒锋柊Token",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?璁よ瘉鏈嶅姟鍒锋柊Token閫氳繃")
            else:
                logger.error(f"鉁?璁よ瘉鏈嶅姟鍒锋柊Token澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?璁よ瘉鏈嶅姟鍒锋柊Token寮傚父: {str(e)}")
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鍒锋柊Token",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_auth_logout(self) -> bool:
        """娴嬭瘯璁よ瘉鏈嶅姟鐧诲嚭"""
        url = f"{self.services['auth']}/api/v1/auth/logout"
        logger.info(f"娴嬭瘯璁よ瘉鏈嶅姟鐧诲嚭: {url}")
        
        try:
            response = self.session.post(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鐢ㄦ埛鐧诲嚭",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?璁よ瘉鏈嶅姟鐧诲嚭閫氳繃")
            else:
                logger.error(f"鉁?璁よ瘉鏈嶅姟鐧诲嚭澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?璁よ瘉鏈嶅姟鐧诲嚭寮傚父: {str(e)}")
            self.results.append({
                "test_case": "璁よ瘉鏈嶅姟-鐢ㄦ埛鐧诲嚭",
                "service": "auth",
                "url": url,
                "method": "POST",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_user_departments(self) -> bool:
        """娴嬭瘯鐢ㄦ埛鏈嶅姟鑾峰彇閮ㄩ棬鍒楄〃"""
        url = f"{self.services['user']}/api/v1/departments"
        logger.info(f"娴嬭瘯鐢ㄦ埛鏈嶅姟鑾峰彇閮ㄩ棬鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鐢ㄦ埛鏈嶅姟-鑾峰彇閮ㄩ棬鍒楄〃",
                "service": "user",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇閮ㄩ棬鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇閮ㄩ棬鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇閮ㄩ棬鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鐢ㄦ埛鏈嶅姟-鑾峰彇閮ㄩ棬鍒楄〃",
                "service": "user",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_user_tenants(self) -> bool:
        """娴嬭瘯鐢ㄦ埛鏈嶅姟鑾峰彇绉熸埛鍒楄〃"""
        url = f"{self.services['user']}/api/v1/tenants"
        logger.info(f"娴嬭瘯鐢ㄦ埛鏈嶅姟鑾峰彇绉熸埛鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鐢ㄦ埛鏈嶅姟-鑾峰彇绉熸埛鍒楄〃",
                "service": "user",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇绉熸埛鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇绉熸埛鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鐢ㄦ埛鏈嶅姟鑾峰彇绉熸埛鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鐢ㄦ埛鏈嶅姟-鑾峰彇绉熸埛鍒楄〃",
                "service": "user",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_permission_permissions(self) -> bool:
        """娴嬭瘯鏉冮檺鏈嶅姟鑾峰彇鏉冮檺鍒楄〃"""
        url = f"{self.services['permission']}/api/v1/permissions"
        logger.info(f"娴嬭瘯鏉冮檺鏈嶅姟鑾峰彇鏉冮檺鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鏉冮檺鏈嶅姟-鑾峰彇鏉冮檺鍒楄〃",
                "service": "permission",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鏉冮檺鏈嶅姟鑾峰彇鏉冮檺鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鏉冮檺鏈嶅姟鑾峰彇鏉冮檺鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鏉冮檺鏈嶅姟鑾峰彇鏉冮檺鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鏉冮檺鏈嶅姟-鑾峰彇鏉冮檺鍒楄〃",
                "service": "permission",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_permission_menus(self) -> bool:
        """娴嬭瘯鏉冮檺鏈嶅姟鑾峰彇鑿滃崟鍒楄〃"""
        url = f"{self.services['permission']}/api/v1/menus"
        logger.info(f"娴嬭瘯鏉冮檺鏈嶅姟鑾峰彇鑿滃崟鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鏉冮檺鏈嶅姟-鑾峰彇鑿滃崟鍒楄〃",
                "service": "permission",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鏉冮檺鏈嶅姟鑾峰彇鑿滃崟鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鏉冮檺鏈嶅姟鑾峰彇鑿滃崟鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鏉冮檺鏈嶅姟鑾峰彇鑿滃崟鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鏉冮檺鏈嶅姟-鑾峰彇鑿滃崟鍒楄〃",
                "service": "permission",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_system_mcp_tools(self) -> bool:
        """娴嬭瘯绯荤粺鏈嶅姟鑾峰彇MCP宸ュ叿鍒楄〃"""
        url = f"{self.services['system']}/api/v1/mcp-tools"
        logger.info(f"娴嬭瘯绯荤粺鏈嶅姟鑾峰彇MCP宸ュ叿鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "绯荤粺鏈嶅姟-鑾峰彇MCP宸ュ叿鍒楄〃",
                "service": "system",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?绯荤粺鏈嶅姟鑾峰彇MCP宸ュ叿鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?绯荤粺鏈嶅姟鑾峰彇MCP宸ュ叿鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?绯荤粺鏈嶅姟鑾峰彇MCP宸ュ叿鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "绯荤粺鏈嶅姟-鑾峰彇MCP宸ュ叿鍒楄〃",
                "service": "system",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_system_dictionaries(self) -> bool:
        """娴嬭瘯绯荤粺鏈嶅姟鑾峰彇瀛楀吀鍒楄〃"""
        url = f"{self.services['system']}/api/v1/dictionaries"
        logger.info(f"娴嬭瘯绯荤粺鏈嶅姟鑾峰彇瀛楀吀鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "绯荤粺鏈嶅姟-鑾峰彇瀛楀吀鍒楄〃",
                "service": "system",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?绯荤粺鏈嶅姟鑾峰彇瀛楀吀鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?绯荤粺鏈嶅姟鑾峰彇瀛楀吀鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?绯荤粺鏈嶅姟鑾峰彇瀛楀吀鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "绯荤粺鏈嶅姟-鑾峰彇瀛楀吀鍒楄〃",
                "service": "system",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_support_login_logs(self) -> bool:
        """娴嬭瘯鏀拺鏈嶅姟鑾峰彇鐧诲綍鏃ュ織"""
        url = f"{self.services['support']}/api/v1/logs/login"
        logger.info(f"娴嬭瘯鏀拺鏈嶅姟鑾峰彇鐧诲綍鏃ュ織: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鏀拺鏈嶅姟-鑾峰彇鐧诲綍鏃ュ織",
                "service": "support",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鏀拺鏈嶅姟鑾峰彇鐧诲綍鏃ュ織閫氳繃")
            else:
                logger.error(f"鉁?鏀拺鏈嶅姟鑾峰彇鐧诲綍鏃ュ織澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鏀拺鏈嶅姟鑾峰彇鐧诲綍鏃ュ織寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鏀拺鏈嶅姟-鑾峰彇鐧诲綍鏃ュ織",
                "service": "support",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_support_operation_logs(self) -> bool:
        """娴嬭瘯鏀拺鏈嶅姟鑾峰彇鎿嶄綔鏃ュ織"""
        url = f"{self.services['support']}/api/v1/logs/operation"
        logger.info(f"娴嬭瘯鏀拺鏈嶅姟鑾峰彇鎿嶄綔鏃ュ織: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鏀拺鏈嶅姟-鑾峰彇鎿嶄綔鏃ュ織",
                "service": "support",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鏀拺鏈嶅姟鑾峰彇鎿嶄綔鏃ュ織閫氳繃")
            else:
                logger.error(f"鉁?鏀拺鏈嶅姟鑾峰彇鎿嶄綔鏃ュ織澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鏀拺鏈嶅姟鑾峰彇鎿嶄綔鏃ュ織寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鏀拺鏈嶅姟-鑾峰彇鎿嶄綔鏃ュ織",
                "service": "support",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_support_todos(self) -> bool:
        """娴嬭瘯鏀拺鏈嶅姟鑾峰彇寰呭姙浠诲姟鍒楄〃"""
        url = f"{self.services['support']}/api/v1/todos"
        logger.info(f"娴嬭瘯鏀拺鏈嶅姟鑾峰彇寰呭姙浠诲姟鍒楄〃: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "鏀拺鏈嶅姟-鑾峰彇寰呭姙浠诲姟鍒楄〃",
                "service": "support",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?鏀拺鏈嶅姟鑾峰彇寰呭姙浠诲姟鍒楄〃閫氳繃")
            else:
                logger.error(f"鉁?鏀拺鏈嶅姟鑾峰彇寰呭姙浠诲姟鍒楄〃澶辫触")
            
            return success
        except Exception as e:
            logger.error(f"鉁?鏀拺鏈嶅姟鑾峰彇寰呭姙浠诲姟鍒楄〃寮傚父: {str(e)}")
            self.results.append({
                "test_case": "鏀拺鏈嶅姟-鑾峰彇寰呭姙浠诲姟鍒楄〃",
                "service": "support",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_business_workflows(self) -> bool:
        """娴嬭瘯涓氬姟鏈嶅姟鑾峰彇宸ヤ綔娴佸垪琛?""
        url = f"{self.services['business']}/api/v1/workflows"
        logger.info(f"娴嬭瘯涓氬姟鏈嶅姟鑾峰彇宸ヤ綔娴佸垪琛? {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "涓氬姟鏈嶅姟-鑾峰彇宸ヤ綔娴佸垪琛?,
                "service": "business",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"鉁?涓氬姟鏈嶅姟鑾峰彇宸ヤ綔娴佸垪琛ㄩ€氳繃")
            else:
                logger.error(f"鉁?涓氬姟鏈嶅姟鑾峰彇宸ヤ綔娴佸垪琛ㄥけ璐?)
            
            return success
        except Exception as e:
            logger.error(f"鉁?涓氬姟鏈嶅姟鑾峰彇宸ヤ綔娴佸垪琛ㄥ紓甯? {str(e)}")
            self.results.append({
                "test_case": "涓氬姟鏈嶅姟-鑾峰彇宸ヤ綔娴佸垪琛?,
                "service": "business",
                "url": url,
                "method": "GET",
                "expected_status": 200,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """杩愯鎵€鏈夋祴璇?""
        logger.info("=" * 60)
        logger.info("寮€濮嬪悗绔泦鎴愭祴璇?)
        logger.info(f"娴嬭瘯鏃堕棿: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # 娴嬭瘯鍋ュ悍妫€鏌?        logger.info("\n" + "=" * 50)
        logger.info("绗竴闃舵锛氬仴搴锋鏌?)
        logger.info("=" * 50)
        
        health_results = {
            "auth": self.test_health_check("auth"),
            "user": self.test_health_check("user"),
            "permission": self.test_health_check("permission"),
            "system": self.test_health_check("system"),
            "support": self.test_health_check("support"),
            "business": self.test_health_check("business")
        }
        
        # 娴嬭瘯鏈嶅姟闂翠氦浜?        logger.info("\n" + "=" * 50)
        logger.info("绗簩闃舵锛氭湇鍔￠棿浜や簰")
        logger.info("=" * 50)
        
        # 璁よ瘉鏈嶅姟娴嬭瘯
        auth_result = self.test_auth_login()
        self.test_auth_register()
        self.test_auth_refresh_token()
        self.test_auth_logout()
        
        # 閲嶆柊鐧诲綍鑾峰彇token
        self.test_auth_login()
        
        # 鐢ㄦ埛鏈嶅姟娴嬭瘯
        user_result = self.test_user_list()
        self.test_user_departments()
        self.test_user_tenants()
        
        # 鏉冮檺鏈嶅姟娴嬭瘯
        permission_result = self.test_permission_roles()
        self.test_permission_permissions()
        self.test_permission_menus()
        
        # 绯荤粺鏈嶅姟娴嬭瘯
        self.test_system_mcp_tools()
        self.test_system_dictionaries()
        
        # 鏀拺鏈嶅姟娴嬭瘯
        self.test_support_login_logs()
        self.test_support_operation_logs()
        self.test_support_todos()
        
        # 涓氬姟鏈嶅姟娴嬭瘯
        self.test_business_workflows()
        
        # 姹囨€荤粨鏋?        total_tests = len(self.results)
        total_passed = sum(1 for r in self.results if r["success"])
        total_failed = total_tests - total_passed
        
        summary = {
            "test_time": datetime.now().isoformat(),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "pass_rate": f"{(total_passed / total_tests * 100):.2f}%" if total_tests > 0 else "0%",
            "health_checks": health_results,
            "test_results": self.results
        }
        
        # 鐢熸垚娴嬭瘯鎶ュ憡
        self.generate_report(summary)
        
        logger.info("\n" + "=" * 60)
        logger.info("娴嬭瘯瀹屾垚")
        logger.info(f"鎬绘祴璇曟暟: {total_tests}")
        logger.info(f"閫氳繃鏁? {total_passed}")
        logger.info(f"澶辫触鏁? {total_failed}")
        logger.info(f"閫氳繃鐜? {summary['pass_rate']}")
        logger.info("=" * 60)
        
        return summary
    
    def generate_report(self, summary: Dict[str, Any]):
        """鐢熸垚娴嬭瘯鎶ュ憡"""
        import os
        
        report_dir = os.path.dirname(os.path.abspath(__file__))
        report_path = os.path.join(report_dir, "integration_test_report.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.success(f"娴嬭瘯鎶ュ憡宸茬敓鎴? {report_path}")


def main():
    """涓诲嚱鏁?""
    tester = IntegrationTester()
    summary = tester.run_all_tests()
    
    # 杩斿洖娴嬭瘯缁撴灉
    return summary


if __name__ == "__main__":
    main()
