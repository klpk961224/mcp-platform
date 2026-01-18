"""
閮ㄩ棬绠＄悊API璺敱
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

router = APIRouter(prefix="/departments", tags=["閮ㄩ棬绠＄悊"])


@router.post("", response_model=DepartmentResponse, summary="鍒涘缓閮ㄩ棬")
async def create_department(
    dept: DepartmentCreate,
    db: Session = Depends(get_db)
):
    """
    鍒涘缓閮ㄩ棬
    
    鍔熻兘锛?    - 楠岃瘉閮ㄩ棬缂栫爜鍞竴鎬?    - 楠岃瘉閮ㄩ棬鍚嶇О鍦ㄧ鎴峰唴鍞竴鎬?    - 鑷姩璁＄畻閮ㄩ棬灞傜骇
    - 鑷姩鐢熸垚閮ㄩ棬缂栫爜锛堝鏋滄湭鎻愪緵锛?    
    Args:
        dept: 閮ㄩ棬鍒涘缓鏁版嵁
    
    Returns:
        DepartmentResponse: 鍒涘缓鐨勯儴闂ㄤ俊鎭?    
    Raises:
        HTTPException: 楠岃瘉澶辫触鏃舵姏鍑?00閿欒
    """
    logger.info(f"鍒涘缓閮ㄩ棬: name={dept.name}, tenant_id={dept.tenant_id}")
    
    try:
        dept_service = DepartmentService(db)
        department = dept_service.create_department(dept.dict())
        return DepartmentResponse(**department.to_dict())
    except ValueError as e:
        logger.error(f"鍒涘缓閮ㄩ棬澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"鍒涘缓閮ㄩ棬寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鍒涘缓閮ㄩ棬澶辫触")


@router.get("", response_model=DepartmentListResponse, summary="鑾峰彇閮ㄩ棬鍒楄〃")
async def get_departments(
    page: int = Query(1, ge=1, description="椤电爜"),
    page_size: int = Query(10, ge=1, le=100, description="姣忛〉鏁伴噺"),
    tenant_id: Optional[str] = Query(None, description="绉熸埛ID"),
    parent_id: Optional[str] = Query(None, description="鐖堕儴闂↖D"),
    keyword: Optional[str] = Query(None, description="鎼滅储鍏抽敭璇?),
    db: Session = Depends(get_db)
):
    """
    鑾峰彇閮ㄩ棬鍒楄〃
    
    鏀寔鎸夌鎴枫€佺埗閮ㄩ棬銆佸叧閿瘝绛涢€?    
    Args:
        page: 椤电爜
        page_size: 姣忛〉鏁伴噺
        tenant_id: 绉熸埛ID锛堝彲閫夛級
        parent_id: 鐖堕儴闂↖D锛堝彲閫夛級
        keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
    
    Returns:
        DepartmentListResponse: 閮ㄩ棬鍒楄〃
    """
    logger.info(f"鑾峰彇閮ㄩ棬鍒楄〃: page={page}, page_size={page_size}, tenant_id={tenant_id}")
    
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
        logger.error(f"鑾峰彇閮ㄩ棬鍒楄〃寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇閮ㄩ棬鍒楄〃澶辫触")


@router.get("/tree", response_model=list[DepartmentTreeResponse], summary="鑾峰彇閮ㄩ棬鏍?)
async def get_department_tree(
    tenant_id: Optional[str] = Query(None, description="绉熸埛ID"),
    db: Session = Depends(get_db)
):
    """
    鑾峰彇閮ㄩ棬鏍?    
    杩斿洖瀹屾暣鐨勯儴闂ㄦ爲褰㈢粨鏋勶紝鍖呭惈鎵€鏈夊眰绾?    
    Args:
        tenant_id: 绉熸埛ID锛堝繀濉級
    
    Returns:
        list[DepartmentTreeResponse]: 閮ㄩ棬鏍?    
    Raises:
        HTTPException: 绉熸埛ID涓虹┖鏃舵姏鍑?00閿欒
    """
    logger.info(f"鑾峰彇閮ㄩ棬鏍? tenant_id={tenant_id}")
    
    if not tenant_id:
        raise HTTPException(status_code=400, detail="绉熸埛ID涓嶈兘涓虹┖")
    
    try:
        dept_service = DepartmentService(db)
        tree = dept_service.get_department_tree(tenant_id)
        return tree
    except Exception as e:
        logger.error(f"鑾峰彇閮ㄩ棬鏍戝紓甯? {str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇閮ㄩ棬鏍戝け璐?)


@router.get("/{dept_id}", response_model=DepartmentResponse, summary="鑾峰彇閮ㄩ棬璇︽儏")
async def get_department(
    dept_id: str,
    db: Session = Depends(get_db)
):
    """
    鑾峰彇閮ㄩ棬璇︽儏
    
    Args:
        dept_id: 閮ㄩ棬ID
    
    Returns:
        DepartmentResponse: 閮ㄩ棬璇︽儏
    
    Raises:
        HTTPException: 閮ㄩ棬涓嶅瓨鍦ㄦ椂鎶涘嚭404閿欒
    """
    logger.info(f"鑾峰彇閮ㄩ棬璇︽儏: dept_id={dept_id}")
    
    try:
        dept_service = DepartmentService(db)
        department = dept_service.get_department(dept_id)
        if not department:
            raise HTTPException(status_code=404, detail="閮ㄩ棬涓嶅瓨鍦?)
        return DepartmentResponse(**department.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇閮ㄩ棬璇︽儏寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鑾峰彇閮ㄩ棬璇︽儏澶辫触")


@router.put("/{dept_id}", response_model=DepartmentResponse, summary="鏇存柊閮ㄩ棬")
async def update_department(
    dept_id: str,
    dept: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    """
    鏇存柊閮ㄩ棬
    
    鍔熻兘锛?    - 楠岃瘉閮ㄩ棬缂栫爜鍞竴鎬э紙濡傛灉淇敼浜嗙紪鐮侊級
    - 楠岃瘉閮ㄩ棬鍚嶇О鍦ㄧ鎴峰唴鍞竴鎬э紙濡傛灉淇敼浜嗗悕绉帮級
    - 鑷姩璁＄畻閮ㄩ棬灞傜骇锛堝鏋滀慨鏀逛簡鐖堕儴闂級
    - 鑷姩鏇存柊瀛愰儴闂ㄧ殑灞傜骇
    
    Args:
        dept_id: 閮ㄩ棬ID
        dept: 閮ㄩ棬鏇存柊鏁版嵁
    
    Returns:
        DepartmentResponse: 鏇存柊鍚庣殑閮ㄩ棬淇℃伅
    
    Raises:
        HTTPException: 楠岃瘉澶辫触鎴栭儴闂ㄤ笉瀛樺湪鏃舵姏鍑?00鎴?04閿欒
    """
    logger.info(f"鏇存柊閮ㄩ棬: dept_id={dept_id}")
    
    try:
        dept_service = DepartmentService(db)
        department = dept_service.update_department(dept_id, dept.dict(exclude_unset=True))
        return DepartmentResponse(**department.to_dict())
    except ValueError as e:
        logger.error(f"鏇存柊閮ㄩ棬澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"鏇存柊閮ㄩ棬寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鏇存柊閮ㄩ棬澶辫触")


@router.delete("/{dept_id}", summary="鍒犻櫎閮ㄩ棬")
async def delete_department(
    dept_id: str,
    db: Session = Depends(get_db)
):
    """
    鍒犻櫎閮ㄩ棬
    
    鍔熻兘锛?    - 妫€鏌ラ儴闂ㄦ槸鍚﹀瓨鍦?    - 妫€鏌ユ槸鍚︽湁瀛愰儴闂?    - 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
    
    Args:
        dept_id: 閮ㄩ棬ID
    
    Returns:
        dict: 鍒犻櫎缁撴灉
    
    Raises:
        HTTPException: 楠岃瘉澶辫触鏃舵姏鍑?00閿欒
    """
    logger.info(f"鍒犻櫎閮ㄩ棬: dept_id={dept_id}")
    
    try:
        dept_service = DepartmentService(db)
        dept_service.delete_department(dept_id)
        return {"message": "鍒犻櫎鎴愬姛"}
    except ValueError as e:
        logger.error(f"鍒犻櫎閮ㄩ棬澶辫触: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"鍒犻櫎閮ㄩ棬寮傚父: {str(e)}")
        raise HTTPException(status_code=500, detail="鍒犻櫎閮ㄩ棬澶辫触")
