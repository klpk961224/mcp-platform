# -*- coding: utf-8 -*-
"""
工作流任务服务

功能说明：
1. 工作流任务管理
2. 审批任务处理
3. 任务转交

使用示例：
    from app.services.workflow_task_service import WorkflowTaskService
    
    task_service = WorkflowTaskService(db)
    task = task_service.approve_task(task_id="task_123", comment="同意")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.workflow import WorkflowTask
from app.repositories.workflow_task_repository import WorkflowTaskRepository
from app.repositories.workflow_repository import WorkflowRepository


class WorkflowTaskService:
    """
    工作流任务服务
    
    功能：
    - 工作流任务管理
    - 审批任务处理
    - 任务转交
    
    使用方法：
        task_service = WorkflowTaskService(db)
        task = task_service.approve_task(task_id="task_123", comment="同意")
    """
    
    def __init__(self, db: Session):
        """
        初始化工作流任务服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.task_repo = WorkflowTaskRepository(db)
        self.workflow_repo = WorkflowRepository(db)
    
    def get_task(self, task_id: str) -> Optional[WorkflowTask]:
        """
        获取任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            Optional[WorkflowTask]: 任务对象，不存在返回None
        """
        return self.task_repo.get_by_id(task_id)
    
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
        return self.task_repo.get_user_tasks(user_id, status, page, page_size)
    
    def approve_task(self, task_id: str, comment: Optional[str] = None) -> Optional[WorkflowTask]:
        """
        通过审批任务
        
        Args:
            task_id: 任务ID
            comment: 审批意见（可选）
        
        Returns:
            Optional[WorkflowTask]: 更新后的任务对象，不存在返回None
        """
        logger.info(f"通过审批任务: task_id={task_id}")
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        if not task.is_pending():
            raise ValueError("任务已处理，无法再次审批")
        
        task.approve(comment)
        task = self.task_repo.update(task)
        
        # 检查工作流是否需要继续
        self._check_workflow_continuation(task.workflow_id)
        
        return task
    
    def reject_task(self, task_id: str, comment: Optional[str] = None) -> Optional[WorkflowTask]:
        """
        拒绝审批任务
        
        Args:
            task_id: 任务ID
            comment: 审批意见（可选）
        
        Returns:
            Optional[WorkflowTask]: 更新后的任务对象，不存在返回None
        """
        logger.info(f"拒绝审批任务: task_id={task_id}")
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        if not task.is_pending():
            raise ValueError("任务已处理，无法再次审批")
        
        task.reject(comment)
        task = self.task_repo.update(task)
        
        # 拒绝后终止工作流
        workflow = self.workflow_repo.get_by_id(task.workflow_id)
        if workflow and workflow.is_running():
            workflow.terminate()
            self.workflow_repo.update(workflow)
        
        return task
    
    def transfer_task(self, task_id: str, new_assignee_id: str, new_assignee_name: str) -> Optional[WorkflowTask]:
        """
        转交任务
        
        Args:
            task_id: 任务ID
            new_assignee_id: 新受理人ID
            new_assignee_name: 新受理人名称
        
        Returns:
            Optional[WorkflowTask]: 更新后的任务对象，不存在返回None
        """
        logger.info(f"转交任务: task_id={task_id}, new_assignee_id={new_assignee_id}")
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        if not task.is_pending():
            raise ValueError("任务已处理，无法转交")
        
        task.transfer(new_assignee_id, new_assignee_name)
        return self.task_repo.update(task)
    
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
        return self.task_repo.get_workflow_tasks(workflow_id, status, page, page_size)
    
    def get_pending_tasks(self, page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        获取待处理任务
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTask]: 任务列表
        """
        return self.task_repo.get_pending_tasks(page, page_size)
    
    def _check_workflow_continuation(self, workflow_id: str):
        """
        检查工作流是否需要继续
        
        Args:
            workflow_id: 工作流ID
        """
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if not workflow:
            return
        
        # 获取工作流的所有任务
        tasks = self.task_repo.get_workflow_tasks(workflow_id)
        
        # 检查是否所有任务都已完成
        all_finished = all(task.is_finished() for task in tasks)
        
        if all_finished:
            # 检查是否有拒绝的任务
            has_rejected = any(task.is_rejected() for task in tasks)
            
            if has_rejected:
                workflow.terminate()
            else:
                workflow.finish()
            
            self.workflow_repo.update(workflow)
    
    def get_task_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户任务统计信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        total = self.task_repo.count_by_user(user_id)
        pending = self.task_repo.count_by_user(user_id, "pending")
        approved = self.task_repo.count_by_user(user_id, "approved")
        rejected = self.task_repo.count_by_user(user_id, "rejected")
        transferred = self.task_repo.count_by_user(user_id, "transferred")
        
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "transferred": transferred,
            "completion_rate": round((approved + rejected + transferred) / total * 100, 2) if total > 0 else 0
        }
    
    def count_tasks(self, user_id: Optional[str] = None) -> int:
        """
        统计任务数量
        
        Args:
            user_id: 用户ID（可选）
        
        Returns:
            int: 任务数量
        """
        if user_id:
            return self.task_repo.count_by_user(user_id)
        else:
            return self.task_repo.count_all()