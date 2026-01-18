# -*- coding: utf-8 -*-
"""
工作流API路由

功能说明：
1. 工作流实例管理
2. 工作流查询
3. 工作流统计

使用示例：
    # 获取工作流列表
    GET /api/v1/workflows
    
    # 创建工作流
    POST /api/v1/workflows
    {
        "name": "请假审批",
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

router = APIRouter(prefix="/workflows", tags=["工作流"])


@router.get("/", summary="获取工作流列表")
async def list_workflows(
    status: Optional[str] = Query(None, description="状态筛选"),
    user_id: Optional[str] = Query(None, description="用户ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取工作流列表
    
    功能说明：
    1. 支持分页查询
    2. 支持状态筛选
    3. 支持用户筛选
    
    Args:
        status: 状态筛选（可选）
        user_id: 用户ID（可选）
        page: 页码
        page_size: 每页数量
        db: 数据库会话
    
    Returns:
        工作流列表
    
    使用示例：
        GET /api/v1/workflows
        GET /api/v1/workflows?status=running
        GET /api/v1/workflows?user_id=123
        GET /api/v1/workflows?page=2&page_size=20
    """
    logger.info(f"获取工作流列表: status={status}, user_id={user_id}, page={page}, page_size={page_size}")
    
    try:
        workflow_repo = WorkflowRepository(db)
        
        if user_id:
            # 获取用户的工作流
            workflows = workflow_repo.get_user_workflows(
                user_id=user_id,
                status=status,
                page=page,
                page_size=page_size
            )
        else:
            # 获取所有工作流
            workflows = workflow_repo.get_tenant_workflows(
                tenant_id="default",  # TODO: 从token中获取
                status=status,
                page=page,
                page_size=page_size
            )
        
        # 转换为字典列表
        workflow_list = [workflow.to_dict() for workflow in workflows]
        
        logger.info(f"获取工作流列表成功: count={len(workflow_list)}")
        
        return {
            "total": len(workflow_list),
            "page": page,
            "page_size": page_size,
            "data": workflow_list
        }
    except Exception as e:
        logger.error(f"获取工作流列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取工作流列表失败"
        )


@router.get("/{workflow_id}", summary="获取工作流详情")
async def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    获取工作流详情
    
    功能说明：
    1. 根据ID获取工作流详情
    2. 包含任务信息
    
    Args:
        workflow_id: 工作流ID
        db: 数据库会话
    
    Returns:
        工作流详情
    
    使用示例：
        GET /api/v1/workflows/123
    """
    logger.info(f"获取工作流详情: workflow_id={workflow_id}")
    
    try:
        workflow_repo = WorkflowRepository(db)
        workflow = workflow_repo.get_by_id(workflow_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="工作流不存在"
            )
        
        logger.info(f"获取工作流详情成功: workflow_id={workflow_id}")
        
        return workflow.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取工作流详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取工作流详情失败"
        )


@router.post("/", summary="创建工作流")
async def create_workflow(
    name: str,
    template_id: Optional[str] = None,
    business_data: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    创建工作流
    
    功能说明：
    1. 创建新的工作流实例
    2. 自动启动工作流
    
    Args:
        name: 工作流名称
        template_id: 模板ID（可选）
        business_data: 业务数据（JSON字符串，可选）
        db: 数据库会话
    
    Returns:
        创建的工作流信息
    
    使用示例：
        POST /api/v1/workflows
        {
            "name": "请假审批",
            "template_id": "template_123",
            "business_data": "{\"reason\": \"年假\", \"days\": 5}"
        }
    """
    logger.info(f"创建工作流: name={name}, template_id={template_id}")
    
    try:
        import uuid
        from datetime import datetime
        
        # 创建工作流实例
        workflow = WorkflowInstance(
            id=str(uuid.uuid4()),
            tenant_id="default",  # TODO: 从token中获取
            name=name,
            template_id=template_id,
            initiator_id="user_123",  # TODO: 从token中获取
            initiator_name="测试用户",  # TODO: 从token中获取
            business_data=business_data,
            status="running",
            started_at=datetime.now()
        )
        
        # 保存工作流
        workflow_repo = WorkflowRepository(db)
        workflow_repo.create(workflow)
        
        logger.info(f"创建工作流成功: workflow_id={workflow.id}")
        
        return workflow.to_dict()
    except Exception as e:
        logger.error(f"创建工作流失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建工作流失败"
        )


@router.delete("/{workflow_id}", summary="删除工作流")
async def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    删除工作流
    
    功能说明：
    1. 删除指定的工作流
    2. 只能删除未启动或已终止的工作流
    
    Args:
        workflow_id: 工作流ID
        db: 数据库会话
    
    Returns:
        删除结果
    
    使用示例：
        DELETE /api/v1/workflows/123
    """
    logger.info(f"删除工作流: workflow_id={workflow_id}")
    
    try:
        workflow_repo = WorkflowRepository(db)
        success = workflow_repo.delete(workflow_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="工作流不存在"
            )
        
        logger.info(f"删除工作流成功: workflow_id={workflow_id}")
        
        return {
            "message": "删除成功",
            "workflow_id": workflow_id
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"删除工作流失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"删除工作流失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除工作流失败"
        )