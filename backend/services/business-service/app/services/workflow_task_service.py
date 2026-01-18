# -*- coding: utf-8 -*-
"""
宸ヤ綔娴佷换鍔℃湇鍔?
鍔熻兘璇存槑锛?1. 宸ヤ綔娴佷换鍔＄鐞?2. 瀹℃壒浠诲姟澶勭悊
3. 浠诲姟杞氦

浣跨敤绀轰緥锛?    from app.services.workflow_task_service import WorkflowTaskService
    
    task_service = WorkflowTaskService(db)
    task = task_service.approve_task(task_id="task_123", comment="鍚屾剰")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.workflow import WorkflowTask
from app.repositories.workflow_task_repository import WorkflowTaskRepository
from app.repositories.workflow_repository import WorkflowRepository


class WorkflowTaskService:
    """
    宸ヤ綔娴佷换鍔℃湇鍔?    
    鍔熻兘锛?    - 宸ヤ綔娴佷换鍔＄鐞?    - 瀹℃壒浠诲姟澶勭悊
    - 浠诲姟杞氦
    
    浣跨敤鏂规硶锛?        task_service = WorkflowTaskService(db)
        task = task_service.approve_task(task_id="task_123", comment="鍚屾剰")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧伐浣滄祦浠诲姟鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.task_repo = WorkflowTaskRepository(db)
        self.workflow_repo = WorkflowRepository(db)
    
    def get_task(self, task_id: str) -> Optional[WorkflowTask]:
        """
        鑾峰彇浠诲姟
        
        Args:
            task_id: 浠诲姟ID
        
        Returns:
            Optional[WorkflowTask]: 浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.task_repo.get_by_id(task_id)
    
    def get_user_tasks(self, user_id: str, status: Optional[str] = None,
                      page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        鑾峰彇鐢ㄦ埛浠诲姟
        
        Args:
            user_id: 鐢ㄦ埛ID
            status: 鐘舵€侊紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowTask]: 浠诲姟鍒楄〃
        """
        return self.task_repo.get_user_tasks(user_id, status, page, page_size)
    
    def approve_task(self, task_id: str, comment: Optional[str] = None) -> Optional[WorkflowTask]:
        """
        閫氳繃瀹℃壒浠诲姟
        
        Args:
            task_id: 浠诲姟ID
            comment: 瀹℃壒鎰忚锛堝彲閫夛級
        
        Returns:
            Optional[WorkflowTask]: 鏇存柊鍚庣殑浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"閫氳繃瀹℃壒浠诲姟: task_id={task_id}")
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        if not task.is_pending():
            raise ValueError("浠诲姟宸插鐞嗭紝鏃犳硶鍐嶆瀹℃壒")
        
        task.approve(comment)
        task = self.task_repo.update(task)
        
        # 妫€鏌ュ伐浣滄祦鏄惁闇€瑕佺户缁?        self._check_workflow_continuation(task.workflow_id)
        
        return task
    
    def reject_task(self, task_id: str, comment: Optional[str] = None) -> Optional[WorkflowTask]:
        """
        鎷掔粷瀹℃壒浠诲姟
        
        Args:
            task_id: 浠诲姟ID
            comment: 瀹℃壒鎰忚锛堝彲閫夛級
        
        Returns:
            Optional[WorkflowTask]: 鏇存柊鍚庣殑浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鎷掔粷瀹℃壒浠诲姟: task_id={task_id}")
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        if not task.is_pending():
            raise ValueError("浠诲姟宸插鐞嗭紝鏃犳硶鍐嶆瀹℃壒")
        
        task.reject(comment)
        task = self.task_repo.update(task)
        
        # 鎷掔粷鍚庣粓姝㈠伐浣滄祦
        workflow = self.workflow_repo.get_by_id(task.workflow_id)
        if workflow and workflow.is_running():
            workflow.terminate()
            self.workflow_repo.update(workflow)
        
        return task
    
    def transfer_task(self, task_id: str, new_assignee_id: str, new_assignee_name: str) -> Optional[WorkflowTask]:
        """
        杞氦浠诲姟
        
        Args:
            task_id: 浠诲姟ID
            new_assignee_id: 鏂板彈鐞嗕汉ID
            new_assignee_name: 鏂板彈鐞嗕汉鍚嶇О
        
        Returns:
            Optional[WorkflowTask]: 鏇存柊鍚庣殑浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"杞氦浠诲姟: task_id={task_id}, new_assignee_id={new_assignee_id}")
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        if not task.is_pending():
            raise ValueError("浠诲姟宸插鐞嗭紝鏃犳硶杞氦")
        
        task.transfer(new_assignee_id, new_assignee_name)
        return self.task_repo.update(task)
    
    def get_workflow_tasks(self, workflow_id: str, status: Optional[str] = None,
                          page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        鑾峰彇宸ヤ綔娴佺殑浠诲姟
        
        Args:
            workflow_id: 宸ヤ綔娴両D
            status: 鐘舵€侊紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowTask]: 浠诲姟鍒楄〃
        """
        return self.task_repo.get_workflow_tasks(workflow_id, status, page, page_size)
    
    def get_pending_tasks(self, page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        鑾峰彇寰呭鐞嗕换鍔?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowTask]: 浠诲姟鍒楄〃
        """
        return self.task_repo.get_pending_tasks(page, page_size)
    
    def _check_workflow_continuation(self, workflow_id: str):
        """
        妫€鏌ュ伐浣滄祦鏄惁闇€瑕佺户缁?        
        Args:
            workflow_id: 宸ヤ綔娴両D
        """
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if not workflow:
            return
        
        # 鑾峰彇宸ヤ綔娴佺殑鎵€鏈変换鍔?        tasks = self.task_repo.get_workflow_tasks(workflow_id)
        
        # 妫€鏌ユ槸鍚︽墍鏈変换鍔￠兘宸插畬鎴?        all_finished = all(task.is_finished() for task in tasks)
        
        if all_finished:
            # 妫€鏌ユ槸鍚︽湁鎷掔粷鐨勪换鍔?            has_rejected = any(task.is_rejected() for task in tasks)
            
            if has_rejected:
                workflow.terminate()
            else:
                workflow.finish()
            
            self.workflow_repo.update(workflow)
    
    def get_task_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        鑾峰彇鐢ㄦ埛浠诲姟缁熻淇℃伅
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            Dict[str, Any]: 缁熻淇℃伅
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
        缁熻浠诲姟鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID锛堝彲閫夛級
        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        if user_id:
            return self.task_repo.count_by_user(user_id)
        else:
            return self.task_repo.count_all()
