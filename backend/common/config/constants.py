"""
常量定义模块

功能说明：
1. 定义系统常量
2. 定义枚举值
3. 定义错误码
4. 定义状态码

使用示例：
    from common.config.constants import (
        UserStatus,
        ErrorCode,
        ResponseCode,
        DEFAULT_PAGE_SIZE
    )
    
    # 使用枚举
    status = UserStatus.ACTIVE
    
    # 使用错误码
    error = ErrorCode.USER_NOT_FOUND
    
    # 使用响应码
    response_code = ResponseCode.SUCCESS
"""

from enum import Enum
from typing import Dict


# ========== 用户状态 ==========
class UserStatus(str, Enum):
    """用户状态枚举"""
    ACTIVE = "active"  # 激活
    INACTIVE = "inactive"  # 未激活
    LOCKED = "locked"  # 锁定
    DELETED = "deleted"  # 已删除


# ========== 用户性别 ==========
class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"  # 男
    FEMALE = "female"  # 女
    UNKNOWN = "unknown"  # 未知


# ========== 订单状态 ==========
class OrderStatus(str, Enum):
    """订单状态枚举"""
    PENDING = "pending"  # 待支付
    PAID = "paid"  # 已支付
    SHIPPED = "shipped"  # 已发货
    DELIVERED = "delivered"  # 已送达
    CANCELLED = "cancelled"  # 已取消
    REFUNDED = "refunded"  # 已退款


# ========== 支付状态 ==========
class PaymentStatus(str, Enum):
    """支付状态枚举"""
    PENDING = "pending"  # 待支付
    SUCCESS = "success"  # 支付成功
    FAILED = "failed"  # 支付失败
    REFUNDED = "refunded"  # 已退款


# ========== 审批状态 ==========
class ApprovalStatus(str, Enum):
    """审批状态枚举"""
    PENDING = "pending"  # 待审批
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    CANCELLED = "cancelled"  # 已取消


# ========== 任务状态 ==========
class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"  # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    CANCELLED = "cancelled"  # 已取消


# ========== 任务优先级 ==========
class TaskPriority(str, Enum):
    """任务优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    URGENT = "urgent"  # 紧急


# ========== 通知类型 ==========
class NotificationType(str, Enum):
    """通知类型枚举"""
    SYSTEM = "system"  # 系统通知
    USER = "user"  # 用户通知
    TASK = "task"  # 任务通知
    APPROVAL = "approval"  # 审批通知


# ========== 日志级别 ==========
class LogLevel(str, Enum):
    """日志级别枚举"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ========== 日志类型 ==========
class LogType(str, Enum):
    """日志类型枚举"""
    LOGIN = "login"  # 登录日志
    OPERATION = "operation"  # 操作日志
    ERROR = "error"  # 错误日志
    SYSTEM = "system"  # 系统日志


# ========== 响应码 ==========
class ResponseCode(int, Enum):
    """响应码枚举"""
    SUCCESS = 200  # 成功
    CREATED = 201  # 创建成功
    NO_CONTENT = 204  # 无内容
    
    BAD_REQUEST = 400  # 请求错误
    UNAUTHORIZED = 401  # 未授权
    FORBIDDEN = 403  # 禁止访问
    NOT_FOUND = 404  # 未找到
    METHOD_NOT_ALLOWED = 405  # 方法不允许
    CONFLICT = 409  # 冲突
    VALIDATION_ERROR = 422  # 验证错误
    
    INTERNAL_ERROR = 500  # 内部错误
    NOT_IMPLEMENTED = 501  # 未实现
    SERVICE_UNAVAILABLE = 503  # 服务不可用


# ========== 错误码 ==========
class ErrorCode(int, Enum):
    """错误码枚举"""
    # 通用错误 (1000-1999)
    SUCCESS = 0  # 成功
    UNKNOWN_ERROR = 1000  # 未知错误
    PARAMETER_ERROR = 1001  # 参数错误
    VALIDATION_ERROR = 1002  # 验证错误
    NOT_FOUND = 1003  # 未找到
    PERMISSION_DENIED = 1004  # 权限不足
    RATE_LIMIT_EXCEEDED = 1005  # 超出速率限制
    
    # 用户错误 (2000-2999)
    USER_NOT_FOUND = 2000  # 用户不存在
    USER_ALREADY_EXISTS = 2001  # 用户已存在
    USER_PASSWORD_ERROR = 2002  # 密码错误
    USER_ACCOUNT_LOCKED = 2003  # 账户已锁定
    USER_ACCOUNT_INACTIVE = 2004  # 账户未激活
    USER_TOKEN_EXPIRED = 2005  # Token已过期
    USER_TOKEN_INVALID = 2006  # Token无效
    
    # 部门错误 (3000-3999)
    DEPARTMENT_NOT_FOUND = 3000  # 部门不存在
    DEPARTMENT_ALREADY_EXISTS = 3001  # 部门已存在
    DEPARTMENT_HAS_CHILDREN = 3002  # 部门有子部门
    DEPARTMENT_HAS_USERS = 3003  # 部门有用户
    
    # 角色错误 (4000-4999)
    ROLE_NOT_FOUND = 4000  # 角色不存在
    ROLE_ALREADY_EXISTS = 4001  # 角色已存在
    ROLE_HAS_USERS = 4002  # 角色有用户
    ROLE_HAS_PERMISSIONS = 4003  # 角色有权限
    
    # 权限错误 (5000-5999)
    PERMISSION_NOT_FOUND = 5000  # 权限不存在
    PERMISSION_ALREADY_EXISTS = 5001  # 权限已存在
    
    # 菜单错误 (6000-6999)
    MENU_NOT_FOUND = 6000  # 菜单不存在
    MENU_ALREADY_EXISTS = 6001  # 菜单已存在
    MENU_HAS_CHILDREN = 6002  # 菜单有子菜单
    
    # 租户错误 (7000-7999)
    TENANT_NOT_FOUND = 7000  # 租户不存在
    TENANT_ALREADY_EXISTS = 7001  # 租户已存在
    TENANT_QUOTA_EXCEEDED = 7002  # 租户配额已超出
    
    # MCP工具错误 (8000-8999)
    MCP_TOOL_NOT_FOUND = 8000  # MCP工具不存在
    MCP_TOOL_ALREADY_EXISTS = 8001  # MCP工具已存在
    MCP_TOOL_EXECUTION_FAILED = 8002  # MCP工具执行失败
    MCP_TOOL_TIMEOUT = 8003  # MCP工具超时
    
    # 数据源错误 (9000-9999)
    DATASOURCE_NOT_FOUND = 9000  # 数据源不存在
    DATASOURCE_ALREADY_EXISTS = 9001  # 数据源已存在
    DATASOURCE_CONNECTION_FAILED = 9002  # 数据源连接失败
    
    # 字典错误 (10000-10999)
    DICT_NOT_FOUND = 10000  # 字典不存在
    DICT_ALREADY_EXISTS = 10001  # 字典已存在
    DICT_ITEM_NOT_FOUND = 10002  # 字典项不存在
    
    # 日志错误 (11000-11999)
    LOG_NOT_FOUND = 11000  # 日志不存在
    
    # 通知错误 (12000-12999)
    NOTIFICATION_NOT_FOUND = 12000  # 通知不存在
    
    # 待办任务错误 (13000-13999)
    TODO_NOT_FOUND = 13000  # 待办任务不存在
    TODO_ALREADY_EXISTS = 13001  # 待办任务已存在
    
    # 工作流错误 (14000-14999)
    WORKFLOW_NOT_FOUND = 14000  # 工作流不存在
    WORKFLOW_TEMPLATE_NOT_FOUND = 14001  # 工作流模板不存在
    WORKFLOW_TASK_NOT_FOUND = 14002  # 工作流任务不存在
    WORKFLOW_ALREADY_EXISTS = 14003  # 工作流已存在


# ========== 错误信息映射 ==========
ERROR_MESSAGES: Dict[int, str] = {
    ErrorCode.SUCCESS: "操作成功",
    ErrorCode.UNKNOWN_ERROR: "未知错误",
    ErrorCode.PARAMETER_ERROR: "参数错误",
    ErrorCode.VALIDATION_ERROR: "验证失败",
    ErrorCode.NOT_FOUND: "资源不存在",
    ErrorCode.PERMISSION_DENIED: "权限不足",
    ErrorCode.RATE_LIMIT_EXCEEDED: "超出速率限制",
    
    ErrorCode.USER_NOT_FOUND: "用户不存在",
    ErrorCode.USER_ALREADY_EXISTS: "用户已存在",
    ErrorCode.USER_PASSWORD_ERROR: "密码错误",
    ErrorCode.USER_ACCOUNT_LOCKED: "账户已锁定",
    ErrorCode.USER_ACCOUNT_INACTIVE: "账户未激活",
    ErrorCode.USER_TOKEN_EXPIRED: "Token已过期",
    ErrorCode.USER_TOKEN_INVALID: "Token无效",
    
    ErrorCode.DEPARTMENT_NOT_FOUND: "部门不存在",
    ErrorCode.DEPARTMENT_ALREADY_EXISTS: "部门已存在",
    ErrorCode.DEPARTMENT_HAS_CHILDREN: "部门有子部门",
    ErrorCode.DEPARTMENT_HAS_USERS: "部门有用户",
    
    ErrorCode.ROLE_NOT_FOUND: "角色不存在",
    ErrorCode.ROLE_ALREADY_EXISTS: "角色已存在",
    ErrorCode.ROLE_HAS_USERS: "角色有用户",
    ErrorCode.ROLE_HAS_PERMISSIONS: "角色有权限",
    
    ErrorCode.PERMISSION_NOT_FOUND: "权限不存在",
    ErrorCode.PERMISSION_ALREADY_EXISTS: "权限已存在",
    
    ErrorCode.MENU_NOT_FOUND: "菜单不存在",
    ErrorCode.MENU_ALREADY_EXISTS: "菜单已存在",
    ErrorCode.MENU_HAS_CHILDREN: "菜单有子菜单",
    
    ErrorCode.TENANT_NOT_FOUND: "租户不存在",
    ErrorCode.TENANT_ALREADY_EXISTS: "租户已存在",
    ErrorCode.TENANT_QUOTA_EXCEEDED: "租户配额已超出",
    
    ErrorCode.MCP_TOOL_NOT_FOUND: "MCP工具不存在",
    ErrorCode.MCP_TOOL_ALREADY_EXISTS: "MCP工具已存在",
    ErrorCode.MCP_TOOL_EXECUTION_FAILED: "MCP工具执行失败",
    ErrorCode.MCP_TOOL_TIMEOUT: "MCP工具超时",
    
    ErrorCode.DATASOURCE_NOT_FOUND: "数据源不存在",
    ErrorCode.DATASOURCE_ALREADY_EXISTS: "数据源已存在",
    ErrorCode.DATASOURCE_CONNECTION_FAILED: "数据源连接失败",
}


def get_error_message(error_code: int) -> str:
    """
    获取错误信息
    
    Args:
        error_code: 错误码
    
    Returns:
        str: 错误信息
    
    使用示例：
        message = get_error_message(ErrorCode.USER_NOT_FOUND)
        print(message)  # "用户不存在"
    """
    return ERROR_MESSAGES.get(error_code, "未知错误")


# ========== 常量 ==========
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
DEFAULT_TIMEOUT = 30

# 日期格式
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# 文件大小限制
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Token配置
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# 缓存配置
CACHE_DEFAULT_TTL = 3600  # 1小时
CACHE_LONG_TTL = 86400  # 24小时
CACHE_SHORT_TTL = 300  # 5分钟