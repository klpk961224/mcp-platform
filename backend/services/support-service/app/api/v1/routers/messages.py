"""
站内信API路由

提供站内信管理的REST API
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.message_service import MessageService


router = APIRouter(prefix="/messages", tags=["站内信管理"])


@router.get("", summary="获取站内信列表")
async def get_messages(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    type: Optional[str] = Query(None, description="类型"),
    sender_id: Optional[str] = Query(None, description="发送者ID"),
    receiver_id: Optional[str] = Query(None, description="接收者ID"),
    status: Optional[str] = Query(None, description="状态"),
    title: Optional[str] = Query(None, description="标题（模糊搜索）"),
    content: Optional[str] = Query(None, description="内容（模糊搜索）"),
    db: Session = Depends(get_db)
):
    """
    获取站内信列表

    支持分页、搜索和筛选
    """
    service = MessageService(db)

    # 构建查询参数
    query_params = {}
    if tenant_id:
        query_params["tenant_id"] = tenant_id
    if type:
        query_params["type"] = type
    if sender_id:
        query_params["sender_id"] = sender_id
    if receiver_id:
        query_params["receiver_id"] = receiver_id
    if status:
        query_params["status"] = status
    if title:
        query_params["title"] = title
    if content:
        query_params["content"] = content

    # 计算偏移量
    skip = (page - 1) * page_size

    # 搜索站内信
    result = service.search_messages(query_params, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/{message_id}", summary="获取站内信详情")
async def get_message_detail(
    message_id: str,
    db: Session = Depends(get_db)
):
    """
    获取站内信详情

    根据站内信ID获取详细信息
    """
    service = MessageService(db)
    message = service.get_message_by_id(message_id)

    if not message:
        raise HTTPException(status_code=404, detail="站内信不存在")

    return {
        "success": True,
        "data": message
    }


@router.get("/receiver/{receiver_id}", summary="根据接收者获取站内信")
async def get_messages_by_receiver(
    receiver_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    根据接收者获取站内信

    根据接收者ID获取站内信列表
    """
    service = MessageService(db)

    # 计算偏移量
    skip = (page - 1) * page_size

    # 获取站内信
    result = service.get_messages_by_receiver(receiver_id, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/receiver/{receiver_id}/unread", summary="获取未读站内信")
async def get_unread_messages(
    receiver_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取未读站内信

    根据接收者ID获取未读站内信列表
    """
    service = MessageService(db)

    # 计算偏移量
    skip = (page - 1) * page_size

    # 获取未读站内信
    result = service.get_unread_messages_by_receiver(receiver_id, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/receiver/{receiver_id}/unread-count", summary="获取未读站内信数量")
async def get_unread_count(
    receiver_id: str,
    db: Session = Depends(get_db)
):
    """
    获取未读站内信数量

    根据接收者ID获取未读站内信数量
    """
    service = MessageService(db)
    count = service.get_unread_count(receiver_id)

    return {
        "success": True,
        "data": {
            "unread_count": count
        }
    }


@router.post("", summary="创建站内信")
async def create_message(
    tenant_id: str = Query(..., description="租户ID"),
    type: str = Query(..., description="类型"),
    title: str = Query(..., description="标题"),
    content: Optional[str] = Query(None, description="内容"),
    sender_id: Optional[str] = Query(None, description="发送者ID"),
    receiver_id: Optional[str] = Query(None, description="接收者ID"),
    receiver_type: str = Query("user", description="接收者类型"),
    priority: int = Query(1, description="优先级"),
    db: Session = Depends(get_db)
):
    """
    创建站内信

    创建新的站内信
    """
    service = MessageService(db)

    message = service.create_message(
        tenant_id=tenant_id,
        type=type,
        title=title,
        content=content,
        sender_id=sender_id,
        receiver_id=receiver_id,
        receiver_type=receiver_type,
        priority=priority
    )

    return {
        "success": True,
        "data": message,
        "message": "站内信创建成功"
    }


@router.put("/{message_id}", summary="更新站内信")
async def update_message(
    message_id: str,
    title: Optional[str] = Query(None, description="标题"),
    content: Optional[str] = Query(None, description="内容"),
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
):
    """
    更新站内信

    更新站内信信息
    """
    service = MessageService(db)
    message = service.update_message(
        message_id=message_id,
        title=title,
        content=content,
        status=status
    )

    if not message:
        raise HTTPException(status_code=404, detail="站内信不存在")

    return {
        "success": True,
        "data": message,
        "message": "站内信更新成功"
    }


@router.delete("/{message_id}", summary="删除站内信")
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """
    删除站内信

    根据站内信ID删除站内信
    """
    service = MessageService(db)
    success = service.delete_message(message_id)

    if not success:
        raise HTTPException(status_code=404, detail="站内信不存在")

    return {
        "success": True,
        "message": "站内信删除成功"
    }


@router.post("/{message_id}/read", summary="标记站内信为已读")
async def mark_message_as_read(
    message_id: str,
    user_id: str = Query(..., description="用户ID"),
    db: Session = Depends(get_db)
):
    """
    标记站内信为已读

    标记站内信为已读状态
    """
    service = MessageService(db)
    success = service.mark_as_read(message_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="站内信不存在或无权限")

    return {
        "success": True,
        "message": "站内信已标记为已读"
    }


@router.get("/receiver/{receiver_id}/statistics", summary="获取站内信统计")
async def get_message_statistics(
    receiver_id: str,
    db: Session = Depends(get_db)
):
    """
    获取站内信统计

    获取站内信的统计信息，包括总数、未读数、已读数
    """
    service = MessageService(db)
    statistics = service.get_statistics(receiver_id)

    return {
        "success": True,
        "data": statistics
    }