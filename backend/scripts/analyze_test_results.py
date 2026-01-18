#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('D:/WorkSpace/mcp-platform/backend/tests/娴嬭瘯鎶ュ憡.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

failed_tests = [t for t in report['test_results'] if not t['success']]
print(f"澶辫触鐢ㄤ緥数量: {len(failed_tests)}")
print(f"鎬绘祴璇曟暟: {report['total_tests']}")
print(f"閫氳繃鏁? {report['total_passed']}")
print(f"閫氳繃鐜? {report['pass_rate']}")

print("\n" + "="*80)
print("澶辫触鐢ㄤ緥鍒楄〃:")
print("="*80)
for i, test in enumerate(failed_tests[:3], 1):  # 显示鍓?涓け璐ョ殑鐢ㄤ緥
    print(f"\n{i}. {test['test_case']}")
    print(f"   鏈嶅姟: {test['service']}")
    print(f"   鎺ュ彛: {test['endpoint']}")
    print(f"   鏂规硶: {test['method']}")
    print(f"   棰勬湡状态? {test['expected_status']}")
    print(f"   瀹為檯状态? {test['actual_status']}")
    if 'error' in test:
        print(f"   閿欒: {test['error']}")
    if 'response_body' in test and test['response_body']:
        error_msg = test['response_body'][:500]  # 鍙樉绀哄墠500瀛楃
        print(f"   鍝嶅簲: {error_msg}...")
