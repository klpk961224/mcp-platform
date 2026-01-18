# -*- coding: utf-8 -*-
"""
杩愯鎵€鏈夐泦鎴愭祴璇?
鍔熻兘璇存槑:
1. 杩愯鎵€鏈夋湇鍔＄殑闆嗘垚娴嬭瘯
2. 鐢熸垚娴嬭瘯鎶ュ憡
3. 璁板綍娴嬭瘯缁撴灉

浣跨敤鏂规硶:
    python run_all_integration_tests.py

渚濊禆:
    pip install requests
"""

import sys
import os
import json
from datetime import datetime
from loguru import logger

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 瀵煎叆鍚勪釜鏈嶅姟鐨勯泦鎴愭祴璇?from test_auth_integration import TestAuthIntegration
from test_user_integration import TestUserIntegration
from test_permission_integration import TestPermissionIntegration
from test_system_integration import TestSystemIntegration
from test_support_integration import TestSupportIntegration
from test_business_integration import TestBusinessIntegration


class IntegrationTestRunner:
    """闆嗘垚娴嬭瘯杩愯鍣?""
    
    def __init__(self):
        self.results = {
            "test_time": datetime.now().isoformat(),
            "services": {}
        }
    
    def run_auth_service_tests(self):
        """杩愯璁よ瘉鏈嶅姟闆嗘垚娴嬭瘯"""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛岃璇佹湇鍔￠泦鎴愭祴璇?)
        logger.info("=" * 60)
        
        try:
            tester = TestAuthIntegration()
            results = tester.run_all_tests()
            self.results["services"]["auth"] = results
            return results
        except Exception as e:
            logger.error(f"璁よ瘉鏈嶅姟闆嗘垚娴嬭瘯澶辫触: {str(e)}")
            self.results["services"]["auth"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_user_service_tests(self):
        """杩愯鐢ㄦ埛鏈嶅姟闆嗘垚娴嬭瘯"""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛岀敤鎴锋湇鍔￠泦鎴愭祴璇?)
        logger.info("=" * 60)
        
        try:
            tester = TestUserIntegration()
            results = tester.run_all_tests()
            self.results["services"]["user"] = results
            return results
        except Exception as e:
            logger.error(f"鐢ㄦ埛鏈嶅姟闆嗘垚娴嬭瘯澶辫触: {str(e)}")
            self.results["services"]["user"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_permission_service_tests(self):
        """杩愯鏉冮檺鏈嶅姟闆嗘垚娴嬭瘯"""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛屾潈闄愭湇鍔￠泦鎴愭祴璇?)
        logger.info("=" * 60)
        
        try:
            tester = TestPermissionIntegration()
            results = tester.run_all_tests()
            self.results["services"]["permission"] = results
            return results
        except Exception as e:
            logger.error(f"鏉冮檺鏈嶅姟闆嗘垚娴嬭瘯澶辫触: {str(e)}")
            self.results["services"]["permission"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_system_service_tests(self):
        """杩愯绯荤粺鏈嶅姟闆嗘垚娴嬭瘯"""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛岀郴缁熸湇鍔￠泦鎴愭祴璇?)
        logger.info("=" * 60)
        
        try:
            tester = TestSystemIntegration()
            results = tester.run_all_tests()
            self.results["services"]["system"] = results
            return results
        except Exception as e:
            logger.error(f"绯荤粺鏈嶅姟闆嗘垚娴嬭瘯澶辫触: {str(e)}")
            self.results["services"]["system"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_support_service_tests(self):
        """杩愯鏀拺鏈嶅姟闆嗘垚娴嬭瘯"""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛屾敮鎾戞湇鍔￠泦鎴愭祴璇?)
        logger.info("=" * 60)
        
        try:
            tester = TestSupportIntegration()
            results = tester.run_all_tests()
            self.results["services"]["support"] = results
            return results
        except Exception as e:
            logger.error(f"鏀拺鏈嶅姟闆嗘垚娴嬭瘯澶辫触: {str(e)}")
            self.results["services"]["support"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_business_service_tests(self):
        """杩愯涓氬姟鏈嶅姟闆嗘垚娴嬭瘯"""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛屼笟鍔℃湇鍔￠泦鎴愭祴璇?)
        logger.info("=" * 60)
        
        try:
            tester = TestBusinessIntegration()
            results = tester.run_all_tests()
            self.results["services"]["business"] = results
            return results
        except Exception as e:
            logger.error(f"涓氬姟鏈嶅姟闆嗘垚娴嬭瘯澶辫触: {str(e)}")
            self.results["services"]["business"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_all_tests(self):
        """杩愯鎵€鏈夐泦鎴愭祴璇?""
        logger.info("=" * 60)
        logger.info("寮€濮嬭繍琛屾墍鏈夐泦鎴愭祴璇?)
        logger.info(f"娴嬭瘯鏃堕棿: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # 杩愯鍚勪釜鏈嶅姟鐨勯泦鎴愭祴璇?        self.run_auth_service_tests()
        self.run_user_service_tests()
        self.run_permission_service_tests()
        self.run_system_service_tests()
        self.run_support_service_tests()
        self.run_business_service_tests()
        
        # 姹囨€荤粨鏋?        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for service_name, service_result in self.results["services"].items():
            if service_result:
                total_tests += service_result.get("total", 0)
                total_passed += service_result.get("passed", 0)
                total_failed += service_result.get("failed", 0)
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "pass_rate": f"{(total_passed / total_tests * 100):.2f}%" if total_tests > 0 else "0%"
        }
        
        # 鐢熸垚娴嬭瘯鎶ュ憡
        self.generate_report()
        
        # 鎵撳嵃姹囨€荤粨鏋?        logger.info("\n" + "=" * 60)
        logger.info("鎵€鏈夐泦鎴愭祴璇曞畬鎴?)
        logger.info(f"鎬绘祴璇曟暟: {total_tests}")
        logger.info(f"閫氳繃鏁? {total_passed}")
        logger.info(f"澶辫触鏁? {total_failed}")
        logger.info(f"閫氳繃鐜? {self.results['summary']['pass_rate']}")
        logger.info("=" * 60)
        
        return self.results
    
    def generate_report(self):
        """鐢熸垚娴嬭瘯鎶ュ憡"""
        report_path = os.path.join(
            os.path.dirname(__file__),
            "integration_test_report.json"
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        logger.success(f"闆嗘垚娴嬭瘯鎶ュ憡宸茬敓鎴? {report_path}")
        
        # 鐢熸垚Markdown鏍煎紡鐨勬姤鍛?        md_report_path = os.path.join(
            os.path.dirname(__file__),
            "integration_test_report.md"
        )
        
        with open(md_report_path, 'w', encoding='utf-8') as f:
            f.write("# 闆嗘垚娴嬭瘯鎶ュ憡\n\n")
            f.write(f"**娴嬭瘯鏃堕棿**: {self.results['test_time']}\n\n")
            f.write("## 娴嬭瘯姹囨€籠n\n")
            f.write(f"- **鎬绘祴璇曟暟**: {self.results['summary']['total_tests']}\n")
            f.write(f"- **閫氳繃鏁?*: {self.results['summary']['total_passed']}\n")
            f.write(f"- **澶辫触鏁?*: {self.results['summary']['total_failed']}\n")
            f.write(f"- **閫氳繃鐜?*: {self.results['summary']['pass_rate']}\n\n")
            
            f.write("## 鍚勬湇鍔℃祴璇曠粨鏋淺n\n")
            
            for service_name, service_result in self.results["services"].items():
                if service_result:
                    f.write(f"### {service_name.upper()} 鏈嶅姟\n\n")
                    f.write(f"- **鎬绘祴璇曟暟**: {service_result.get('total', 0)}\n")
                    f.write(f"- **閫氳繃鏁?*: {service_result.get('passed', 0)}\n")
                    f.write(f"- **澶辫触鏁?*: {service_result.get('failed', 0)}\n")
                    f.write(f"- **閫氳繃鐜?*: {(service_result.get('passed', 0) / service_result.get('total', 1) * 100):.2f}%\n\n")
                    
                    if service_result.get("details"):
                        f.write("#### 娴嬭瘯璇︽儏\n\n")
                        f.write("| 娴嬭瘯鐢ㄤ緥 | 鐘舵€?|\n")
                        f.write("|---------|------|\n")
                        
                        for detail in service_result["details"]:
                            status_icon = "鉁? if detail["status"] == "passed" else "鉁?
                            f.write(f"| {detail['test_name']} | {status_icon} |\n")
                        
                        f.write("\n")
        
        logger.success(f"闆嗘垚娴嬭瘯Markdown鎶ュ憡宸茬敓鎴? {md_report_path}")


def main():
    """涓诲嚱鏁?""
    runner = IntegrationTestRunner()
    results = runner.run_all_tests()
    
    # 濡傛灉鏈夊け璐ョ殑娴嬭瘯锛岃繑鍥為潪闆堕€€鍑虹爜
    total_failed = results["summary"]["total_failed"]
    if total_failed > 0:
        logger.warning(f"鏈?{total_failed} 涓祴璇曞け璐?)
        sys.exit(1)
    
    return results


if __name__ == "__main__":
    main()
