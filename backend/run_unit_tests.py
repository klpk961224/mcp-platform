# -*- coding: utf-8 -*-
"""
后端单元测试运行脚本

功能说明：
1. 运行所有服务的单元测试
2. 生成测试报告
3. 显示测试结果

使用方法：
    python run_unit_tests.py

依赖：
    pip install pytest pytest-cov pytest-html
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def run_tests(service_name: str, test_path: str) -> dict:
    """
    运行指定服务的单元测试

    Args:
        service_name: 服务名称
        test_path: 测试路径

    Returns:
        dict: 测试结果
    """
    print(f"\n{'='*60}")
    print(f"开始测试: {service_name}")
    print(f"{'='*60}")

    # 构建pytest命令
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "--tb=short",
        "--strict-markers",
        f"--html=reports/{service_name}_report.html",
        f"--self-contained-html",
        f"--cov=backend/services/{service_name}/app",
        f"--cov-report=html:reports/{service_name}_coverage",
        f"--cov-report=term-missing",
        "--cov-fail-under=0"
    ]

    # 运行测试
    result = subprocess.run(cmd, capture_output=True, text=True)

    # 解析结果
    output = result.stdout + result.stderr

    # 提取测试统计信息
    passed = output.count("PASSED")
    failed = output.count("FAILED")
    errors = output.count("ERROR")
    skipped = output.count("SKIPPED")

    test_result = {
        "service": service_name,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "total": passed + failed + errors,
        "success": result.returncode == 0,
        "output": output
    }

    # 打印结果
    print(f"\n测试结果: {service_name}")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  错误: {errors}")
    print(f"  跳过: {skipped}")
    print(f"  总计: {test_result['total']}")
    print(f"  状态: {'✓ 成功' if test_result['success'] else '✗ 失败'}")

    return test_result


def generate_summary_report(results: list, backend_dir: Path):
    """
    生成测试汇总报告

    Args:
        results: 测试结果列表
        backend_dir: backend目录路径
    """
    print(f"\n{'='*60}")
    print("测试汇总报告")
    print(f"{'='*60}")

    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)
    total_tests = sum(r["total"] for r in results)

    print(f"\n总体统计:")
    print(f"  服务数量: {len(results)}")
    print(f"  通过: {total_passed}")
    print(f"  失败: {total_failed}")
    print(f"  错误: {total_errors}")
    print(f"  跳过: {total_skipped}")
    print(f"  总计: {total_tests}")

    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        print(f"  通过率: {success_rate:.2f}%")

    print(f"\n各服务详情:")
    for result in results:
        status = "✓ 成功" if result["success"] else "✗ 失败"
        print(f"  {result['service']:20s} - {status:8s} (通过: {result['passed']}, 失败: {result['failed']}, 错误: {result['errors']}, 跳过: {result['skipped']})")

    # 保存报告到文件
    tests_dir = backend_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    report_path = tests_dir / "测试报告_单元测试.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("后端单元测试报告\n")
        f.write("="*60 + "\n")
        f.write(f"测试时间: {datetime.now().isoformat()}\n")
        f.write(f"\n总体统计:\n")
        f.write(f"  服务数量: {len(results)}\n")
        f.write(f"  通过: {total_passed}\n")
        f.write(f"  失败: {total_failed}\n")
        f.write(f"  错误: {total_errors}\n")
        f.write(f"  跳过: {total_skipped}\n")
        f.write(f"  总计: {total_tests}\n")
        if total_tests > 0:
            success_rate = (total_passed / total_tests) * 100
            f.write(f"  通过率: {success_rate:.2f}%\n")
        f.write(f"\n各服务详情:\n")
        for result in results:
            status = "成功" if result["success"] else "失败"
            f.write(f"  {result['service']:20s} - {status:8s} (通过: {result['passed']}, 失败: {result['failed']}, 错误: {result['errors']}, 跳过: {result['skipped']})\n")

    print(f"\n测试报告已保存: {report_path}")


def main():
    """主函数"""
    # 确保在backend目录下运行
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # 创建reports目录
    reports_dir = backend_dir / "reports"
    reports_dir.mkdir(exist_ok=True)

    # 定义要测试的服务
    services = [
        {
            "name": "auth-service",
            "path": "services/auth-service/tests/unit"
        },
        {
            "name": "user-service",
            "path": "services/user-service/tests/unit"
        },
        {
            "name": "permission-service",
            "path": "services/permission-service/tests/unit"
        },
        {
            "name": "system-service",
            "path": "services/system-service/tests/unit"
        },
        {
            "name": "support-service",
            "path": "services/support-service/tests/unit"
        },
        {
            "name": "business-service",
            "path": "services/business-service/tests/unit"
        }
    ]

    # 运行所有测试
    results = []
    for service in services:
        test_path = Path(service["path"])
        if test_path.exists():
            result = run_tests(service["name"], service["path"])
            results.append(result)
        else:
            print(f"\n{'='*60}")
            print(f"跳过测试: {service['name']} (测试目录不存在)")
            print(f"{'='*60}")
            results.append({
                "service": service["name"],
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "total": 0,
                "success": False,
                "output": "测试目录不存在"
            })

    # 生成汇总报告
    generate_summary_report(results, backend_dir)

    # 返回退出码
    if any(not r["success"] for r in results):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
