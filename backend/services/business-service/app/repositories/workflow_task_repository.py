# -*- coding: utf-8 -*-
"""
工作流任务数据访问层

功能说明：
1. 工作流任务CRUD操作
2. 工作流任务查询操作
3. 工作流任务统计操作

使用示例：
    from app.repositories.workflow_task_repository import WorkflowTaskRepository
    
    task_repo = WorkflowTaskRepository(db)
    tasks = task_repo.get_user_tasks(user_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from app.models.workflow_task import WorkflowTask


class WorkflowTaskRepository:
    """
    工作流任务数据访问层
    
    功能：
    - 工作流任务CRUD操作
    - 工作流任务查询操作
    - 工作流任务统计操作
    
    使用方法：
        task_repo = WorkflowTaskRepository(db)
        tasks = task_repo.get_user_tasks(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        初始化工作流任务数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, task: WorkflowTask) -> WorkflowTask:
        """
        创建工作流任务
        
        Args:
            task: 任务对象
        
        Returns:
            WorkflowTask: 创建的任务对象
        """
        logger.info(f"创建工作流任务: node_name={task.node_name}, assignee_id={task.assignee_id}")
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_id(self, task_id: str) -> Optional[WorkflowTask]:
        """
        根据ID获取任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            Optional[WorkflowTask]: 任务对象，不存在返回None
        """
        return self.db.query(WorkflowTask).filter(WorkflowTask.id == task_id).first()
    
    def get_user_tasks(self, user_id: str, status: Optional[str] = None,
                      page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        获取用户任务
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTask]: 任务列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTask).filter(WorkflowTask.assignee_id == user_id)
        
        if status:
            query = query.filter(WorkflowTask.status == status)
        
        return query.order_by(WorkflowTask.started_at.desc()).offset(offset).limit(page_size).all()
    
    def get_workflow_tasks(self, workflow_id: str, status: Optional[str] = None,
                          page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        获取工作流的任务
        
        Args:
            workflow_id: 工作流ID
            status: 状态（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTask]: 任务列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow_id)
        
        if status:
            query = query.filter(WorkflowTask.status == status)
        
        return query.order_by(WorkflowTask.started_at.asc()).offset(offset).limit(page_size).all()
    
    def get_pending_tasks(self, page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        获取待处理任务
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTask]: 任务列表
        """
        offset = (page - 1) * page_size
        return self.db.query(WorkflowTask).filter(
            WorkflowTask.status == "pending"
        ).order_by(WorkflowTask.started_at.asc()).offset(offset).limit(page_size).all()
    
    def search_tasks(self, keyword: str, tenant_id: Optional[str] = None,
                    page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        搜索任务
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTask]: 任务列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTask).join(Workflow).filter(
            or_(
                WorkflowTask.node_name.like(f"%{keyword}%"),
                WorkflowTask.assignee_name.like(f"%{keyword}%"),
                Workflow.name.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Workflow.tenant_id == tenant_id)
        
        return query.order_by(WorkflowTask.started_at.desc()).offset(offset).limit(page_size).all()
    
    def update(self, task: WorkflowTask) -> WorkflowTask:
        """
        更新任务
        
        Args:
            task: 任务对象
        
        Returns:
            WorkflowTask: 更新后的任务对象
        """
        logger.info(f"更新工作流任务: task_id={task.id}")
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, task_id: str) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除工作流任务: task_id={task_id}")
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        # 检查是否可以删除（只有待处理的任务可以删除）
        if not task.is_pending():
            raise ValueError("无法删除已处理的任务")
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    def count_by_user(self, user_id: str, status: Optional[str] = None) -> int:
        """
        统计用户任务数量
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
        
        Returns:
            int: 任务数量
        """
        query = self.db.query(WorkflowTask).filter(WorkflowTask.assignee_id == user_id)
        if status:
            query = query.filter(WorkflowTask.status == status)
        return query.count()
    
    def count_by_workflow(self, workflow_id: str) -> int:
        """
        统计工作流的任务数量
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            int: 任务数量
        """
        return self.db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow_id).count()
    
    def count_all(self) -> int:
        """
        统计所有任务数量
        
        Returns:
            int: 任务数量
        """
        return self.db.query(WorkflowTask).count()