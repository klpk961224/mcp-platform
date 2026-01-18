# -*- coding: utf-8 -*-
"""
认证服务集成测试

测试认证服务与其他服务的交互:
1. 用户注册流程（数据库操作）
2. 用户登录流程（JWT生成）
3. Token刷新流程（Token管理）
4. API Key认证（API Key验证）
"""

import pytest
import requests
import time
from typing import Dict, Any
from datetime import datetime


class TestAuthIntegration:
    """认证服务集成测试"""
    
    def __init__(self):
        self.base_url = "http://localhost:28001/api/v1"
        self.user_service_url = "http://localhost:28002/api/v1"
        self.session = requests.Session()
        self.test_user_id = None
        self.test_tenant_id = None
        self.access_token = None
        self.refresh_token = None
        self.api_key = None
    
    def setup_method(self):
        """测试前准备"""
        print("\n" + "=" * 60)
        print("开始认证服务集成测试")
        print("=" * 60)
        
        # 等待服务启动
        self._wait_for_service()
        
        # 准备测试数据
        self._prepare_test_data()
    
    def teardown_method(self):
        """测试后清理"""
        print("\n" + "=" * 60)
        print("清理测试数据")
        print("=" * 60)
        
        # 清理测试数据
        self._cleanup_test_data()
    
    def _wait_for_service(self, max_retries: int = 30):
        """等待服务启动"""
        print("等待认证服务启动...")
        
        for i in range(max_retries):
            try:
                response = self.session.get(f"http://localhost:28001/health", timeout=2)
                if response.status_code == 200:
                    print("✓ 认证服务已启动")
                    return
            except:
                pass
            
            time.sleep(1)
        
        raise Exception("认证服务启动超时")
    
    def _prepare_test_data(self):
        """准备测试数据"""
        print("准备测试数据...")
        
        # 创建测试租户
        try:
            response = self.session.post(
                f"{self.user_service_url}/tenants",
                json={
                    "name": "测试租户_集成测试",
                    "code": f"test_tenant_{int(time.time())}",
                    "status": 1
                },
                timeout=5
            )
            
            if response.status_code == 200:
                self.test_tenant_id = response.json().get("data", {}).get("id")
                print(f"✓ 创建测试租户: {self.test_tenant_id}")
        except Exception as e:
            print(f"⚠ 创建测试租户失败: {str(e)}")
    
    def _cleanup_test_data(self):
        """清理测试数据"""
        print("清理测试数据...")
        
        # 清理测试用户
        if self.test_user_id:
            try:
                self.session.delete(
                    f"{self.user_service_url}/users/{self.test_user_id}",
                    timeout=5
                )
                print(f"✓ 删除测试用户: {self.test_user_id}")
            except Exception as e:
                print(f"⚠ 删除测试用户失败: {str(e)}")
        
        # 清理测试租户
        if self.test_tenant_id:
            try:
                self.session.delete(
                    f"{self.user_service_url}/tenants/{self.test_tenant_id}",
                    timeout=5
                )
                print(f"✓ 删除测试租户: {self.test_tenant_id}")
            except Exception as e:
                print(f"⚠ 删除测试租户失败: {str(e)}")
    
    def test_01_user_registration(self):
        """测试用户注册流程"""
        print("\n" + "-" * 50)
        print("测试用例 1: 用户注册流程")
        print("-" * 50)
        
        # 准备注册数据
        username = f"testuser_{int(time.time())}"
        email = f"test_{int(time.time())}@example.com"
        
        registration_data = {
            "username": username,
            "password": "Test@123456",
            "email": email,
            "phone": "13800138000",
            "tenant_id": self.test_tenant_id or "default"
        }
        
        print(f"注册数据: {registration_data}")
        
        # 发送注册请求
        response = self.session.post(
            f"{self.base_url}/auth/register",
            json=registration_data,
            timeout=10
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        
        # 验证响应
        assert response.status_code == 200, f"注册失败: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"注册失败: {result}"
        
        data = result.get("data", {})
        assert "user_id" in data, "响应中缺少user_id"
        assert "access_token" in data, "响应中缺少access_token"
        
        # 保存测试数据
        self.test_user_id = data.get("user_id")
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        
        print(f"✓ 用户注册成功")
        print(f"  用户ID: {self.test_user_id}")
        print(f"  Access Token: {self.access_token[:50]}...")
        
        return True
    
    def test_02_user_login(self):
        """测试用户登录流程"""
        print("\n" + "-" * 50)
        print("测试用例 2: 用户登录流程")
        print("-" * 50)
        
        # 准备登录数据
        login_data = {
            "username": "admin",
            "password": "123456"
        }
        
        print(f"登录数据: {login_data}")
        
        # 发送登录请求
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        
        # 验证响应
        assert response.status_code == 200, f"登录失败: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"登录失败: {result}"
        
        data = result.get("data", {})
        assert "access_token" in data, "响应中缺少access_token"
        assert "refresh_token" in data, "响应中缺少refresh_token"
        
        # 保存Token
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        
        print(f"✓ 用户登录成功")
        print(f"  Access Token: {self.access_token[:50]}...")
        print(f"  Refresh Token: {self.refresh_token[:50]}...")
        
        return True
    
    def test_03_token_refresh(self):
        """测试Token刷新流程"""
        print("\n" + "-" * 50)
        print("测试用例 3: Token刷新流程")
        print("-" * 50)
        
        # 先登录获取Token
        if not self.access_token:
            self.test_02_user_login()
        
        # 准备刷新Token数据
        refresh_data = {
            "refresh_token": self.refresh_token
        }
        
        print(f"刷新Token数据: refresh_token={self.refresh_token[:50]}...")
        
        # 发送刷新Token请求
        response = self.session.post(
            f"{self.base_url}/auth/refresh",
            json=refresh_data,
            timeout=10
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        
        # 验证响应
        assert response.status_code == 200, f"刷新Token失败: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"刷新Token失败: {result}"
        
        data = result.get("data", {})
        assert "access_token" in data, "响应中缺少access_token"
        assert "refresh_token" in data, "响应中缺少refresh_token"
        
        # 验证新Token与旧Token不同
        new_access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token")
        
        assert new_access_token != self.access_token, "新access_token应该与旧token不同"
        assert new_refresh_token != self.refresh_token, "新refresh_token应该与旧token不同"
        
        # 更新Token
        self.access_token = new_access_token
        self.refresh_token = new_refresh_token
        
        print(f"✓ Token刷新成功")
        print(f"  新Access Token: {self.access_token[:50]}...")
        print(f"  新Refresh Token: {self.refresh_token[:50]}...")
        
        return True
    
    def test_04_api_key_authentication(self):
        """测试API Key认证"""
        print("\n" + "-" * 50)
        print("测试用例 4: API Key认证")
        print("-" * 50)
        
        # 先登录获取Token
        if not self.access_token:
            self.test_02_user_login()
        
        # 创建API Key
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        create_api_key_data = {
            "name": "测试API Key",
            "description": "集成测试API Key"
        }
        
        print(f"创建API Key数据: {create_api_key_data}")
        
        # 发送创建API Key请求
        response = self.session.post(
            f"{self.base_url}/auth/api-keys",
            json=create_api_key_data,
            headers=headers,
            timeout=10
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        
        # 验证响应
        assert response.status_code == 200, f"创建API Key失败: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"创建API Key失败: {result}"
        
        data = result.get("data", {})
        assert "api_key" in data, "响应中缺少api_key"
        
        self.api_key = data.get("api_key")
        
        print(f"✓ API Key创建成功")
        print(f"  API Key: {self.api_key[:50]}...")
        
        # 使用API Key进行认证
        api_key_headers = {
            "X-API-Key": self.api_key
        }
        
        # 测试API Key认证
        test_response = self.session.get(
            f"{self.base_url}/auth/me",
            headers=api_key_headers,
            timeout=10
        )
        
        print(f"API Key认证响应状态码: {test_response.status_code}")
        print(f"API Key认证响应内容: {test_response.text[:500]}")
        
        # 验证API Key认证成功
        assert test_response.status_code == 200, f"API Key认证失败: {test_response.text}"
        
        print(f"✓ API Key认证成功")
        
        return True
    
    def test_05_user_logout(self):
        """测试用户登出流程"""
        print("\n" + "-" * 50)
        print("测试用例 5: 用户登出流程")
        print("-" * 50)
        
        # 先登录获取Token
        if not self.access_token:
            self.test_02_user_login()
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        # 发送登出请求
        response = self.session.post(
            f"{self.base_url}/auth/logout",
            headers=headers,
            timeout=10
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        
        # 验证响应
        assert response.status_code == 200, f"登出失败: {response.text}"
        
        result = response.json()
        assert result.get("code") == 0, f"登出失败: {result}"
        
        print(f"✓ 用户登出成功")
        
        # 验证Token已失效
        test_response = self.session.get(
            f"{self.base_url}/auth/me",
            headers=headers,
            timeout=10
        )
        
        print(f"验证Token失效响应状态码: {test_response.status_code}")
        
        # Token应该失效
        assert test_response.status_code != 200, "登出后Token应该失效"
        
        print(f"✓ Token已失效")
        
        return True


def run_all_tests():
    """运行所有测试"""
    tester = TestAuthIntegration()
    
    tests = [
        ("用户注册流程", tester.test_01_user_registration),
        ("用户登录流程", tester.test_02_user_login),
        ("Token刷新流程", tester.test_03_token_refresh),
        ("API Key认证", tester.test_04_api_key_authentication),
        ("用户登出流程", tester.test_05_user_logout),
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
            print(f"✓ {test_name} - 通过")
        except Exception as e:
            results["failed"] += 1
            results["details"].append({
                "test_name": test_name,
                "status": "failed",
                "error": str(e)
            })
            print(f"✗ {test_name} - 失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("认证服务集成测试完成")
    print(f"总测试数: {results['total']}")
    print(f"通过数: {results['passed']}")
    print(f"失败数: {results['failed']}")
    print(f"通过率: {(results['passed'] / results['total'] * 100):.2f}%")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    run_all_tests()
