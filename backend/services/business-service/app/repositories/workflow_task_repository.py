# -*- coding: utf-8 -*-
"""
宸ヤ綔娴佷换鍔℃暟鎹闂眰

鍔熻兘璇存槑锛?1. 宸ヤ綔娴佷换鍔RUD鎿嶄綔
2. 宸ヤ綔娴佷换鍔℃煡璇㈡搷浣?3. 宸ヤ綔娴佷换鍔＄粺璁℃搷浣?
浣跨敤绀轰緥锛?    from app.repositories.workflow_task_repository import WorkflowTaskRepository
    
    task_repo = WorkflowTaskRepository(db)
    tasks = task_repo.get_user_tasks(user_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.workflow import WorkflowTask


class WorkflowTaskRepository:
    """
    宸ヤ綔娴佷换鍔℃暟鎹闂眰
    
    鍔熻兘锛?    - 宸ヤ綔娴佷换鍔RUD鎿嶄綔
    - 宸ヤ綔娴佷换鍔℃煡璇㈡搷浣?    - 宸ヤ綔娴佷换鍔＄粺璁℃搷浣?    
    浣跨敤鏂规硶锛?        task_repo = WorkflowTaskRepository(db)
        tasks = task_repo.get_user_tasks(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧伐浣滄祦浠诲姟鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, task: WorkflowTask) -> WorkflowTask:
        """
        鍒涘缓宸ヤ綔娴佷换鍔?        
        Args:
            task: 浠诲姟瀵硅薄
        
        Returns:
            WorkflowTask: 鍒涘缓鐨勪换鍔″璞?        """
        logger.info(f"鍒涘缓宸ヤ綔娴佷换鍔? node_name={task.node_name}, assignee_id={task.assignee_id}")
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_id(self, task_id: str) -> Optional[WorkflowTask]:
        """
        鏍规嵁ID鑾峰彇浠诲姟
        
        Args:
            task_id: 浠诲姟ID
        
        Returns:
            Optional[WorkflowTask]: 浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(WorkflowTask).filter(WorkflowTask.id == task_id).first()
    
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
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTask).filter(WorkflowTask.assignee_id == user_id)
        
        if status:
            query = query.filter(WorkflowTask.status == status)
        
        return query.order_by(WorkflowTask.started_at.desc()).offset(offset).limit(page_size).all()
    
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
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow_id)
        
        if status:
            query = query.filter(WorkflowTask.status == status)
        
        return query.order_by(WorkflowTask.started_at.asc()).offset(offset).limit(page_size).all()
    
    def get_pending_tasks(self, page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        鑾峰彇寰呭鐞嗕换鍔?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowTask]: 浠诲姟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(WorkflowTask).filter(
            WorkflowTask.status == "pending"
        ).order_by(WorkflowTask.started_at.asc()).offset(offset).limit(page_size).all()
    
    def search_tasks(self, keyword: str, tenant_id: Optional[str] = None,
                    page: int = 1, page_size: int = 10) -> List[WorkflowTask]:
        """
        鎼滅储浠诲姟
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 绉熸埛ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowTask]: 浠诲姟鍒楄〃
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
        鏇存柊浠诲姟
        
        Args:
            task: 浠诲姟瀵硅薄
        
        Returns:
            WorkflowTask: 鏇存柊鍚庣殑浠诲姟瀵硅薄
        """
        logger.info(f"鏇存柊宸ヤ綔娴佷换鍔? task_id={task.id}")
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, task_id: str) -> bool:
        """
        鍒犻櫎浠诲姟
        
        Args:
            task_id: 浠诲姟ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎宸ヤ綔娴佷换鍔? task_id={task_id}")
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        # 妫€鏌ユ槸鍚﹀彲浠ュ垹闄わ紙鍙湁寰呭鐞嗙殑浠诲姟鍙互鍒犻櫎锛?        if not task.is_pending():
            raise ValueError("鏃犳硶鍒犻櫎宸插鐞嗙殑浠诲姟")
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    def count_by_user(self, user_id: str, status: Optional[str] = None) -> int:
        """
        缁熻鐢ㄦ埛浠诲姟鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID
            status: 鐘舵€侊紙鍙€夛級
        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        query = self.db.query(WorkflowTask).filter(WorkflowTask.assignee_id == user_id)
        if status:
            query = query.filter(WorkflowTask.status == status)
        return query.count()
    
    def count_by_workflow(self, workflow_id: str) -> int:
        """
        缁熻宸ヤ綔娴佺殑浠诲姟鏁伴噺
        
        Args:
            workflow_id: 宸ヤ綔娴両D
        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        return self.db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈変换鍔℃暟閲?        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        return self.db.query(WorkflowTask).count()
