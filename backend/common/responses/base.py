"""统一响应格式"""
from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    """成功响应"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: Optional[T] = Field(None, description="数据")


class ErrorResponse(BaseModel):
    """错误响应"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="详细信息")


def success(data: Optional[Any] = None, message: str = "success") -> dict:
    """成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
    
    Returns:
        dict: 响应字典
    
    使用示例：
        return success({"id": 1, "name": "test"})
        return success(message="操作成功")
    """
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error(message: str, code: int = 500, detail: Optional[str] = None) -> dict:
    """错误响应
    
    Args:
        message: 错误消息
        code: 错误码
        detail: 详细信息
    
    Returns:
        dict: 错误响应字典
    
    使用示例：
        return error("用户不存在", code=404)
        return error("参数错误", code=400, detail="缺少user_id参数")
    """
    response = {
        "code": code,
        "message": message
    }
    if detail:
        response["detail"] = detail
    return response