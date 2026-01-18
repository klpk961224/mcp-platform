"""
部门管理API路由
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings
from app.core.deps import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentListResponse,
    DepartmentTreeResponse
)
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["部门管理"])


@router.post("", response_model=DepartmentResponse, summary="创建部门")
async def create_department(
    dept: DepartmentCreate,
    db: Session = Depends(get_db)
):
    """
    创建部门
    
    功能：
    - 验证部门编码唯一性
    - 验证部门名称在租户内唯一性
    - 自动计算部门层级
    - 自动生成部门编码（如果未提供）
    
    Args:
        dept: 部门创建数据
    
    Returns:
        DepartmentResponse: 创建的部门信息
    
    Raises:
        HTTPException: 验证失败时抛出400错误
    """
    logger.info(f"创建部门: name={dept.name}, tenant_id={dept.tenant_id}")
    
    try:
        dept_service = DepartmentService(db)
        department = dept_service.create_department(dept.dict())
        return DepartmentResponse(**department.to_dict())
    except ValueError as e:
        logger.error(f"创建部门失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建部门异常: {str(e)}")
        raise HTTPException(status_code=500, detail="创建部门失败")


@router.get("", response_model=DepartmentListResponse, summary="获取部门列表")
async def get_departments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    parent_id: Optional[str] = Query(None, description="父部门ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    获取部门列表
    
    支持按租户、父部门、关键词筛选
    
    Args:
        page: 页码
        page_size: 每页数量
        tenant_id: 租户ID（可选）
        parent_id: 父部门ID（可选）
        keyword: 搜索关键词（可选）
    
    Returns:
        DepartmentListResponse: 部门列表
    """
    logger.info(f"获取部门列表: page={page}, page_size={page_size}, tenant_id={tenant_id}")
    
    try:
        dept_service = DepartmentService(db)
        result = dept_service.list_departments(
            tenant_id=tenant_id,
            parent_id=parent_id,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        return DepartmentListResponse(**result)
    except Exception as e:
        logger.error(f"获取部门列表异常: {str(e)}")
        raise HTTPException(status_code=500, detail="获取部门列表失败")


@router.get("/tree", response_model=list[DepartmentTreeResponse], summary="获取部门树")
async def get_department_tree(
    tenant_id: Optional[str] = Query(None, description="租户ID"),
    db: Session = Depends(get_db)
):
    """
    获取部门树
    
    返回完整的部门树形结构，包含所有层级
    
    Args:
        tenant_id: 租户ID（必填）
    
    Returns:
        list[DepartmentTreeResponse]: 部门树
    
    Raises:
        HTTPException: 租户ID为空时抛出400错误
    """
    logger.info(f"获取部门树: tenant_id={tenant_id}")
    
    if not tenant_id:
        raise HTTPException(status_code=400, detail="租户ID不能为空")
    
    try:
        dept_service = DepartmentService(db)
        tree = dept_service.get_department_tree(tenant_id)
        return tree
    except Exception as e:
        logger.error(f"获取部门树异常: {str(e)}")
        raise HTTPException(status_code=500, detail="获取部门树失败")


@router.get("/{dept_id}", response_model=DepartmentResponse, summary="获取部门详情")
async def get_department(
    dept_id: str,
    db: Session = Depends(get_db)
):
    """
    获取部门详情
    
    Args:
        dept_id: 部门ID
    
    Returns:
        DepartmentResponse: 部门详情
    
    Raises:
        HTTPException: 部门不存在时抛出404错误
    """
    logger.info(f"获取部门详情: dept_id={dept_id}")
    
    try:
        dept_service = DepartmentService(db)
        department = dept_service.get_department(dept_id)
        if not department:
            raise HTTPException(status_code=404, detail="部门不存在")
        return DepartmentResponse(**department.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取部门详情异常: {str(e)}")
        raise HTTPException(status_code=500, detail="获取部门详情失败")


@router.put("/{dept_id}", response_model=DepartmentResponse, summary="更新部门")
async def update_department(
    dept_id: str,
    dept: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    """
    更新部门
    
    功能：
    - 验证部门编码唯一性（如果修改了编码）
    - 验证部门名称在租户内唯一性（如果修改了名称）
    - 自动计算部门层级（如果修改了父部门）
    - 自动更新子部门的层级
    
    Args:
        dept_id: 部门ID
        dept: 部门更新数据
    
    Returns:
        DepartmentResponse: 更新后的部门信息
    
    Raises:
        HTTPException: 验证失败或部门不存在时抛出400或404错误
    """
    logger.info(f"更新部门: dept_id={dept_id}")
    
    try:
        dept_service = DepartmentService(db)
        department = dept_service.update_department(dept_id, dept.dict(exclude_unset=True))
        return DepartmentResponse(**department.to_dict())
    except ValueError as e:
        logger.error(f"更新部门失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新部门异常: {str(e)}")
        raise HTTPException(status_code=500, detail="更新部门失败")


@router.delete("/{dept_id}", summary="删除部门")
async def delete_department(
    dept_id: str,
    db: Session = Depends(get_db)
):
    """
    删除部门
    
    功能：
    - 检查部门是否存在
    - 检查是否有子部门
    - 检查是否有用户
    
    Args:
        dept_id: 部门ID
    
    Returns:
        dict: 删除结果
    
    Raises:
        HTTPException: 验证失败时抛出400错误
    """
    logger.info(f"删除部门: dept_id={dept_id}")
    
    try:
        dept_service = DepartmentService(db)
        dept_service.delete_department(dept_id)
        return {"message": "删除成功"}
    except ValueError as e:
        logger.error(f"删除部门失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"删除部门异常: {str(e)}")
        raise HTTPException(status_code=500, detail="删除部门失败")