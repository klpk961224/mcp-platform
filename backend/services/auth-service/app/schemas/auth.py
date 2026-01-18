"""
认证相关Schema

功能说明：
1. 定义请求和响应的数据模型
2. 数据验证

使用示例：
    from app.schemas.auth import LoginRequest, LoginResponse
    
    @router.post("/login", response_model=LoginResponse)
    async def login(request: LoginRequest):
        return LoginResponse(access_token="xxx", refresh_token="yyy")
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """登录请求"""
    
    username: str = Field(..., description="用户名", min_length=4, max_length=50)
    password: str = Field(..., description="密码", min_length=6)
    tenant_code: Optional[str] = Field(None, description="租户编码")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "123456",
                "tenant_code": "default"
            }
        }


class LoginResponse(BaseModel):
    """登录响应"""
    
    access_token: str = Field(..., description="访问Token")
    refresh_token: str = Field(..., description="刷新Token")
    token_type: str = Field(default="bearer", description="Token类型")
    expires_in: int = Field(..., description="过期时间（秒）")
    user_info: dict = Field(..., description="用户信息")
    
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
    """刷新Token请求"""
    
    refresh_token: str = Field(..., description="刷新Token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshTokenResponse(BaseModel):
    """刷新Token响应"""
    
    access_token: str = Field(..., description="新的访问Token")
    token_type: str = Field(default="bearer", description="Token类型")
    expires_in: int = Field(..., description="过期时间（秒）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400
            }
        }


class LogoutResponse(BaseModel):
    """登出响应"""
    
    message: str = Field(default="登出成功", description="消息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "登出成功"
            }
        }


class RegisterRequest(BaseModel):
    """注册请求"""
    
    username: str = Field(..., description="用户名", min_length=4, max_length=50)
    password: str = Field(..., description="密码", min_length=6)
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    tenant_code: Optional[str] = Field(None, description="租户编码")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "newuser",
                "password": "123456",
                "email": "newuser@example.com",
                "phone": "13800138000",
                "tenant_code": "default"
            }
        }


class RegisterResponse(BaseModel):
    """注册响应"""
    
    message: str = Field(default="注册成功", description="消息")
    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "注册成功",
                "user_id": "123",
                "username": "newuser",
                "email": "newuser@example.com"
            }
        }