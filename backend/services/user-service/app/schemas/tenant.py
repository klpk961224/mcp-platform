"""
租户相关Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TenantBase(BaseModel):
    """租户基础模型"""
    
    name: str = Field(..., description="租户名称")
    code: str = Field(..., description="租户编码")
    status: str = Field(default="active", description="状态")
    description: Optional[str] = Field(None, description="描述")


class TenantCreate(TenantBase):
    """创建租户"""
    
    pass


class TenantUpdate(BaseModel):
    """更新租户"""
    
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


class TenantResponse(TenantBase):
    """租户响应"""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    """租户列表响应"""
    
    total: int
    items: List[TenantResponse]
    page: int
    page_size: int