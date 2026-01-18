"""
后端接口自动化测试脚本

功能说明：
1. 自动化测试所有后端接口
2. 生成测试报告
3. 记录测试结果

使用方法：
    python test_backend_apis.py

依赖：
    pip install requests pytest
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class APITester:
    """API测试器"""
    
    def __init__(self):
        self.base_urls = {
            "auth": "http://localhost:8001/api/v1",
            "user": "http://localhost:8002/api/v1",
            "permission": "http://localhost:8003/api/v1"
        }
        self.results = []
        self.session = requests.Session()
    
    def test_health_check(self, service_name: str) -> bool:
        """测试健康检查接口"""
        url = f"http://localhost:{self.get_service_port(service_name)}/health"
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
            
            return success
        except Exception as e:
            logger.error(f"健康检查失败: {service_name} - {str(e)}")
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
    
    def get_service_port(self, service_name: str) -> int:
        """获取服务端口"""
        ports = {
            "auth": 8001,
            "user": 8002,
            "permission": 8003
        }
        return ports.get(service_name, 8000)
    
    def test_api(
        self,
        test_case: str,
        service: str,
        endpoint: str,
        method: str,
        data: Dict[str, Any] = None,
        expected_status: int = 200,
        headers: Dict[str, str] = None
    ) -> bool:
        """
        测试API接口
        
        Args:
            test_case: 测试用例名称
            service: 服务名称
            endpoint: 接口路径
            method: HTTP方法
            data: 请求数据
            expected_status: 预期状态码
            headers: 请求头
        
        Returns:
            bool: 测试是否成功
        """
        url = f"{self.base_urls[service]}{endpoint}"
        logger.info(f"测试API: {test_case} - {method} {url}")
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=10)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=10)
            else:
                logger.error(f"不支持的HTTP方法: {method}")
                return False
            
            success = response.status_code == expected_status
            
            # 尝试解析响应数据
            response_data = None
            try:
                if response.text:
                    response_data = response.json()
            except:
                pass
            
            self.results.append({
                "test_case": test_case,
                "service": service,
                "endpoint": endpoint,
                "url": url,
                "method": method,
                "expected_status": expected_status,
                "actual_status": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "response_body": response.text if not success else None,
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                logger.success(f"✓ {test_case} - 成功 ({response.elapsed.total_seconds():.3f}s)")
            else:
                logger.error(f"✗ {test_case} - 失败 (预期: {expected_status}, 实际: {response.status_code})")
            
            return success
        except Exception as e:
            logger.error(f"✗ {test_case} - 异常: {str(e)}")
            self.results.append({
                "test_case": test_case,
                "service": service,
                "endpoint": endpoint,
                "url": url,
                "method": method,
                "expected_status": expected_status,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_auth_service(self) -> Dict[str, int]:
        """测试认证域服务"""
        logger.info("=" * 50)
        logger.info("开始测试认证域服务")
        logger.info("=" * 50)
        
        results = {"total": 0, "passed": 0, "failed": 0}
        
        # TC-001: 用户登录
        results["total"] += 1
        login_response = None
        if self.test_api(
            test_case="TC-001-用户登录",
            service="auth",
            endpoint="/auth/login",
            method="POST",
            data={
                "username": "admin",
                "password": "123456"
            },
            expected_status=200
        ):
            results["passed"] += 1
            # 获取登录响应，用于后续测试
            if self.results and self.results[-1]["success"]:
                try:
                    login_response = self.results[-1].get("response_data", {})
                except:
                    pass
        else:
            results["failed"] += 1
        
        # TC-002: 刷新Token（使用登录获取的refresh_token）
        results["total"] += 1
        refresh_token = None
        if login_response:
            refresh_token = login_response.get("refresh_token")
        
        if refresh_token:
            if self.test_api(
                test_case="TC-002-刷新Token",
                service="auth",
                endpoint="/auth/refresh",
                method="POST",
                data={
                    "refresh_token": refresh_token
                },
                expected_status=200
            ):
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            logger.warning("TC-002-刷新Token: 跳过测试（无法获取refresh_token）")
            results["failed"] += 1
        
        # TC-003: 用户登出（使用登录获取的refresh_token）
        results["total"] += 1
        if refresh_token:
            if self.test_api(
                test_case="TC-003-用户登出",
                service="auth",
                endpoint="/auth/logout",
                method="POST",
                data={
                    "refresh_token": refresh_token
                },
                expected_status=200
            ):
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            logger.warning("TC-003-用户登出: 跳过测试（无法获取refresh_token）")
            results["failed"] += 1
        
        logger.info(f"认证域服务测试完成: 通过 {results['passed']}/{results['total']}")
        return results
    
    def test_user_service(self) -> Dict[str, int]:
        """测试用户域服务"""
        logger.info("=" * 50)
        logger.info("开始测试用户域服务")
        logger.info("=" * 50)
        
        results = {"total": 0, "passed": 0, "failed": 0}
        
        # TC-004: 创建用户
        results["total"] += 1
        if self.test_api(
            test_case="TC-004-创建用户",
            service="user",
            endpoint="/users",
            method="POST",
            data={
                "username": "testuser",
                "password": "123456",
                "email": "test@example.com",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-005: 获取用户列表
        results["total"] += 1
        if self.test_api(
            test_case="TC-005-获取用户列表",
            service="user",
            endpoint="/users",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-006: 获取用户详情
        results["total"] += 1
        if self.test_api(
            test_case="TC-006-获取用户详情",
            service="user",
            endpoint="/users/123",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-007: 更新用户
        results["total"] += 1
        if self.test_api(
            test_case="TC-007-更新用户",
            service="user",
            endpoint="/users/123",
            method="PUT",
            data={
                "email": "newemail@example.com"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-008: 删除用户
        results["total"] += 1
        if self.test_api(
            test_case="TC-008-删除用户",
            service="user",
            endpoint="/users/123",
            method="DELETE",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-009: 创建部门
        results["total"] += 1
        if self.test_api(
            test_case="TC-009-创建部门",
            service="user",
            endpoint="/departments",
            method="POST",
            data={
                "name": "技术部",
                "code": "tech",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-010: 获取部门列表
        results["total"] += 1
        if self.test_api(
            test_case="TC-010-获取部门列表",
            service="user",
            endpoint="/departments",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-011: 获取部门树
        results["total"] += 1
        if self.test_api(
            test_case="TC-011-获取部门树",
            service="user",
            endpoint="/departments/tree",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-012: 创建租户
        results["total"] += 1
        if self.test_api(
            test_case="TC-012-创建租户",
            service="user",
            endpoint="/tenants",
            method="POST",
            data={
                "name": "测试租户",
                "code": "test_tenant"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        logger.info(f"用户域服务测试完成: 通过 {results['passed']}/{results['total']}")
        return results
    
    def test_permission_service(self) -> Dict[str, int]:
        """测试权限域服务"""
        logger.info("=" * 50)
        logger.info("开始测试权限域服务")
        logger.info("=" * 50)
        
        results = {"total": 0, "passed": 0, "failed": 0}
        
        # TC-013: 创建角色
        results["total"] += 1
        if self.test_api(
            test_case="TC-013-创建角色",
            service="permission",
            endpoint="/roles",
            method="POST",
            data={
                "name": "管理员",
                "code": "admin",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-014: 获取角色列表
        results["total"] += 1
        if self.test_api(
            test_case="TC-014-获取角色列表",
            service="permission",
            endpoint="/roles",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-015: 获取角色详情
        results["total"] += 1
        if self.test_api(
            test_case="TC-015-获取角色详情",
            service="permission",
            endpoint="/roles/123",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-016: 创建权限
        results["total"] += 1
        if self.test_api(
            test_case="TC-016-创建权限",
            service="permission",
            endpoint="/permissions",
            method="POST",
            data={
                "name": "用户创建",
                "code": "user:create",
                "type": "operation"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-017: 获取权限列表
        results["total"] += 1
        if self.test_api(
            test_case="TC-017-获取权限列表",
            service="permission",
            endpoint="/permissions",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-018: 创建菜单
        results["total"] += 1
        if self.test_api(
            test_case="TC-018-创建菜单",
            service="permission",
            endpoint="/menus",
            method="POST",
            data={
                "name": "系统管理",
                "path": "/system",
                "icon": "setting",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-019: 获取菜单列表
        results["total"] += 1
        if self.test_api(
            test_case="TC-019-获取菜单列表",
            service="permission",
            endpoint="/menus",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-020: 获取菜单树
        results["total"] += 1
        if self.test_api(
            test_case="TC-020-获取菜单树",
            service="permission",
            endpoint="/menus/tree",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        logger.info(f"权限域服务测试完成: 通过 {results['passed']}/{results['total']}")
        return results
    
    def test_all_services(self) -> Dict[str, Any]:
        """测试所有服务"""
        logger.info("=" * 60)
        logger.info("开始后端接口自动化测试")
        logger.info(f"测试时间: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # 测试健康检查
        logger.info("\n" + "=" * 50)
        logger.info("第一阶段：健康检查")
        logger.info("=" * 50)
        
        health_results = {
            "auth": self.test_health_check("auth"),
            "user": self.test_health_check("user"),
            "permission": self.test_health_check("permission")
        }
        
        # 测试认证域服务
        auth_results = self.test_auth_service()
        
        # 测试用户域服务
        user_results = self.test_user_service()
        
        # 测试权限域服务
        permission_results = self.test_permission_service()
        
        # 汇总结果
        total_tests = (
            sum([r["total"] for r in [auth_results, user_results, permission_results]]) +
            len(health_results)
        )
        total_passed = (
            sum([r["passed"] for r in [auth_results, user_results, permission_results]]) +
            sum([1 for v in health_results.values() if v])
        )
        total_failed = total_tests - total_passed
        
        summary = {
            "test_time": datetime.now().isoformat(),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "pass_rate": f"{(total_passed / total_tests * 100):.2f}%" if total_tests > 0 else "0%",
            "health_checks": health_results,
            "auth_service": auth_results,
            "user_service": user_results,
            "permission_service": permission_results,
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
        report_path = os.path.join(os.path.dirname(__file__), "测试报告.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.success(f"测试报告已生成: {report_path}")


def main():
    """主函数"""
    tester = APITester()
    summary = tester.test_all_services()
    
    return summary


if __name__ == "__main__":
    main()