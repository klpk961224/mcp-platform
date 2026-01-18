# -*- coding: utf-8 -*-
"""
服务健康检查测试

测试所有后端服务的健康检查接口
"""

import requests
import time
from typing import Dict, Any


class TestHealthCheck:
    """服务健康检查测试"""
    
    def __init__(self):
        self.services = {
            "auth": "http://localhost:228001/health",
            "user": "http://localhost:228002/health",
            "permission": "http://localhost:228003/health",
            "system": "http://localhost:228004/health",
            "support": "http://localhost:228005/health",
            "business": "http://localhost:228006/health"
        }
        self.session = requests.Session()
    
    def test_service_health(self, service_name: str, url: str) -> bool:
        """测试单个服务的健康检查"""
        print(f"测试 {service_name} 服务健康检查...")
        
        max_retries = 30
        for i in range(max_retries):
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✓ {service_name} 服务健康检查通过")
                    return True
            except Exception as e:
                if i < max_retries - 1:
                    print(f"⚠ {service_name} 服务未就绪，重试中... ({i+1}/{max_retries})")
                    time.sleep(1)
        
        print(f"✗ {service_name} 服务健康检查失败")
        return False
    
    def run_all_health_checks(self) -> Dict[str, Any]:
        """运行所有服务的健康检查"""
        print("=" * 60)
        print("开始所有服务健康检查")
        print("=" * 60)
        print()
        
        results = {
            "total": len(self.services),
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for service_name, url in self.services.items():
            if self.test_service_health(service_name, url):
                results["passed"] += 1
                results["details"].append({
                    "service": service_name,
                    "status": "passed"
                })
            else:
                results["failed"] += 1
                results["details"].append({
                    "service": service_name,
                    "status": "failed"
                })
        
        print()
        print("=" * 60)
        print("所有服务健康检查完成")
        print(f"总服务数: {results['total']}")
        print(f"通过数: {results['passed']}")
        print(f"失败数: {results['failed']}")
        print(f"通过率: {(results['passed'] / results['total'] * 100):.2f}%")
        print("=" * 60)
        
        return results


if __name__ == "__main__":
    tester = TestHealthCheck()
    results = tester.run_all_health_checks()
    
    # 如果有服务未通过健康检查，返回非零退出码
    if results["failed"] > 0:
        print(f"\n⚠ 有 {results['failed']} 个服务未通过健康检查")
        exit(1)
    
    print("\n✓ 所有服务健康检查通过")
    exit(0)