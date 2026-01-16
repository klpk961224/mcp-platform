"""
权限相关Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PermissionBase(BaseModel):
    """权限基础模型"""
    
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限编码")
    type: str = Field(..., description="类型")
    description: Optional[str] = Field(None, description="描述")


class PermissionCreate(PermissionBase):
    """创建权限"""
    pass


class PermissionUpdate(BaseModel):
    """更新权限"""
    
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionResponse(PermissionBase):
    """权限响应"""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PermissionListResponse(BaseModel):
    """权限列表响应"""
    
    total: int
    items: List[PermissionResponse]
    page: int
    page_size: int