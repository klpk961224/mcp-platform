#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除所有表"""

import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'mcp_platform',
    'charset': 'utf8mb4'
}

try:
    # 连接MySQL数据库
    print("正在连接数据库...")
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 禁用外键检查
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    # 获取所有表
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 删除所有表
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"已删除表: {table_name}")

    # 启用外键检查
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    connection.commit()
    print("\n所有表已删除！")

except Exception as e:
    print(f"错误: {e}")
    if 'connection' in locals():
        connection.rollback()
finally:
    if 'connection' in locals():
        connection.close()
        print("数据库连接已关闭")