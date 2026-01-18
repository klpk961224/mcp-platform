"""
角色相关Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    """角色基础模型"""
    
    name: str = Field(..., description="角色名称")
    code: str = Field(..., description="角色编码")
    description: Optional[str] = Field(None, description="描述")
    status: str = Field(default="active", description="状态")


class RoleCreate(RoleBase):
    """创建角色"""
    
    tenant_id: str = Field(..., description="租户ID")


class RoleUpdate(BaseModel):
    """更新角色"""
    
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class RoleResponse(RoleBase):
    """角色响应"""
    
    id: str
    tenant_id: str
    is_system: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """角色列表响应"""
    
    total: int
    items: List[RoleResponse]
    page: int
    page_size: int