"""缁熶竴鍝嶅簲鏍煎紡"""
from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    """鎴愬姛鍝嶅簲"""
    code: int = Field(200, description="鐘舵€佺爜")
    message: str = Field("success", description="娑堟伅")
    data: Optional[T] = Field(None, description="鏁版嵁")


class ErrorResponse(BaseModel):
    """閿欒鍝嶅簲"""
    code: int = Field(..., description="閿欒鐮?)
    message: str = Field(..., description="閿欒娑堟伅")
    detail: Optional[str] = Field(None, description="璇︾粏淇℃伅")


def success(data: Optional[Any] = None, message: str = "success") -> dict:
    """鎴愬姛鍝嶅簲
    
    Args:
        data: 鍝嶅簲鏁版嵁
        message: 鍝嶅簲娑堟伅
    
    Returns:
        dict: 鍝嶅簲瀛楀吀
    
    浣跨敤绀轰緥锛?        return success({"id": 1, "name": "test"})
        return success(message="鎿嶄綔鎴愬姛")
    """
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error(message: str, code: int = 500, detail: Optional[str] = None) -> dict:
    """閿欒鍝嶅簲
    
    Args:
        message: 閿欒娑堟伅
        code: 閿欒鐮?        detail: 璇︾粏淇℃伅
    
    Returns:
        dict: 閿欒鍝嶅簲瀛楀吀
    
    浣跨敤绀轰緥锛?        return error("鐢ㄦ埛涓嶅瓨鍦?, code=404)
        return error("鍙傛暟閿欒", code=400, detail="缂哄皯user_id鍙傛暟")
    """
    response = {
        "code": code,
        "message": message
    }
    if detail:
        response["detail"] = detail
    return response
