# -*- coding: utf-8 -*-
"""
宸ヤ綔娴佹湇鍔?
鍔熻兘璇存槑锛?1. 宸ヤ綔娴佸疄渚嬬鐞?2. 宸ヤ綔娴佹墽琛?3. 宸ヤ綔娴佺洃鎺?
浣跨敤绀轰緥锛?    from app.services.workflow_service import WorkflowService
    
    workflow_service = WorkflowService(db)
    workflow = workflow_service.start_workflow(template_id="template_123", initiator_id="user_123")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from common.database.models.workflow import WorkflowInstance
from common.database.models.workflow import WorkflowTask
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.workflow_task_repository import WorkflowTaskRepository
from app.repositories.workflow_template_repository import WorkflowTemplateRepository


class WorkflowService:
    """
    宸ヤ綔娴佹湇鍔?    
    鍔熻兘锛?    - 宸ヤ綔娴佸疄渚嬬鐞?    - 宸ヤ綔娴佹墽琛?    - 宸ヤ綔娴佺洃鎺?    
    浣跨敤鏂规硶锛?        workflow_service = WorkflowService(db)
        workflow = workflow_service.start_workflow(template_id="template_123", initiator_id="user_123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧伐浣滄祦鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.workflow_repo = WorkflowRepository(db)
        self.task_repo = WorkflowTaskRepository(db)
        self.template_repo = WorkflowTemplateRepository(db)
    
    def start_workflow(self, template_id: str, initiator_id: str, initiator_name: str,
                      tenant_id: str, business_data: Optional[Dict[str, Any]] = None,
                      variables: Optional[Dict[str, Any]] = None) -> WorkflowInstance:
        """
        鍚姩宸ヤ綔娴?        
        Args:
            template_id: 妯℃澘ID
            initiator_id: 鍙戣捣浜篒D
            initiator_name: 鍙戣捣浜哄悕绉?            tenant_id: 绉熸埛ID
            business_data: 涓氬姟鏁版嵁锛堝彲閫夛級
            variables: 鍙橀噺锛堝彲閫夛級
        
        Returns:
            WorkflowInstance: 鍒涘缓鐨勫伐浣滄祦瀵硅薄
        """
        logger.info(f"鍚姩宸ヤ綔娴? template_id={template_id}, initiator_id={initiator_id}")
        
        # 鑾峰彇妯℃澘
        template = self.template_repo.get_by_id(template_id)
        if not template:
            raise ValueError("宸ヤ綔娴佹ā鏉夸笉瀛樺湪")
        
        if not template.is_available():
            raise ValueError("宸ヤ綔娴佹ā鏉夸笉鍙敤")
        
        # 澧炲姞妯℃澘浣跨敤娆℃暟
        template.increment_usage()
        self.template_repo.update(template)
        
        import json
        workflow = WorkflowInstance(
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
        
        # 瑙ｆ瀽娴佺▼瀹氫箟骞跺垱寤轰换鍔?        definition = json.loads(template.definition)
        self._create_tasks_from_definition(workflow, definition)
        
        logger.info(f"宸ヤ綔娴佸惎鍔ㄦ垚鍔? workflow_id={workflow.id}")
        return workflow
    
    def _create_tasks_from_definition(self, workflow: WorkflowInstance, definition: Dict[str, Any]):
        """浠庢祦绋嬪畾涔夊垱寤轰换鍔?""
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
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """
        鑾峰彇宸ヤ綔娴?        
        Args:
            workflow_id: 宸ヤ綔娴両D
        
        Returns:
            Optional[WorkflowInstance]: 宸ヤ綔娴佸璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.workflow_repo.get_by_id(workflow_id)
    
    def get_user_workflows(self, user_id: str, status: Optional[str] = None,
                           page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        鑾峰彇鐢ㄦ埛宸ヤ綔娴?        
        Args:
            user_id: 鐢ㄦ埛ID
            status: 鐘舵€侊紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowInstance]: 宸ヤ綔娴佸垪琛?        """
        return self.workflow_repo.get_user_workflows(user_id, status, page, page_size)
    
    def terminate_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """
        缁堟宸ヤ綔娴?        
        Args:
            workflow_id: 宸ヤ綔娴両D
        
        Returns:
            Optional[WorkflowInstance]: 鏇存柊鍚庣殑宸ヤ綔娴佸璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        logger.info(f"缁堟宸ヤ綔娴? workflow_id={workflow_id}")
        
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if not workflow:
            return None
        
        workflow.terminate()
        return self.workflow_repo.update(workflow)
    
    def get_workflow_statistics(self, tenant_id: str) -> Dict[str, Any]:
        """
        鑾峰彇宸ヤ綔娴佺粺璁′俊鎭?        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            Dict[str, Any]: 缁熻淇℃伅
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
        缁熻宸ヤ綔娴佹暟閲?        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 宸ヤ綔娴佹暟閲?        """
        if tenant_id:
            return self.workflow_repo.count_by_tenant(tenant_id)
        else:
            return self.workflow_repo.count_all()
