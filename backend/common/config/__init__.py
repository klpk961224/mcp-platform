"""
配置模块

导出：
- Settings: 配置类
- settings: 全局配置实例
- get_settings: 获取配置实例
- UserStatus: 用户状态枚举
- ErrorCode: 错误码枚举
- ResponseCode: 响应码枚举
- ERROR_MESSAGES: 错误信息映射
- get_error_message: 获取错误信息

使用示例：
    from common.config import settings, UserStatus, ErrorCode
    
    # 访问配置
    print(settings.APP_NAME)
    
    # 使用枚举
    status = UserStatus.ACTIVE
    
    # 使用错误码
    error = ErrorCode.USER_NOT_FOUND
"""

from .settings import Settings, get_settings, settings
from .constants import (
    UserStatus,
    Gender,
    OrderStatus,
    PaymentStatus,
    ApprovalStatus,
    TaskStatus,
    TaskPriority,
    NotificationType,
    LogLevel,
    LogType,
    ResponseCode,
    ErrorCode,
    ERROR_MESSAGES,
    get_error_message,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    DEFAULT_TIMEOUT,
    DATETIME_FORMAT,
    DATE_FORMAT,
    TIME_FORMAT,
    MAX_FILE_SIZE,
    MAX_IMAGE_SIZE,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    CACHE_DEFAULT_TTL,
    CACHE_LONG_TTL,
    CACHE_SHORT_TTL,
)

__all__ = [
    # 配置
    'Settings',
    'settings',
    'get_settings',
    
    # 枚举
    'UserStatus',
    'Gender',
    'OrderStatus',
    'PaymentStatus',
    'ApprovalStatus',
    'TaskStatus',
    'TaskPriority',
    'NotificationType',
    'LogLevel',
    'LogType',
    'ResponseCode',
    'ErrorCode',
    
    # 错误处理
    'ERROR_MESSAGES',
    'get_error_message',
    
    # 常量
    'DEFAULT_PAGE_SIZE',
    'MAX_PAGE_SIZE',
    'DEFAULT_TIMEOUT',
    'DATETIME_FORMAT',
    'DATE_FORMAT',
    'TIME_FORMAT',
    'MAX_FILE_SIZE',
    'MAX_IMAGE_SIZE',
    'ACCESS_TOKEN_EXPIRE_MINUTES',
    'REFRESH_TOKEN_EXPIRE_DAYS',
    'CACHE_DEFAULT_TTL',
    'CACHE_LONG_TTL',
    'CACHE_SHORT_TTL',
]