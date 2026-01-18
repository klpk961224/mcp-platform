#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('D:/WorkSpace/mcp-platform/backend/tests/测试报告.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

failed_tests = [t for t in report['test_results'] if not t['success']]
print(f"失败用例数量: {len(failed_tests)}")
print(f"总测试数: {report['total_tests']}")
print(f"通过数: {report['total_passed']}")
print(f"通过率: {report['pass_rate']}")

print("\n" + "="*80)
print("失败用例列表:")
print("="*80)
for i, test in enumerate(failed_tests[:3], 1):  # 显示前3个失败的用例
    print(f"\n{i}. {test['test_case']}")
    print(f"   服务: {test['service']}")
    print(f"   接口: {test['endpoint']}")
    print(f"   方法: {test['method']}")
    print(f"   预期状态: {test['expected_status']}")
    print(f"   实际状态: {test['actual_status']}")
    if 'error' in test:
        print(f"   错误: {test['error']}")
    if 'response_body' in test and test['response_body']:
        error_msg = test['response_body'][:500]  # 只显示前500字符
        print(f"   响应: {error_msg}...")