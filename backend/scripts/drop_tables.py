#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""鍒犻櫎鎵€鏈夎〃"""

import pymysql

# 鏁版嵁搴撹繛鎺ラ厤缃?db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'mcp_platform',
    'charset': 'utf8mb4'
}

try:
    # 杩炴帴MySQL鏁版嵁搴?    print("姝ｅ湪杩炴帴鏁版嵁搴?..")
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 绂佺敤澶栭敭妫€鏌?    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    # 鑾峰彇鎵€鏈夎〃
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 鍒犻櫎鎵€鏈夎〃
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"宸插垹闄よ〃: {table_name}")

    # 鍚敤澶栭敭妫€鏌?    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    connection.commit()
    print("\n鎵€鏈夎〃宸插垹闄わ紒")

except Exception as e:
    print(f"閿欒: {e}")
    if 'connection' in locals():
        connection.rollback()
finally:
    if 'connection' in locals():
        connection.close()
        print("鏁版嵁搴撹繛鎺ュ凡鍏抽棴")
