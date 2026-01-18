# -*- coding: utf-8 -*-
"""
工作流数据访问层

功能说明：
1. 工作流实例CRUD操作
2. 工作流查询操作
3. 工作流统计操作

使用示例：
    from app.repositories.workflow_repository import WorkflowRepository
    
    workflow_repo = WorkflowRepository(db)
    workflows = workflow_repo.get_user_workflows(user_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.workflow import WorkflowInstance


class WorkflowRepository:
    """
    工作流数据访问层
    
    功能：
    - 工作流实例CRUD操作
    - 工作流查询操作
    - 工作流统计操作
    
    使用方法：
        workflow_repo = WorkflowRepository(db)
        workflows = workflow_repo.get_user_workflows(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        初始化工作流数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, workflow: WorkflowInstance) -> WorkflowInstance:
        """
        创建工作流
        
        Args:
            workflow: 工作流对象
        
        Returns:
            Workflow: 创建的工作流对象
        """
        logger.info(f"创建工作流: name={workflow.name}, initiator_id={workflow.initiator_id}")
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow
    
    def get_by_id(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """
        根据ID获取工作流
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            Optional[WorkflowInstance]: 工作流对象，不存在返回None
        """
        return self.db.query(WorkflowInstance).filter(WorkflowInstance.id == workflow_id).first()
    
    def get_user_workflows(self, user_id: str, status: Optional[str] = None,
                           page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        获取用户工作流
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowInstance]: 工作流列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowInstance).filter(WorkflowInstance.initiator_id == user_id)
        
        if status:
            query = query.filter(WorkflowInstance.status == status)
        
        return query.order_by(WorkflowInstance.started_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_workflows(self, tenant_id: str, status: Optional[str] = None,
                             page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        获取租户工作流
        
        Args:
            tenant_id: 租户ID
            status: 状态（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowInstance]: 工作流列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowInstance).filter(WorkflowInstance.tenant_id == tenant_id)
        
        if status:
            query = query.filter(WorkflowInstance.status == status)
        
        return query.order_by(WorkflowInstance.started_at.desc()).offset(offset).limit(page_size).all()
    
    def get_running_workflows(self, page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        获取运行中的工作流
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowInstance]: 工作流列表
        """
        offset = (page - 1) * page_size
        return self.db.query(WorkflowInstance).filter(
            WorkflowInstance.status == "running"
        ).order_by(WorkflowInstance.started_at.asc()).offset(offset).limit(page_size).all()
    
    def search_workflows(self, keyword: str, tenant_id: Optional[str] = None,
                         page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        搜索工作流
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowInstance]: 工作流列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowInstance).filter(
            or_(
                WorkflowInstance.name.like(f"%{keyword}%"),
                WorkflowInstance.initiator_name.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(WorkflowInstance.tenant_id == tenant_id)
        
        return query.order_by(WorkflowInstance.started_at.desc()).offset(offset).limit(page_size).all()
    
    def update(self, workflow: WorkflowInstance) -> WorkflowInstance:
        """
        更新工作流
        
        Args:
            workflow: 工作流对象
        
        Returns:
            Workflow: 更新后的工作流对象
        """
        logger.info(f"更新工作流: workflow_id={workflow.id}")
        self.db.commit()
        self.db.refresh(workflow)
        return workflow
    
    def delete(self, workflow_id: str) -> bool:
        """
        删除工作流
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除工作流: workflow_id={workflow_id}")
        workflow = self.get_by_id(workflow_id)
        if not workflow:
            return False
        
        # 检查是否可以删除（只有未启动或已终止的工作流可以删除）
        if workflow.is_running():
            raise ValueError("无法删除运行中的工作流")
        
        self.db.delete(workflow)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str, status: Optional[str] = None) -> int:
        """
        统计租户工作流数量
        
        Args:
            tenant_id: 租户ID
            status: 状态（可选）
        
        Returns:
            int: 工作流数量
        """
        query = self.db.query(WorkflowInstance).filter(WorkflowInstance.tenant_id == tenant_id)
        if status:
            query = query.filter(WorkflowInstance.status == status)
        return query.count()
    
    def count_all(self) -> int:
        """
        统计所有工作流数量
        
        Returns:
            int: 工作流数量
        """
        return self.db.query(WorkflowInstance).count()