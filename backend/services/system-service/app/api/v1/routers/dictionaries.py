# -*- coding: utf-8 -*-
"""
字典API路由

功能说明：
1. 字典CRUD操作
2. 字典项管理
3. 字典缓存管理

使用示例：
    from app.api.v1.routers.dictionaries import router as dictionaries_router
    
    app.include_router(dictionaries_router, prefix="/api/v1/dictionaries", tags=["字典"])
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from loguru import logger

from common.database.session import get_db
from app.services.dict_service import DictService


# 创建路由器
router = APIRouter()


# ==================== Pydantic模型 ====================

class DictionaryCreate(BaseModel):
    """创建字典请求"""
    name: str = Field(..., description="字典名称", min_length=1, max_length=100)
    code: str = Field(..., description="字典编码", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="描述")
    status: str = Field("active", description="状态（active/inactive）")
    tenant_id: Optional[str] = Field(None, description="租户ID")


class DictionaryUpdate(BaseModel):
    """更新字典请求"""
    name: Optional[str] = Field(None, description="字典名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="描述")
    status: Optional[str] = Field(None, description="状态（active/inactive）")


class DictionaryResponse(BaseModel):
    """字典响应"""
    id: str
    tenant_id: Optional[str]
    name: str
    code: str
    description: Optional[str]
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class DictionaryItemCreate(BaseModel):
    """创建字典项请求"""
    label: str = Field(..., description="标签", min_length=1, max_length=100)
    value: str = Field(..., description="值", min_length=1, max_length=100)
    sort_order: int = Field(0, description="排序")
    description: Optional[str] = Field(None, description="描述")
    status: str = Field("active", description="状态（active/inactive）")


class DictionaryItemUpdate(BaseModel):
    """更新字典项请求"""
    label: Optional[str] = Field(None, description="标签", min_length=1, max_length=100)
    value: Optional[str] = Field(None, description="值", min_length=1, max_length=100)
    sort_order: Optional[int] = Field(None, description="排序")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[str] = Field(None, description="状态（active/inactive）")


class DictionaryItemResponse(BaseModel):
    """字典项响应"""
    id: str
    dictionary_id: str
    label: str
    value: str
    sort_order: int
    description: Optional[str]
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


# ==================== API端点 ====================

@router.post("/", response_model=DictionaryResponse, status_code=status.HTTP_201_CREATED)
def create_dictionary(
    dictionary_data: DictionaryCreate,
    db: Session = Depends(get_db)
) -> DictionaryResponse:
    """
    创建字典
    
    Args:
        dictionary_data: 字典数据
        db: 数据库会话
    
    Returns:
        DictionaryResponse: 创建的字典对象
    
    Raises:
        HTTPException: 字典编码已存在
    """
    dict_service = DictService(db)
    
    try:
        dictionary = dict_service.create_dictionary(dictionary_data.model_dump())
        return DictionaryResponse.model_validate(dictionary)
    except ValueError as e:
        logger.error(f"创建字典失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{dictionary_id}", response_model=DictionaryResponse)
def get_dictionary(
    dictionary_id: str,
    db: Session = Depends(get_db)
) -> DictionaryResponse:
    """
    获取字典
    
    Args:
        dictionary_id: 字典ID
        db: 数据库会话
    
    Returns:
        DictionaryResponse: 字典对象
    
    Raises:
        HTTPException: 字典不存在
    """
    dict_service = DictService(db)
    
    dictionary = dict_service.get_dictionary(dictionary_id)
    if not dictionary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典不存在")
    
    return DictionaryResponse.model_validate(dictionary)


@router.put("/{dictionary_id}", response_model=DictionaryResponse)
def update_dictionary(
    dictionary_id: str,
    dictionary_data: DictionaryUpdate,
    db: Session = Depends(get_db)
) -> DictionaryResponse:
    """
    更新字典
    
    Args:
        dictionary_id: 字典ID
        dictionary_data: 更新数据
        db: 数据库会话
    
    Returns:
        DictionaryResponse: 更新后的字典对象
    
    Raises:
        HTTPException: 字典不存在
    """
    dict_service = DictService(db)
    
    dictionary = dict_service.update_dictionary(
        dictionary_id,
        dictionary_data.model_dump(exclude_none=True)
    )
    if not dictionary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典不存在")
    
    return DictionaryResponse.model_validate(dictionary)


@router.delete("/{dictionary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dictionary(
    dictionary_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    删除字典
    
    Args:
        dictionary_id: 字典ID
        db: 数据库会话
    
    Raises:
        HTTPException: 字典不存在
    """
    dict_service = DictService(db)
    
    success = dict_service.delete_dictionary(dictionary_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典不存在")


@router.get("/", response_model=List[DictionaryResponse])
def list_dictionaries(
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    status: Optional[str] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
) -> List[DictionaryResponse]:
    """
    获取字典列表
    
    Args:
        tenant_id: 租户ID
        status: 状态
        page: 页码
        page_size: 每页数量
        db: 数据库会话
    
    Returns:
        List[DictionaryResponse]: 字典列表
    """
    dict_service = DictService(db)
    
    dictionaries = dict_service.list_dictionaries(
        tenant_id=tenant_id,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return [DictionaryResponse.model_validate(d) for d in dictionaries]


@router.get("/{dictionary_id}/items", response_model=List[DictionaryItemResponse])
def get_dictionary_items(
    dictionary_id: str,
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
) -> List[DictionaryItemResponse]:
    """
    获取字典项列表
    
    Args:
        dictionary_id: 字典ID
        status: 状态
        db: 数据库会话
    
    Returns:
        List[DictionaryItemResponse]: 字典项列表
    
    Raises:
        HTTPException: 字典不存在
    """
    dict_service = DictService(db)
    
    items = dict_service.get_dictionary_items(dictionary_id, status=status)
    return [DictionaryItemResponse.model_validate(item) for item in items]


@router.post("/{dictionary_id}/items", response_model=DictionaryItemResponse, status_code=status.HTTP_201_CREATED)
def create_dictionary_item(
    dictionary_id: str,
    item_data: DictionaryItemCreate,
    db: Session = Depends(get_db)
) -> DictionaryItemResponse:
    """
    创建字典项
    
    Args:
        dictionary_id: 字典ID
        item_data: 字典项数据
        db: 数据库会话
    
    Returns:
        DictionaryItemResponse: 创建的字典项对象
    
    Raises:
        HTTPException: 字典不存在
    """
    dict_service = DictService(db)
    
    try:
        item = dict_service.create_dictionary_item(dictionary_id, item_data.model_dump())
        return DictionaryItemResponse.model_validate(item)
    except ValueError as e:
        logger.error(f"创建字典项失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{dictionary_id}/items/{item_id}", response_model=DictionaryItemResponse)
def update_dictionary_item(
    dictionary_id: str,
    item_id: str,
    item_data: DictionaryItemUpdate,
    db: Session = Depends(get_db)
) -> DictionaryItemResponse:
    """
    更新字典项
    
    Args:
        dictionary_id: 字典ID
        item_id: 字典项ID
        item_data: 更新数据
        db: 数据库会话
    
    Returns:
        DictionaryItemResponse: 更新后的字典项对象
    
    Raises:
        HTTPException: 字典项不存在
    """
    dict_service = DictService(db)
    
    item = dict_service.update_dictionary_item(
        dictionary_id,
        item_id,
        item_data.model_dump(exclude_none=True)
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典项不存在")
    
    return DictionaryItemResponse.model_validate(item)


@router.delete("/{dictionary_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dictionary_item(
    dictionary_id: str,
    item_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    删除字典项
    
    Args:
        dictionary_id: 字典ID
        item_id: 字典项ID
        db: 数据库会话
    
    Raises:
        HTTPException: 字典项不存在
    """
    dict_service = DictService(db)
    
    success = dict_service.delete_dictionary_item(dictionary_id, item_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="字典项不存在")


@router.get("/code/{code}", response_model=List[DictionaryItemResponse])
def get_dictionary_by_code(
    code: str,
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
) -> List[DictionaryItemResponse]:
    """
    根据编码获取字典项
    
    Args:
        code: 字典编码
        status: 状态
        db: 数据库会话
    
    Returns:
        List[DictionaryItemResponse]: 字典项列表
    
    Raises:
        HTTPException: 字典不存在
    """
    dict_service = DictService(db)
    
    items = dict_service.get_dictionary_by_code(code, status=status)
    return [DictionaryItemResponse.model_validate(item) for item in items]