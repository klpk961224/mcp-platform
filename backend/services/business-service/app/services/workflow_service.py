# -*- coding: utf-8 -*-
"""
工作流服务

功能说明：
1. 工作流实例管理
2. 工作流执行
3. 工作流监控

使用示例：
    from app.services.workflow_service import WorkflowService
    
    workflow_service = WorkflowService(db)
    workflow = workflow_service.start_workflow(template_id="template_123", initiator_id="user_123")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.workflow import Workflow
from app.models.workflow_task import WorkflowTask
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.workflow_task_repository import WorkflowTaskRepository
from app.repositories.workflow_template_repository import WorkflowTemplateRepository


class WorkflowService:
    """
    工作流服务
    
    功能：
    - 工作流实例管理
    - 工作流执行
    - 工作流监控
    
    使用方法：
        workflow_service = WorkflowService(db)
        workflow = workflow_service.start_workflow(template_id="template_123", initiator_id="user_123")
    """
    
    def __init__(self, db: Session):
        """
        初始化工作流服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.workflow_repo = WorkflowRepository(db)
        self.task_repo = WorkflowTaskRepository(db)
        self.template_repo = WorkflowTemplateRepository(db)
    
    def start_workflow(self, template_id: str, initiator_id: str, initiator_name: str,
                      tenant_id: str, business_data: Optional[Dict[str, Any]] = None,
                      variables: Optional[Dict[str, Any]] = None) -> Workflow:
        """
        启动工作流
        
        Args:
            template_id: 模板ID
            initiator_id: 发起人ID
            initiator_name: 发起人名称
            tenant_id: 租户ID
            business_data: 业务数据（可选）
            variables: 变量（可选）
        
        Returns:
            Workflow: 创建的工作流对象
        """
        logger.info(f"启动工作流: template_id={template_id}, initiator_id={initiator_id}")
        
        # 获取模板
        template = self.template_repo.get_by_id(template_id)
        if not template:
            raise ValueError("工作流模板不存在")
        
        if not template.is_available():
            raise ValueError("工作流模板不可用")
        
        # 增加模板使用次数
        template.increment_usage()
        self.template_repo.update(template)
        
        import json
        workflow = Workflow(
            tenant_id=tenant_id,
            name=template.name,
            template_id=template_id,
            initiator_id=initiator_id,
            initiator_name=initiator_name,
            business_data=json.dumps(business_data) if business_data else None,
            variables=json.dumps(variables) if variables else None,
            status="running"
        )
        
        workflow = self.workflow_repo.create(workflow)
        
        # 解析流程定义并创建任务
        definition = json.loads(template.definition)
        self._create_tasks_from_definition(workflow, definition)
        
        logger.info(f"工作流启动成功: workflow_id={workflow.id}")
        return workflow
    
    def _create_tasks_from_definition(self, workflow: Workflow, definition: Dict[str, Any]):
        """从流程定义创建任务"""
        nodes = definition.get("nodes", [])
        for node in nodes:
            if node.get("type") == "approval":
                task = WorkflowTask(
                    workflow_id=workflow.id,
                    node_id=node.get("id"),
                    node_name=node.get("name"),
                    node_type=node.get("type"),
                    assignee_id=node.get("assignee_id"),
                    assignee_name=node.get("assignee_name"),
                    status="pending"
                )
                self.task_repo.create(task)
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        获取工作流
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            Optional[Workflow]: 工作流对象，不存在返回None
        """
        return self.workflow_repo.get_by_id(workflow_id)
    
    def get_user_workflows(self, user_id: str, status: Optional[str] = None,
                           page: int = 1, page_size: int = 10) -> List[Workflow]:
        """
        获取用户工作流
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Workflow]: 工作流列表
        """
        return self.workflow_repo.get_user_workflows(user_id, status, page, page_size)
    
    def terminate_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        终止工作流
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            Optional[Workflow]: 更新后的工作流对象，不存在返回None
        """
        logger.info(f"终止工作流: workflow_id={workflow_id}")
        
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if not workflow:
            return None
        
        workflow.terminate()
        return self.workflow_repo.update(workflow)
    
    def get_workflow_statistics(self, tenant_id: str) -> Dict[str, Any]:
        """
        获取工作流统计信息
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        total = self.workflow_repo.count_by_tenant(tenant_id)
        running = self.workflow_repo.count_by_tenant(tenant_id, "running")
        completed = self.workflow_repo.count_by_tenant(tenant_id, "completed")
        terminated = self.workflow_repo.count_by_tenant(tenant_id, "terminated")
        
        return {
            "total": total,
            "running": running,
            "completed": completed,
            "terminated": terminated,
            "completion_rate": round(completed / total * 100, 2) if total > 0 else 0
        }
    
    def count_workflows(self, tenant_id: Optional[str] = None) -> int:
        """
        统计工作流数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 工作流数量
        """
        if tenant_id:
            return self.workflow_repo.count_by_tenant(tenant_id)
        else:
            return self.workflow_repo.count_all()