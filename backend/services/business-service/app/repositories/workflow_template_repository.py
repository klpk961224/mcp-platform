# -*- coding: utf-8 -*-
"""
宸ヤ綔娴佹ā鏉挎暟鎹闂眰

鍔熻兘璇存槑锛?1. 宸ヤ綔娴佹ā鏉緾RUD鎿嶄綔
2. 宸ヤ綔娴佹ā鏉挎煡璇㈡搷浣?3. 宸ヤ綔娴佹ā鏉跨粺璁℃搷浣?
浣跨敤绀轰緥锛?    from app.repositories.workflow_template_repository import WorkflowTemplateRepository
    
    template_repo = WorkflowTemplateRepository(db)
    templates = template_repo.get_tenant_templates(tenant_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.workflow import WorkflowTemplate


class WorkflowTemplateRepository:
    """
    宸ヤ綔娴佹ā鏉挎暟鎹闂眰
    
    鍔熻兘锛?    - 宸ヤ綔娴佹ā鏉緾RUD鎿嶄綔
    - 宸ヤ綔娴佹ā鏉挎煡璇㈡搷浣?    - 宸ヤ綔娴佹ā鏉跨粺璁℃搷浣?    
    浣跨敤鏂规硶锛?        template_repo = WorkflowTemplateRepository(db)
        templates = template_repo.get_tenant_templates(tenant_id="123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧伐浣滄祦妯℃澘鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, template: WorkflowTemplate) -> WorkflowTemplate:
        """
        创建宸ヤ綔娴佹ā鏉?        
        Args:
            template: 宸ヤ綔娴佹ā鏉垮璞?        
        Returns:
            WorkflowTemplate: 创建鐨勫伐浣滄祦妯℃澘瀵硅薄
        """
        logger.info(f"创建宸ヤ綔娴佹ā鏉? name={template.name}, code={template.code}")
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def get_by_id(self, template_id: str) -> Optional[WorkflowTemplate]:
        """
        根据ID鑾峰彇宸ヤ綔娴佹ā鏉?        
        Args:
            template_id: 妯℃澘ID
        
        Returns:
            Optional[WorkflowTemplate]: 宸ヤ綔娴佹ā鏉垮璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(WorkflowTemplate).filter(WorkflowTemplate.id == template_id).first()
    
    def get_by_code(self, code: str) -> Optional[WorkflowTemplate]:
        """
        根据编码鑾峰彇宸ヤ綔娴佹ā鏉?        
        Args:
            code: 妯℃澘编码
        
        Returns:
            Optional[WorkflowTemplate]: 宸ヤ綔娴佹ā鏉垮璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(WorkflowTemplate).filter(WorkflowTemplate.code == code).first()
    
    def get_tenant_templates(self, tenant_id: str, category: Optional[str] = None,
                            page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        鑾峰彇绉熸埛宸ヤ綔娴佹ā鏉?        
        Args:
            tenant_id: 租户ID
            category: 鍒嗙被锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[WorkflowTemplate]: 宸ヤ綔娴佹ā鏉垮垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(WorkflowTemplate.tenant_id == tenant_id)
        
        if category:
            query = query.filter(WorkflowTemplate.category == category)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_system_templates(self, category: Optional[str] = None,
                            page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        鑾峰彇绯荤粺宸ヤ綔娴佹ā鏉?        
        Args:
            category: 鍒嗙被锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[WorkflowTemplate]: 宸ヤ綔娴佹ā鏉垮垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(WorkflowTemplate.is_system == True)
        
        if category:
            query = query.filter(WorkflowTemplate.category == category)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_active_templates(self, tenant_id: Optional[str] = None,
                           page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        鑾峰彇婵€娲荤殑宸ヤ綔娴佹ā鏉?        
        Args:
            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[WorkflowTemplate]: 宸ヤ綔娴佹ā鏉垮垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(WorkflowTemplate.is_active == True)
        
        if tenant_id:
            query = query.filter(WorkflowTemplate.tenant_id == tenant_id)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def search_templates(self, keyword: str, tenant_id: Optional[str] = None,
                        page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        鎼滅储宸ヤ綔娴佹ā鏉?        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[WorkflowTemplate]: 宸ヤ綔娴佹ā鏉垮垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(
            or_(
                WorkflowTemplate.name.like(f"%{keyword}%"),
                WorkflowTemplate.code.like(f"%{keyword}%"),
                WorkflowTemplate.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(WorkflowTemplate.tenant_id == tenant_id)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def update(self, template: WorkflowTemplate) -> WorkflowTemplate:
        """
        更新宸ヤ綔娴佹ā鏉?        
        Args:
            template: 宸ヤ綔娴佹ā鏉垮璞?        
        Returns:
            WorkflowTemplate: 更新鍚庣殑宸ヤ綔娴佹ā鏉垮璞?        """
        logger.info(f"更新宸ヤ綔娴佹ā鏉? template_id={template.id}")
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def delete(self, template_id: str) -> bool:
        """
        删除宸ヤ綔娴佹ā鏉?        
        Args:
            template_id: 妯℃澘ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除宸ヤ綔娴佹ā鏉? template_id={template_id}")
        template = self.get_by_id(template_id)
        if not template:
            return False
        
        # 妫€鏌ユ槸鍚︿负绯荤粺妯℃澘
        if template.is_system:
            raise ValueError("鏃犳硶删除绯荤粺妯℃澘")
        
        self.db.delete(template)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛妯℃澘数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 妯℃澘数量
        """
        return self.db.query(WorkflowTemplate).filter(WorkflowTemplate.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夋ā鏉挎暟閲?        
        Returns:
            int: 妯℃澘数量
        """
        return self.db.query(WorkflowTemplate).count()
