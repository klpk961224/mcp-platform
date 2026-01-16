#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复所有__init__.py文件"""

import os
import glob

# 查找所有__init__.py文件
init_files = glob.glob('D:/WorkSpace/mcp-platform/backend/services/**/__init__.py', recursive=True)

# 需要修复的文件内容映射
fixes = {
    '认证域服务应用包': '# 认证域服务应用包',
    '用户域服务应用包': '# 用户域服务应用包',
    '权限域服务应用包': '# 权限域服务应用包',
    '核心模块': '# 核心模块',
    'API模块': '# API模块',
    'API v1模块': '# API v1模块',
    'Schema模块': '# Schema模块',
    '认证Schema': '# 认证Schema',
    '用户Schema': '# 用户Schema',
    '部门Schema': '# 部门Schema',
    '租户Schema': '# 租户Schema',
    '角色Schema': '# 角色Schema',
    '权限Schema': '# 权限Schema',
    '菜单Schema': '# 菜单Schema',
}

for file_path in init_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # 检查是否需要修复
    if content in fixes:
        new_content = fixes[content]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已修复: {file_path}")
    elif content == '' or content.startswith('#'):
        print(f"无需修复: {file_path}")
    else:
        print(f"未知内容: {file_path} -> {content}")

print("\n所有__init__.py文件修复完成！")