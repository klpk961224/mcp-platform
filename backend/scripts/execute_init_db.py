#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""执行数据库初始化脚本"""

import pymysql
import re

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'charset': 'utf8mb4'
}

try:
    # 连接MySQL服务器
    print("正在连接MySQL服务器...")
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 创建数据库（如果不存在）
    print("正在创建数据库 mcp_platform...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS mcp_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute("USE mcp_platform")

    # 读取并执行SQL脚本
    print("正在读取SQL脚本...")
    with open('D:/WorkSpace/mcp-platform/backend/scripts/init_db.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # 分割SQL语句（以分号分隔）
    print("正在分析SQL脚本...")
    statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

    # 分离CREATE TABLE语句和ALTER TABLE语句
    create_statements = []
    alter_statements = []

    for statement in statements:
        # 跳过CREATE DATABASE和USE语句
        if 'CREATE DATABASE' in statement or 'USE ' in statement.upper():
            continue

        # 提取CREATE TABLE语句，去除FOREIGN KEY约束
        if 'CREATE TABLE' in statement.upper():
            # 移除外键约束
            table_def = statement
            # 移除FOREIGN KEY行
            foreign_key_pattern = r',\s*FOREIGN KEY.*?(?:,\s*FOREIGN KEY.*?)*\s*\) ENGINE'
            table_def = re.sub(foreign_key_pattern, ') ENGINE', table_def, flags=re.IGNORECASE | re.DOTALL)
            create_statements.append(table_def)
        else:
            alter_statements.append(statement)

    # 第一步：创建所有表（不带外键约束）
    print(f"\n第一步：创建所有表（共{len(create_statements)}个）...")
    for i, statement in enumerate(create_statements, 1):
        if statement:
            try:
                cursor.execute(statement)
                print(f"创建第 {i} 个表成功")
            except Exception as e:
                print(f"创建第 {i} 个表失败: {e}")

    # 第二步：添加外键约束
    print(f"\n第二步：添加外键约束...")
    # 重新读取SQL脚本，提取所有FOREIGN KEY约束
    foreign_key_constraints = []

    for statement in statements:
        if 'CREATE TABLE' in statement.upper():
            # 提取表名
            table_name_match = re.search(r'CREATE TABLE IF NOT EXISTS\s+(\w+)', statement, re.IGNORECASE)
            if not table_name_match:
                continue
            table_name = table_name_match.group(1)

            # 提取所有FOREIGN KEY约束
            foreign_key_matches = re.findall(r'FOREIGN KEY\s*\([^)]+\)\s*REFERENCES\s+\w+\([^)]+\)(?:\s+ON DELETE\s+(?:CASCADE|SET NULL|RESTRICT|NO ACTION))?(?:\s+ON UPDATE\s+(?:CASCADE|SET NULL|RESTRICT|NO ACTION))?', statement, re.IGNORECASE)
            for constraint in foreign_key_matches:
                foreign_key_constraints.append(f"ALTER TABLE {table_name} ADD {constraint};")

    for i, constraint in enumerate(foreign_key_constraints, 1):
        try:
            cursor.execute(constraint)
            print(f"添加第 {i} 个外键约束成功")
        except Exception as e:
            print(f"添加第 {i} 个外键约束失败: {e}")
            print(f"约束内容: {constraint[:100]}...")

    # 提交事务
    connection.commit()
    print("\n数据库初始化成功！")

    # 查看创建的表
    print("\n已创建的表：")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")

except Exception as e:
    print(f"错误: {e}")
    if 'connection' in locals():
        connection.rollback()
finally:
    if 'connection' in locals():
        connection.close()
        print("\n数据库连接已关闭")