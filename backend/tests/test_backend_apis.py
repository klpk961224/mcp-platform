"""
鍚庣鎺ュ彛鑷姩鍖栨祴璇曡剼鏈?
鍔熻兘璇存槑锛?1. 鑷姩鍖栨祴璇曟墍鏈夊悗绔帴鍙?2. 鐢熸垚娴嬭瘯鎶ュ憡
3. 璁板綍娴嬭瘯缁撴灉

浣跨敤鏂规硶锛?    python test_backend_apis.py

渚濊禆锛?    pip install requests pytest
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
from loguru import logger
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class APITester:
    """API娴嬭瘯鍣?""
    
    def __init__(self):
        self.base_urls = {
            "auth": "http://localhost:228001/api/v1",
            "user": "http://localhost:228002/api/v1",
            "permission": "http://localhost:228003/api/v1"
        }
        self.results = []
        self.session = requests.Session()
    
    def test_health_check(self, service_name: str) -> bool:
        """娴嬭瘯鍋ュ悍妫€鏌ユ帴鍙?""
        url = f"http://localhost:{self.get_service_port(service_name)}/health"
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
            
            return success
        except Exception as e:
            logger.error(f"鍋ュ悍妫€鏌ュけ璐? {service_name} - {str(e)}")
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
    
    def get_service_port(self, service_name: str) -> int:
        """鑾峰彇鏈嶅姟绔彛"""
        ports = {
            "auth": 228001,
            "user": 228002,
            "permission": 228003
        }
        return ports.get(service_name, 28000)
    
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
        娴嬭瘯API鎺ュ彛
        
        Args:
            test_case: 娴嬭瘯鐢ㄤ緥名称
            service: 鏈嶅姟名称
            endpoint: 鎺ュ彛璺緞
            method: HTTP鏂规硶
            data: 璇锋眰鏁版嵁
            expected_status: 棰勬湡状态佺爜
            headers: 璇锋眰澶?        
        Returns:
            bool: 娴嬭瘯鏄惁鎴愬姛
        """
        url = f"{self.base_urls[service]}{endpoint}"
        logger.info(f"娴嬭瘯API: {test_case} - {method} {url}")
        
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
                logger.error(f"涓嶆敮鎸佺殑HTTP鏂规硶: {method}")
                return False
            
            success = response.status_code == expected_status
            
            # 灏濊瘯瑙ｆ瀽鍝嶅簲鏁版嵁
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
                logger.success(f"鉁?{test_case} - 鎴愬姛 ({response.elapsed.total_seconds():.3f}s)")
            else:
                logger.error(f"鉁?{test_case} - 澶辫触 (棰勬湡: {expected_status}, 瀹為檯: {response.status_code})")
            
            return success
        except Exception as e:
            logger.error(f"鉁?{test_case} - 寮傚父: {str(e)}")
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
        """娴嬭瘯认证域服务?""
        logger.info("=" * 50)
        logger.info("寮€濮嬫祴璇曡璇佸煙鏈嶅姟")
        logger.info("=" * 50)
        
        results = {"total": 0, "passed": 0, "failed": 0}
        
        # TC-001: 鐢ㄦ埛鐧诲綍
        results["total"] += 1
        login_response = None
        if self.test_api(
            test_case="TC-001-鐢ㄦ埛鐧诲綍",
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
            # 鑾峰彇鐧诲綍鍝嶅簲锛岀敤浜庡悗缁祴璇?            if self.results and self.results[-1]["success"]:
                try:
                    login_response = self.results[-1].get("response_data", {})
                except:
                    pass
        else:
            results["failed"] += 1
        
        # TC-002: 鍒锋柊Token锛堜娇鐢ㄧ櫥褰曡幏鍙栫殑refresh_token锛?        results["total"] += 1
        refresh_token = None
        if login_response:
            refresh_token = login_response.get("refresh_token")
        
        if refresh_token:
            if self.test_api(
                test_case="TC-002-鍒锋柊Token",
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
            logger.warning("TC-002-鍒锋柊Token: 璺宠繃娴嬭瘯锛堟棤娉曡幏鍙杛efresh_token锛?)
            results["failed"] += 1
        
        # TC-003: 鐢ㄦ埛鐧诲嚭锛堜娇鐢ㄧ櫥褰曡幏鍙栫殑refresh_token锛?        results["total"] += 1
        if refresh_token:
            if self.test_api(
                test_case="TC-003-鐢ㄦ埛鐧诲嚭",
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
            logger.warning("TC-003-鐢ㄦ埛鐧诲嚭: 璺宠繃娴嬭瘯锛堟棤娉曡幏鍙杛efresh_token锛?)
            results["failed"] += 1
        
        logger.info(f"认证域服务℃祴璇曞畬鎴? 閫氳繃 {results['passed']}/{results['total']}")
        return results
    
    def test_user_service(self) -> Dict[str, int]:
        """娴嬭瘯用户域服务?""
        logger.info("=" * 50)
        logger.info("寮€濮嬫祴璇曠敤鎴峰煙鏈嶅姟")
        logger.info("=" * 50)
        
        results = {"total": 0, "passed": 0, "failed": 0}
        
        # TC-004: 创建鐢ㄦ埛
        results["total"] += 1
        if self.test_api(
            test_case="TC-004-创建鐢ㄦ埛",
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
        
        # TC-005: 鑾峰彇鐢ㄦ埛鍒楄〃
        results["total"] += 1
        if self.test_api(
            test_case="TC-005-鑾峰彇鐢ㄦ埛鍒楄〃",
            service="user",
            endpoint="/users",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-006: 鑾峰彇鐢ㄦ埛璇︽儏
        results["total"] += 1
        if self.test_api(
            test_case="TC-006-鑾峰彇鐢ㄦ埛璇︽儏",
            service="user",
            endpoint="/users/123",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-007: 更新鐢ㄦ埛
        results["total"] += 1
        if self.test_api(
            test_case="TC-007-更新鐢ㄦ埛",
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
        
        # TC-008: 删除鐢ㄦ埛
        results["total"] += 1
        if self.test_api(
            test_case="TC-008-删除鐢ㄦ埛",
            service="user",
            endpoint="/users/123",
            method="DELETE",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-009: 创建閮ㄩ棬
        results["total"] += 1
        if self.test_api(
            test_case="TC-009-创建閮ㄩ棬",
            service="user",
            endpoint="/departments",
            method="POST",
            data={
                "name": "鎶€鏈儴",
                "code": "tech",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-010: 鑾峰彇閮ㄩ棬鍒楄〃
        results["total"] += 1
        if self.test_api(
            test_case="TC-010-鑾峰彇閮ㄩ棬鍒楄〃",
            service="user",
            endpoint="/departments",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-011: 鑾峰彇閮ㄩ棬鏍?        results["total"] += 1
        if self.test_api(
            test_case="TC-011-鑾峰彇閮ㄩ棬鏍?,
            service="user",
            endpoint="/departments/tree",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-012: 创建绉熸埛
        results["total"] += 1
        if self.test_api(
            test_case="TC-012-创建绉熸埛",
            service="user",
            endpoint="/tenants",
            method="POST",
            data={
                "name": "娴嬭瘯绉熸埛",
                "code": "test_tenant"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        logger.info(f"用户域服务℃祴璇曞畬鎴? 閫氳繃 {results['passed']}/{results['total']}")
        return results
    
    def test_permission_service(self) -> Dict[str, int]:
        """娴嬭瘯权限域服务?""
        logger.info("=" * 50)
        logger.info("寮€濮嬫祴璇曟潈闄愬煙鏈嶅姟")
        logger.info("=" * 50)
        
        results = {"total": 0, "passed": 0, "failed": 0}
        
        # TC-013: 创建瑙掕壊
        results["total"] += 1
        if self.test_api(
            test_case="TC-013-创建瑙掕壊",
            service="permission",
            endpoint="/roles",
            method="POST",
            data={
                "name": "绠＄悊鍛?,
                "code": "admin",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-014: 鑾峰彇瑙掕壊鍒楄〃
        results["total"] += 1
        if self.test_api(
            test_case="TC-014-鑾峰彇瑙掕壊鍒楄〃",
            service="permission",
            endpoint="/roles",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-015: 鑾峰彇瑙掕壊璇︽儏
        results["total"] += 1
        if self.test_api(
            test_case="TC-015-鑾峰彇瑙掕壊璇︽儏",
            service="permission",
            endpoint="/roles/123",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-016: 创建鏉冮檺
        results["total"] += 1
        if self.test_api(
            test_case="TC-016-创建鏉冮檺",
            service="permission",
            endpoint="/permissions",
            method="POST",
            data={
                "name": "鐢ㄦ埛创建",
                "code": "user:create",
                "type": "operation"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-017: 鑾峰彇鏉冮檺鍒楄〃
        results["total"] += 1
        if self.test_api(
            test_case="TC-017-鑾峰彇鏉冮檺鍒楄〃",
            service="permission",
            endpoint="/permissions",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-018: 创建鑿滃崟
        results["total"] += 1
        if self.test_api(
            test_case="TC-018-创建鑿滃崟",
            service="permission",
            endpoint="/menus",
            method="POST",
            data={
                "name": "绯荤粺绠＄悊",
                "path": "/system",
                "icon": "setting",
                "tenant_id": "default"
            },
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-019: 鑾峰彇鑿滃崟鍒楄〃
        results["total"] += 1
        if self.test_api(
            test_case="TC-019-鑾峰彇鑿滃崟鍒楄〃",
            service="permission",
            endpoint="/menus",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # TC-020: 鑾峰彇鑿滃崟鏍?        results["total"] += 1
        if self.test_api(
            test_case="TC-020-鑾峰彇鑿滃崟鏍?,
            service="permission",
            endpoint="/menus/tree",
            method="GET",
            expected_status=200
        ):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        logger.info(f"权限域服务℃祴璇曞畬鎴? 閫氳繃 {results['passed']}/{results['total']}")
        return results
    
    def test_all_services(self) -> Dict[str, Any]:
        """娴嬭瘯鎵€鏈夋湇鍔?""
        logger.info("=" * 60)
        logger.info("寮€濮嬪悗绔帴鍙ｈ嚜鍔ㄥ寲娴嬭瘯")
        logger.info(f"娴嬭瘯鏃堕棿: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # 娴嬭瘯鍋ュ悍妫€鏌?        logger.info("\n" + "=" * 50)
        logger.info("绗竴闃舵锛氬仴搴锋鏌?)
        logger.info("=" * 50)
        
        health_results = {
            "auth": self.test_health_check("auth"),
            "user": self.test_health_check("user"),
            "permission": self.test_health_check("permission")
        }
        
        # 娴嬭瘯认证域服务?        auth_results = self.test_auth_service()
        
        # 娴嬭瘯用户域服务?        user_results = self.test_user_service()
        
        # 娴嬭瘯权限域服务?        permission_results = self.test_permission_service()
        
        # 姹囨€荤粨鏋?        total_tests = (
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
        report_path = os.path.join(os.path.dirname(__file__), "娴嬭瘯鎶ュ憡.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.success(f"娴嬭瘯鎶ュ憡宸茬敓鎴? {report_path}")


def main():
    """涓诲嚱鏁?""
    tester = APITester()
    summary = tester.test_all_services()
    
    return summary


if __name__ == "__main__":
    main()
