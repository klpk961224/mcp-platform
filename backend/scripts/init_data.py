#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化默认数据脚本

功能：
1. 创建默认租户
2. 创建超级管理员账号
3. 创建默认角色（超级管理员）
4. 创建基础权限
5. 创建默认菜单
6. 分配角色和权限

使用方法：
    python scripts/init_data.py
"""

import sys
import os
import uuid
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
# 添加backend目录到Python路径
backend_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, backend_root)

import pymysql
from common.security.password import hash_password

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'mcp_platform',
    'charset': 'utf8mb4'
}


def init_default_data():
    """初始化默认数据"""
    print("=" * 60)
    print("开始初始化默认数据...")
    print("=" * 60)
    
    connection = None
    cursor = None
    
    try:
        # 连接数据库
        print("\n[1/6] 连接数据库...")
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        print("✅ 数据库连接成功")
        
        # 1. 创建默认租户
        print("\n[2/6] 创建默认租户...")
        tenant_id = str(uuid.uuid4())
        cursor.execute("""
            SELECT id FROM tenants WHERE code = 'default'
        """)
        existing_tenant = cursor.fetchone()
        
        if existing_tenant:
            tenant_id = existing_tenant[0]
            print(f"✅ 默认租户已存在: {tenant_id}")
        else:
            cursor.execute("""
                INSERT INTO tenants (id, name, code, status, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (tenant_id, '默认租户', 'default', 'active', '系统默认租户', datetime.now(), datetime.now()))
            print(f"✅ 默认租户创建成功: {tenant_id}")
        
        # 2. 创建超级管理员
        print("\n[3/6] 创建超级管理员...")
        admin_id = str(uuid.uuid4())
        password_hash = hash_password('admin123456')
        
        cursor.execute("""
            SELECT id FROM users WHERE username = 'admin'
        """)
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            admin_id = existing_admin[0]
            print(f"✅ 超级管理员已存在: {admin_id}")
        else:
            cursor.execute("""
                INSERT INTO users (id, tenant_id, username, email, password, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (admin_id, tenant_id, 'admin', 'admin@example.com', password_hash, 'active', datetime.now(), datetime.now()))
            print(f"✅ 超级管理员创建成功: {admin_id}")
        
        # 3. 创建默认角色
        print("\n[4/6] 创建默认角色...")
        roles = [
            {
                'name': '超级管理员',
                'code': 'super_admin',
                'description': '系统超级管理员角色，拥有所有权限',
                'is_system': True
            },
            {
                'name': '普通用户',
                'code': 'user',
                'description': '普通用户角色',
                'is_system': False
            },
            {
                'name': '管理员',
                'code': 'admin',
                'description': '管理员角色',
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
                print(f"✅ 角色已存在: {role['name']}")
            else:
                role_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO roles (id, tenant_id, name, code, description, is_system, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (role_id, tenant_id, role['name'], role['code'], role['description'], role['is_system'], 'active', datetime.now(), datetime.now()))
                role_ids[role['code']] = role_id
                print(f"✅ 角色创建成功: {role['name']}")
        
        # 4. 分配角色给超级管理员
        print("\n[5/6] 分配角色给超级管理员...")
        cursor.execute("""
            SELECT id FROM user_roles WHERE user_id = %s AND role_id = %s
        """, (admin_id, role_ids['super_admin']))
        existing_user_role = cursor.fetchone()
        
        if existing_user_role:
            print(f"✅ 角色已分配")
        else:
            cursor.execute("""
                INSERT INTO user_roles (id, user_id, role_id, created_at)
                VALUES (%s, %s, %s, %s)
            """, (str(uuid.uuid4()), admin_id, role_ids['super_admin'], datetime.now()))
            print(f"✅ 角色分配成功")
        
        # 5. 创建基础权限
        print("\n[6/6] 创建基础权限...")
        permissions = [
            # 用户管理
            ('user:create', '创建用户', 'operation', '用户管理'),
            ('user:read', '查看用户', 'operation', '用户管理'),
            ('user:update', '更新用户', 'operation', '用户管理'),
            ('user:delete', '删除用户', 'operation', '用户管理'),
            ('user:export', '导出用户', 'operation', '用户管理'),
            ('user:import', '导入用户', 'operation', '用户管理'),
            
            # 角色管理
            ('role:create', '创建角色', 'operation', '角色管理'),
            ('role:read', '查看角色', 'operation', '角色管理'),
            ('role:update', '更新角色', 'operation', '角色管理'),
            ('role:delete', '删除角色', 'operation', '角色管理'),
            ('role:assign', '分配角色', 'operation', '角色管理'),
            
            # 权限管理
            ('permission:read', '查看权限', 'operation', '权限管理'),
            ('permission:update', '更新权限', 'operation', '权限管理'),
            
            # 菜单管理
            ('menu:create', '创建菜单', 'operation', '菜单管理'),
            ('menu:read', '查看菜单', 'operation', '菜单管理'),
            ('menu:update', '更新菜单', 'operation', '菜单管理'),
            ('menu:delete', '删除菜单', 'operation', '菜单管理'),
            
            # 部门管理
            ('department:create', '创建部门', 'operation', '部门管理'),
            ('department:read', '查看部门', 'operation', '部门管理'),
            ('department:update', '更新部门', 'operation', '部门管理'),
            ('department:delete', '删除部门', 'operation', '部门管理'),
            
            # 租户管理
            ('tenant:create', '创建租户', 'operation', '租户管理'),
            ('tenant:read', '查看租户', 'operation', '租户管理'),
            ('tenant:update', '更新租户', 'operation', '租户管理'),
            ('tenant:delete', '删除租户', 'operation', '租户管理'),
            
            # MCP工具管理
            ('mcp:register', '注册MCP工具', 'operation', 'MCP工具管理'),
            ('mcp:read', '查看MCP工具', 'operation', 'MCP工具管理'),
            ('mcp:update', '更新MCP工具', 'operation', 'MCP工具管理'),
            ('mcp:delete', '删除MCP工具', 'operation', 'MCP工具管理'),
            ('mcp:execute', '执行MCP工具', 'operation', 'MCP工具管理'),
            
            # 数据源管理
            ('datasource:create', '创建数据源', 'operation', '数据源管理'),
            ('datasource:read', '查看数据源', 'operation', '数据源管理'),
            ('datasource:update', '更新数据源', 'operation', '数据源管理'),
            ('datasource:delete', '删除数据源', 'operation', '数据源管理'),
            ('datasource:query', '查询数据源', 'operation', '数据源管理'),
            
            # 字典管理
            ('dict:create', '创建字典', 'operation', '字典管理'),
            ('dict:read', '查看字典', 'operation', '字典管理'),
            ('dict:update', '更新字典', 'operation', '字典管理'),
            ('dict:delete', '删除字典', 'operation', '字典管理'),
            
            # 日志管理
            ('log:read', '查看日志', 'operation', '日志管理'),
            ('log:export', '导出日志', 'operation', '日志管理'),
            
            # 待办任务管理
            ('todo:create', '创建待办任务', 'operation', '待办任务管理'),
            ('todo:read', '查看待办任务', 'operation', '待办任务管理'),
            ('todo:update', '更新待办任务', 'operation', '待办任务管理'),
            ('todo:delete', '删除待办任务', 'operation', '待办任务管理'),
            
            # 工作流管理
            ('workflow:create', '创建工作流', 'operation', '工作流管理'),
            ('workflow:read', '查看工作流', 'operation', '工作流管理'),
            ('workflow:update', '更新工作流', 'operation', '工作流管理'),
            ('workflow:delete', '删除工作流', 'operation', '工作流管理'),
            ('workflow:approve', '审批工作流', 'operation', '工作流管理'),
            
            # 系统管理
            ('system:config', '系统配置', 'operation', '系统管理'),
            ('system:monitor', '系统监控', 'operation', '系统管理'),
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
        
        print(f"✅ 基础权限创建成功: {permission_count} 个新权限")
        
        # 6. 创建默认菜单
        print("\n[7/7] 创建默认菜单...")
        menus = [
            {
                'name': '系统管理',
                'path': '/system',
                'icon': 'setting',
                'parent_id': None,
                'sort_order': 100,
                'children': [
                    {
                        'name': '用户管理',
                        'path': '/system/users',
                        'icon': 'user',
                        'sort_order': 101
                    },
                    {
                        'name': '角色管理',
                        'path': '/system/roles',
                        'icon': 'team',
                        'sort_order': 102
                    },
                    {
                        'name': '权限管理',
                        'path': '/system/permissions',
                        'icon': 'key',
                        'sort_order': 103
                    },
                    {
                        'name': '菜单管理',
                        'path': '/system/menus',
                        'icon': 'menu',
                        'sort_order': 104
                    },
                    {
                        'name': '部门管理',
                        'path': '/system/departments',
                        'icon': 'apartment',
                        'sort_order': 105
                    },
                ]
            },
            {
                'name': 'MCP工具',
                'path': '/mcp',
                'icon': 'api',
                'parent_id': None,
                'sort_order': 200,
                'children': [
                    {
                        'name': '工具管理',
                        'path': '/mcp/tools',
                        'icon': 'tool',
                        'sort_order': 201
                    },
                    {
                        'name': '数据源管理',
                        'path': '/mcp/datasources',
                        'icon': 'database',
                        'sort_order': 202
                    },
                    {
                        'name': '字典管理',
                        'path': '/mcp/dictionaries',
                        'icon': 'book',
                        'sort_order': 203
                    },
                ]
            },
            {
                'name': '工作中心',
                'path': '/work',
                'icon': 'work',
                'parent_id': None,
                'sort_order': 300,
                'children': [
                    {
                        'name': '待办任务',
                        'path': '/work/todos',
                        'icon': 'check-circle',
                        'sort_order': 301
                    },
                    {
                        'name': '工作流管理',
                        'path': '/work/workflows',
                        'icon': 'branch',
                        'sort_order': 302
                    },
                ]
            },
            {
                'name': '系统监控',
                'path': '/monitor',
                'icon': 'monitor',
                'parent_id': None,
                'sort_order': 400,
                'children': [
                    {
                        'name': '登录日志',
                        'path': '/monitor/login-logs',
                        'icon': 'login',
                        'sort_order': 401
                    },
                    {
                        'name': '操作日志',
                        'path': '/monitor/operation-logs',
                        'icon': 'file-text',
                        'sort_order': 402
                    },
                ]
            },
        ]
        
        menu_count = 0
        for menu in menus:
            # 创建父菜单
            cursor.execute("""
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
            
            # 创建子菜单
            for child in menu['children']:
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
        
        print(f"✅ 默认菜单创建成功: {menu_count} 个新菜单")
        
        # 提交事务
        connection.commit()
        
        print("\n" + "=" * 60)
        print("✅ 默认数据初始化成功！")
        print("=" * 60)
        print("\n登录信息：")
        print(f"超级管理员账号: admin")
        print(f"超级管理员密码: admin123456")
        print(f"默认租户: default")
        print("\n重要提示：")
        print("1. 请在生产环境中修改超级管理员密码")
        print("2. 请根据实际需求调整角色和权限配置")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("\n数据库连接已关闭")


if __name__ == "__main__":
    init_default_data()