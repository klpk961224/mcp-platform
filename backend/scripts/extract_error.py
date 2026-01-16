#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

with open('D:/WorkSpace/mcp-platform/backend/tests/测试报告.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

# 获取第一个失败的测试用例
failed_tests = [t for t in report['test_results'] if not t['success']]

if failed_tests:
    test = failed_tests[0]
    print(f"测试用例: {test['test_case']}")
    print(f"接口: {test['endpoint']}")
    print(f"方法: {test['method']}")
    
    # 提取关键错误行
    if 'response_body' in test:
        error_text = test['response_body']
        
        # 查找所有 "File" 开头的行
        file_lines = re.findall(r'.*File ".*\.py".*line \d+.*', error_text)
        
        print("\n错误堆栈:")
        for line in file_lines[-10:]:  # 显示最后10行
            print(line)
        
        # 查找具体的错误类型
        error_lines = re.findall(r'[A-Z][a-zA-Z]+Error:.*', error_text)
        if error_lines:
            print(f"\n错误类型: {error_lines[-1]}")