# -*- coding: utf-8 -*-
"""
待办任务API路由

功能说明：
1. 待办任务CRUD操作
2. 任务状态管理
3. 任务提醒

使用示例：
    from app.api.v1.routers.todos import router as todos_router
    
    app.include_router(todos_router, prefix="/api/v1/todos", tags=["待办任务"])
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from loguru import logger
from datetime import datetime

from app.core.deps import get_db
from app.services.todo_service import TodoService


# 创建路由器
router = APIRouter()


# ==================== Pydantic模型 ====================

class TodoTaskCreate(BaseModel):
    """创建待办任务请求"""
    title: str = Field(..., description="任务标题", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="任务描述")
    task_type: str = Field("personal", description="任务类型")
    priority: str = Field("medium", description="优先级")
    due_date: Optional[datetime] = Field(None, description="截止日期")
    due_time: Optional[str] = Field(None, description="截止时间")
    tags: Optional[List[str]] = Field(None, description="标签")
    attachment: Optional[str] = Field(None, description="附件URL")
    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    tenant_id: Optional[str] = Field(None, description="租户ID")


class TodoTaskUpdate(BaseModel):
    """更新待办任务请求"""
    title: Optional[str] = Field(None, description="任务标题", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="任务描述")
    priority: Optional[str] = Field(None, description="优先级")
    due_date: Optional[datetime] = Field(None, description="截止日期")
    due_time: Optional[str] = Field(None, description="截止时间")
    tags: Optional[List[str]] = Field(None, description="标签")
    attachment: Optional[str] = Field(None, description="附件URL")


class TodoTaskResponse(BaseModel):
    """待办任务响应"""
    id: str
    tenant_id: Optional[str]
    user_id: str
    username: str
    title: str
    description: Optional[str]
    task_type: str
    priority: str
    status: str
    due_date: Optional[str]
    due_time: Optional[str]
    tags: Optional[List[str]]
    attachment: Optional[str]
    completed_at: Optional[str]
    is_overdue: bool
    reminder_sent: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


# ==================== API端点 ====================

@router.post("/", response_model=TodoTaskResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoTaskCreate,
    db: Session = Depends(get_db)
) -> TodoTaskResponse:
    """
    创建待办任务
    
    Args:
        todo_data: 待办任务数据
        db: 数据库会话
    
    Returns:
        TodoTaskResponse: 创建的待办任务对象
    """
    todo_service = TodoService(db)
    
    try:
        todo = todo_service.create_todo(todo_data.model_dump())
        return TodoTaskResponse.model_validate(todo)
    except ValueError as e:
        logger.error(f"创建待办任务失败: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{todo_id}", response_model=TodoTaskResponse)
def get_todo(
    todo_id: str,
    db: Session = Depends(get_db)
) -> TodoTaskResponse:
    """
    获取待办任务
    
    Args:
        todo_id: 待办任务ID
        db: 数据库会话
    
    Returns:
        TodoTaskResponse: 待办任务对象
    
    Raises:
        HTTPException: 待办任务不存在
    """
    todo_service = TodoService(db)
    
    todo = todo_service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待办任务不存在")
    
    return TodoTaskResponse.model_validate(todo)


@router.put("/{todo_id}", response_model=TodoTaskResponse)
def update_todo(
    todo_id: str,
    todo_data: TodoTaskUpdate,
    db: Session = Depends(get_db)
) -> TodoTaskResponse:
    """
    更新待办任务
    
    Args:
        todo_id: 待办任务ID
        todo_data: 更新数据
        db: 数据库会话
    
    Returns:
        TodoTaskResponse: 更新后的待办任务对象
    
    Raises:
        HTTPException: 待办任务不存在
    """
    todo_service = TodoService(db)
    
    todo = todo_service.update_todo(todo_id, todo_data.model_dump(exclude_none=True))
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待办任务不存在")
    
    return TodoTaskResponse.model_validate(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    删除待办任务
    
    Args:
        todo_id: 待办任务ID
        db: 数据库会话
    
    Raises:
        HTTPException: 待办任务不存在
    """
    todo_service = TodoService(db)
    
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待办任务不存在")


@router.get("/", response_model=List[TodoTaskResponse])
def list_todos(
    user_id: Optional[str] = Query(None, description="用户ID"),
    status: Optional[str] = Query(None, description="状态"),
    task_type: Optional[str] = Query(None, description="任务类型"),
    priority: Optional[str] = Query(None, description="优先级"),
    is_overdue: Optional[bool] = Query(None, description="是否逾期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
) -> List[TodoTaskResponse]:
    """
    获取待办任务列表
    
    Args:
        user_id: 用户ID（可选）
        status: 状态
        task_type: 任务类型
        priority: 优先级
        is_overdue: 是否逾期
        page: 页码
        page_size: 每页数量
        db: 数据库会话
    
    Returns:
        List[TodoTaskResponse]: 待办任务列表
    """
    todo_service = TodoService(db)
    
    # 如果没有提供user_id，返回空列表
    if not user_id:
        return []
    
    todos = todo_service.list_todos(
        user_id=user_id,
        status=status,
        task_type=task_type,
        priority=priority,
        is_overdue=is_overdue,
        page=page,
        page_size=page_size
    )
    
    return [TodoTaskResponse.model_validate(todo) for todo in todos]


@router.post("/{todo_id}/complete", response_model=TodoTaskResponse)
def complete_todo(
    todo_id: str,
    db: Session = Depends(get_db)
) -> TodoTaskResponse:
    """
    完成待办任务
    
    Args:
        todo_id: 待办任务ID
        db: 数据库会话
    
    Returns:
        TodoTaskResponse: 更新后的待办任务对象
    
    Raises:
        HTTPException: 待办任务不存在
    """
    todo_service = TodoService(db)
    
    todo = todo_service.complete_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待办任务不存在")
    
    return TodoTaskResponse.model_validate(todo)


@router.post("/{todo_id}/uncomplete", response_model=TodoTaskResponse)
def uncomplete_todo(
    todo_id: str,
    db: Session = Depends(get_db)
) -> TodoTaskResponse:
    """
    取消完成待办任务
    
    Args:
        todo_id: 待办任务ID
        db: 数据库会话
    
    Returns:
        TodoTaskResponse: 更新后的待办任务对象
    
    Raises:
        HTTPException: 待办任务不存在
    """
    todo_service = TodoService(db)
    
    todo = todo_service.uncomplete_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待办任务不存在")
    
    return TodoTaskResponse.model_validate(todo)