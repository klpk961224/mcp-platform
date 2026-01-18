"""
閮ㄩ棬鐩稿叧Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DepartmentBase(BaseModel):
    """閮ㄩ棬鍩虹妯″瀷"""
    
    name: str = Field(..., description="部门名称")
    code: str = Field(..., description="部门编码")
    parent_id: Optional[str] = Field(None, description="鐖堕儴闂↖D")
    level: int = Field(default=1, description="灞傜骇")
    sort_order: int = Field(default=0, description="排序")
    status: str = Field(default="active", description="状态?)


class DepartmentCreate(DepartmentBase):
    """创建閮ㄩ棬"""
    
    tenant_id: str = Field(..., description="租户ID")


class DepartmentUpdate(BaseModel):
    """更新閮ㄩ棬"""
    
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    """閮ㄩ棬鍝嶅簲"""
    
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DepartmentTreeResponse(DepartmentResponse):
    """閮ㄩ棬鏍戝搷搴?""
    
    children: List['DepartmentTreeResponse'] = []


class DepartmentListResponse(BaseModel):
    """閮ㄩ棬鍒楄〃鍝嶅簲"""
    
    total: int
    items: List[DepartmentResponse]
    page: int
    page_size: int
