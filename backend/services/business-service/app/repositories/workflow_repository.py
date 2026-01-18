# -*- coding: utf-8 -*-
"""
宸ヤ綔娴佹暟鎹闂眰

鍔熻兘璇存槑锛?1. 宸ヤ綔娴佸疄渚婥RUD鎿嶄綔
2. 宸ヤ綔娴佹煡璇㈡搷浣?3. 宸ヤ綔娴佺粺璁℃搷浣?
浣跨敤绀轰緥锛?    from app.repositories.workflow_repository import WorkflowRepository
    
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
    宸ヤ綔娴佹暟鎹闂眰
    
    鍔熻兘锛?    - 宸ヤ綔娴佸疄渚婥RUD鎿嶄綔
    - 宸ヤ綔娴佹煡璇㈡搷浣?    - 宸ヤ綔娴佺粺璁℃搷浣?    
    浣跨敤鏂规硶锛?        workflow_repo = WorkflowRepository(db)
        workflows = workflow_repo.get_user_workflows(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧伐浣滄祦鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, workflow: WorkflowInstance) -> WorkflowInstance:
        """
        创建宸ヤ綔娴?        
        Args:
            workflow: 宸ヤ綔娴佸璞?        
        Returns:
            Workflow: 创建鐨勫伐浣滄祦瀵硅薄
        """
        logger.info(f"创建宸ヤ綔娴? name={workflow.name}, initiator_id={workflow.initiator_id}")
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow
    
    def get_by_id(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """
        根据ID鑾峰彇宸ヤ綔娴?        
        Args:
            workflow_id: 宸ヤ綔娴両D
        
        Returns:
            Optional[WorkflowInstance]: 宸ヤ綔娴佸璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(WorkflowInstance).filter(WorkflowInstance.id == workflow_id).first()
    
    def get_user_workflows(self, user_id: str, workflow_status: Optional[str] = None,
                           page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        鑾峰彇鐢ㄦ埛宸ヤ綔娴?
        Args:
            user_id: 用户ID
            workflow_status: 状态侊紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉数量

        Returns:
            List[WorkflowInstance]: 宸ヤ綔娴佸垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowInstance).filter(WorkflowInstance.initiator_id == user_id)

        if workflow_status:
            query = query.filter(WorkflowInstance.status == workflow_status)

        return query.order_by(WorkflowInstance.started_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_workflows(self, tenant_id: str, workflow_status: Optional[str] = None,
                             page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        鑾峰彇绉熸埛宸ヤ綔娴?
        Args:
            tenant_id: 租户ID
            workflow_status: 状态侊紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉数量

        Returns:
            List[WorkflowInstance]: 宸ヤ綔娴佸垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowInstance).filter(WorkflowInstance.tenant_id == tenant_id)

        if workflow_status:
            query = query.filter(WorkflowInstance.status == workflow_status)

        return query.order_by(WorkflowInstance.started_at.desc()).offset(offset).limit(page_size).all()
    
    def get_running_workflows(self, page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        鑾峰彇杩愯涓殑宸ヤ綔娴?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[WorkflowInstance]: 宸ヤ綔娴佸垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(WorkflowInstance).filter(
            WorkflowInstance.status == "running"
        ).order_by(WorkflowInstance.started_at.asc()).offset(offset).limit(page_size).all()
    
    def search_workflows(self, keyword: str, tenant_id: Optional[str] = None,
                         page: int = 1, page_size: int = 10) -> List[WorkflowInstance]:
        """
        鎼滅储宸ヤ綔娴?        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[WorkflowInstance]: 宸ヤ綔娴佸垪琛?        """
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
        更新宸ヤ綔娴?        
        Args:
            workflow: 宸ヤ綔娴佸璞?        
        Returns:
            Workflow: 更新鍚庣殑宸ヤ綔娴佸璞?        """
        logger.info(f"更新宸ヤ綔娴? workflow_id={workflow.id}")
        self.db.commit()
        self.db.refresh(workflow)
        return workflow
    
    def delete(self, workflow_id: str) -> bool:
        """
        删除宸ヤ綔娴?        
        Args:
            workflow_id: 宸ヤ綔娴両D
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除宸ヤ綔娴? workflow_id={workflow_id}")
        workflow = self.get_by_id(workflow_id)
        if not workflow:
            return False
        
        # 妫€鏌ユ槸鍚﹀彲浠ュ垹闄わ紙鍙湁鏈惎鍔ㄦ垨宸茬粓姝㈢殑宸ヤ綔娴佸彲浠ュ垹闄わ級
        if workflow.is_running():
            raise ValueError("鏃犳硶删除杩愯涓殑宸ヤ綔娴?)
        
        self.db.delete(workflow)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str, workflow_status: Optional[str] = None) -> int:
        """
        缁熻绉熸埛宸ヤ綔娴佹暟閲?
        Args:
            tenant_id: 租户ID
            workflow_status: 状态侊紙鍙€夛級

        Returns:
            int: 宸ヤ綔娴佹暟閲?        """
        query = self.db.query(WorkflowInstance).filter(WorkflowInstance.tenant_id == tenant_id)
        if workflow_status:
            query = query.filter(WorkflowInstance.status == workflow_status)
        return query.count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夊伐浣滄祦数量
        
        Returns:
            int: 宸ヤ綔娴佹暟閲?        """
        return self.db.query(WorkflowInstance).count()
