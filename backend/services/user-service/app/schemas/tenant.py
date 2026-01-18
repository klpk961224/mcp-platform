"""
绉熸埛鐩稿叧Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TenantBase(BaseModel):
    """绉熸埛鍩虹妯″瀷"""
    
    name: str = Field(..., description="绉熸埛鍚嶇О")
    code: str = Field(..., description="绉熸埛缂栫爜")
    status: str = Field(default="active", description="鐘舵€?)
    description: Optional[str] = Field(None, description="鎻忚堪")


class TenantCreate(TenantBase):
    """鍒涘缓绉熸埛"""
    
    pass


class TenantUpdate(BaseModel):
    """鏇存柊绉熸埛"""
    
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


class TenantResponse(TenantBase):
    """绉熸埛鍝嶅簲"""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    """绉熸埛鍒楄〃鍝嶅簲"""
    
    total: int
    items: List[TenantResponse]
    page: int
    page_size: int
