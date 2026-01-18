"""
閰嶇疆妯″潡

瀵煎嚭锛?- Settings: 閰嶇疆绫?- settings: 鍏ㄥ眬閰嶇疆瀹炰緥
- get_settings: 鑾峰彇閰嶇疆瀹炰緥
- UserStatus: 鐢ㄦ埛鐘舵€佹灇涓?- ErrorCode: 閿欒鐮佹灇涓?- ResponseCode: 鍝嶅簲鐮佹灇涓?- ERROR_MESSAGES: 閿欒淇℃伅鏄犲皠
- get_error_message: 鑾峰彇閿欒淇℃伅

浣跨敤绀轰緥锛?    from common.config import settings, UserStatus, ErrorCode
    
    # 璁块棶閰嶇疆
    print(settings.APP_NAME)
    
    # 浣跨敤鏋氫妇
    status = UserStatus.ACTIVE
    
    # 浣跨敤閿欒鐮?    error = ErrorCode.USER_NOT_FOUND
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
    # 閰嶇疆
    'Settings',
    'settings',
    'get_settings',
    
    # 鏋氫妇
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
    
    # 閿欒澶勭悊
    'ERROR_MESSAGES',
    'get_error_message',
    
    # 甯搁噺
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
