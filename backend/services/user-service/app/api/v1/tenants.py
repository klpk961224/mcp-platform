"""
租户管理API路由
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
from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantResponse,
    TenantListResponse
)
from app.services.tenant_service import TenantService

router = APIRouter(prefix="/tenants", tags=["租户管理"])


@router.post("", response_model=TenantResponse, summary="创建租户")
async def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    """
    创建租户
    
    功能：
    - 验证租户编码唯一性
    - 验证租户名称唯一性
    - 自动应用套餐配置（默认basic）
    - 自动计算过期时间（365天）
    
    Args:
        tenant: 租户创建数据
    
    Returns:
        TenantResponse: 创建的租户信息
    
    Raises:
        HTTPException: 验证失败时抛出400错误
    """
    logger.info(f"创建租户: name={tenant.name}, code={tenant.code}")
    
    try:
        tenant_service = TenantService(db)
        tenant_obj = tenant_service.create_tenant(tenant.dict())
        
        # 转换为响应格式
        response_data = tenant_obj.to_dict()
        return TenantResponse(**response_data)
    except ValueError as e:
        logger.error(f"创建租户失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建租户异常: {str(e)}")
        raise HTTPException(status_code=500, detail="创建租户失败")


@router.get("", response_model=TenantListResponse, summary="获取租户列表")
async def get_tenants(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="状态筛选"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    获取租户列表
    
    支持按状态、关键词筛选
    
    Args:
        page: 页码
        page_size: 每页数量
        status: 状态筛选（可选）
        keyword: 搜索关键词（可选）
    
    Returns:
        TenantListResponse: 租户列表
    """
    logger.info(f"获取租户列表: page={page}, page_size={page_size}, status={status}")
    
    try:
        tenant_service = TenantService(db)
        result = tenant_service.list_tenants(
            status=status,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        return TenantListResponse(**result)
    except Exception as e:
        logger.error(f"获取租户列表异常: {str(e)}")
        raise HTTPException(status_code=500, detail="获取租户列表失败")


@router.get("/{tenant_id}", response_model=TenantResponse, summary="获取租户详情")
async def get_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """
    获取租户详情
    
    Args:
        tenant_id: 租户ID
    
    Returns:
        TenantResponse: 租户详情
    
    Raises:
        HTTPException: 租户不存在时抛出404错误
    """
    logger.info(f"获取租户详情: tenant_id={tenant_id}")
    
    try:
        tenant_service = TenantService(db)
        tenant = tenant_service.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="租户不存在")
        
        response_data = tenant.to_dict()
        return TenantResponse(**response_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取租户详情异常: {str(e)}")
        raise HTTPException(status_code=500, detail="获取租户详情失败")


@router.put("/{tenant_id}", response_model=TenantResponse, summary="更新租户")
async def update_tenant(
    tenant_id: str,
    tenant: TenantUpdate,
    db: Session = Depends(get_db)
):
    """
    更新租户
    
    功能：
    - 验证租户编码唯一性（如果修改了编码）
    - 验证租户名称唯一性（如果修改了名称）
    - 更新套餐配置（如果修改了套餐）
    - 重新计算过期时间（如果修改了状态或套餐）
    
    Args:
        tenant_id: 租户ID
        tenant: 租户更新数据
    
    Returns:
        TenantResponse: 更新后的租户信息
    
    Raises:
        HTTPException: 验证失败或租户不存在时抛出400或404错误
    """
    logger.info(f"更新租户: tenant_id={tenant_id}")
    
    try:
        tenant_service = TenantService(db)
        tenant_obj = tenant_service.update_tenant(tenant_id, tenant.dict(exclude_unset=True))
        
        response_data = tenant_obj.to_dict()
        return TenantResponse(**response_data)
    except ValueError as e:
        logger.error(f"更新租户失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新租户异常: {str(e)}")
        raise HTTPException(status_code=500, detail="更新租户失败")


@router.delete("/{tenant_id}", summary="删除租户")
async def delete_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """
    删除租户
    
    功能：
    - 检查租户是否存在
    - 检查是否有用户
    - 检查是否有部门
    
    Args:
        tenant_id: 租户ID
    
    Returns:
        dict: 删除结果
    
    Raises:
        HTTPException: 验证失败时抛出400错误
    """
    logger.info(f"删除租户: tenant_id={tenant_id}")
    
    try:
        tenant_service = TenantService(db)
        tenant_service.delete_tenant(tenant_id)
        return {"message": "删除成功"}
    except ValueError as e:
        logger.error(f"删除租户失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"删除租户异常: {str(e)}")
        raise HTTPException(status_code=500, detail="删除租户失败")


@router.get("/{tenant_id}/quota/{quota_type}", summary="检查租户资源配额")
async def check_tenant_quota(
    tenant_id: str,
    quota_type: str,
    db: Session = Depends(get_db)
):
    """
    检查租户资源配额
    
    支持的配额类型：
    - users: 用户数配额
    - departments: 部门数配额
    - storage: 存储空间配额
    
    Args:
        tenant_id: 租户ID
        quota_type: 配额类型
    
    Returns:
        dict: 配额信息
    
    Raises:
        HTTPException: 租户不存在或配额类型不支持时抛出400或404错误
    """
    logger.info(f"检查租户配额: tenant_id={tenant_id}, quota_type={quota_type}")
    
    try:
        tenant_service = TenantService(db)
        quota = tenant_service.check_quota(tenant_id, quota_type)
        return quota
    except ValueError as e:
        logger.error(f"检查租户配额失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"检查租户配额异常: {str(e)}")
        raise HTTPException(status_code=500, detail="检查租户配额失败")


@router.get("/packages", summary="获取所有套餐信息")
async def get_all_packages(db: Session = Depends(get_db)):
    """
    获取所有套餐信息
    
    预定义套餐：
    - free: 免费版（10用户，5部门，1GB存储，30天）
    - basic: 基础版（50用户，20部门，10GB存储，365天）
    - professional: 专业版（200用户，100部门，100GB存储，365天）
    - enterprise: 企业版（1000用户，500部门，1TB存储，365天）
    
    Returns:
        dict: 所有套餐信息
    """
    logger.info("获取所有套餐信息")
    
    try:
        tenant_service = TenantService(db)
        packages = tenant_service.get_all_packages()
        return packages
    except Exception as e:
        logger.error(f"获取套餐信息异常: {str(e)}")
        raise HTTPException(status_code=500, detail="获取套餐信息失败")


@router.post("/{tenant_id}/renew", summary="续费租户")
async def renew_tenant(
    tenant_id: str,
    days: int = Query(365, ge=1, description="续费天数"),
    db: Session = Depends(get_db)
):
    """
    续费租户
    
    功能：
    - 如果租户已过期，从当前时间开始计算
    - 如果租户未过期，在原有过期时间基础上延长
    
    Args:
        tenant_id: 租户ID
        days: 续费天数（默认365天）
    
    Returns:
        dict: 续费结果
    
    Raises:
        HTTPException: 租户不存在时抛出404错误
    """
    logger.info(f"续费租户: tenant_id={tenant_id}, days={days}")
    
    try:
        tenant_service = TenantService(db)
        tenant = tenant_service.renew_tenant(tenant_id, days)
        
        response_data = tenant.to_dict()
        return {
            "message": "续费成功",
            "tenant": response_data
        }
    except ValueError as e:
        logger.error(f"续费租户失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"续费租户异常: {str(e)}")
        raise HTTPException(status_code=500, detail="续费租户失败")