# -*- coding: utf-8 -*-
"""
鍚庣鍗曞厓娴嬭瘯杩愯鑴氭湰

鍔熻兘璇存槑锛?1. 杩愯鎵€鏈夋湇鍔＄殑鍗曞厓娴嬭瘯
2. 鐢熸垚娴嬭瘯鎶ュ憡
3. 鏄剧ず娴嬭瘯缁撴灉

浣跨敤鏂规硶锛?    python run_unit_tests.py

渚濊禆锛?    pip install pytest pytest-cov pytest-html
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def run_tests(service_name: str, test_path: str) -> dict:
    """
    杩愯鎸囧畾鏈嶅姟鐨勫崟鍏冩祴璇?
    Args:
        service_name: 鏈嶅姟鍚嶇О
        test_path: 娴嬭瘯璺緞

    Returns:
        dict: 娴嬭瘯缁撴灉
    """
    print(f"\n{'='*60}")
    print(f"寮€濮嬫祴璇? {service_name}")
    print(f"{'='*60}")

    # 鏋勫缓pytest鍛戒护
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

    # 杩愯娴嬭瘯
    result = subprocess.run(cmd, capture_output=True, text=True)

    # 瑙ｆ瀽缁撴灉
    output = result.stdout + result.stderr

    # 鎻愬彇娴嬭瘯缁熻淇℃伅
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

    # 鎵撳嵃缁撴灉
    print(f"\n娴嬭瘯缁撴灉: {service_name}")
    print(f"  閫氳繃: {passed}")
    print(f"  澶辫触: {failed}")
    print(f"  閿欒: {errors}")
    print(f"  璺宠繃: {skipped}")
    print(f"  鎬昏: {test_result['total']}")
    print(f"  鐘舵€? {'鉁?鎴愬姛' if test_result['success'] else '鉁?澶辫触'}")

    return test_result


def generate_summary_report(results: list, backend_dir: Path):
    """
    鐢熸垚娴嬭瘯姹囨€绘姤鍛?
    Args:
        results: 娴嬭瘯缁撴灉鍒楄〃
        backend_dir: backend鐩綍璺緞
    """
    print(f"\n{'='*60}")
    print("娴嬭瘯姹囨€绘姤鍛?)
    print(f"{'='*60}")

    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)
    total_tests = sum(r["total"] for r in results)

    print(f"\n鎬讳綋缁熻:")
    print(f"  鏈嶅姟鏁伴噺: {len(results)}")
    print(f"  閫氳繃: {total_passed}")
    print(f"  澶辫触: {total_failed}")
    print(f"  閿欒: {total_errors}")
    print(f"  璺宠繃: {total_skipped}")
    print(f"  鎬昏: {total_tests}")

    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        print(f"  閫氳繃鐜? {success_rate:.2f}%")

    print(f"\n鍚勬湇鍔¤鎯?")
    for result in results:
        status = "鉁?鎴愬姛" if result["success"] else "鉁?澶辫触"
        print(f"  {result['service']:20s} - {status:8s} (閫氳繃: {result['passed']}, 澶辫触: {result['failed']}, 閿欒: {result['errors']}, 璺宠繃: {result['skipped']})")

    # 淇濆瓨鎶ュ憡鍒版枃浠?    tests_dir = backend_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    report_path = tests_dir / "娴嬭瘯鎶ュ憡_鍗曞厓娴嬭瘯.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("鍚庣鍗曞厓娴嬭瘯鎶ュ憡\n")
        f.write("="*60 + "\n")
        f.write(f"娴嬭瘯鏃堕棿: {datetime.now().isoformat()}\n")
        f.write(f"\n鎬讳綋缁熻:\n")
        f.write(f"  鏈嶅姟鏁伴噺: {len(results)}\n")
        f.write(f"  閫氳繃: {total_passed}\n")
        f.write(f"  澶辫触: {total_failed}\n")
        f.write(f"  閿欒: {total_errors}\n")
        f.write(f"  璺宠繃: {total_skipped}\n")
        f.write(f"  鎬昏: {total_tests}\n")
        if total_tests > 0:
            success_rate = (total_passed / total_tests) * 100
            f.write(f"  閫氳繃鐜? {success_rate:.2f}%\n")
        f.write(f"\n鍚勬湇鍔¤鎯?\n")
        for result in results:
            status = "鎴愬姛" if result["success"] else "澶辫触"
            f.write(f"  {result['service']:20s} - {status:8s} (閫氳繃: {result['passed']}, 澶辫触: {result['failed']}, 閿欒: {result['errors']}, 璺宠繃: {result['skipped']})\n")

    print(f"\n娴嬭瘯鎶ュ憡宸蹭繚瀛? {report_path}")


def main():
    """涓诲嚱鏁?""
    # 纭繚鍦╞ackend鐩綍涓嬭繍琛?    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # 鍒涘缓reports鐩綍
    reports_dir = backend_dir / "reports"
    reports_dir.mkdir(exist_ok=True)

    # 瀹氫箟瑕佹祴璇曠殑鏈嶅姟
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

    # 杩愯鎵€鏈夋祴璇?    results = []
    for service in services:
        test_path = Path(service["path"])
        if test_path.exists():
            result = run_tests(service["name"], service["path"])
            results.append(result)
        else:
            print(f"\n{'='*60}")
            print(f"璺宠繃娴嬭瘯: {service['name']} (娴嬭瘯鐩綍涓嶅瓨鍦?")
            print(f"{'='*60}")
            results.append({
                "service": service["name"],
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "total": 0,
                "success": False,
                "output": "娴嬭瘯鐩綍涓嶅瓨鍦?
            })

    # 鐢熸垚姹囨€绘姤鍛?    generate_summary_report(results, backend_dir)

    # 杩斿洖閫€鍑虹爜
    if any(not r["success"] for r in results):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

