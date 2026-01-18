"""
敏感词API路由

提供敏感词管理的REST API
"""

from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.deps import get_db
from app.services.sensitive_word_service import SensitiveWordService


router = APIRouter(prefix="/sensitive-words", tags=["敏感词管理"])


class TextCheckRequest(BaseModel):
    """文本检查请求"""
    text: str


class TextFilterRequest(BaseModel):
    """文本过滤请求"""
    text: str


@router.get("", summary="获取敏感词列表")
async def get_sensitive_words(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    category: Optional[str] = Query(None, description="分类"),
    level: Optional[int] = Query(None, description="敏感级别"),
    status: Optional[str] = Query(None, description="状态"),
    word: Optional[str] = Query(None, description="敏感词（模糊搜索）"),
    db: Session = Depends(get_db)
):
    """
    获取敏感词列表

    支持分页、搜索和筛选
    """
    service = SensitiveWordService(db)

    # 构建查询参数
    query_params = {}
    if category:
        query_params["category"] = category
    if level:
        query_params["level"] = level
    if status:
        query_params["status"] = status
    if word:
        query_params["word"] = word

    # 计算偏移量
    skip = (page - 1) * page_size

    # 搜索敏感词
    result = service.search_sensitive_words(query_params, skip=skip, limit=page_size)

    return {
        "success": True,
        "data": result["items"],
        "total": result["total"],
        "page": page,
        "page_size": page_size
    }


@router.get("/{sensitive_word_id}", summary="获取敏感词详情")
async def get_sensitive_word_detail(
    sensitive_word_id: str,
    db: Session = Depends(get_db)
):
    """
    获取敏感词详情

    根据敏感词ID获取详细信息
    """
    service = SensitiveWordService(db)
    sensitive_word = service.get_sensitive_word_by_id(sensitive_word_id)

    if not sensitive_word:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    return {
        "success": True,
        "data": sensitive_word
    }


@router.get("/word/{word}", summary="根据敏感词获取")
async def get_sensitive_word_by_word(
    word: str,
    db: Session = Depends(get_db)
):
    """
    根据敏感词获取

    根据敏感词字符串获取详细信息
    """
    service = SensitiveWordService(db)
    sensitive_word = service.get_sensitive_word_by_word(word)

    if not sensitive_word:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    return {
        "success": True,
        "data": sensitive_word
    }


@router.post("", summary="创建敏感词")
async def create_sensitive_word(
    word: str = Query(..., description="敏感词"),
    category: str = Query(..., description="分类"),
    level: int = Query(1, description="敏感级别"),
    replacement: Optional[str] = Query(None, description="替换词"),
    description: Optional[str] = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """
    创建敏感词

    创建新的敏感词
    """
    service = SensitiveWordService(db)

    try:
        sensitive_word = service.create_sensitive_word(
            word=word,
            category=category,
            level=level,
            replacement=replacement,
            description=description
        )
        return {
            "success": True,
            "data": sensitive_word,
            "message": "敏感词创建成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{sensitive_word_id}", summary="更新敏感词")
async def update_sensitive_word(
    sensitive_word_id: str,
    word: Optional[str] = Query(None, description="敏感词"),
    category: Optional[str] = Query(None, description="分类"),
    level: Optional[int] = Query(None, description="敏感级别"),
    replacement: Optional[str] = Query(None, description="替换词"),
    description: Optional[str] = Query(None, description="描述"),
    status: Optional[str] = Query(None, description="状态"),
    db: Session = Depends(get_db)
):
    """
    更新敏感词

    更新敏感词信息
    """
    service = SensitiveWordService(db)
    sensitive_word = service.update_sensitive_word(
        sensitive_word_id=sensitive_word_id,
        word=word,
        category=category,
        level=level,
        replacement=replacement,
        description=description,
        status=status
    )

    if not sensitive_word:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    return {
        "success": True,
        "data": sensitive_word,
        "message": "敏感词更新成功"
    }


@router.delete("/{sensitive_word_id}", summary="删除敏感词")
async def delete_sensitive_word(
    sensitive_word_id: str,
    db: Session = Depends(get_db)
):
    """
    删除敏感词

    根据敏感词ID删除敏感词
    """
    service = SensitiveWordService(db)
    success = service.delete_sensitive_word(sensitive_word_id)

    if not success:
        raise HTTPException(status_code=404, detail="敏感词不存在")

    return {
        "success": True,
        "message": "敏感词删除成功"
    }


@router.post("/check", summary="检查文本")
async def check_text(
    request: TextCheckRequest,
    db: Session = Depends(get_db)
):
    """
    检查文本

    检查文本是否包含敏感词
    """
    service = SensitiveWordService(db)
    result = service.check_text(request.text)

    return {
        "success": True,
        "data": result
    }


@router.post("/filter", summary="过滤文本")
async def filter_text(
    request: TextFilterRequest,
    db: Session = Depends(get_db)
):
    """
    过滤文本

    过滤文本中的敏感词
    """
    service = SensitiveWordService(db)
    filtered_text = service.filter_text(request.text)

    return {
        "success": True,
        "data": {
            "original": request.text,
            "filtered": filtered_text
        }
    }


@router.get("/statistics/summary", summary="获取敏感词统计")
async def get_sensitive_word_statistics(
    db: Session = Depends(get_db)
):
    """
    获取敏感词统计

    获取敏感词的统计信息，包括总数、按分类统计、按级别统计
    """
    service = SensitiveWordService(db)
    statistics = service.get_statistics()

    return {
        "success": True,
        "data": statistics
    }