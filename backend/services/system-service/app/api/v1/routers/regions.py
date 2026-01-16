"""
地区API路由

提供地区管理的REST API
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from common.database.session import get_db
from app.services.region_service import RegionService


router = APIRouter(prefix="/regions", tags=["地区管理"])


@router.get("", summary="获取地区列表")
async def get_regions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    level: Optional[str] = Query(None, description="地区级别"),
    parent_id: Optional[str] = Query(None, description="父级ID"),
    status: Optional[str] = Query(None, description="状态"),
    name: Optional[str] = Query(None, description="地区名称（模糊搜索）"),
    code: Optional[str] = Query(None, description="地区编码（模糊搜索）"),
    db: Session = Depends(get_db)
):
    """
    获取地区列表

    支持分页、搜索和筛选
    """
    service = RegionService(db)

    # 构建查询参数
    query_params = {}
    if level:
        query_params["level"] = level
    if parent_id:
        query_params["parent_id"] = parent_id
    if status:
        query_params["status"] = status
    if name:
        query_params["name"] = name
    if code:
        query_params["code"] = code

    # 计算偏移量
    skip = (page - 1) * page_size

    # 搜索地区
    result = service.search_regions(query_params, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/tree", summary="获取地区树")
async def get_region_tree(
    parent_id: Optional[str] = Query(None, description="父级ID（不传则获取顶级地区）"),
    db: Session = Depends(get_db)
):
    """
    获取地区树

    获取地区层级树结构
    """
    service = RegionService(db)
    tree = service.get_region_tree(parent_id)

    return {
        "success": True,
        "data": tree
    }


@router.get("/{region_id}", summary="获取地区详情")
async def get_region_detail(
    region_id: str,
    db: Session = Depends(get_db)
):
    """
    获取地区详情

    根据地区ID获取详细信息
    """
    service = RegionService(db)
    region = service.get_region_by_id(region_id)

    if not region:
        raise HTTPException(status_code=404, detail="地区不存在")

    return {
        "success": True,
        "data": region
    }


@router.get("/code/{code}", summary="根据地区编码获取")
async def get_region_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    根据地区编码获取

    根据地区编码字符串获取详细信息
    """
    service = RegionService(db)
    region = service.get_region_by_code(code)

    if not region:
        raise HTTPException(status_code=404, detail="地区不存在")

    return {
        "success": True,
        "data": region
    }


@router.get("/{region_id}/children", summary="获取子地区")
async def get_region_children(
    region_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取子地区

    根据地区ID获取子地区列表
    """
    service = RegionService(db)

    # 计算偏移量
    skip = (page - 1) * page_size

    # 获取子地区
    result = service.get_children(region_id, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/{region_id}/all-children", summary="获取所有子地区（递归）")
async def get_all_region_children(
    region_id: str,
    db: Session = Depends(get_db)
):
    """
    获取所有子地区（递归）

    根据地区ID获取所有子地区（包括多级子地区）
    """
    service = RegionService(db)
    children = service.get_all_children(region_id)

    return {
        "success": True,
        "data": children
    }


@router.post("", summary="创建地区")
async def create_region(
    name: str = Query(..., description="地区名称"),
    code: str = Query(..., description="地区编码"),
    level: str = Query(..., description="地区级别"),
    parent_id: Optional[str] = Query(None, description="父级ID"),
    sort_order: int = Query(0, description="排序"),
    db: Session = Depends(get_db)
):
    """
    创建地区

    创建新的地区
    """
    service = RegionService(db)

    try:
        region = service.create_region(
            name=name,
            code=code,
            level=level,
            parent_id=parent_id,
            sort_order=sort_order
        )
        return {
            "success": True,
            "data": region,
            "message": "地区创建成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{region_id}", summary="更新地区")
async def update_region(
    region_id: str,
    name: Optional[str] = Query(None, description="地区名称"),
    code: Optional[str] = Query(None, description="地区编码"),
    level: Optional[str] = Query(None, description="地区级别"),
    parent_id: Optional[str] = Query(None, description="父级ID"),
    sort_order: Optional[int] = Query(None, description="排序"),
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
):
    """
    更新地区

    更新地区信息
    """
    service = RegionService(db)
    region = service.update_region(
        region_id=region_id,
        name=name,
        code=code,
        level=level,
        parent_id=parent_id,
        sort_order=sort_order,
        status=status
    )

    if not region:
        raise HTTPException(status_code=404, detail="地区不存在")

    return {
        "success": True,
        "data": region,
        "message": "地区更新成功"
    }


@router.delete("/{region_id}", summary="删除地区")
async def delete_region(
    region_id: str,
    db: Session = Depends(get_db)
):
    """
    删除地区

    根据地区ID删除地区
    """
    service = RegionService(db)
    success = service.delete_region(region_id)

    if not success:
        raise HTTPException(status_code=404, detail="地区不存在")

    return {
        "success": True,
        "message": "地区删除成功"
    }


@router.get("/statistics/summary", summary="获取地区统计")
async def get_region_statistics(
    db: Session = Depends(get_db)
):
    """
    获取地区统计

    获取地区的统计信息，包括总数、按级别统计、按状态统计
    """
    service = RegionService(db)
    statistics = service.get_statistics()

    return {
        "success": True,
        "data": statistics
    }