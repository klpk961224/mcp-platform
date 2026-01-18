"""
绉熸埛绠＄悊API璺敱
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

router = APIRouter(prefix="/tenants", tags=["绉熸埛绠＄悊"])


@router.post("", response_model=TenantResponse, summary="创建绉熸埛")
async def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    """
    创建绉熸埛
    
    鍔熻兘锛?    - 楠岃瘉绉熸埛编码鍞竴鎬?    - 楠岃瘉绉熸埛名称鍞竴鎬?    - 鑷姩搴旂敤濂楅閰嶇疆锛堥粯璁asic锛?    - 鑷姩璁＄畻杩囨湡鏃堕棿锛?65澶╋級
    
    Args:
        tenant: 绉熸埛创建鏁版嵁
    
    Returns:
        TenantResponse: 创建鐨勭鎴蜂俊鎭?    
    Raises:
        HTTPException: 楠岃瘉澶辫触鏃舵姏鍑?00閿欒
    """
    logger.info(f"创建绉熸埛: name={tenant.name}, code={tenant.code}")
    
    try:
        tenant_service = TenantService(db)
        tenant_obj = tenant_service.create_tenant(tenant.dict())
        
        # 杞崲涓哄搷搴旀牸寮?        response_data = tenant_obj.to_dict()
        return TenantResponse(**response_data)
    except ValueError as e:
        logger.error(f"创建绉熸埛澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建绉熸埛寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="创建绉熸埛澶辫触")


@router.get("", response_model=TenantListResponse, summary="鑾峰彇绉熸埛鍒楄〃")
async def get_tenants(
    page: int = Query(1, ge=1, description="椤电爜"),
    page_size: int = Query(10, ge=1, le=100, description="姣忛〉数量"),
    status: Optional[str] = Query(None, description="状态佺瓫閫?),
    keyword: Optional[str] = Query(None, description="鎼滅储鍏抽敭璇?),
    db: Session = Depends(get_db)
):
    """
    鑾峰彇绉熸埛鍒楄〃
    
    鏀寔鎸夌姸鎬併€佸叧閿瘝绛涢€?    
    Args:
        page: 椤电爜
        page_size: 姣忛〉数量
        status: 状态佺瓫閫夛紙鍙€夛級
        keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
    
    Returns:
        TenantListResponse: 绉熸埛鍒楄〃
    """
    logger.info(f"鑾峰彇绉熸埛鍒楄〃: page={page}, page_size={page_size}, status={status}")
    
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
        logger.error(f"鑾峰彇绉熸埛鍒楄〃寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇绉熸埛鍒楄〃澶辫触")


@router.get("/{tenant_id}", response_model=TenantResponse, summary="鑾峰彇绉熸埛璇︽儏")
async def get_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """
    鑾峰彇绉熸埛璇︽儏
    
    Args:
        tenant_id: 租户ID
    
    Returns:
        TenantResponse: 绉熸埛璇︽儏
    
    Raises:
        HTTPException: 绉熸埛涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"鑾峰彇绉熸埛璇︽儏: tenant_id={tenant_id}")
    
    try:
        tenant_service = TenantService(db)
        tenant = tenant_service.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="绉熸埛涓嶅瓨鍦?)
        
        response_data = tenant.to_dict()
        return TenantResponse(**response_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇绉熸埛璇︽儏寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇绉熸埛璇︽儏澶辫触")


@router.put("/{tenant_id}", response_model=TenantResponse, summary="更新绉熸埛")
async def update_tenant(
    tenant_id: str,
    tenant: TenantUpdate,
    db: Session = Depends(get_db)
):
    """
    更新绉熸埛
    
    鍔熻兘锛?    - 楠岃瘉绉熸埛编码鍞竴鎬э紙濡傛灉淇敼浜嗙紪鐮侊級
    - 楠岃瘉绉熸埛名称鍞竴鎬э紙濡傛灉淇敼浜嗗悕绉帮級
    - 更新濂楅閰嶇疆锛堝鏋滀慨鏀逛簡濂楅锛?    - 閲嶆柊璁＄畻杩囨湡鏃堕棿锛堝鏋滀慨鏀逛簡状态佹垨濂楅锛?    
    Args:
        tenant_id: 租户ID
        tenant: 绉熸埛更新鏁版嵁
    
    Returns:
        TenantResponse: 更新鍚庣殑绉熸埛淇℃伅
    
    Raises:
        HTTPException: 楠岃瘉澶辫触鎴栫鎴蜂笉瀛樺湪鏃舵姏鍑?00鎴?04閿欒
    """
    logger.info(f"更新绉熸埛: tenant_id={tenant_id}")
    
    try:
        tenant_service = TenantService(db)
        tenant_obj = tenant_service.update_tenant(tenant_id, tenant.dict(exclude_unset=True))
        
        response_data = tenant_obj.to_dict()
        return TenantResponse(**response_data)
    except ValueError as e:
        logger.error(f"更新绉熸埛澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新绉熸埛寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="更新绉熸埛澶辫触")


@router.delete("/{tenant_id}", summary="删除绉熸埛")
async def delete_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """
    删除绉熸埛
    
    鍔熻兘锛?    - 妫€鏌ョ鎴锋槸鍚﹀瓨鍦?    - 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
    - 妫€鏌ユ槸鍚︽湁閮ㄩ棬
    
    Args:
        tenant_id: 租户ID
    
    Returns:
        dict: 删除缁撴灉
    
    Raises:
        HTTPException: 楠岃瘉澶辫触鏃舵姏鍑?00閿欒
    """
    logger.info(f"删除绉熸埛: tenant_id={tenant_id}")
    
    try:
        tenant_service = TenantService(db)
        tenant_service.delete_tenant(tenant_id)
        return {"message": "删除鎴愬姛"}
    except ValueError as e:
        logger.error(f"删除绉熸埛澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"删除绉熸埛寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="删除绉熸埛澶辫触")


@router.get("/{tenant_id}/quota/{quota_type}", summary="妫€鏌ョ鎴疯祫婧愰厤棰?)
async def check_tenant_quota(
    tenant_id: str,
    quota_type: str,
    db: Session = Depends(get_db)
):
    """
    妫€鏌ョ鎴疯祫婧愰厤棰?    
    鏀寔鐨勯厤棰濈被鍨嬶細
    - users: 鐢ㄦ埛鏁伴厤棰?    - departments: 閮ㄩ棬鏁伴厤棰?    - storage: 瀛樺偍绌洪棿閰嶉
    
    Args:
        tenant_id: 租户ID
        quota_type: 閰嶉类型
    
    Returns:
        dict: 閰嶉淇℃伅
    
    Raises:
        HTTPException: 绉熸埛涓嶅瓨鍦ㄦ垨閰嶉类型涓嶆敮鎸佹椂鎶涘嚭400鎴?04閿欒
    """
    logger.info(f"妫€鏌ョ鎴烽厤棰? tenant_id={tenant_id}, quota_type={quota_type}")
    
    try:
        tenant_service = TenantService(db)
        quota = tenant_service.check_quota(tenant_id, quota_type)
        return quota
    except ValueError as e:
        logger.error(f"妫€鏌ョ鎴烽厤棰濆け璐? {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"妫€鏌ョ鎴烽厤棰濆紓甯? {str(e)}")
        raise HTTPException(status_code=500, detail="妫€鏌ョ鎴烽厤棰濆け璐?)


@router.get("/packages", summary="鑾峰彇鎵€鏈夊椁愪俊鎭?)
async def get_all_packages(db: Session = Depends(get_db)):
    """
    鑾峰彇鎵€鏈夊椁愪俊鎭?    
    棰勫畾涔夊椁愶細
    - free: 鍏嶈垂鐗堬紙10鐢ㄦ埛锛?閮ㄩ棬锛?GB瀛樺偍锛?0澶╋級
    - basic: 鍩虹鐗堬紙50鐢ㄦ埛锛?0閮ㄩ棬锛?0GB瀛樺偍锛?65澶╋級
    - professional: 涓撲笟鐗堬紙200鐢ㄦ埛锛?00閮ㄩ棬锛?00GB瀛樺偍锛?65澶╋級
    - enterprise: 浼佷笟鐗堬紙1000鐢ㄦ埛锛?00閮ㄩ棬锛?TB瀛樺偍锛?65澶╋級
    
    Returns:
        dict: 鎵€鏈夊椁愪俊鎭?    """
    logger.info("鑾峰彇鎵€鏈夊椁愪俊鎭?)
    
    try:
        tenant_service = TenantService(db)
        packages = tenant_service.get_all_packages()
        return packages
    except Exception as e:
        logger.error(f"鑾峰彇濂楅淇℃伅寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇濂楅淇℃伅澶辫触")


@router.post("/{tenant_id}/renew", summary="缁垂绉熸埛")
async def renew_tenant(
    tenant_id: str,
    days: int = Query(365, ge=1, description="缁垂澶╂暟"),
    db: Session = Depends(get_db)
):
    """
    缁垂绉熸埛
    
    鍔熻兘锛?    - 濡傛灉绉熸埛宸茶繃鏈燂紝浠庡綋鍓嶆椂闂村紑濮嬭绠?    - 濡傛灉绉熸埛鏈繃鏈燂紝鍦ㄥ師鏈夎繃鏈熸椂闂村熀纭€涓婂欢闀?    
    Args:
        tenant_id: 租户ID
        days: 缁垂澶╂暟锛堥粯璁?65澶╋級
    
    Returns:
        dict: 缁垂缁撴灉
    
    Raises:
        HTTPException: 绉熸埛涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"缁垂绉熸埛: tenant_id={tenant_id}, days={days}")
    
    try:
        tenant_service = TenantService(db)
        tenant = tenant_service.renew_tenant(tenant_id, days)
        
        response_data = tenant.to_dict()
        return {
            "message": "缁垂鎴愬姛",
            "tenant": response_data
        }
    except ValueError as e:
        logger.error(f"缁垂绉熸埛澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"缁垂绉熸埛寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="缁垂绉熸埛澶辫触")
