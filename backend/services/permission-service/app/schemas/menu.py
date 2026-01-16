"""
菜单相关Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MenuBase(BaseModel):
    """菜单基础模型"""
    
    name: str = Field(..., description="菜单名称")
    path: Optional[str] = Field(None, description="菜单路径")
    icon: Optional[str] = Field(None, description="菜单图标")
    parent_id: Optional[str] = Field(None, description="父菜单ID")
    sort_order: int = Field(default=0, description="排序")
    is_visible: bool = Field(default=True, description="是否可见")
    status: str = Field(default="active", description="状态")


class MenuCreate(MenuBase):
    """创建菜单"""
    
    tenant_id: str = Field(..., description="租户ID")


class MenuUpdate(BaseModel):
    """更新菜单"""
    
    name: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: Optional[int] = None
    is_visible: Optional[bool] = None
    status: Optional[str] = None


class MenuResponse(MenuBase):
    """菜单响应"""
    
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MenuTreeResponse(MenuResponse):
    """菜单树响应"""
    
    children: List['MenuTreeResponse'] = []


class MenuListResponse(BaseModel):
    """菜单列表响应"""
    
    total: int
    items: List[MenuResponse]
    page: int
    page_size: int