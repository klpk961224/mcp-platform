"""
鏉冮檺鐩稿叧Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PermissionBase(BaseModel):
    """鏉冮檺鍩虹妯″瀷"""
    
    name: str = Field(..., description="鏉冮檺名称")
    code: str = Field(..., description="鏉冮檺编码")
    type: str = Field(..., description="类型")
    description: Optional[str] = Field(None, description="描述")


class PermissionCreate(PermissionBase):
    """创建鏉冮檺"""
    pass


class PermissionUpdate(BaseModel):
    """更新鏉冮檺"""
    
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionResponse(PermissionBase):
    """鏉冮檺鍝嶅簲"""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PermissionListResponse(BaseModel):
    """鏉冮檺鍒楄〃鍝嶅簲"""
    
    total: int
    items: List[PermissionResponse]
    page: int
    page_size: int
