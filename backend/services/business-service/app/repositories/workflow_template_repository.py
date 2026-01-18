# -*- coding: utf-8 -*-
"""
工作流模板数据访问层

功能说明：
1. 工作流模板CRUD操作
2. 工作流模板查询操作
3. 工作流模板统计操作

使用示例：
    from app.repositories.workflow_template_repository import WorkflowTemplateRepository
    
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
    工作流模板数据访问层
    
    功能：
    - 工作流模板CRUD操作
    - 工作流模板查询操作
    - 工作流模板统计操作
    
    使用方法：
        template_repo = WorkflowTemplateRepository(db)
        templates = template_repo.get_tenant_templates(tenant_id="123")
    """
    
    def __init__(self, db: Session):
        """
        初始化工作流模板数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, template: WorkflowTemplate) -> WorkflowTemplate:
        """
        创建工作流模板
        
        Args:
            template: 工作流模板对象
        
        Returns:
            WorkflowTemplate: 创建的工作流模板对象
        """
        logger.info(f"创建工作流模板: name={template.name}, code={template.code}")
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def get_by_id(self, template_id: str) -> Optional[WorkflowTemplate]:
        """
        根据ID获取工作流模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            Optional[WorkflowTemplate]: 工作流模板对象，不存在返回None
        """
        return self.db.query(WorkflowTemplate).filter(WorkflowTemplate.id == template_id).first()
    
    def get_by_code(self, code: str) -> Optional[WorkflowTemplate]:
        """
        根据编码获取工作流模板
        
        Args:
            code: 模板编码
        
        Returns:
            Optional[WorkflowTemplate]: 工作流模板对象，不存在返回None
        """
        return self.db.query(WorkflowTemplate).filter(WorkflowTemplate.code == code).first()
    
    def get_tenant_templates(self, tenant_id: str, category: Optional[str] = None,
                            page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        获取租户工作流模板
        
        Args:
            tenant_id: 租户ID
            category: 分类（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTemplate]: 工作流模板列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(WorkflowTemplate.tenant_id == tenant_id)
        
        if category:
            query = query.filter(WorkflowTemplate.category == category)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_system_templates(self, category: Optional[str] = None,
                            page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        获取系统工作流模板
        
        Args:
            category: 分类（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTemplate]: 工作流模板列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(WorkflowTemplate.is_system == True)
        
        if category:
            query = query.filter(WorkflowTemplate.category == category)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_active_templates(self, tenant_id: Optional[str] = None,
                           page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        获取激活的工作流模板
        
        Args:
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTemplate]: 工作流模板列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(WorkflowTemplate).filter(WorkflowTemplate.is_active == True)
        
        if tenant_id:
            query = query.filter(WorkflowTemplate.tenant_id == tenant_id)
        
        return query.order_by(WorkflowTemplate.created_at.desc()).offset(offset).limit(page_size).all()
    
    def search_templates(self, keyword: str, tenant_id: Optional[str] = None,
                        page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        搜索工作流模板
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTemplate]: 工作流模板列表
        """
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
        更新工作流模板
        
        Args:
            template: 工作流模板对象
        
        Returns:
            WorkflowTemplate: 更新后的工作流模板对象
        """
        logger.info(f"更新工作流模板: template_id={template.id}")
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def delete(self, template_id: str) -> bool:
        """
        删除工作流模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除工作流模板: template_id={template_id}")
        template = self.get_by_id(template_id)
        if not template:
            return False
        
        # 检查是否为系统模板
        if template.is_system:
            raise ValueError("无法删除系统模板")
        
        self.db.delete(template)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户模板数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 模板数量
        """
        return self.db.query(WorkflowTemplate).filter(WorkflowTemplate.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        统计所有模板数量
        
        Returns:
            int: 模板数量
        """
        return self.db.query(WorkflowTemplate).count()