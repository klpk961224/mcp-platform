# -*- coding: utf-8 -*-
"""
MCP工具API路由

功能说明：
1. MCP工具CRUD操作
2. MCP工具调用
3. MCP工具监控

使用示例：
    from app.api.v1.routers.mcp_tools import router as mcp_tools_router
    
    app.include_router(mcp_tools_router, prefix="/api/v1/mcp-tools", tags=["MCP工具"])
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from loguru import logger

from common.database.session import get_db
from app.services.mcp_tool_service import MCPToolService


# 创建路由器
router = APIRouter()


# ==================== Pydantic模型 ====================

class MCPToolCreate(BaseModel):
    """创建MCP工具请求"""
    name: str = Field(..., description="工具名称", min_length=1, max_length=100)
    code: str = Field(..., description="工具编码", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="工具描述")
    api_endpoint: str = Field(..., description="API端点")
    api_method: str = Field("GET", description="API方法（GET/POST/PUT/DELETE）")
    api_timeout: int = Field(30, description="API超时时间（秒）")
    api_retry_count: int = Field(3, description="API重试次数")
    status: str = Field("active", description="状态（active/inactive）")
    is_public: bool = Field(False, description="是否公开")
    required_permissions: Optional[List[str]] = Field(None, description="所需权限")
    rate_limit: Optional[int] = Field(None, description="速率限制（次/分钟）")
    tenant_id: Optional[str] = Field(None, description="租户ID")


class MCPToolUpdate(BaseModel):
    """更新MCP工具请求"""
    name: Optional[str] = Field(None, description="工具名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="工具描述")
    api_endpoint: Optional[str] = Field(None, description="API端点")
    api_method: Optional[str] = Field(None, description="API方法（GET/POST/PUT/DELETE）")
    api_timeout: Optional[int] = Field(None, description="API超时时间（秒）")
    api_retry_count: Optional[int] = Field(None, description="API重试次数")
    status: Optional[str] = Field(None, description="状态（active/inactive）")
    is_public: Optional[bool] = Field(None, description="是否公开")
    required_permissions: Optional[List[str]] = Field(None, description="所需权限")
    rate_limit: Optional[int] = Field(None, description="速率限制（次/分钟）")


class MCPToolResponse(BaseModel):
    """MCP工具响应"""
    id: str
    tenant_id: Optional[str]
    name: str
    code: str
    description: Optional[str]
    api_endpoint: str
    api_method: str
    api_timeout: int
    api_retry_count: int
    status: str
    is_public: bool
    required_permissions: Optional[List[str]]
    rate_limit: Optional[int]
    call_count: int
    last_called_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class MCPToolCallRequest(BaseModel):
    """调用MCP工具请求"""
    params: Optional[Dict[str, Any]] = Field(None, description="调用参数")


class MCPToolCallResponse(BaseModel):
    """调用MCP工具响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float


# ==================== API端点 ====================

@router.post("/", response_model=MCPToolResponse, status_code=status.HTTP_201_CREATED)
def create_tool(
    tool_data: MCPToolCreate,
    db: Session = Depends(get_db)
) -> MCPToolResponse:
    """
    创建MCP工具
    
    Args:
        tool_data: 工具数据
        db: 数据库会话
    
    Returns:
        MCPToolResponse: 创建的工具对象
    
    Raises:
        HTTPException: 工具编码已存在
    """
    tool_service = MCPToolService(db)
    
    try:
        tool = tool_service.create_tool(tool_data.model_dump())
        return MCPToolResponse.model_validate(tool)
    except ValueError as e:
        logger.error(f"创建MCP工具失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{tool_id}", response_model=MCPToolResponse)
def get_tool(
    tool_id: str,
    db: Session = Depends(get_db)
) -> MCPToolResponse:
    """
    获取MCP工具
    
    Args:
        tool_id: 工具ID
        db: 数据库会话
    
    Returns:
        MCPToolResponse: 工具对象
    
    Raises:
        HTTPException: 工具不存在
    """
    tool_service = MCPToolService(db)
    
    tool = tool_service.get_tool(tool_id)
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工具不存在")
    
    return MCPToolResponse.model_validate(tool)


@router.put("/{tool_id}", response_model=MCPToolResponse)
def update_tool(
    tool_id: str,
    tool_data: MCPToolUpdate,
    db: Session = Depends(get_db)
) -> MCPToolResponse:
    """
    更新MCP工具
    
    Args:
        tool_id: 工具ID
        tool_data: 更新数据
        db: 数据库会话
    
    Returns:
        MCPToolResponse: 更新后的工具对象
    
    Raises:
        HTTPException: 工具不存在
    """
    tool_service = MCPToolService(db)
    
    tool = tool_service.update_tool(tool_id, tool_data.model_dump(exclude_none=True))
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工具不存在")
    
    return MCPToolResponse.model_validate(tool)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool(
    tool_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    删除MCP工具
    
    Args:
        tool_id: 工具ID
        db: 数据库会话
    
    Raises:
        HTTPException: 工具不存在
    """
    tool_service = MCPToolService(db)
    
    success = tool_service.delete_tool(tool_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工具不存在")


@router.get("/", response_model=List[MCPToolResponse])
def list_tools(
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    status: Optional[str] = Query(None, description="状态"),
    is_public: Optional[bool] = Query(None, description="是否公开"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
) -> List[MCPToolResponse]:
    """
    获取MCP工具列表
    
    Args:
        tenant_id: 租户ID
        status: 状态
        is_public: 是否公开
        page: 页码
        page_size: 每页数量
        db: 数据库会话
    
    Returns:
        List[MCPToolResponse]: 工具列表
    """
    tool_service = MCPToolService(db)
    
    tools = tool_service.list_tools(
        tenant_id=tenant_id,
        status=status,
        is_public=is_public,
        page=page,
        page_size=page_size
    )
    
    return [MCPToolResponse.model_validate(tool) for tool in tools]


@router.post("/{tool_id}/call", response_model=MCPToolCallResponse)
def call_tool(
    tool_id: str,
    call_request: MCPToolCallRequest,
    db: Session = Depends(get_db)
) -> MCPToolCallResponse:
    """
    调用MCP工具
    
    Args:
        tool_id: 工具ID
        call_request: 调用请求
        db: 数据库会话
    
    Returns:
        MCPToolCallResponse: 调用结果
    
    Raises:
        HTTPException: 工具不存在或调用失败
    """
    tool_service = MCPToolService(db)
    
    try:
        result = tool_service.call_tool(tool_id, call_request.params or {})
        return MCPToolCallResponse(
            success=True,
            data=result.get("data"),
            execution_time=result.get("execution_time", 0)
        )
    except ValueError as e:
        logger.error(f"调用MCP工具失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"调用MCP工具失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{tool_id}/statistics", response_model=Dict[str, Any])
def get_tool_statistics(
    tool_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取MCP工具统计信息
    
    Args:
        tool_id: 工具ID
        db: 数据库会话
    
    Returns:
        Dict[str, Any]: 统计信息
    
    Raises:
        HTTPException: 工具不存在
    """
    tool_service = MCPToolService(db)
    
    stats = tool_service.get_tool_statistics(tool_id)
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工具不存在")
    
    return stats