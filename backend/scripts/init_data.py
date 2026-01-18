#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鍒濆鍖栭粯璁ゆ暟鎹剼鏈?
鍔熻兘锛?1. 鍒涘缓榛樿绉熸埛
2. 鍒涘缓瓒呯骇绠＄悊鍛樿处鍙?3. 鍒涘缓榛樿瑙掕壊锛堣秴绾х鐞嗗憳锛?4. 鍒涘缓鍩虹鏉冮檺
5. 鍒涘缓榛樿鑿滃崟
6. 鍒嗛厤瑙掕壊鍜屾潈闄?
浣跨敤鏂规硶锛?    python scripts/init_data.py
"""

import sys
import os
import uuid
from datetime import datetime

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
# 娣诲姞backend鐩綍鍒癙ython璺緞
backend_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, backend_root)

import pymysql
from common.security.password import hash_password

# 鏁版嵁搴撹繛鎺ラ厤缃?db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'mcp_platform',
    'charset': 'utf8mb4'
}


def init_default_data():
    """鍒濆鍖栭粯璁ゆ暟鎹?""
    print("=" * 60)
    print("寮€濮嬪垵濮嬪寲榛樿鏁版嵁...")
    print("=" * 60)
    
    connection = None
    cursor = None
    
    try:
        # 杩炴帴鏁版嵁搴?        print("\n[1/6] 杩炴帴鏁版嵁搴?..")
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        print("鉁?鏁版嵁搴撹繛鎺ユ垚鍔?)
        
        # 1. 鍒涘缓榛樿绉熸埛
        print("\n[2/6] 鍒涘缓榛樿绉熸埛...")
        tenant_id = str(uuid.uuid4())
        cursor.execute("""
            SELECT id FROM tenants WHERE code = 'default'
        """)
        existing_tenant = cursor.fetchone()
        
        if existing_tenant:
            tenant_id = existing_tenant[0]
            print(f"鉁?榛樿绉熸埛宸插瓨鍦? {tenant_id}")
        else:
            cursor.execute("""
                INSERT INTO tenants (id, name, code, status, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (tenant_id, '榛樿绉熸埛', 'default', 'active', '绯荤粺榛樿绉熸埛', datetime.now(), datetime.now()))
            print(f"鉁?榛樿绉熸埛鍒涘缓鎴愬姛: {tenant_id}")
        
        # 2. 鍒涘缓瓒呯骇绠＄悊鍛?        print("\n[3/6] 鍒涘缓瓒呯骇绠＄悊鍛?..")
        admin_id = str(uuid.uuid4())
        password_hash = hash_password('admin123456')
        
        cursor.execute("""
            SELECT id FROM users WHERE username = 'admin'
        """)
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            admin_id = existing_admin[0]
            print(f"鉁?瓒呯骇绠＄悊鍛樺凡瀛樺湪: {admin_id}")
        else:
            cursor.execute("""
                INSERT INTO users (id, tenant_id, username, email, password, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (admin_id, tenant_id, 'admin', 'admin@example.com', password_hash, 'active', datetime.now(), datetime.now()))
            print(f"鉁?瓒呯骇绠＄悊鍛樺垱寤烘垚鍔? {admin_id}")
        
        # 3. 鍒涘缓榛樿瑙掕壊
        print("\n[4/6] 鍒涘缓榛樿瑙掕壊...")
        roles = [
            {
                'name': '瓒呯骇绠＄悊鍛?,
                'code': 'super_admin',
                'description': '绯荤粺瓒呯骇绠＄悊鍛樿鑹诧紝鎷ユ湁鎵€鏈夋潈闄?,
                'is_system': True
            },
            {
                'name': '鏅€氱敤鎴?,
                'code': 'user',
                'description': '鏅€氱敤鎴疯鑹?,
                'is_system': False
            },
            {
                'name': '绠＄悊鍛?,
                'code': 'admin',
                'description': '绠＄悊鍛樿鑹?,
                'is_system': False
            }
        ]
        
        role_ids = {}
        for role in roles:
            cursor.execute("""
                SELECT id FROM roles WHERE code = %s AND tenant_id = %s
            """, (role['code'], tenant_id))
            existing_role = cursor.fetchone()
            
            if existing_role:
                role_ids[role['code']] = existing_role[0]
                print(f"鉁?瑙掕壊宸插瓨鍦? {role['name']}")
            else:
                role_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO roles (id, tenant_id, name, code, description, is_system, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (role_id, tenant_id, role['name'], role['code'], role['description'], role['is_system'], 'active', datetime.now(), datetime.now()))
                role_ids[role['code']] = role_id
                print(f"鉁?瑙掕壊鍒涘缓鎴愬姛: {role['name']}")
        
        # 4. 鍒嗛厤瑙掕壊缁欒秴绾х鐞嗗憳
        print("\n[5/6] 鍒嗛厤瑙掕壊缁欒秴绾х鐞嗗憳...")
        cursor.execute("""
            SELECT id FROM user_roles WHERE user_id = %s AND role_id = %s
        """, (admin_id, role_ids['super_admin']))
        existing_user_role = cursor.fetchone()
        
        if existing_user_role:
            print(f"鉁?瑙掕壊宸插垎閰?)
        else:
            cursor.execute("""
                INSERT INTO user_roles (id, user_id, role_id, created_at)
                VALUES (%s, %s, %s, %s)
            """, (str(uuid.uuid4()), admin_id, role_ids['super_admin'], datetime.now()))
            print(f"鉁?瑙掕壊鍒嗛厤鎴愬姛")
        
        # 5. 鍒涘缓鍩虹鏉冮檺
        print("\n[6/6] 鍒涘缓鍩虹鏉冮檺...")
        permissions = [
            # 鐢ㄦ埛绠＄悊
            ('user:create', '鍒涘缓鐢ㄦ埛', 'operation', '鐢ㄦ埛绠＄悊'),
            ('user:read', '鏌ョ湅鐢ㄦ埛', 'operation', '鐢ㄦ埛绠＄悊'),
            ('user:update', '鏇存柊鐢ㄦ埛', 'operation', '鐢ㄦ埛绠＄悊'),
            ('user:delete', '鍒犻櫎鐢ㄦ埛', 'operation', '鐢ㄦ埛绠＄悊'),
            ('user:export', '瀵煎嚭鐢ㄦ埛', 'operation', '鐢ㄦ埛绠＄悊'),
            ('user:import', '瀵煎叆鐢ㄦ埛', 'operation', '鐢ㄦ埛绠＄悊'),
            
            # 瑙掕壊绠＄悊
            ('role:create', '鍒涘缓瑙掕壊', 'operation', '瑙掕壊绠＄悊'),
            ('role:read', '鏌ョ湅瑙掕壊', 'operation', '瑙掕壊绠＄悊'),
            ('role:update', '鏇存柊瑙掕壊', 'operation', '瑙掕壊绠＄悊'),
            ('role:delete', '鍒犻櫎瑙掕壊', 'operation', '瑙掕壊绠＄悊'),
            ('role:assign', '鍒嗛厤瑙掕壊', 'operation', '瑙掕壊绠＄悊'),
            
            # 鏉冮檺绠＄悊
            ('permission:read', '鏌ョ湅鏉冮檺', 'operation', '鏉冮檺绠＄悊'),
            ('permission:update', '鏇存柊鏉冮檺', 'operation', '鏉冮檺绠＄悊'),
            
            # 鑿滃崟绠＄悊
            ('menu:create', '鍒涘缓鑿滃崟', 'operation', '鑿滃崟绠＄悊'),
            ('menu:read', '鏌ョ湅鑿滃崟', 'operation', '鑿滃崟绠＄悊'),
            ('menu:update', '鏇存柊鑿滃崟', 'operation', '鑿滃崟绠＄悊'),
            ('menu:delete', '鍒犻櫎鑿滃崟', 'operation', '鑿滃崟绠＄悊'),
            
            # 閮ㄩ棬绠＄悊
            ('department:create', '鍒涘缓閮ㄩ棬', 'operation', '閮ㄩ棬绠＄悊'),
            ('department:read', '鏌ョ湅閮ㄩ棬', 'operation', '閮ㄩ棬绠＄悊'),
            ('department:update', '鏇存柊閮ㄩ棬', 'operation', '閮ㄩ棬绠＄悊'),
            ('department:delete', '鍒犻櫎閮ㄩ棬', 'operation', '閮ㄩ棬绠＄悊'),
            
            # 绉熸埛绠＄悊
            ('tenant:create', '鍒涘缓绉熸埛', 'operation', '绉熸埛绠＄悊'),
            ('tenant:read', '鏌ョ湅绉熸埛', 'operation', '绉熸埛绠＄悊'),
            ('tenant:update', '鏇存柊绉熸埛', 'operation', '绉熸埛绠＄悊'),
            ('tenant:delete', '鍒犻櫎绉熸埛', 'operation', '绉熸埛绠＄悊'),
            
            # MCP宸ュ叿绠＄悊
            ('mcp:register', '娉ㄥ唽MCP宸ュ叿', 'operation', 'MCP宸ュ叿绠＄悊'),
            ('mcp:read', '鏌ョ湅MCP宸ュ叿', 'operation', 'MCP宸ュ叿绠＄悊'),
            ('mcp:update', '鏇存柊MCP宸ュ叿', 'operation', 'MCP宸ュ叿绠＄悊'),
            ('mcp:delete', '鍒犻櫎MCP宸ュ叿', 'operation', 'MCP宸ュ叿绠＄悊'),
            ('mcp:execute', '鎵цMCP宸ュ叿', 'operation', 'MCP宸ュ叿绠＄悊'),
            
            # 鏁版嵁婧愮鐞?            ('datasource:create', '鍒涘缓鏁版嵁婧?, 'operation', '鏁版嵁婧愮鐞?),
            ('datasource:read', '鏌ョ湅鏁版嵁婧?, 'operation', '鏁版嵁婧愮鐞?),
            ('datasource:update', '鏇存柊鏁版嵁婧?, 'operation', '鏁版嵁婧愮鐞?),
            ('datasource:delete', '鍒犻櫎鏁版嵁婧?, 'operation', '鏁版嵁婧愮鐞?),
            ('datasource:query', '鏌ヨ鏁版嵁婧?, 'operation', '鏁版嵁婧愮鐞?),
            
            # 瀛楀吀绠＄悊
            ('dict:create', '鍒涘缓瀛楀吀', 'operation', '瀛楀吀绠＄悊'),
            ('dict:read', '鏌ョ湅瀛楀吀', 'operation', '瀛楀吀绠＄悊'),
            ('dict:update', '鏇存柊瀛楀吀', 'operation', '瀛楀吀绠＄悊'),
            ('dict:delete', '鍒犻櫎瀛楀吀', 'operation', '瀛楀吀绠＄悊'),
            
            # 鏃ュ織绠＄悊
            ('log:read', '鏌ョ湅鏃ュ織', 'operation', '鏃ュ織绠＄悊'),
            ('log:export', '瀵煎嚭鏃ュ織', 'operation', '鏃ュ織绠＄悊'),
            
            # 寰呭姙浠诲姟绠＄悊
            ('todo:create', '鍒涘缓寰呭姙浠诲姟', 'operation', '寰呭姙浠诲姟绠＄悊'),
            ('todo:read', '鏌ョ湅寰呭姙浠诲姟', 'operation', '寰呭姙浠诲姟绠＄悊'),
            ('todo:update', '鏇存柊寰呭姙浠诲姟', 'operation', '寰呭姙浠诲姟绠＄悊'),
            ('todo:delete', '鍒犻櫎寰呭姙浠诲姟', 'operation', '寰呭姙浠诲姟绠＄悊'),
            
            # 宸ヤ綔娴佺鐞?            ('workflow:create', '鍒涘缓宸ヤ綔娴?, 'operation', '宸ヤ綔娴佺鐞?),
            ('workflow:read', '鏌ョ湅宸ヤ綔娴?, 'operation', '宸ヤ綔娴佺鐞?),
            ('workflow:update', '鏇存柊宸ヤ綔娴?, 'operation', '宸ヤ綔娴佺鐞?),
            ('workflow:delete', '鍒犻櫎宸ヤ綔娴?, 'operation', '宸ヤ綔娴佺鐞?),
            ('workflow:approve', '瀹℃壒宸ヤ綔娴?, 'operation', '宸ヤ綔娴佺鐞?),
            
            # 绯荤粺绠＄悊
            ('system:config', '绯荤粺閰嶇疆', 'operation', '绯荤粺绠＄悊'),
            ('system:monitor', '绯荤粺鐩戞帶', 'operation', '绯荤粺绠＄悊'),
        ]
        
        permission_count = 0
        for code, name, type_, module in permissions:
            cursor.execute("""
                SELECT id FROM permissions WHERE code = %s
            """, (code,))
            existing_permission = cursor.fetchone()
            
            if not existing_permission:
                perm_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO permissions (id, name, code, type, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (perm_id, name, code, type_, datetime.now(), datetime.now()))
                permission_count += 1
        
        print(f"鉁?鍩虹鏉冮檺鍒涘缓鎴愬姛: {permission_count} 涓柊鏉冮檺")
        
        # 6. 鍒涘缓榛樿鑿滃崟
        print("\n[7/7] 鍒涘缓榛樿鑿滃崟...")
        menus = [
            {
                'name': '绯荤粺绠＄悊',
                'path': '/system',
                'icon': 'setting',
                'parent_id': None,
                'sort_order': 100,
                'children': [
                    {
                        'name': '鐢ㄦ埛绠＄悊',
                        'path': '/system/users',
                        'icon': 'user',
                        'sort_order': 101
                    },
                    {
                        'name': '瑙掕壊绠＄悊',
                        'path': '/system/roles',
                        'icon': 'team',
                        'sort_order': 102
                    },
                    {
                        'name': '鏉冮檺绠＄悊',
                        'path': '/system/permissions',
                        'icon': 'key',
                        'sort_order': 103
                    },
                    {
                        'name': '鑿滃崟绠＄悊',
                        'path': '/system/menus',
                        'icon': 'menu',
                        'sort_order': 104
                    },
                    {
                        'name': '閮ㄩ棬绠＄悊',
                        'path': '/system/departments',
                        'icon': 'apartment',
                        'sort_order': 105
                    },
                ]
            },
            {
                'name': 'MCP宸ュ叿',
                'path': '/mcp',
                'icon': 'api',
                'parent_id': None,
                'sort_order': 200,
                'children': [
                    {
                        'name': '宸ュ叿绠＄悊',
                        'path': '/mcp/tools',
                        'icon': 'tool',
                        'sort_order': 201
                    },
                    {
                        'name': '鏁版嵁婧愮鐞?,
                        'path': '/mcp/datasources',
                        'icon': 'database',
                        'sort_order': 202
                    },
                    {
                        'name': '瀛楀吀绠＄悊',
                        'path': '/mcp/dictionaries',
                        'icon': 'book',
                        'sort_order': 203
                    },
                ]
            },
            {
                'name': '宸ヤ綔涓績',
                'path': '/work',
                'icon': 'work',
                'parent_id': None,
                'sort_order': 300,
                'children': [
                    {
                        'name': '寰呭姙浠诲姟',
                        'path': '/work/todos',
                        'icon': 'check-circle',
                        'sort_order': 301
                    },
                    {
                        'name': '宸ヤ綔娴佺鐞?,
                        'path': '/work/workflows',
                        'icon': 'branch',
                        'sort_order': 302
                    },
                ]
            },
            {
                'name': '绯荤粺鐩戞帶',
                'path': '/monitor',
                'icon': 'monitor',
                'parent_id': None,
                'sort_order': 400,
                'children': [
                    {
                        'name': '鐧诲綍鏃ュ織',
                        'path': '/monitor/login-logs',
                        'icon': 'login',
                        'sort_order': 401
                    },
                    {
                        'name': '鎿嶄綔鏃ュ織',
                        'path': '/monitor/operation-logs',
                        'icon': 'file-text',
                        'sort_order': 402
                    },
                ]
            },
        ]
        
        menu_count = 0
        for menu in menus:
            # 鍒涘缓鐖惰彍鍗?            cursor.execute("""
                SELECT id FROM menus WHERE path = %s AND tenant_id = %s
            """, (menu['path'], tenant_id))
            existing_menu = cursor.fetchone()
            
            if existing_menu:
                parent_id = existing_menu[0]
            else:
                parent_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO menus (id, tenant_id, name, path, icon, parent_id, sort_order, is_visible, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (parent_id, tenant_id, menu['name'], menu['path'], menu['icon'], None, menu['sort_order'], True, 'active', datetime.now(), datetime.now()))
                menu_count += 1
            
            # 鍒涘缓瀛愯彍鍗?            for child in menu['children']:
                cursor.execute("""
                    SELECT id FROM menus WHERE path = %s AND tenant_id = %s
                """, (child['path'], tenant_id))
                existing_child = cursor.fetchone()
                
                if not existing_child:
                    child_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO menus (id, tenant_id, name, path, icon, parent_id, sort_order, is_visible, status, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (child_id, tenant_id, child['name'], child['path'], child['icon'], parent_id, child['sort_order'], True, 'active', datetime.now(), datetime.now()))
                    menu_count += 1
        
        print(f"鉁?榛樿鑿滃崟鍒涘缓鎴愬姛: {menu_count} 涓柊鑿滃崟")
        
        # 鎻愪氦浜嬪姟
        connection.commit()
        
        print("\n" + "=" * 60)
        print("鉁?榛樿鏁版嵁鍒濆鍖栨垚鍔燂紒")
        print("=" * 60)
        print("\n鐧诲綍淇℃伅锛?)
        print(f"瓒呯骇绠＄悊鍛樿处鍙? admin")
        print(f"瓒呯骇绠＄悊鍛樺瘑鐮? admin123456")
        print(f"榛樿绉熸埛: default")
        print("\n閲嶈鎻愮ず锛?)
        print("1. 璇峰湪鐢熶骇鐜涓慨鏀硅秴绾х鐞嗗憳瀵嗙爜")
        print("2. 璇锋牴鎹疄闄呴渶姹傝皟鏁磋鑹插拰鏉冮檺閰嶇疆")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n鉂?鍒濆鍖栧け璐? {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("\n鏁版嵁搴撹繛鎺ュ凡鍏抽棴")


if __name__ == "__main__":
    init_default_data()
