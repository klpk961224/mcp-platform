# -*- coding: utf-8 -*-
"""
运行后端集成测试

功能说明：
1. 测试所有服务的健康检查
2. 测试服务间的基本交互
3. 生成测试报告

使用方法：
    python run_integration_tests.py
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
from loguru import logger


class IntegrationTester:
    """集成测试器"""
    
    def __init__(self):
        self.services = {
            "auth": "http://localhost:28001",
            "user": "http://localhost:28002",
            "permission": "http://localhost:28003",
            "system": "http://localhost:28004",
            "support": "http://localhost:28005",
            "business": "http://localhost:28006"
        }
        self.results = []
        self.session = requests.Session()
    
    def test_health_check(self, service_name: str) -> bool:
        """测试健康检查"""
        url = f"{self.services[service_name]}/health"
        logger.info(f"测试健康检查: {service_name} - {url}")
        
        try:
            response = self.session.get(url, timeout=5)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": f"健康检查-{service_name}",
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
                logger.success(f"✓ {service_name} 健康检查通过")
            else:
                logger.error(f"✗ {service_name} 健康检查失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ {service_name} 健康检查异常: {str(e)}")
            self.results.append({
                "test_case": f"健康检查-{service_name}",
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
        """测试认证服务登录"""
        url = f"{self.services['auth']}/api/v1/auth/login"
        logger.info(f"测试认证服务登录: {url}")
        
        try:
            response = self.session.post(
                url,
                json={
                    "username": "admin",
                    "password": "123456"
                },
                timeout=10
            )
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "认证服务-用户登录",
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
                logger.success(f"✓ 认证服务登录通过")
                result = response.json()
                if result.get("code") == 0:
                    # 保存token用于后续测试
                    access_token = result.get("data", {}).get("access_token")
                    if access_token:
                        self.session.headers.update({
                            "Authorization": f"Bearer {access_token}"
                        })
                        logger.info("已保存access_token")
            else:
                logger.error(f"✗ 认证服务登录失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 认证服务登录异常: {str(e)}")
            self.results.append({
                "test_case": "认证服务-用户登录",
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
        """测试用户服务获取用户列表"""
        url = f"{self.services['user']}/api/v1/users"
        logger.info(f"测试用户服务获取用户列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "用户服务-获取用户列表",
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
                logger.success(f"✓ 用户服务获取用户列表通过")
            else:
                logger.error(f"✗ 用户服务获取用户列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 用户服务获取用户列表异常: {str(e)}")
            self.results.append({
                "test_case": "用户服务-获取用户列表",
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
        """测试权限服务获取角色列表"""
        url = f"{self.services['permission']}/api/v1/roles"
        logger.info(f"测试权限服务获取角色列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "权限服务-获取角色列表",
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
                logger.success(f"✓ 权限服务获取角色列表通过")
            else:
                logger.error(f"✗ 权限服务获取角色列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 权限服务获取角色列表异常: {str(e)}")
            self.results.append({
                "test_case": "权限服务-获取角色列表",
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
        """测试认证服务用户注册"""
        url = f"{self.services['auth']}/api/v1/auth/register"
        logger.info(f"测试认证服务用户注册: {url}")
        
        import time
        username = f"testuser_{int(time.time())}"
        
        try:
            response = self.session.post(
                url,
                json={
                    "username": username,
                    "password": "Test@123456",
                    "email": f"{username}@example.com",
                    "phone": "13800138000"
                },
                timeout=10
            )
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "认证服务-用户注册",
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
                logger.success(f"✓ 认证服务用户注册通过")
            else:
                logger.error(f"✗ 认证服务用户注册失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 认证服务用户注册异常: {str(e)}")
            self.results.append({
                "test_case": "认证服务-用户注册",
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
        """测试认证服务刷新Token"""
        url = f"{self.services['auth']}/api/v1/auth/refresh"
        logger.info(f"测试认证服务刷新Token: {url}")
        
        try:
            # 先登录获取refresh_token
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
                logger.error(f"✗ 认证服务刷新Token失败：登录失败")
                return False
            
            refresh_token = login_response.json().get("refresh_token")
            if not refresh_token:
                logger.error(f"✗ 认证服务刷新Token失败：未获取到refresh_token")
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
                "test_case": "认证服务-刷新Token",
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
                logger.success(f"✓ 认证服务刷新Token通过")
            else:
                logger.error(f"✗ 认证服务刷新Token失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 认证服务刷新Token异常: {str(e)}")
            self.results.append({
                "test_case": "认证服务-刷新Token",
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
        """测试认证服务登出"""
        url = f"{self.services['auth']}/api/v1/auth/logout"
        logger.info(f"测试认证服务登出: {url}")
        
        try:
            response = self.session.post(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "认证服务-用户登出",
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
                logger.success(f"✓ 认证服务登出通过")
            else:
                logger.error(f"✗ 认证服务登出失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 认证服务登出异常: {str(e)}")
            self.results.append({
                "test_case": "认证服务-用户登出",
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
        """测试用户服务获取部门列表"""
        url = f"{self.services['user']}/api/v1/departments"
        logger.info(f"测试用户服务获取部门列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "用户服务-获取部门列表",
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
                logger.success(f"✓ 用户服务获取部门列表通过")
            else:
                logger.error(f"✗ 用户服务获取部门列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 用户服务获取部门列表异常: {str(e)}")
            self.results.append({
                "test_case": "用户服务-获取部门列表",
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
        """测试用户服务获取租户列表"""
        url = f"{self.services['user']}/api/v1/tenants"
        logger.info(f"测试用户服务获取租户列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "用户服务-获取租户列表",
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
                logger.success(f"✓ 用户服务获取租户列表通过")
            else:
                logger.error(f"✗ 用户服务获取租户列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 用户服务获取租户列表异常: {str(e)}")
            self.results.append({
                "test_case": "用户服务-获取租户列表",
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
        """测试权限服务获取权限列表"""
        url = f"{self.services['permission']}/api/v1/permissions"
        logger.info(f"测试权限服务获取权限列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "权限服务-获取权限列表",
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
                logger.success(f"✓ 权限服务获取权限列表通过")
            else:
                logger.error(f"✗ 权限服务获取权限列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 权限服务获取权限列表异常: {str(e)}")
            self.results.append({
                "test_case": "权限服务-获取权限列表",
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
        """测试权限服务获取菜单列表"""
        url = f"{self.services['permission']}/api/v1/menus"
        logger.info(f"测试权限服务获取菜单列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "权限服务-获取菜单列表",
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
                logger.success(f"✓ 权限服务获取菜单列表通过")
            else:
                logger.error(f"✗ 权限服务获取菜单列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 权限服务获取菜单列表异常: {str(e)}")
            self.results.append({
                "test_case": "权限服务-获取菜单列表",
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
        """测试系统服务获取MCP工具列表"""
        url = f"{self.services['system']}/api/v1/mcp-tools"
        logger.info(f"测试系统服务获取MCP工具列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "系统服务-获取MCP工具列表",
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
                logger.success(f"✓ 系统服务获取MCP工具列表通过")
            else:
                logger.error(f"✗ 系统服务获取MCP工具列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 系统服务获取MCP工具列表异常: {str(e)}")
            self.results.append({
                "test_case": "系统服务-获取MCP工具列表",
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
        """测试系统服务获取字典列表"""
        url = f"{self.services['system']}/api/v1/dictionaries"
        logger.info(f"测试系统服务获取字典列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "系统服务-获取字典列表",
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
                logger.success(f"✓ 系统服务获取字典列表通过")
            else:
                logger.error(f"✗ 系统服务获取字典列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 系统服务获取字典列表异常: {str(e)}")
            self.results.append({
                "test_case": "系统服务-获取字典列表",
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
        """测试支撑服务获取登录日志"""
        url = f"{self.services['support']}/api/v1/logs/login"
        logger.info(f"测试支撑服务获取登录日志: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "支撑服务-获取登录日志",
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
                logger.success(f"✓ 支撑服务获取登录日志通过")
            else:
                logger.error(f"✗ 支撑服务获取登录日志失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 支撑服务获取登录日志异常: {str(e)}")
            self.results.append({
                "test_case": "支撑服务-获取登录日志",
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
        """测试支撑服务获取操作日志"""
        url = f"{self.services['support']}/api/v1/logs/operation"
        logger.info(f"测试支撑服务获取操作日志: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "支撑服务-获取操作日志",
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
                logger.success(f"✓ 支撑服务获取操作日志通过")
            else:
                logger.error(f"✗ 支撑服务获取操作日志失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 支撑服务获取操作日志异常: {str(e)}")
            self.results.append({
                "test_case": "支撑服务-获取操作日志",
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
        """测试支撑服务获取待办任务列表"""
        url = f"{self.services['support']}/api/v1/todos"
        logger.info(f"测试支撑服务获取待办任务列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "支撑服务-获取待办任务列表",
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
                logger.success(f"✓ 支撑服务获取待办任务列表通过")
            else:
                logger.error(f"✗ 支撑服务获取待办任务列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 支撑服务获取待办任务列表异常: {str(e)}")
            self.results.append({
                "test_case": "支撑服务-获取待办任务列表",
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
        """测试业务服务获取工作流列表"""
        url = f"{self.services['business']}/api/v1/workflows"
        logger.info(f"测试业务服务获取工作流列表: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            success = response.status_code == 200
            
            self.results.append({
                "test_case": "业务服务-获取工作流列表",
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
                logger.success(f"✓ 业务服务获取工作流列表通过")
            else:
                logger.error(f"✗ 业务服务获取工作流列表失败")
            
            return success
        except Exception as e:
            logger.error(f"✗ 业务服务获取工作流列表异常: {str(e)}")
            self.results.append({
                "test_case": "业务服务-获取工作流列表",
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
        """运行所有测试"""
        logger.info("=" * 60)
        logger.info("开始后端集成测试")
        logger.info(f"测试时间: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # 测试健康检查
        logger.info("\n" + "=" * 50)
        logger.info("第一阶段：健康检查")
        logger.info("=" * 50)
        
        health_results = {
            "auth": self.test_health_check("auth"),
            "user": self.test_health_check("user"),
            "permission": self.test_health_check("permission"),
            "system": self.test_health_check("system"),
            "support": self.test_health_check("support"),
            "business": self.test_health_check("business")
        }
        
        # 测试服务间交互
        logger.info("\n" + "=" * 50)
        logger.info("第二阶段：服务间交互")
        logger.info("=" * 50)
        
        # 认证服务测试
        auth_result = self.test_auth_login()
        self.test_auth_register()
        self.test_auth_refresh_token()
        self.test_auth_logout()
        
        # 重新登录获取token
        self.test_auth_login()
        
        # 用户服务测试
        user_result = self.test_user_list()
        self.test_user_departments()
        self.test_user_tenants()
        
        # 权限服务测试
        permission_result = self.test_permission_roles()
        self.test_permission_permissions()
        self.test_permission_menus()
        
        # 系统服务测试
        self.test_system_mcp_tools()
        self.test_system_dictionaries()
        
        # 支撑服务测试
        self.test_support_login_logs()
        self.test_support_operation_logs()
        self.test_support_todos()
        
        # 业务服务测试
        self.test_business_workflows()
        
        # 汇总结果
        total_tests = len(self.results)
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
        
        # 生成测试报告
        self.generate_report(summary)
        
        logger.info("\n" + "=" * 60)
        logger.info("测试完成")
        logger.info(f"总测试数: {total_tests}")
        logger.info(f"通过数: {total_passed}")
        logger.info(f"失败数: {total_failed}")
        logger.info(f"通过率: {summary['pass_rate']}")
        logger.info("=" * 60)
        
        return summary
    
    def generate_report(self, summary: Dict[str, Any]):
        """生成测试报告"""
        import os
        
        report_dir = os.path.dirname(os.path.abspath(__file__))
        report_path = os.path.join(report_dir, "integration_test_report.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.success(f"测试报告已生成: {report_path}")


def main():
    """主函数"""
    tester = IntegrationTester()
    summary = tester.run_all_tests()
    
    # 返回测试结果
    return summary


if __name__ == "__main__":
    main()