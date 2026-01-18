"""
瑙掕壊鐩稿叧Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    """瑙掕壊鍩虹妯″瀷"""
    
    name: str = Field(..., description="瑙掕壊鍚嶇О")
    code: str = Field(..., description="瑙掕壊缂栫爜")
    description: Optional[str] = Field(None, description="鎻忚堪")
    status: str = Field(default="active", description="鐘舵€?)


class RoleCreate(RoleBase):
    """鍒涘缓瑙掕壊"""
    
    tenant_id: str = Field(..., description="绉熸埛ID")


class RoleUpdate(BaseModel):
    """鏇存柊瑙掕壊"""
    
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class RoleResponse(RoleBase):
    """瑙掕壊鍝嶅簲"""
    
    id: str
    tenant_id: str
    is_system: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """瑙掕壊鍒楄〃鍝嶅簲"""
    
    total: int
    items: List[RoleResponse]
    page: int
    page_size: int
