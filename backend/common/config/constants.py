"""
甯搁噺瀹氫箟妯″潡

鍔熻兘璇存槑锛?1. 瀹氫箟绯荤粺甯搁噺
2. 瀹氫箟鏋氫妇鍊?3. 瀹氫箟閿欒鐮?4. 瀹氫箟状态佺爜

浣跨敤绀轰緥锛?    from common.config.constants import (
        UserStatus,
        ErrorCode,
        ResponseCode,
        DEFAULT_PAGE_SIZE
    )
    
    # 浣跨敤鏋氫妇
    status = UserStatus.ACTIVE
    
    # 浣跨敤閿欒鐮?    error = ErrorCode.USER_NOT_FOUND
    
    # 浣跨敤鍝嶅簲鐮?    response_code = ResponseCode.SUCCESS
"""

from enum import Enum
from typing import Dict


# ========== 鐢ㄦ埛状态?==========
class UserStatus(str, Enum):
    """鐢ㄦ埛状态佹灇涓?""
    ACTIVE = "active"  # 婵€娲?    INACTIVE = "inactive"  # 鏈縺娲?    LOCKED = "locked"  # 閿佸畾
    DELETED = "deleted"  # 宸插垹闄?

# ========== 鐢ㄦ埛鎬у埆 ==========
class Gender(str, Enum):
    """鎬у埆鏋氫妇"""
    MALE = "male"  # 鐢?    FEMALE = "female"  # 濂?    UNKNOWN = "unknown"  # 鏈煡


# ========== 璁㈠崟状态?==========
class OrderStatus(str, Enum):
    """璁㈠崟状态佹灇涓?""
    PENDING = "pending"  # 寰呮敮浠?    PAID = "paid"  # 宸叉敮浠?    SHIPPED = "shipped"  # 宸插彂璐?    DELIVERED = "delivered"  # 宸查€佽揪
    CANCELLED = "cancelled"  # 宸插彇娑?    REFUNDED = "refunded"  # 宸查€€娆?

# ========== 鏀粯状态?==========
class PaymentStatus(str, Enum):
    """鏀粯状态佹灇涓?""
    PENDING = "pending"  # 寰呮敮浠?    SUCCESS = "success"  # 鏀粯鎴愬姛
    FAILED = "failed"  # 鏀粯澶辫触
    REFUNDED = "refunded"  # 宸查€€娆?

# ========== 瀹℃壒状态?==========
class ApprovalStatus(str, Enum):
    """瀹℃壒状态佹灇涓?""
    PENDING = "pending"  # 寰呭鎵?    APPROVED = "approved"  # 宸查€氳繃
    REJECTED = "rejected"  # 宸叉嫆缁?    CANCELLED = "cancelled"  # 宸插彇娑?

# ========== 浠诲姟状态?==========
class TaskStatus(str, Enum):
    """浠诲姟状态佹灇涓?""
    PENDING = "pending"  # 寰呭鐞?    IN_PROGRESS = "in_progress"  # 杩涜涓?    COMPLETED = "completed"  # 宸插畬鎴?    FAILED = "failed"  # 澶辫触
    CANCELLED = "cancelled"  # 宸插彇娑?

# ========== 浠诲姟浼樺厛绾?==========
class TaskPriority(str, Enum):
    """浠诲姟浼樺厛绾ф灇涓?""
    LOW = "low"  # 浣?    MEDIUM = "medium"  # 涓?    HIGH = "high"  # 楂?    URGENT = "urgent"  # 绱ф€?

# ========== 閫氱煡类型 ==========
class NotificationType(str, Enum):
    """閫氱煡类型鏋氫妇"""
    SYSTEM = "system"  # 绯荤粺閫氱煡
    USER = "user"  # 鐢ㄦ埛閫氱煡
    TASK = "task"  # 浠诲姟閫氱煡
    APPROVAL = "approval"  # 瀹℃壒閫氱煡


# ========== 鏃ュ織级别 ==========
class LogLevel(str, Enum):
    """鏃ュ織级别鏋氫妇"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ========== 鏃ュ織类型 ==========
class LogType(str, Enum):
    """鏃ュ織类型鏋氫妇"""
    LOGIN = "login"  # 鐧诲綍鏃ュ織
    OPERATION = "operation"  # 鎿嶄綔鏃ュ織
    ERROR = "error"  # 閿欒鏃ュ織
    SYSTEM = "system"  # 绯荤粺鏃ュ織


# ========== 鍝嶅簲鐮?==========
class ResponseCode(int, Enum):
    """鍝嶅簲鐮佹灇涓?""
    SUCCESS = 200  # 鎴愬姛
    CREATED = 201  # 创建鎴愬姛
    NO_CONTENT = 204  # 鏃犲唴瀹?    
    BAD_REQUEST = 400  # 璇锋眰閿欒
    UNAUTHORIZED = 401  # 鏈巿鏉?    FORBIDDEN = 403  # 绂佹璁块棶
    NOT_FOUND = 404  # 鏈壘鍒?    METHOD_NOT_ALLOWED = 405  # 鏂规硶涓嶅厑璁?    CONFLICT = 409  # 鍐茬獊
    VALIDATION_ERROR = 422  # 楠岃瘉閿欒
    
    INTERNAL_ERROR = 500  # 鍐呴儴閿欒
    NOT_IMPLEMENTED = 501  # 鏈疄鐜?    SERVICE_UNAVAILABLE = 503  # 鏈嶅姟涓嶅彲鐢?

# ========== 閿欒鐮?==========
class ErrorCode(int, Enum):
    """閿欒鐮佹灇涓?""
    # 閫氱敤閿欒 (1000-1999)
    SUCCESS = 0  # 鎴愬姛
    UNKNOWN_ERROR = 1000  # 鏈煡閿欒
    PARAMETER_ERROR = 1001  # 鍙傛暟閿欒
    VALIDATION_ERROR = 1002  # 楠岃瘉閿欒
    NOT_FOUND = 1003  # 鏈壘鍒?    PERMISSION_DENIED = 1004  # 鏉冮檺涓嶈冻
    RATE_LIMIT_EXCEEDED = 1005  # 瓒呭嚭閫熺巼闄愬埗
    
    # 鐢ㄦ埛閿欒 (2000-2999)
    USER_NOT_FOUND = 2000  # 鐢ㄦ埛涓嶅瓨鍦?    USER_ALREADY_EXISTS = 2001  # 鐢ㄦ埛宸插瓨鍦?    USER_PASSWORD_ERROR = 2002  # 瀵嗙爜閿欒
    USER_ACCOUNT_LOCKED = 2003  # 璐︽埛宸查攣瀹?    USER_ACCOUNT_INACTIVE = 2004  # 璐︽埛鏈縺娲?    USER_TOKEN_EXPIRED = 2005  # Token宸茶繃鏈?    USER_TOKEN_INVALID = 2006  # Token鏃犳晥
    
    # 閮ㄩ棬閿欒 (3000-3999)
    DEPARTMENT_NOT_FOUND = 3000  # 閮ㄩ棬涓嶅瓨鍦?    DEPARTMENT_ALREADY_EXISTS = 3001  # 閮ㄩ棬宸插瓨鍦?    DEPARTMENT_HAS_CHILDREN = 3002  # 閮ㄩ棬鏈夊瓙閮ㄩ棬
    DEPARTMENT_HAS_USERS = 3003  # 閮ㄩ棬鏈夌敤鎴?    
    # 瑙掕壊閿欒 (4000-4999)
    ROLE_NOT_FOUND = 4000  # 瑙掕壊涓嶅瓨鍦?    ROLE_ALREADY_EXISTS = 4001  # 瑙掕壊宸插瓨鍦?    ROLE_HAS_USERS = 4002  # 瑙掕壊鏈夌敤鎴?    ROLE_HAS_PERMISSIONS = 4003  # 瑙掕壊鏈夋潈闄?    
    # 鏉冮檺閿欒 (5000-5999)
    PERMISSION_NOT_FOUND = 5000  # 鏉冮檺涓嶅瓨鍦?    PERMISSION_ALREADY_EXISTS = 5001  # 鏉冮檺宸插瓨鍦?    
    # 鑿滃崟閿欒 (6000-6999)
    MENU_NOT_FOUND = 6000  # 鑿滃崟涓嶅瓨鍦?    MENU_ALREADY_EXISTS = 6001  # 鑿滃崟宸插瓨鍦?    MENU_HAS_CHILDREN = 6002  # 鑿滃崟鏈夊瓙鑿滃崟
    
    # 绉熸埛閿欒 (7000-7999)
    TENANT_NOT_FOUND = 7000  # 绉熸埛涓嶅瓨鍦?    TENANT_ALREADY_EXISTS = 7001  # 绉熸埛宸插瓨鍦?    TENANT_QUOTA_EXCEEDED = 7002  # 绉熸埛閰嶉宸茶秴鍑?    
    # MCP宸ュ叿閿欒 (8000-8999)
    MCP_TOOL_NOT_FOUND = 8000  # MCP宸ュ叿涓嶅瓨鍦?    MCP_TOOL_ALREADY_EXISTS = 28001  # MCP宸ュ叿宸插瓨鍦?    MCP_TOOL_EXECUTION_FAILED = 28002  # MCP宸ュ叿鎵ц澶辫触
    MCP_TOOL_TIMEOUT = 28003  # MCP宸ュ叿瓒呮椂
    
    # 鏁版嵁婧愰敊璇?(9000-9999)
    DATASOURCE_NOT_FOUND = 9000  # 鏁版嵁婧愪笉瀛樺湪
    DATASOURCE_ALREADY_EXISTS = 9001  # 鏁版嵁婧愬凡瀛樺湪
    DATASOURCE_CONNECTION_FAILED = 9002  # 鏁版嵁婧愯繛鎺ュけ璐?    
    # 瀛楀吀閿欒 (10000-10999)
    DICT_NOT_FOUND = 10000  # 瀛楀吀涓嶅瓨鍦?    DICT_ALREADY_EXISTS = 10001  # 瀛楀吀宸插瓨鍦?    DICT_ITEM_NOT_FOUND = 10002  # 瀛楀吀椤逛笉瀛樺湪
    
    # 鏃ュ織閿欒 (11000-11999)
    LOG_NOT_FOUND = 11000  # 鏃ュ織涓嶅瓨鍦?    
    # 閫氱煡閿欒 (12000-12999)
    NOTIFICATION_NOT_FOUND = 12000  # 閫氱煡涓嶅瓨鍦?    
    # 寰呭姙浠诲姟閿欒 (13000-13999)
    TODO_NOT_FOUND = 13000  # 寰呭姙浠诲姟涓嶅瓨鍦?    TODO_ALREADY_EXISTS = 13001  # 寰呭姙浠诲姟宸插瓨鍦?    
    # 宸ヤ綔娴侀敊璇?(14000-14999)
    WORKFLOW_NOT_FOUND = 14000  # 宸ヤ綔娴佷笉瀛樺湪
    WORKFLOW_TEMPLATE_NOT_FOUND = 14001  # 宸ヤ綔娴佹ā鏉夸笉瀛樺湪
    WORKFLOW_TASK_NOT_FOUND = 14002  # 宸ヤ綔娴佷换鍔′笉瀛樺湪
    WORKFLOW_ALREADY_EXISTS = 14003  # 宸ヤ綔娴佸凡瀛樺湪


# ========== 閿欒淇℃伅鏄犲皠 ==========
ERROR_MESSAGES: Dict[int, str] = {
    ErrorCode.SUCCESS: "鎿嶄綔鎴愬姛",
    ErrorCode.UNKNOWN_ERROR: "鏈煡閿欒",
    ErrorCode.PARAMETER_ERROR: "鍙傛暟閿欒",
    ErrorCode.VALIDATION_ERROR: "楠岃瘉澶辫触",
    ErrorCode.NOT_FOUND: "资源涓嶅瓨鍦?,
    ErrorCode.PERMISSION_DENIED: "鏉冮檺涓嶈冻",
    ErrorCode.RATE_LIMIT_EXCEEDED: "瓒呭嚭閫熺巼闄愬埗",
    
    ErrorCode.USER_NOT_FOUND: "鐢ㄦ埛涓嶅瓨鍦?,
    ErrorCode.USER_ALREADY_EXISTS: "鐢ㄦ埛宸插瓨鍦?,
    ErrorCode.USER_PASSWORD_ERROR: "瀵嗙爜閿欒",
    ErrorCode.USER_ACCOUNT_LOCKED: "璐︽埛宸查攣瀹?,
    ErrorCode.USER_ACCOUNT_INACTIVE: "璐︽埛鏈縺娲?,
    ErrorCode.USER_TOKEN_EXPIRED: "Token宸茶繃鏈?,
    ErrorCode.USER_TOKEN_INVALID: "Token鏃犳晥",
    
    ErrorCode.DEPARTMENT_NOT_FOUND: "閮ㄩ棬涓嶅瓨鍦?,
    ErrorCode.DEPARTMENT_ALREADY_EXISTS: "閮ㄩ棬宸插瓨鍦?,
    ErrorCode.DEPARTMENT_HAS_CHILDREN: "閮ㄩ棬鏈夊瓙閮ㄩ棬",
    ErrorCode.DEPARTMENT_HAS_USERS: "閮ㄩ棬鏈夌敤鎴?,
    
    ErrorCode.ROLE_NOT_FOUND: "瑙掕壊涓嶅瓨鍦?,
    ErrorCode.ROLE_ALREADY_EXISTS: "瑙掕壊宸插瓨鍦?,
    ErrorCode.ROLE_HAS_USERS: "瑙掕壊鏈夌敤鎴?,
    ErrorCode.ROLE_HAS_PERMISSIONS: "瑙掕壊鏈夋潈闄?,
    
    ErrorCode.PERMISSION_NOT_FOUND: "鏉冮檺涓嶅瓨鍦?,
    ErrorCode.PERMISSION_ALREADY_EXISTS: "鏉冮檺宸插瓨鍦?,
    
    ErrorCode.MENU_NOT_FOUND: "鑿滃崟涓嶅瓨鍦?,
    ErrorCode.MENU_ALREADY_EXISTS: "鑿滃崟宸插瓨鍦?,
    ErrorCode.MENU_HAS_CHILDREN: "鑿滃崟鏈夊瓙鑿滃崟",
    
    ErrorCode.TENANT_NOT_FOUND: "绉熸埛涓嶅瓨鍦?,
    ErrorCode.TENANT_ALREADY_EXISTS: "绉熸埛宸插瓨鍦?,
    ErrorCode.TENANT_QUOTA_EXCEEDED: "绉熸埛閰嶉宸茶秴鍑?,
    
    ErrorCode.MCP_TOOL_NOT_FOUND: "MCP宸ュ叿涓嶅瓨鍦?,
    ErrorCode.MCP_TOOL_ALREADY_EXISTS: "MCP宸ュ叿宸插瓨鍦?,
    ErrorCode.MCP_TOOL_EXECUTION_FAILED: "MCP宸ュ叿鎵ц澶辫触",
    ErrorCode.MCP_TOOL_TIMEOUT: "MCP宸ュ叿瓒呮椂",
    
    ErrorCode.DATASOURCE_NOT_FOUND: "鏁版嵁婧愪笉瀛樺湪",
    ErrorCode.DATASOURCE_ALREADY_EXISTS: "鏁版嵁婧愬凡瀛樺湪",
    ErrorCode.DATASOURCE_CONNECTION_FAILED: "鏁版嵁婧愯繛鎺ュけ璐?,
}


def get_error_message(error_code: int) -> str:
    """
    鑾峰彇閿欒淇℃伅
    
    Args:
        error_code: 閿欒鐮?    
    Returns:
        str: 閿欒淇℃伅
    
    浣跨敤绀轰緥锛?        message = get_error_message(ErrorCode.USER_NOT_FOUND)
        print(message)  # "鐢ㄦ埛涓嶅瓨鍦?
    """
    return ERROR_MESSAGES.get(error_code, "鏈煡閿欒")


# ========== 甯搁噺 ==========
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
DEFAULT_TIMEOUT = 30

# 鏃ユ湡鏍煎紡
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# 鏂囦欢澶у皬闄愬埗
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Token閰嶇疆
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# 缂撳瓨閰嶇疆
CACHE_DEFAULT_TTL = 3600  # 1灏忔椂
CACHE_LONG_TTL = 86400  # 24灏忔椂
CACHE_SHORT_TTL = 300  # 5鍒嗛挓
