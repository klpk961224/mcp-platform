"""
鑿滃崟鐩稿叧Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MenuBase(BaseModel):
    """鑿滃崟鍩虹妯″瀷"""
    
    name: str = Field(..., description="鑿滃崟名称")
    path: Optional[str] = Field(None, description="鑿滃崟璺緞")
    icon: Optional[str] = Field(None, description="鑿滃崟鍥炬爣")
    parent_id: Optional[str] = Field(None, description="鐖惰彍鍗旾D")
    sort_order: int = Field(default=0, description="排序")
    is_visible: bool = Field(default=True, description="鏄惁鍙")
    status: str = Field(default="active", description="状态?)


class MenuCreate(MenuBase):
    """创建鑿滃崟"""
    
    tenant_id: str = Field(..., description="租户ID")


class MenuUpdate(BaseModel):
    """更新鑿滃崟"""
    
    name: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: Optional[int] = None
    is_visible: Optional[bool] = None
    status: Optional[str] = None


class MenuResponse(MenuBase):
    """鑿滃崟鍝嶅簲"""
    
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MenuTreeResponse(MenuResponse):
    """鑿滃崟鏍戝搷搴?""
    
    children: List['MenuTreeResponse'] = []


class MenuListResponse(BaseModel):
    """鑿滃崟鍒楄〃鍝嶅簲"""
    
    total: int
    items: List[MenuResponse]
    page: int
    page_size: int
