# -*- coding: utf-8 -*-
"""
鏈嶅姟鍋ュ悍妫€鏌ユ祴璇?
娴嬭瘯鎵€鏈夊悗绔湇鍔＄殑鍋ュ悍妫€鏌ユ帴鍙?"""

import requests
import time
from typing import Dict, Any


class TestHealthCheck:
    """鏈嶅姟鍋ュ悍妫€鏌ユ祴璇?""
    
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
        """娴嬭瘯鍗曚釜鏈嶅姟鐨勫仴搴锋鏌?""
        print(f"娴嬭瘯 {service_name} 鏈嶅姟鍋ュ悍妫€鏌?..")
        
        max_retries = 30
        for i in range(max_retries):
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"鉁?{service_name} 鏈嶅姟鍋ュ悍妫€鏌ラ€氳繃")
                    return True
            except Exception as e:
                if i < max_retries - 1:
                    print(f"鈿?{service_name} 鏈嶅姟鏈氨缁紝閲嶈瘯涓?.. ({i+1}/{max_retries})")
                    time.sleep(1)
        
        print(f"鉁?{service_name} 鏈嶅姟鍋ュ悍妫€鏌ュけ璐?)
        return False
    
    def run_all_health_checks(self) -> Dict[str, Any]:
        """杩愯鎵€鏈夋湇鍔＄殑鍋ュ悍妫€鏌?""
        print("=" * 60)
        print("寮€濮嬫墍鏈夋湇鍔″仴搴锋鏌?)
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
        print("鎵€鏈夋湇鍔″仴搴锋鏌ュ畬鎴?)
        print(f"鎬绘湇鍔℃暟: {results['total']}")
        print(f"閫氳繃鏁? {results['passed']}")
        print(f"澶辫触鏁? {results['failed']}")
        print(f"閫氳繃鐜? {(results['passed'] / results['total'] * 100):.2f}%")
        print("=" * 60)
        
        return results


if __name__ == "__main__":
    tester = TestHealthCheck()
    results = tester.run_all_health_checks()
    
    # 濡傛灉鏈夋湇鍔℃湭閫氳繃鍋ュ悍妫€鏌ワ紝杩斿洖闈為浂閫€鍑虹爜
    if results["failed"] > 0:
        print(f"\n鈿?鏈?{results['failed']} 涓湇鍔℃湭閫氳繃鍋ュ悍妫€鏌?)
        exit(1)
    
    print("\n鉁?鎵€鏈夋湇鍔″仴搴锋鏌ラ€氳繃")
    exit(0)
