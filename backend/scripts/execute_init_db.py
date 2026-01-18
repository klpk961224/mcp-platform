#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""鎵ц鏁版嵁搴撳垵濮嬪寲鑴氭湰"""

import pymysql
import re

# 鏁版嵁搴撹繛鎺ラ厤缃?db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'charset': 'utf8mb4'
}

try:
    # 杩炴帴MySQL鏈嶅姟鍣?    print("姝ｅ湪杩炴帴MySQL鏈嶅姟鍣?..")
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 创建鏁版嵁搴擄紙濡傛灉涓嶅瓨鍦級
    print("姝ｅ湪创建鏁版嵁搴?mcp_platform...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS mcp_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute("USE mcp_platform")

    # 璇诲彇骞舵墽琛孲QL鑴氭湰
    print("姝ｅ湪璇诲彇SQL鑴氭湰...")
    with open('D:/WorkSpace/mcp-platform/backend/scripts/init_db.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # 鍒嗗壊SQL璇彞锛堜互鍒嗗彿鍒嗛殧锛?    print("姝ｅ湪鍒嗘瀽SQL鑴氭湰...")
    statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

    # 鍒嗙CREATE TABLE璇彞鍜孉LTER TABLE璇彞
    create_statements = []
    alter_statements = []

    for statement in statements:
        # 璺宠繃CREATE DATABASE鍜孶SE璇彞
        if 'CREATE DATABASE' in statement or 'USE ' in statement.upper():
            continue

        # 鎻愬彇CREATE TABLE璇彞锛屽幓闄OREIGN KEY绾︽潫
        if 'CREATE TABLE' in statement.upper():
            # 绉婚櫎澶栭敭绾︽潫
            table_def = statement
            # 绉婚櫎FOREIGN KEY琛?            foreign_key_pattern = r',\s*FOREIGN KEY.*?(?:,\s*FOREIGN KEY.*?)*\s*\) ENGINE'
            table_def = re.sub(foreign_key_pattern, ') ENGINE', table_def, flags=re.IGNORECASE | re.DOTALL)
            create_statements.append(table_def)
        else:
            alter_statements.append(statement)

    # 绗竴姝ワ細创建鎵€鏈夎〃锛堜笉甯﹀閿害鏉燂級
    print(f"\n绗竴姝ワ細创建鎵€鏈夎〃锛堝叡{len(create_statements)}涓級...")
    for i, statement in enumerate(create_statements, 1):
        if statement:
            try:
                cursor.execute(statement)
                print(f"创建绗?{i} 涓〃鎴愬姛")
            except Exception as e:
                print(f"创建绗?{i} 涓〃澶辫触: {e}")

    # 绗簩姝ワ細娣诲姞澶栭敭绾︽潫
    print(f"\n绗簩姝ワ細娣诲姞澶栭敭绾︽潫...")
    # 閲嶆柊璇诲彇SQL鑴氭湰锛屾彁鍙栨墍鏈塅OREIGN KEY绾︽潫
    foreign_key_constraints = []

    for statement in statements:
        if 'CREATE TABLE' in statement.upper():
            # 鎻愬彇琛ㄥ悕
            table_name_match = re.search(r'CREATE TABLE IF NOT EXISTS\s+(\w+)', statement, re.IGNORECASE)
            if not table_name_match:
                continue
            table_name = table_name_match.group(1)

            # 鎻愬彇鎵€鏈塅OREIGN KEY绾︽潫
            foreign_key_matches = re.findall(r'FOREIGN KEY\s*\([^)]+\)\s*REFERENCES\s+\w+\([^)]+\)(?:\s+ON DELETE\s+(?:CASCADE|SET NULL|RESTRICT|NO ACTION))?(?:\s+ON UPDATE\s+(?:CASCADE|SET NULL|RESTRICT|NO ACTION))?', statement, re.IGNORECASE)
            for constraint in foreign_key_matches:
                foreign_key_constraints.append(f"ALTER TABLE {table_name} ADD {constraint};")

    for i, constraint in enumerate(foreign_key_constraints, 1):
        try:
            cursor.execute(constraint)
            print(f"娣诲姞绗?{i} 涓閿害鏉熸垚鍔?)
        except Exception as e:
            print(f"娣诲姞绗?{i} 涓閿害鏉熷け璐? {e}")
            print(f"绾︽潫鍐呭: {constraint[:100]}...")

    # 鎻愪氦浜嬪姟
    connection.commit()
    print("\n鏁版嵁搴撳垵濮嬪寲鎴愬姛锛?)

    # 鏌ョ湅创建鐨勮〃
    print("\n宸插垱寤虹殑琛細")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")

except Exception as e:
    print(f"閿欒: {e}")
    if 'connection' in locals():
        connection.rollback()
finally:
    if 'connection' in locals():
        connection.close()
        print("\n鏁版嵁搴撹繛鎺ュ凡鍏抽棴")
