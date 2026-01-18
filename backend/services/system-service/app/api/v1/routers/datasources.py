# -*- coding: utf-8 -*-
"""
数据源API路由

功能说明：
1. 数据源CRUD操作
2. 数据源测试连接
3. 数据源管理

使用示例：
    from app.api.v1.routers.datasources import router as datasources_router
    
    app.include_router(datasources_router, prefix="/api/v1/datasources", tags=["数据源"])
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from loguru import logger

from app.core.deps import get_db
from app.services.datasource_service import DataSourceService


# 创建路由器
router = APIRouter()


# ==================== Pydantic模型 ====================

class DataSourceCreate(BaseModel):
    """创建数据源请求"""
    name: str = Field(..., description="数据源名称", min_length=1, max_length=100)
    code: str = Field(..., description="数据源编码", min_length=1, max_length=50)
    type: str = Field(..., description="数据源类型（mysql/postgresql/oracle/mongodb/redis等）")
    host: str = Field(..., description="主机地址")
    port: int = Field(..., description="端口号")
    database: str = Field(..., description="数据库名称")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    description: Optional[str] = Field(None, description="描述")
    status: str = Field("active", description="状态（active/inactive）")
    tenant_id: Optional[str] = Field(None, description="租户ID")


class DataSourceUpdate(BaseModel):
    """更新数据源请求"""
    name: Optional[str] = Field(None, description="数据源名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="描述")
    status: Optional[str] = Field(None, description="状态（active/inactive）")
    username: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="密码")


class DataSourceResponse(BaseModel):
    """数据源响应"""
    id: str
    tenant_id: Optional[str]
    name: str
    code: str
    type: str
    host: str
    port: int
    database: str
    username: str
    description: Optional[str]
    status: str
    is_connected: bool
    last_connected_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class DataSourceTestRequest(BaseModel):
    """测试数据源连接请求"""
    # 使用现有的连接信息进行测试


class DataSourceTestResponse(BaseModel):
    """测试数据源连接响应"""
    success: bool
    message: str
    execution_time: float


# ==================== API端点 ====================

@router.post("/", response_model=DataSourceResponse, status_code=status.HTTP_201_CREATED)
def create_datasource(
    datasource_data: DataSourceCreate,
    db: Session = Depends(get_db)
) -> DataSourceResponse:
    """
    创建数据源
    
    Args:
        datasource_data: 数据源数据
        db: 数据库会话
    
    Returns:
        DataSourceResponse: 创建的数据源对象
    
    Raises:
        HTTPException: 数据源编码已存在
    """
    datasource_service = DataSourceService(db)
    
    try:
        datasource = datasource_service.create_datasource(datasource_data.model_dump())
        return DataSourceResponse.model_validate(datasource)
    except ValueError as e:
        logger.error(f"创建数据源失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{datasource_id}", response_model=DataSourceResponse)
def get_datasource(
    datasource_id: str,
    db: Session = Depends(get_db)
) -> DataSourceResponse:
    """
    获取数据源
    
    Args:
        datasource_id: 数据源ID
        db: 数据库会话
    
    Returns:
        DataSourceResponse: 数据源对象
    
    Raises:
        HTTPException: 数据源不存在
    """
    datasource_service = DataSourceService(db)
    
    datasource = datasource_service.get_datasource(datasource_id)
    if not datasource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据源不存在")
    
    return DataSourceResponse.model_validate(datasource)


@router.put("/{datasource_id}", response_model=DataSourceResponse)
def update_datasource(
    datasource_id: str,
    datasource_data: DataSourceUpdate,
    db: Session = Depends(get_db)
) -> DataSourceResponse:
    """
    更新数据源
    
    Args:
        datasource_id: 数据源ID
        datasource_data: 更新数据
        db: 数据库会话
    
    Returns:
        DataSourceResponse: 更新后的数据源对象
    
    Raises:
        HTTPException: 数据源不存在
    """
    datasource_service = DataSourceService(db)
    
    datasource = datasource_service.update_datasource(
        datasource_id,
        datasource_data.model_dump(exclude_none=True)
    )
    if not datasource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据源不存在")
    
    return DataSourceResponse.model_validate(datasource)


@router.delete("/{datasource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_datasource(
    datasource_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    删除数据源
    
    Args:
        datasource_id: 数据源ID
        db: 数据库会话
    
    Raises:
        HTTPException: 数据源不存在
    """
    datasource_service = DataSourceService(db)
    
    success = datasource_service.delete_datasource(datasource_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据源不存在")


@router.get("/", response_model=List[DataSourceResponse])
def list_datasources(
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    type: Optional[str] = Query(None, description="数据源类型"),
    status: Optional[str] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
) -> List[DataSourceResponse]:
    """
    获取数据源列表
    
    Args:
        tenant_id: 租户ID
        type: 数据源类型
        status: 状态
        page: 页码
        page_size: 每页数量
        db: 数据库会话
    
    Returns:
        List[DataSourceResponse]: 数据源列表
    """
    datasource_service = DataSourceService(db)
    
    datasources = datasource_service.list_datasources(
        tenant_id=tenant_id,
        type=type,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return [DataSourceResponse.model_validate(ds) for ds in datasources]


@router.post("/{datasource_id}/test", response_model=DataSourceTestResponse)
def test_datasource_connection(
    datasource_id: str,
    db: Session = Depends(get_db)
) -> DataSourceTestResponse:
    """
    测试数据源连接
    
    Args:
        datasource_id: 数据源ID
        db: 数据库会话
    
    Returns:
        DataSourceTestResponse: 测试结果
    
    Raises:
        HTTPException: 数据源不存在
    """
    datasource_service = DataSourceService(db)
    
    try:
        result = datasource_service.test_connection(datasource_id)
        return DataSourceTestResponse(
            success=result.get("success", False),
            message=result.get("message", ""),
            execution_time=result.get("execution_time", 0)
        )
    except ValueError as e:
        logger.error(f"测试数据源连接失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"测试数据源连接失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))