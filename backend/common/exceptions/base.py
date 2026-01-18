"""基础异常类"""
from typing import Optional


class BaseException(Exception):
    """基础异常类"""
    
    def __init__(
        self,
        message: str,
        code: int = 500,
        detail: Optional[str] = None
    ):
        self.message = message
        self.code = code
        self.detail = detail or message
        super().__init__(self.message)


class ValidationError(BaseException):
    """验证异常"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=400, detail=detail)


class NotFoundError(BaseException):
    """未找到异常"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=404, detail=detail)


class UnauthorizedError(BaseException):
    """未授权异常"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=401, detail=detail)


class ForbiddenError(BaseException):
    """禁止访问异常"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=403, detail=detail)


class ConflictError(BaseException):
    """冲突异常"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=409, detail=detail)