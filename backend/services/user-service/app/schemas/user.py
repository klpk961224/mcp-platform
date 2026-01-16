"""
用户相关Schema
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    
    username: str = Field(..., description="用户名", min_length=4, max_length=50)
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    dept_id: Optional[str] = Field(None, description="部门ID")
    position_id: Optional[str] = Field(None, description="岗位ID")
    status: str = Field(default="active", description="状态")


class UserCreate(UserBase):
    """创建用户"""
    
    password: str = Field(..., description="密码", min_length=6)
    tenant_id: str = Field(..., description="租户ID")
    
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
    """更新用户"""
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dept_id: Optional[str] = None
    position_id: Optional[str] = None
    status: Optional[str] = None


class UserResponse(UserBase):
    """用户响应"""
    
    id: str
    tenant_id: str
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应"""
    
    total: int
    items: List[UserResponse]
    page: int
    page_size: int