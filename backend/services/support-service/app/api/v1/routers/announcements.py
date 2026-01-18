"""
通知公告API路由

提供通知公告管理的REST API
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.announcement_service import AnnouncementService


router = APIRouter(prefix="/announcements", tags=["通知公告管理"])


@router.get("", summary="获取通知公告列表")
async def get_announcements(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    type: Optional[str] = Query(None, description="类型"),
    publisher_id: Optional[str] = Query(None, description="发布者ID"),
    status: Optional[str] = Query(None, description="状态"),
    title: Optional[str] = Query(None, description="标题（模糊搜索）"),
    content: Optional[str] = Query(None, description="内容（模糊搜索）"),
    is_top: Optional[int] = Query(None, description="是否置顶"),
    db: Session = Depends(get_db)
):
    """
    获取通知公告列表

    支持分页、搜索和筛选
    """
    service = AnnouncementService(db)

    # 构建查询参数
    query_params = {}
    if tenant_id:
        query_params["tenant_id"] = tenant_id
    if type:
        query_params["type"] = type
    if publisher_id:
        query_params["publisher_id"] = publisher_id
    if status:
        query_params["status"] = status
    if title:
        query_params["title"] = title
    if content:
        query_params["content"] = content
    if is_top is not None:
        query_params["is_top"] = is_top

    # 计算偏移量
    skip = (page - 1) * page_size

    # 搜索通知公告
    result = service.search_announcements(query_params, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/published", summary="获取已发布通知公告")
async def get_published_announcements(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取已发布通知公告

    获取所有已发布的通知公告列表
    """
    service = AnnouncementService(db)

    # 计算偏移量
    skip = (page - 1) * page_size

    # 获取已发布通知公告
    result = service.get_published_announcements(skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/{announcement_id}", summary="获取通知公告详情")
async def get_announcement_detail(
    announcement_id: str,
    db: Session = Depends(get_db)
):
    """
    获取通知公告详情

    根据通知公告ID获取详细信息
    """
    service = AnnouncementService(db)
    announcement = service.get_announcement_by_id(announcement_id)

    if not announcement:
        raise HTTPException(status_code=404, detail="通知公告不存在")

    return {
        "success": True,
        "data": announcement
    }


@router.get("/{announcement_id}/read-count", summary="获取阅读数量")
async def get_read_count(
    announcement_id: str,
    db: Session = Depends(get_db)
):
    """
    获取阅读数量

    根据通知公告ID获取阅读数量
    """
    service = AnnouncementService(db)
    count = service.get_read_count(announcement_id)

    return {
        "success": True,
        "data": {
            "read_count": count
        }
    }


@router.post("", summary="创建通知公告")
async def create_announcement(
    tenant_id: str = Query(..., description="租户ID"),
    type: str = Query(..., description="类型"),
    title: str = Query(..., description="标题"),
    content: Optional[str] = Query(None, description="内容"),
    publisher_id: Optional[str] = Query(None, description="发布者ID"),
    priority: int = Query(1, description="优先级"),
    status: str = Query("draft", description="状态"),
    is_top: int = Query(0, description="是否置顶"),
    db: Session = Depends(get_db)
):
    """
    创建通知公告

    创建新的通知公告
    """
    service = AnnouncementService(db)

    announcement = service.create_announcement(
        tenant_id=tenant_id,
        type=type,
        title=title,
        content=content,
        publisher_id=publisher_id,
        priority=priority,
        status=status,
        is_top=is_top
    )

    return {
        "success": True,
        "data": announcement,
        "message": "通知公告创建成功"
    }


@router.put("/{announcement_id}", summary="更新通知公告")
async def update_announcement(
    announcement_id: str,
    title: Optional[str] = Query(None, description="标题"),
    content: Optional[str] = Query(None, description="内容"),
    priority: Optional[int] = Query(None, description="优先级"),
    status: Optional[str] = Query(None, description="状态"),
    is_top: Optional[int] = Query(None, description="是否置顶"),
    db: Session = Depends(get_db)
):
    """
    更新通知公告

    更新通知公告信息
    """
    service = AnnouncementService(db)
    announcement = service.update_announcement(
        announcement_id=announcement_id,
        title=title,
        content=content,
        priority=priority,
        status=status,
        is_top=is_top
    )

    if not announcement:
        raise HTTPException(status_code=404, detail="通知公告不存在")

    return {
        "success": True,
        "data": announcement,
        "message": "通知公告更新成功"
    }


@router.delete("/{announcement_id}", summary="删除通知公告")
async def delete_announcement(
    announcement_id: str,
    db: Session = Depends(get_db)
):
    """
    删除通知公告

    根据通知公告ID删除通知公告
    """
    service = AnnouncementService(db)
    success = service.delete_announcement(announcement_id)

    if not success:
        raise HTTPException(status_code=404, detail="通知公告不存在")

    return {
        "success": True,
        "message": "通知公告删除成功"
    }


@router.post("/{announcement_id}/publish", summary="发布通知公告")
async def publish_announcement(
    announcement_id: str,
    db: Session = Depends(get_db)
):
    """
    发布通知公告

    将通知公告状态改为已发布
    """
    service = AnnouncementService(db)
    announcement = service.publish_announcement(announcement_id)

    if not announcement:
        raise HTTPException(status_code=404, detail="通知公告不存在")

    return {
        "success": True,
        "data": announcement,
        "message": "通知公告发布成功"
    }


@router.post("/{announcement_id}/archive", summary="归档通知公告")
async def archive_announcement(
    announcement_id: str,
    db: Session = Depends(get_db)
):
    """
    归档通知公告

    将通知公告状态改为已归档
    """
    service = AnnouncementService(db)
    announcement = service.archive_announcement(announcement_id)

    if not announcement:
        raise HTTPException(status_code=404, detail="通知公告不存在")

    return {
        "success": True,
        "data": announcement,
        "message": "通知公告归档成功"
    }


@router.post("/{announcement_id}/read", summary="标记通知公告为已读")
async def mark_announcement_as_read(
    announcement_id: str,
    user_id: str = Query(..., description="用户ID"),
    db: Session = Depends(get_db)
):
    """
    标记通知公告为已读

    标记通知公告为已读状态
    """
    service = AnnouncementService(db)
    success = service.mark_as_read(announcement_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="通知公告不存在")

    return {
        "success": True,
        "message": "通知公告已标记为已读"
    }


@router.get("/user/{user_id}/unread-count", summary="获取用户未读通知公告数量")
async def get_user_unread_count(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    获取用户未读通知公告数量

    根据用户ID获取未读通知公告数量
    """
    service = AnnouncementService(db)
    count = service.get_user_unread_count(user_id)

    return {
        "success": True,
        "data": {
            "unread_count": count
        }
    }
