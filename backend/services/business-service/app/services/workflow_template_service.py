# -*- coding: utf-8 -*-
"""
宸ヤ綔娴佹ā鏉挎湇鍔?
鍔熻兘璇存槑锛?1. 宸ヤ綔娴佹ā鏉跨鐞?2. 棰勭疆瀹℃壒妯℃澘
3. 妯℃澘瀵煎叆瀵煎嚭

浣跨敤绀轰緥锛?    from app.services.workflow_template_service import WorkflowTemplateService
    
    template_service = WorkflowTemplateService(db)
    template = template_service.create_template(name="璇峰亣瀹℃壒", code="leave_approval")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.workflow import WorkflowTemplate
from app.repositories.workflow_template_repository import WorkflowTemplateRepository


class WorkflowTemplateService:
    """
    宸ヤ綔娴佹ā鏉挎湇鍔?    
    鍔熻兘锛?    - 宸ヤ綔娴佹ā鏉跨鐞?    - 棰勭疆瀹℃壒妯℃澘
    - 妯℃澘瀵煎叆瀵煎嚭
    
    浣跨敤鏂规硶锛?        template_service = WorkflowTemplateService(db)
        template = template_service.create_template(name="璇峰亣瀹℃壒", code="leave_approval")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧伐浣滄祦妯℃澘鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.template_repo = WorkflowTemplateRepository(db)
    
    def create_template(self, name: str, code: str, tenant_id: str, definition: Dict[str, Any],
                       description: Optional[str] = None, category: str = "custom",
                       version: str = "1.0") -> WorkflowTemplate:
        """
        鍒涘缓宸ヤ綔娴佹ā鏉?        
        Args:
            name: 妯℃澘鍚嶇О
            code: 妯℃澘缂栫爜
            tenant_id: 绉熸埛ID
            definition: 娴佺▼瀹氫箟
            description: 妯℃澘鎻忚堪锛堝彲閫夛級
            category: 鍒嗙被
            version: 鐗堟湰
        
        Returns:
            WorkflowTemplate: 鍒涘缓鐨勬ā鏉垮璞?        
        Raises:
            ValueError: 妯℃澘缂栫爜宸插瓨鍦?        """
        logger.info(f"鍒涘缓宸ヤ綔娴佹ā鏉? name={name}, code={code}")
        
        # 妫€鏌ユā鏉跨紪鐮佹槸鍚﹀凡瀛樺湪
        if self.template_repo.get_by_code(code):
            raise ValueError("妯℃澘缂栫爜宸插瓨鍦?)
        
        import json
        template = WorkflowTemplate(
            tenant_id=tenant_id,
            name=name,
            code=code,
            description=description,
            category=category,
            version=version,
            definition=json.dumps(definition),
            is_system=False,
            is_active=True
        )
        
        return self.template_repo.create(template)
    
    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """
        鑾峰彇妯℃澘
        
        Args:
            template_id: 妯℃澘ID
        
        Returns:
            Optional[WorkflowTemplate]: 妯℃澘瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.template_repo.get_by_id(template_id)
    
    def get_template_by_code(self, code: str) -> Optional[WorkflowTemplate]:
        """
        鏍规嵁缂栫爜鑾峰彇妯℃澘
        
        Args:
            code: 妯℃澘缂栫爜
        
        Returns:
            Optional[WorkflowTemplate]: 妯℃澘瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.template_repo.get_by_code(code)
    
    def update_template(self, template_id: str, template_data: Dict[str, Any]) -> Optional[WorkflowTemplate]:
        """
        鏇存柊妯℃澘
        
        Args:
            template_id: 妯℃澘ID
            template_data: 妯℃澘鏁版嵁
        
        Returns:
            Optional[WorkflowTemplate]: 鏇存柊鍚庣殑妯℃澘瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鏇存柊宸ヤ綔娴佹ā鏉? template_id={template_id}")
        
        template = self.template_repo.get_by_id(template_id)
        if not template:
            return None
        
        # 鏇存柊妯℃澘
        for key, value in template_data.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        return self.template_repo.update(template)
    
    def delete_template(self, template_id: str) -> bool:
        """
        鍒犻櫎妯℃澘
        
        Args:
            template_id: 妯℃澘ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎宸ヤ綔娴佹ā鏉? template_id={template_id}")
        return self.template_repo.delete(template_id)
    
    def list_templates(self, tenant_id: Optional[str] = None, category: Optional[str] = None,
                      keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        鑾峰彇妯℃澘鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            category: 鍒嗙被锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[WorkflowTemplate]: 妯℃澘鍒楄〃
        """
        if keyword:
            return self.template_repo.search_templates(keyword, tenant_id, page, page_size)
        elif category:
            return self.template_repo.get_tenant_templates(tenant_id, category, page, page_size)
        elif tenant_id:
            return self.template_repo.get_tenant_templates(tenant_id, page=page_size)
        else:
            return self.template_repo.get_system_templates(page=page_size)
    
    def activate_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """
        婵€娲绘ā鏉?        
        Args:
            template_id: 妯℃澘ID
        
        Returns:
            Optional[WorkflowTemplate]: 鏇存柊鍚庣殑妯℃澘瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"婵€娲诲伐浣滄祦妯℃澘: template_id={template_id}")
        
        template = self.template_repo.get_by_id(template_id)
        if not template:
            return None
        
        template.activate()
        return self.template_repo.update(template)
    
    def deactivate_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """
        鍋滅敤妯℃澘
        
        Args:
            template_id: 妯℃澘ID
        
        Returns:
            Optional[WorkflowTemplate]: 鏇存柊鍚庣殑妯℃澘瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鍋滅敤宸ヤ綔娴佹ā鏉? template_id={template_id}")
        
        template = self.template_repo.get_by_id(template_id)
        if not template:
            return None
        
        template.deactivate()
        return self.template_repo.update(template)
    
    def count_templates(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻妯℃澘鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 妯℃澘鏁伴噺
        """
        if tenant_id:
            return self.template_repo.count_by_tenant(tenant_id)
        else:
            return self.template_repo.count_all()
