"""
错误码API路由

提供错误码管理的REST API
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.error_code_service import ErrorCodeService


router = APIRouter(prefix="/error-codes", tags=["错误码管理"])


@router.get("", summary="获取错误码列表")
async def get_error_codes(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    module: Optional[str] = Query(None, description="模块"),
    level: Optional[str] = Query(None, description="错误级别"),
    status: Optional[str] = Query(None, description="状态"),
    code: Optional[str] = Query(None, description="错误码（模糊搜索）"),
    message: Optional[str] = Query(None, description="错误信息（模糊搜索）"),
    db: Session = Depends(get_db)
):
    """
    获取错误码列表

    支持分页、搜索和筛选
    """
    service = ErrorCodeService(db)

    # 构建查询参数
    query_params = {}
    if module:
        query_params["module"] = module
    if level:
        query_params["level"] = level
    if status:
        query_params["status"] = status
    if code:
        query_params["code"] = code
    if message:
        query_params["message"] = message

    # 计算偏移量
    skip = (page - 1) * page_size

    # 搜索错误码
    result = service.search_error_codes(query_params, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/{error_code_id}", summary="获取错误码详情")
async def get_error_code_detail(
    error_code_id: str,
    db: Session = Depends(get_db)
):
    """
    获取错误码详情

    根据错误码ID获取详细信息
    """
    service = ErrorCodeService(db)
    error_code = service.get_error_code_by_id(error_code_id)

    if not error_code:
        raise HTTPException(status_code=404, detail="错误码不存在")

    return {
        "success": True,
        "data": error_code
    }


@router.get("/code/{code}", summary="根据错误码获取")
async def get_error_code_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    根据错误码获取

    根据错误码字符串获取详细信息
    """
    service = ErrorCodeService(db)
    error_code = service.get_error_code_by_code(code)

    if not error_code:
        raise HTTPException(status_code=404, detail="错误码不存在")

    return {
        "success": True,
        "data": error_code
    }


@router.post("", summary="创建错误码")
async def create_error_code(
    code: str = Query(..., description="错误码"),
    message: str = Query(..., description="错误信息"),
    module: str = Query(..., description="模块"),
    level: str = Query("error", description="错误级别"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """
    创建错误码

    创建新的错误码
    """
    service = ErrorCodeService(db)

    try:
        error_code = service.create_error_code(
            code=code,
            message=message,
            module=module,
            level=level,
            description=description
        )
        return {
            "success": True,
            "data": error_code,
            "message": "错误码创建成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{error_code_id}", summary="更新错误码")
async def update_error_code(
    error_code_id: str,
    code: Optional[str] = Query(None, description="错误码"),
    message: Optional[str] = Query(None, description="错误信息"),
    level: Optional[str] = Query(None, description="错误级别"),
    module: Optional[str] = Query(None, description="模块"),
    description: Optional[str] = Query(None, description="描述"),
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
):
    """
    更新错误码

    更新错误码信息
    """
    service = ErrorCodeService(db)
    error_code = service.update_error_code(
        error_code_id=error_code_id,
        code=code,
        message=message,
        level=level,
        module=module,
        description=description,
        status=status
    )

    if not error_code:
        raise HTTPException(status_code=404, detail="错误码不存在")

    return {
        "success": True,
        "data": error_code,
        "message": "错误码更新成功"
    }


@router.delete("/{error_code_id}", summary="删除错误码")
async def delete_error_code(
    error_code_id: str,
    db: Session = Depends(get_db)
):
    """
    删除错误码

    根据错误码ID删除错误码
    """
    service = ErrorCodeService(db)
    success = service.delete_error_code(error_code_id)

    if not success:
        raise HTTPException(status_code=404, detail="错误码不存在")

    return {
        "success": True,
        "message": "错误码删除成功"
    }


@router.get("/statistics/summary", summary="获取错误码统计")
async def get_error_code_statistics(
    db: Session = Depends(get_db)
):
    """
    获取错误码统计

    获取错误码的统计信息，包括总数、按级别统计、按状态统计
    """
    service = ErrorCodeService(db)
    statistics = service.get_statistics()

    return {
        "success": True,
        "data": statistics
    }
