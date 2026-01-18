"""
部门相关Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DepartmentBase(BaseModel):
    """部门基础模型"""
    
    name: str = Field(..., description="部门名称")
    code: str = Field(..., description="部门编码")
    parent_id: Optional[str] = Field(None, description="父部门ID")
    level: int = Field(default=1, description="层级")
    sort_order: int = Field(default=0, description="排序")
    status: str = Field(default="active", description="状态")


class DepartmentCreate(DepartmentBase):
    """创建部门"""
    
    tenant_id: str = Field(..., description="租户ID")


class DepartmentUpdate(BaseModel):
    """更新部门"""
    
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    """部门响应"""
    
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DepartmentTreeResponse(DepartmentResponse):
    """部门树响应"""
    
    children: List['DepartmentTreeResponse'] = []


class DepartmentListResponse(BaseModel):
    """部门列表响应"""
    
    total: int
    items: List[DepartmentResponse]
    page: int
    page_size: int