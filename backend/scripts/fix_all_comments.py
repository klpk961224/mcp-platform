#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量修复所有Python文件的注释格式"""

import os
import glob

# 查找所有Python文件
python_files = glob.glob('D:/WorkSpace/mcp-platform/backend/**/*.py', recursive=True)

for file_path in python_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查文件开头是否有非#注释的文本
        lines = content.split('\n')
        if lines and lines[0] and not lines[0].startswith('#') and not lines[0].startswith('"""') and not lines[0].startswith("'''"):
            # 检查是否是纯中文描述（可能是注释）
            first_line = lines[0].strip()
            if first_line and all('\u4e00' <= c <= '\u9fff' or c in '：，。、！？；：' for c in first_line if not c.isspace()):
                # 添加#注释
                new_content = '#' + lines[0] + '\n' + '\n'.join(lines[1:])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已修复: {file_path}")
    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")

print("\n所有文件修复完成！")