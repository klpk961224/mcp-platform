# -*- coding: utf-8 -*-
"""
宸ヤ綔娴丄PI璺敱

鍔熻兘璇存槑锛?1. 宸ヤ綔娴佸疄渚嬬鐞?2. 宸ヤ綔娴佹煡璇?3. 宸ヤ綔娴佺粺璁?
浣跨敤绀轰緥锛?    # 鑾峰彇宸ヤ綔娴佸垪琛?    GET /api/v1/workflows
    
    # 创建宸ヤ綔娴?    POST /api/v1/workflows
    {
        "name": "璇峰亣瀹℃壒",
        "template_id": "template_123"
    }
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional

from app.core.deps import get_db
from app.repositories.workflow_repository import WorkflowRepository
from common.database.models.workflow import WorkflowInstance

router = APIRouter(prefix="/workflows", tags=["宸ヤ綔娴?])


@router.get("/", summary="鑾峰彇宸ヤ綔娴佸垪琛?)
async def list_workflows(
    workflow_status: Optional[str] = Query(None, description="状态佺瓫閫?),
    user_id: Optional[str] = Query(None, description="用户ID"),
    page: int = Query(1, ge=1, description="椤电爜"),
    page_size: int = Query(10, ge=1, le=100, description="姣忛〉数量"),
    db: Session = Depends(get_db)
):
    """
    鑾峰彇宸ヤ綔娴佸垪琛?
    鍔熻兘璇存槑锛?    1. 鏀寔鍒嗛〉查询
    2. 鏀寔状态佺瓫閫?    3. 鏀寔鐢ㄦ埛绛涢€?
    Args:
        workflow_status: 状态佺瓫閫夛紙鍙€夛級
        user_id: 用户ID锛堝彲閫夛級
        page: 椤电爜
        page_size: 姣忛〉数量
        db: 鏁版嵁搴撲細璇?
    Returns:
        宸ヤ綔娴佸垪琛?
    浣跨敤绀轰緥锛?        GET /api/v1/workflows
        GET /api/v1/workflows?workflow_status=running
        GET /api/v1/workflows?user_id=123
        GET /api/v1/workflows?page=2&page_size=20
    """
    logger.info(f"鑾峰彇宸ヤ綔娴佸垪琛? workflow_status={workflow_status}, user_id={user_id}, page={page}, page_size={page_size}")

    try:
        workflow_repo = WorkflowRepository(db)

        if user_id:
            # 鑾峰彇鐢ㄦ埛鐨勫伐浣滄祦
            workflows = workflow_repo.get_user_workflows(
                user_id=user_id,
                workflow_status=workflow_status,
                page=page,
                page_size=page_size
            )
        else:
            # 鑾峰彇鎵€鏈夊伐浣滄祦
            workflows = workflow_repo.get_tenant_workflows(
                tenant_id="default",  # TODO: 浠巘oken涓幏鍙?                workflow_status=workflow_status,
                page=page,
                page_size=page_size
            )

        # 杞崲涓哄瓧鍏稿垪琛?        workflow_list = [workflow.to_dict() for workflow in workflows]

        logger.info(f"鑾峰彇宸ヤ綔娴佸垪琛ㄦ垚鍔? count={len(workflow_list)}")

        return {
            "total": len(workflow_list),
            "page": page,
            "page_size": page_size,
            "data": workflow_list
        }
    except Exception as e:
        logger.error(f"鑾峰彇宸ヤ綔娴佸垪琛ㄥけ璐? {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="鑾峰彇宸ヤ綔娴佸垪琛ㄥけ璐?
        )


@router.get("/{workflow_id}", summary="鑾峰彇宸ヤ綔娴佽鎯?)
async def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    鑾峰彇宸ヤ綔娴佽鎯?    
    鍔熻兘璇存槑锛?    1. 根据ID鑾峰彇宸ヤ綔娴佽鎯?    2. 鍖呭惈浠诲姟淇℃伅
    
    Args:
        workflow_id: 宸ヤ綔娴両D
        db: 鏁版嵁搴撲細璇?    
    Returns:
        宸ヤ綔娴佽鎯?    
    浣跨敤绀轰緥锛?        GET /api/v1/workflows/123
    """
    logger.info(f"鑾峰彇宸ヤ綔娴佽鎯? workflow_id={workflow_id}")
    
    try:
        workflow_repo = WorkflowRepository(db)
        workflow = workflow_repo.get_by_id(workflow_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="宸ヤ綔娴佷笉瀛樺湪"
            )
        
        logger.info(f"鑾峰彇宸ヤ綔娴佽鎯呮垚鍔? workflow_id={workflow_id}")
        
        return workflow.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鑾峰彇宸ヤ綔娴佽鎯呭け璐? {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="鑾峰彇宸ヤ綔娴佽鎯呭け璐?
        )


@router.post("/", summary="创建宸ヤ綔娴?)
async def create_workflow(
    name: str,
    template_id: Optional[str] = None,
    business_data: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    创建宸ヤ綔娴?    
    鍔熻兘璇存槑锛?    1. 创建鏂扮殑宸ヤ綔娴佸疄渚?    2. 鑷姩鍚姩宸ヤ綔娴?    
    Args:
        name: 宸ヤ綔娴佸悕绉?        template_id: 妯℃澘ID锛堝彲閫夛級
        business_data: 涓氬姟鏁版嵁锛圝SON瀛楃涓诧紝鍙€夛級
        db: 鏁版嵁搴撲細璇?    
    Returns:
        创建鐨勫伐浣滄祦淇℃伅
    
    浣跨敤绀轰緥锛?        POST /api/v1/workflows
        {
            "name": "璇峰亣瀹℃壒",
            "template_id": "template_123",
            "business_data": "{\"reason\": \"骞村亣\", \"days\": 5}"
        }
    """
    logger.info(f"创建宸ヤ綔娴? name={name}, template_id={template_id}")
    
    try:
        import uuid
        from datetime import datetime
        
        # 创建宸ヤ綔娴佸疄渚?        workflow = WorkflowInstance(
            id=str(uuid.uuid4()),
            tenant_id="default",  # TODO: 浠巘oken涓幏鍙?            name=name,
            template_id=template_id,
            initiator_id="user_123",  # TODO: 浠巘oken涓幏鍙?            initiator_name="娴嬭瘯鐢ㄦ埛",  # TODO: 浠巘oken涓幏鍙?            business_data=business_data,
            status="running",
            started_at=datetime.now()
        )
        
        # 保存宸ヤ綔娴?        workflow_repo = WorkflowRepository(db)
        workflow_repo.create(workflow)
        
        logger.info(f"创建宸ヤ綔娴佹垚鍔? workflow_id={workflow.id}")
        
        return workflow.to_dict()
    except Exception as e:
        logger.error(f"创建宸ヤ綔娴佸け璐? {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建宸ヤ綔娴佸け璐?
        )


@router.delete("/{workflow_id}", summary="删除宸ヤ綔娴?)
async def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    删除宸ヤ綔娴?    
    鍔熻兘璇存槑锛?    1. 删除鎸囧畾鐨勫伐浣滄祦
    2. 鍙兘删除鏈惎鍔ㄦ垨宸茬粓姝㈢殑宸ヤ綔娴?    
    Args:
        workflow_id: 宸ヤ綔娴両D
        db: 鏁版嵁搴撲細璇?    
    Returns:
        删除缁撴灉
    
    浣跨敤绀轰緥锛?        DELETE /api/v1/workflows/123
    """
    logger.info(f"删除宸ヤ綔娴? workflow_id={workflow_id}")
    
    try:
        workflow_repo = WorkflowRepository(db)
        success = workflow_repo.delete(workflow_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="宸ヤ綔娴佷笉瀛樺湪"
            )
        
        logger.info(f"删除宸ヤ綔娴佹垚鍔? workflow_id={workflow_id}")
        
        return {
            "message": "删除鎴愬姛",
            "workflow_id": workflow_id
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"删除宸ヤ綔娴佸け璐? {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"删除宸ヤ綔娴佸け璐? {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除宸ヤ綔娴佸け璐?
        )
