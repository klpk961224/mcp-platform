"""鍩虹寮傚父绫?""
from typing import Optional


class BaseException(Exception):
    """鍩虹寮傚父绫?""
    
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
    """楠岃瘉寮傚父"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=400, detail=detail)


class NotFoundError(BaseException):
    """鏈壘鍒板紓甯?""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=404, detail=detail)


class UnauthorizedError(BaseException):
    """鏈巿鏉冨紓甯?""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=401, detail=detail)


class ForbiddenError(BaseException):
    """绂佹璁块棶寮傚父"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=403, detail=detail)


class ConflictError(BaseException):
    """鍐茬獊寮傚父"""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, code=409, detail=detail)
