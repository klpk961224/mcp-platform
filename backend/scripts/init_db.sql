-- =====================================================
-- 企业级AI综合管理平台 - 数据库初始化脚本
-- =====================================================
-- 创建时间：2026-01-15
-- 数据库版本：MySQL 8.0+
-- 说明：创建所有数据库表和索引
-- =====================================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS mcp_platform 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE mcp_platform;

-- =====================================================
-- 1. 租户表（tenants）
-- =====================================================
CREATE TABLE IF NOT EXISTS tenants (
    id VARCHAR(50) PRIMARY KEY COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '租户名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '租户编码（唯一）',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    description TEXT COMMENT '描述',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    deleted_at DATETIME COMMENT '删除时间',
    created_by VARCHAR(36) COMMENT '创建人ID',
    updated_by VARCHAR(36) COMMENT '更新人ID',
    deleted_by VARCHAR(36) COMMENT '删除人ID',
    INDEX idx_status (status),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='租户表';

-- =====================================================
-- 2. 部门表（departments）
-- =====================================================
CREATE TABLE IF NOT EXISTS departments (
    id VARCHAR(50) PRIMARY KEY COMMENT '部门ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '部门名称',
    code VARCHAR(100) NOT NULL COMMENT '部门编码（如dept001/child002）',
    parent_id VARCHAR(50) COMMENT '父部门ID',
    level INT NOT NULL DEFAULT 1 COMMENT '层级（1-5）',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    deleted_at DATETIME COMMENT '删除时间',
    created_by VARCHAR(36) COMMENT '创建人ID',
    updated_by VARCHAR(36) COMMENT '更新人ID',
    deleted_by VARCHAR(36) COMMENT '删除人ID',
    UNIQUE KEY uk_tenant_code (tenant_id, code),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_level (level),
    INDEX idx_is_deleted (is_deleted),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='部门表';

-- =====================================================
-- 3. 用户表（users）
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY COMMENT '用户ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密）',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    dept_id VARCHAR(50) COMMENT '部门ID',
    position_id VARCHAR(50) COMMENT '岗位ID',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive/locked）',
    last_login_at DATETIME COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    deleted_at DATETIME COMMENT '删除时间',
    created_by VARCHAR(36) COMMENT '创建人ID',
    updated_by VARCHAR(36) COMMENT '更新人ID',
    deleted_by VARCHAR(36) COMMENT '删除人ID',
    UNIQUE KEY uk_tenant_username (tenant_id, username),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_dept_id (dept_id),
    INDEX idx_status (status),
    INDEX idx_is_deleted (is_deleted),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =====================================================
-- 4. 角色表（roles）
-- =====================================================
CREATE TABLE IF NOT EXISTS roles (
    id VARCHAR(50) PRIMARY KEY COMMENT '角色ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '角色名称',
    code VARCHAR(50) NOT NULL COMMENT '角色编码',
    description TEXT COMMENT '描述',
    is_system BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否系统角色',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    deleted_at DATETIME COMMENT '删除时间',
    created_by VARCHAR(36) COMMENT '创建人ID',
    updated_by VARCHAR(36) COMMENT '更新人ID',
    deleted_by VARCHAR(36) COMMENT '删除人ID',
    UNIQUE KEY uk_tenant_code (tenant_id, code),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_is_system (is_system),
    INDEX idx_is_deleted (is_deleted),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- =====================================================
-- 5. 权限表（permissions）
-- =====================================================
CREATE TABLE IF NOT EXISTS permissions (
    id VARCHAR(50) PRIMARY KEY COMMENT '权限ID',
    name VARCHAR(100) NOT NULL COMMENT '权限名称',
    code VARCHAR(100) NOT NULL UNIQUE COMMENT '权限编码（如user:create）',
    type VARCHAR(20) NOT NULL COMMENT '类型（menu/operation/button）',
    description TEXT COMMENT '描述',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- =====================================================
-- 6. 菜单表（menus）
-- =====================================================
CREATE TABLE IF NOT EXISTS menus (
    id VARCHAR(50) PRIMARY KEY COMMENT '菜单ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '菜单名称',
    path VARCHAR(255) COMMENT '菜单路径',
    icon VARCHAR(100) COMMENT '菜单图标',
    parent_id VARCHAR(50) COMMENT '父菜单ID',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序',
    is_visible BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否可见',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_sort_order (sort_order),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES menus(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单表';

-- =====================================================
-- 7. 用户角色关联表（user_roles）
-- =====================================================
CREATE TABLE IF NOT EXISTS user_roles (
    id VARCHAR(50) PRIMARY KEY COMMENT '关联ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    role_id VARCHAR(50) NOT NULL COMMENT '角色ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_role (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- =====================================================
-- 8. 角色权限关联表（role_permissions）
-- =====================================================
CREATE TABLE IF NOT EXISTS role_permissions (
    id VARCHAR(50) PRIMARY KEY COMMENT '关联ID',
    role_id VARCHAR(50) NOT NULL COMMENT '角色ID',
    permission_id VARCHAR(50) NOT NULL COMMENT '权限ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_role_permission (role_id, permission_id),
    INDEX idx_role_id (role_id),
    INDEX idx_permission_id (permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- =====================================================
-- 9. 角色菜单关联表（role_menus）
-- =====================================================
CREATE TABLE IF NOT EXISTS role_menus (
    id VARCHAR(50) PRIMARY KEY COMMENT '关联ID',
    role_id VARCHAR(50) NOT NULL COMMENT '角色ID',
    menu_id VARCHAR(50) NOT NULL COMMENT '菜单ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_role_menu (role_id, menu_id),
    INDEX idx_role_id (role_id),
    INDEX idx_menu_id (menu_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单关联表';

-- =====================================================
-- 10. MCP工具表（mcp_tools）
-- =====================================================
CREATE TABLE IF NOT EXISTS mcp_tools (
    id VARCHAR(50) PRIMARY KEY COMMENT '工具ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '工具名称',
    description TEXT COMMENT '描述',
    api_path VARCHAR(255) NOT NULL COMMENT 'API路径',
    api_method VARCHAR(10) NOT NULL COMMENT 'API方法（GET/POST/PUT/DELETE）',
    tool_type VARCHAR(50) NOT NULL COMMENT '工具类型',
    auth_type VARCHAR(50) NOT NULL COMMENT '认证类型',
    timeout INT NOT NULL DEFAULT 30 COMMENT '超时时间（秒）',
    max_retries INT NOT NULL DEFAULT 3 COMMENT '最大重试次数',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    call_count INT NOT NULL DEFAULT 0 COMMENT '调用次数',
    success_count INT NOT NULL DEFAULT 0 COMMENT '成功次数',
    failure_count INT NOT NULL DEFAULT 0 COMMENT '失败次数',
    avg_response_time INT COMMENT '平均响应时间（毫秒）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否删除',
    deleted_at DATETIME COMMENT '删除时间',
    created_by VARCHAR(36) COMMENT '创建人ID',
    updated_by VARCHAR(36) COMMENT '更新人ID',
    deleted_by VARCHAR(36) COMMENT '删除人ID',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_status (status),
    INDEX idx_tool_type (tool_type),
    INDEX idx_is_deleted (is_deleted),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='MCP工具表';

-- =====================================================
-- 11. MCP工具调用日志表（mcp_tool_call_logs）
-- =====================================================
CREATE TABLE IF NOT EXISTS mcp_tool_call_logs (
    id VARCHAR(50) PRIMARY KEY COMMENT '日志ID',
    tool_id VARCHAR(50) NOT NULL COMMENT '工具ID',
    caller_id VARCHAR(50) NOT NULL COMMENT '调用者ID',
    caller_type VARCHAR(20) NOT NULL COMMENT '调用者类型（user/system）',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    request_params JSON COMMENT '请求参数',
    response_status INT COMMENT '响应状态码',
    response_data JSON COMMENT '响应数据',
    response_time INT COMMENT '响应时间（毫秒）',
    error_message TEXT COMMENT '错误信息',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_tool_id (tool_id),
    INDEX idx_caller_id (caller_id),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (tool_id) REFERENCES mcp_tools(id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='MCP工具调用日志表';

-- =====================================================
-- 12. 登录日志表（login_logs）
-- =====================================================
CREATE TABLE IF NOT EXISTS login_logs (
    id VARCHAR(50) PRIMARY KEY COMMENT '日志ID',
    user_id VARCHAR(50) COMMENT '用户ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    login_status VARCHAR(20) NOT NULL COMMENT '登录状态（success/failed）',
    error_message TEXT COMMENT '错误信息',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_created_at (created_at),
    INDEX idx_login_status (login_status),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='登录日志表';

-- =====================================================
-- 13. 操作日志表（operation_logs）
-- =====================================================
CREATE TABLE IF NOT EXISTS operation_logs (
    id VARCHAR(50) PRIMARY KEY COMMENT '日志ID',
    user_id VARCHAR(50) COMMENT '用户ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    module VARCHAR(50) NOT NULL COMMENT '模块',
    operation VARCHAR(50) NOT NULL COMMENT '操作',
    method VARCHAR(10) NOT NULL COMMENT 'HTTP方法',
    path VARCHAR(255) NOT NULL COMMENT '请求路径',
    request_params JSON COMMENT '请求参数',
    response_data JSON COMMENT '响应数据',
    response_status INT COMMENT '响应状态码',
    response_time INT COMMENT '响应时间（毫秒）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- =====================================================
-- 14. 租户套餐表（tenant_packages）
-- =====================================================
CREATE TABLE IF NOT EXISTS tenant_packages (
    id VARCHAR(50) PRIMARY KEY COMMENT '套餐ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '套餐名称',
    description TEXT COMMENT '描述',
    features JSON COMMENT '功能配置',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_status (status),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='租户套餐表';

-- =====================================================
-- 15. 字典表（dicts）
-- =====================================================
CREATE TABLE IF NOT EXISTS dicts (
    id VARCHAR(50) PRIMARY KEY COMMENT '字典ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    type VARCHAR(50) NOT NULL COMMENT '字典类型',
    name VARCHAR(100) NOT NULL COMMENT '字典名称',
    description TEXT COMMENT '描述',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_type (type),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='字典表';

-- =====================================================
-- 16. 字典项表（dict_items）
-- =====================================================
CREATE TABLE IF NOT EXISTS dict_items (
    id VARCHAR(50) PRIMARY KEY COMMENT '字典项ID',
    dict_id VARCHAR(50) NOT NULL COMMENT '字典ID',
    label VARCHAR(100) NOT NULL COMMENT '标签',
    value VARCHAR(100) NOT NULL COMMENT '值',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_dict_id (dict_id),
    INDEX idx_value (value),
    FOREIGN KEY (dict_id) REFERENCES dicts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='字典项表';

-- =====================================================
-- 17. 通知表（notifications）
-- =====================================================
CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR(50) PRIMARY KEY COMMENT '通知ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    type VARCHAR(50) NOT NULL COMMENT '通知类型',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT COMMENT '内容',
    sender_id VARCHAR(50) COMMENT '发送者ID',
    receiver_ids JSON COMMENT '接收者ID列表',
    status VARCHAR(20) NOT NULL DEFAULT 'unread' COMMENT '状态（unread/read）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知表';

-- =====================================================
-- 18. 待办任务表（todo_tasks）
-- =====================================================
CREATE TABLE IF NOT EXISTS todo_tasks (
    id VARCHAR(50) PRIMARY KEY COMMENT '任务ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    title VARCHAR(200) NOT NULL COMMENT '任务标题',
    description TEXT COMMENT '任务描述',
    task_type VARCHAR(20) NOT NULL COMMENT '任务类型（personal/daily/workflow）',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium' COMMENT '优先级（high/medium/low）',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态（pending/completed/cancelled）',
    due_date DATETIME COMMENT '截止日期',
    completed_at DATETIME COMMENT '完成时间',
    workflow_instance_id VARCHAR(50) COMMENT '工作流实例ID',
    workflow_task_id VARCHAR(50) COMMENT '工作流任务ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_task_type (task_type),
    INDEX idx_due_date (due_date),
    INDEX idx_workflow_instance_id (workflow_instance_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (workflow_instance_id) REFERENCES workflow_instances(id) ON DELETE SET NULL,
    FOREIGN KEY (workflow_task_id) REFERENCES workflow_tasks(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='待办任务表';

-- =====================================================
-- 19. 待办任务标签表（todo_tags）
-- =====================================================
CREATE TABLE IF NOT EXISTS todo_tags (
    id VARCHAR(50) PRIMARY KEY COMMENT '标签ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(50) NOT NULL COMMENT '标签名称',
    color VARCHAR(20) COMMENT '标签颜色',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_tenant_id (tenant_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='待办任务标签表';

-- =====================================================
-- 20. 待办任务标签关联表（todo_task_tags）
-- =====================================================
CREATE TABLE IF NOT EXISTS todo_task_tags (
    id VARCHAR(50) PRIMARY KEY COMMENT '关联ID',
    todo_task_id VARCHAR(50) NOT NULL COMMENT '任务ID',
    tag_id VARCHAR(50) NOT NULL COMMENT '标签ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_task_tag (todo_task_id, tag_id),
    INDEX idx_todo_task_id (todo_task_id),
    INDEX idx_tag_id (tag_id),
    FOREIGN KEY (todo_task_id) REFERENCES todo_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES todo_tags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='待办任务标签关联表';

-- =====================================================
-- 21. 待办任务附件表（todo_attachments）
-- =====================================================
CREATE TABLE IF NOT EXISTS todo_attachments (
    id VARCHAR(50) PRIMARY KEY COMMENT '附件ID',
    todo_task_id VARCHAR(50) NOT NULL COMMENT '任务ID',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    file_size INT COMMENT '文件大小（字节）',
    file_type VARCHAR(50) COMMENT '文件类型',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_todo_task_id (todo_task_id),
    FOREIGN KEY (todo_task_id) REFERENCES todo_tasks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='待办任务附件表';

-- =====================================================
-- 22. 每日计划表（daily_plans）
-- =====================================================
CREATE TABLE IF NOT EXISTS daily_plans (
    id VARCHAR(50) PRIMARY KEY COMMENT '计划ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    plan_date DATE NOT NULL COMMENT '计划日期',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/completed）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_user_date (user_id, plan_date),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_user_id (user_id),
    INDEX idx_plan_date (plan_date),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='每日计划表';

-- =====================================================
-- 23. 每日计划任务关联表（daily_plan_tasks）
-- =====================================================
CREATE TABLE IF NOT EXISTS daily_plan_tasks (
    id VARCHAR(50) PRIMARY KEY COMMENT '关联ID',
    daily_plan_id VARCHAR(50) NOT NULL COMMENT '计划ID',
    todo_task_id VARCHAR(50) NOT NULL COMMENT '任务ID',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_plan_task (daily_plan_id, todo_task_id),
    INDEX idx_daily_plan_id (daily_plan_id),
    INDEX idx_todo_task_id (todo_task_id),
    FOREIGN KEY (daily_plan_id) REFERENCES daily_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (todo_task_id) REFERENCES todo_tasks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='每日计划任务关联表';

-- =====================================================
-- 24. 任务提醒表（todo_reminders）
-- =====================================================
CREATE TABLE IF NOT EXISTS todo_reminders (
    id VARCHAR(50) PRIMARY KEY COMMENT '提醒ID',
    todo_task_id VARCHAR(50) NOT NULL COMMENT '任务ID',
    reminder_type VARCHAR(20) NOT NULL COMMENT '提醒类型（due_date/daily/overdue）',
    reminder_time DATETIME NOT NULL COMMENT '提醒时间',
    is_sent BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否已发送',
    sent_at DATETIME COMMENT '发送时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_todo_task_id (todo_task_id),
    INDEX idx_reminder_time (reminder_time),
    INDEX idx_is_sent (is_sent),
    FOREIGN KEY (todo_task_id) REFERENCES todo_tasks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务提醒表';

-- =====================================================
-- 25. 工作流定义表（workflow_definitions）
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_definitions (
    id VARCHAR(50) PRIMARY KEY COMMENT '定义ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '工作流名称',
    code VARCHAR(50) NOT NULL COMMENT '工作流编码',
    description TEXT COMMENT '描述',
    workflow_type VARCHAR(50) NOT NULL COMMENT '工作流类型（hr/permission/finance/it/custom）',
    definition_json JSON NOT NULL COMMENT '工作流定义JSON',
    version INT NOT NULL DEFAULT 1 COMMENT '版本号',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_by VARCHAR(50) COMMENT '创建者ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_tenant_code (tenant_id, code),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_workflow_type (workflow_type),
    INDEX idx_status (status),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流定义表';

-- =====================================================
-- 26. 工作流实例表（workflow_instances）
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_instances (
    id VARCHAR(50) PRIMARY KEY COMMENT '实例ID',
    instance_no VARCHAR(50) NOT NULL UNIQUE COMMENT '实例编号',
    definition_id VARCHAR(50) NOT NULL COMMENT '定义ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    status VARCHAR(20) NOT NULL DEFAULT 'running' COMMENT '状态（running/completed/cancelled/failed）',
    current_node_id VARCHAR(50) COMMENT '当前节点ID',
    initiator_id VARCHAR(50) NOT NULL COMMENT '发起者ID',
    business_key VARCHAR(100) COMMENT '业务键',
    title VARCHAR(200) COMMENT '标题',
    variables JSON COMMENT '流程变量',
    started_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_tenant_definition (tenant_id, definition_id),
    INDEX idx_tenant_status (tenant_id, status),
    INDEX idx_status (status),
    INDEX idx_started_at (started_at),
    FOREIGN KEY (definition_id) REFERENCES workflow_definitions(id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (initiator_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流实例表';

-- =====================================================
-- 27. 工作流节点表（workflow_nodes）
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_nodes (
    id VARCHAR(50) PRIMARY KEY COMMENT '节点ID',
    definition_id VARCHAR(50) NOT NULL COMMENT '定义ID',
    node_key VARCHAR(50) NOT NULL COMMENT '节点键',
    node_type VARCHAR(50) NOT NULL COMMENT '节点类型（start/end/approve/condition/parallel）',
    node_name VARCHAR(100) NOT NULL COMMENT '节点名称',
    node_config JSON COMMENT '节点配置',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_definition_id (definition_id),
    INDEX idx_node_key (node_key),
    FOREIGN KEY (definition_id) REFERENCES workflow_definitions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流节点表';

-- =====================================================
-- 28. 工作流任务表（workflow_tasks）
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_tasks (
    id VARCHAR(50) PRIMARY KEY COMMENT '任务ID',
    instance_id VARCHAR(50) NOT NULL COMMENT '实例ID',
    node_id VARCHAR(50) NOT NULL COMMENT '节点ID',
    task_key VARCHAR(50) NOT NULL COMMENT '任务键',
    task_name VARCHAR(100) NOT NULL COMMENT '任务名称',
    assignee_id VARCHAR(50) COMMENT '分配给用户ID',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态（pending/completed/cancelled/delegated）',
    action VARCHAR(20) COMMENT '操作类型（approve/reject/delegate/transfer）',
    comment TEXT COMMENT '审批意见',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_instance_id (instance_id),
    INDEX idx_node_id (node_id),
    INDEX idx_assignee_id (assignee_id),
    INDEX idx_status (status),
    FOREIGN KEY (instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (node_id) REFERENCES workflow_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流任务表';

-- =====================================================
-- 29. 工作流日志表（workflow_logs）
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_logs (
    id VARCHAR(50) PRIMARY KEY COMMENT '日志ID',
    instance_id VARCHAR(50) NOT NULL COMMENT '实例ID',
    task_id VARCHAR(50) COMMENT '任务ID',
    user_id VARCHAR(50) COMMENT '用户ID',
    action VARCHAR(50) NOT NULL COMMENT '操作',
    comment TEXT COMMENT '备注',
    log_data JSON COMMENT '日志数据',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_instance_id (instance_id),
    INDEX idx_task_id (task_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES workflow_tasks(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流日志表';

-- =====================================================
-- 30. 工作流模板表（workflow_templates）
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_templates (
    id VARCHAR(50) PRIMARY KEY COMMENT '模板ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT '租户ID',
    name VARCHAR(100) NOT NULL COMMENT '模板名称',
    description TEXT COMMENT '描述',
    template_type VARCHAR(50) NOT NULL COMMENT '模板类型（hr/permission/finance/it）',
    definition_json JSON NOT NULL COMMENT '工作流定义JSON',
    is_system BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否系统模板',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态（active/inactive）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_template_type (template_type),
    INDEX idx_status (status),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流模板表';

-- =====================================================
-- 31. 错误码表（error_codes）
-- =====================================================
CREATE TABLE IF NOT EXISTS error_codes (
    id VARCHAR(50) PRIMARY KEY COMMENT '错误码ID',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '错误码',
    message VARCHAR(500) NOT NULL COMMENT '错误信息',
    level VARCHAR(20) NOT NULL DEFAULT 'error' COMMENT '错误级别',
    module VARCHAR(50) NOT NULL COMMENT '模块',
    description TEXT COMMENT '描述',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_code (code),
    INDEX idx_level (level),
    INDEX idx_module (module),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='错误码表';

-- =====================================================
-- 初始化完成
-- =====================================================

-- 显示创建的表
SHOW TABLES;

-- 显示表数量
SELECT COUNT(*) AS table_count FROM information_schema.tables 
WHERE table_schema = 'mcp_platform';

-- =====================================================
-- 说明：
-- 1. 本脚本创建了30个表，涵盖了所有业务模块
-- 2. 所有表都使用utf8mb4字符集，支持emoji等特殊字符
-- 3. 所有表都包含created_at和updated_at字段
-- 4. 主键使用VARCHAR(50)，便于存储UUID
-- 5. 外键级联删除设置为CASCADE或SET NULL
-- 6. 索引根据查询需求创建
-- 7. JSON字段用于存储复杂数据结构
-- =====================================================