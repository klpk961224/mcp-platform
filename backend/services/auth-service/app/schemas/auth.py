"""
璁よ瘉鐩稿叧Schema

鍔熻兘璇存槑锛?1. 瀹氫箟璇锋眰鍜屽搷搴旂殑鏁版嵁妯″瀷
2. 鏁版嵁楠岃瘉

浣跨敤绀轰緥锛?    from app.schemas.auth import LoginRequest, LoginResponse
    
    @router.post("/login", response_model=LoginResponse)
    async def login(request: LoginRequest):
        return LoginResponse(access_token="xxx", refresh_token="yyy")
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """鐧诲綍璇锋眰"""
    
    username: str = Field(..., description="鐢ㄦ埛鍚?, min_length=4, max_length=50)
    password: str = Field(..., description="瀵嗙爜", min_length=6)
    tenant_code: Optional[str] = Field(None, description="绉熸埛缂栫爜")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "123456",
                "tenant_code": "default"
            }
        }


class LoginResponse(BaseModel):
    """鐧诲綍鍝嶅簲"""
    
    access_token: str = Field(..., description="璁块棶Token")
    refresh_token: str = Field(..., description="鍒锋柊Token")
    token_type: str = Field(default="bearer", description="Token绫诲瀷")
    expires_in: int = Field(..., description="杩囨湡鏃堕棿锛堢锛?)
    user_info: dict = Field(..., description="鐢ㄦ埛淇℃伅")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400,
                "user_info": {
                    "id": "123",
                    "username": "admin",
                    "email": "admin@example.com"
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    """鍒锋柊Token璇锋眰"""
    
    refresh_token: str = Field(..., description="鍒锋柊Token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshTokenResponse(BaseModel):
    """鍒锋柊Token鍝嶅簲"""
    
    access_token: str = Field(..., description="鏂扮殑璁块棶Token")
    token_type: str = Field(default="bearer", description="Token绫诲瀷")
    expires_in: int = Field(..., description="杩囨湡鏃堕棿锛堢锛?)
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400
            }
        }


class LogoutResponse(BaseModel):
    """鐧诲嚭鍝嶅簲"""
    
    message: str = Field(default="鐧诲嚭鎴愬姛", description="娑堟伅")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "鐧诲嚭鎴愬姛"
            }
        }


class RegisterRequest(BaseModel):
    """娉ㄥ唽璇锋眰"""
    
    username: str = Field(..., description="鐢ㄦ埛鍚?, min_length=4, max_length=50)
    password: str = Field(..., description="瀵嗙爜", min_length=6)
    email: EmailStr = Field(..., description="閭")
    phone: Optional[str] = Field(None, description="鎵嬫満鍙?)
    tenant_code: Optional[str] = Field(None, description="绉熸埛缂栫爜")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "newuser",
                "password": "123456",
                "email": "newuser@example.com",
                "phone": "132800138000",
                "tenant_code": "default"
            }
        }


class RegisterResponse(BaseModel):
    """娉ㄥ唽鍝嶅簲"""
    
    message: str = Field(default="娉ㄥ唽鎴愬姛", description="娑堟伅")
    user_id: str = Field(..., description="鐢ㄦ埛ID")
    username: str = Field(..., description="鐢ㄦ埛鍚?)
    email: str = Field(..., description="閭")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "娉ㄥ唽鎴愬姛",
                "user_id": "123",
                "username": "newuser",
                "email": "newuser@example.com"
            }
        }
