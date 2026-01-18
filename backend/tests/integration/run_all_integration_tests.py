# -*- coding: utf-8 -*-
"""
运行所有集成测试

功能说明:
1. 运行所有服务的集成测试
2. 生成测试报告
3. 记录测试结果

使用方法:
    python run_all_integration_tests.py

依赖:
    pip install requests
"""

import sys
import os
import json
from datetime import datetime
from loguru import logger

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入各个服务的集成测试
from test_auth_integration import TestAuthIntegration
from test_user_integration import TestUserIntegration
from test_permission_integration import TestPermissionIntegration
from test_system_integration import TestSystemIntegration
from test_support_integration import TestSupportIntegration
from test_business_integration import TestBusinessIntegration


class IntegrationTestRunner:
    """集成测试运行器"""
    
    def __init__(self):
        self.results = {
            "test_time": datetime.now().isoformat(),
            "services": {}
        }
    
    def run_auth_service_tests(self):
        """运行认证服务集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行认证服务集成测试")
        logger.info("=" * 60)
        
        try:
            tester = TestAuthIntegration()
            results = tester.run_all_tests()
            self.results["services"]["auth"] = results
            return results
        except Exception as e:
            logger.error(f"认证服务集成测试失败: {str(e)}")
            self.results["services"]["auth"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_user_service_tests(self):
        """运行用户服务集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行用户服务集成测试")
        logger.info("=" * 60)
        
        try:
            tester = TestUserIntegration()
            results = tester.run_all_tests()
            self.results["services"]["user"] = results
            return results
        except Exception as e:
            logger.error(f"用户服务集成测试失败: {str(e)}")
            self.results["services"]["user"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_permission_service_tests(self):
        """运行权限服务集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行权限服务集成测试")
        logger.info("=" * 60)
        
        try:
            tester = TestPermissionIntegration()
            results = tester.run_all_tests()
            self.results["services"]["permission"] = results
            return results
        except Exception as e:
            logger.error(f"权限服务集成测试失败: {str(e)}")
            self.results["services"]["permission"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_system_service_tests(self):
        """运行系统服务集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行系统服务集成测试")
        logger.info("=" * 60)
        
        try:
            tester = TestSystemIntegration()
            results = tester.run_all_tests()
            self.results["services"]["system"] = results
            return results
        except Exception as e:
            logger.error(f"系统服务集成测试失败: {str(e)}")
            self.results["services"]["system"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_support_service_tests(self):
        """运行支撑服务集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行支撑服务集成测试")
        logger.info("=" * 60)
        
        try:
            tester = TestSupportIntegration()
            results = tester.run_all_tests()
            self.results["services"]["support"] = results
            return results
        except Exception as e:
            logger.error(f"支撑服务集成测试失败: {str(e)}")
            self.results["services"]["support"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_business_service_tests(self):
        """运行业务服务集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行业务服务集成测试")
        logger.info("=" * 60)
        
        try:
            tester = TestBusinessIntegration()
            results = tester.run_all_tests()
            self.results["services"]["business"] = results
            return results
        except Exception as e:
            logger.error(f"业务服务集成测试失败: {str(e)}")
            self.results["services"]["business"] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }
            return None
    
    def run_all_tests(self):
        """运行所有集成测试"""
        logger.info("=" * 60)
        logger.info("开始运行所有集成测试")
        logger.info(f"测试时间: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # 运行各个服务的集成测试
        self.run_auth_service_tests()
        self.run_user_service_tests()
        self.run_permission_service_tests()
        self.run_system_service_tests()
        self.run_support_service_tests()
        self.run_business_service_tests()
        
        # 汇总结果
        total_tests = 0
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
        
        # 生成测试报告
        self.generate_report()
        
        # 打印汇总结果
        logger.info("\n" + "=" * 60)
        logger.info("所有集成测试完成")
        logger.info(f"总测试数: {total_tests}")
        logger.info(f"通过数: {total_passed}")
        logger.info(f"失败数: {total_failed}")
        logger.info(f"通过率: {self.results['summary']['pass_rate']}")
        logger.info("=" * 60)
        
        return self.results
    
    def generate_report(self):
        """生成测试报告"""
        report_path = os.path.join(
            os.path.dirname(__file__),
            "integration_test_report.json"
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        logger.success(f"集成测试报告已生成: {report_path}")
        
        # 生成Markdown格式的报告
        md_report_path = os.path.join(
            os.path.dirname(__file__),
            "integration_test_report.md"
        )
        
        with open(md_report_path, 'w', encoding='utf-8') as f:
            f.write("# 集成测试报告\n\n")
            f.write(f"**测试时间**: {self.results['test_time']}\n\n")
            f.write("## 测试汇总\n\n")
            f.write(f"- **总测试数**: {self.results['summary']['total_tests']}\n")
            f.write(f"- **通过数**: {self.results['summary']['total_passed']}\n")
            f.write(f"- **失败数**: {self.results['summary']['total_failed']}\n")
            f.write(f"- **通过率**: {self.results['summary']['pass_rate']}\n\n")
            
            f.write("## 各服务测试结果\n\n")
            
            for service_name, service_result in self.results["services"].items():
                if service_result:
                    f.write(f"### {service_name.upper()} 服务\n\n")
                    f.write(f"- **总测试数**: {service_result.get('total', 0)}\n")
                    f.write(f"- **通过数**: {service_result.get('passed', 0)}\n")
                    f.write(f"- **失败数**: {service_result.get('failed', 0)}\n")
                    f.write(f"- **通过率**: {(service_result.get('passed', 0) / service_result.get('total', 1) * 100):.2f}%\n\n")
                    
                    if service_result.get("details"):
                        f.write("#### 测试详情\n\n")
                        f.write("| 测试用例 | 状态 |\n")
                        f.write("|---------|------|\n")
                        
                        for detail in service_result["details"]:
                            status_icon = "✓" if detail["status"] == "passed" else "✗"
                            f.write(f"| {detail['test_name']} | {status_icon} |\n")
                        
                        f.write("\n")
        
        logger.success(f"集成测试Markdown报告已生成: {md_report_path}")


def main():
    """主函数"""
    runner = IntegrationTestRunner()
    results = runner.run_all_tests()
    
    # 如果有失败的测试，返回非零退出码
    total_failed = results["summary"]["total_failed"]
    if total_failed > 0:
        logger.warning(f"有 {total_failed} 个测试失败")
        sys.exit(1)
    
    return results


if __name__ == "__main__":
    main()