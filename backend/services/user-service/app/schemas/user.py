"""
鐢ㄦ埛鐩稿叧Schema
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """鐢ㄦ埛鍩虹妯″瀷"""
    
    username: str = Field(..., description="鐢ㄦ埛鍚?, min_length=4, max_length=50)
    email: Optional[EmailStr] = Field(None, description="閭")
    phone: Optional[str] = Field(None, description="鎵嬫満鍙?)
    dept_id: Optional[str] = Field(None, description="閮ㄩ棬ID")
    position_id: Optional[str] = Field(None, description="宀椾綅ID")
    status: str = Field(default="active", description="鐘舵€?)


class UserCreate(UserBase):
    """鍒涘缓鐢ㄦ埛"""
    
    password: str = Field(..., description="瀵嗙爜", min_length=6)
    tenant_id: str = Field(..., description="绉熸埛ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "123456",
                "email": "test@example.com",
                "tenant_id": "default"
            }
        }


class UserUpdate(BaseModel):
    """鏇存柊鐢ㄦ埛"""
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dept_id: Optional[str] = None
    position_id: Optional[str] = None
    status: Optional[str] = None


class UserResponse(UserBase):
    """鐢ㄦ埛鍝嶅簲"""
    
    id: str
    tenant_id: str
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """鐢ㄦ埛鍒楄〃鍝嶅簲"""
    
    total: int
    items: List[UserResponse]
    page: int
    page_size: int
