# -*- coding: utf-8 -*-
"""
工作流模板服务

功能说明：
1. 工作流模板管理
2. 预置审批模板
3. 模板导入导出

使用示例：
    from app.services.workflow_template_service import WorkflowTemplateService
    
    template_service = WorkflowTemplateService(db)
    template = template_service.create_template(name="请假审批", code="leave_approval")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.workflow import WorkflowTemplate
from app.repositories.workflow_template_repository import WorkflowTemplateRepository


class WorkflowTemplateService:
    """
    工作流模板服务
    
    功能：
    - 工作流模板管理
    - 预置审批模板
    - 模板导入导出
    
    使用方法：
        template_service = WorkflowTemplateService(db)
        template = template_service.create_template(name="请假审批", code="leave_approval")
    """
    
    def __init__(self, db: Session):
        """
        初始化工作流模板服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.template_repo = WorkflowTemplateRepository(db)
    
    def create_template(self, name: str, code: str, tenant_id: str, definition: Dict[str, Any],
                       description: Optional[str] = None, category: str = "custom",
                       version: str = "1.0") -> WorkflowTemplate:
        """
        创建工作流模板
        
        Args:
            name: 模板名称
            code: 模板编码
            tenant_id: 租户ID
            definition: 流程定义
            description: 模板描述（可选）
            category: 分类
            version: 版本
        
        Returns:
            WorkflowTemplate: 创建的模板对象
        
        Raises:
            ValueError: 模板编码已存在
        """
        logger.info(f"创建工作流模板: name={name}, code={code}")
        
        # 检查模板编码是否已存在
        if self.template_repo.get_by_code(code):
            raise ValueError("模板编码已存在")
        
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
        获取模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            Optional[WorkflowTemplate]: 模板对象，不存在返回None
        """
        return self.template_repo.get_by_id(template_id)
    
    def get_template_by_code(self, code: str) -> Optional[WorkflowTemplate]:
        """
        根据编码获取模板
        
        Args:
            code: 模板编码
        
        Returns:
            Optional[WorkflowTemplate]: 模板对象，不存在返回None
        """
        return self.template_repo.get_by_code(code)
    
    def update_template(self, template_id: str, template_data: Dict[str, Any]) -> Optional[WorkflowTemplate]:
        """
        更新模板
        
        Args:
            template_id: 模板ID
            template_data: 模板数据
        
        Returns:
            Optional[WorkflowTemplate]: 更新后的模板对象，不存在返回None
        """
        logger.info(f"更新工作流模板: template_id={template_id}")
        
        template = self.template_repo.get_by_id(template_id)
        if not template:
            return None
        
        # 更新模板
        for key, value in template_data.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        return self.template_repo.update(template)
    
    def delete_template(self, template_id: str) -> bool:
        """
        删除模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除工作流模板: template_id={template_id}")
        return self.template_repo.delete(template_id)
    
    def list_templates(self, tenant_id: Optional[str] = None, category: Optional[str] = None,
                      keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[WorkflowTemplate]:
        """
        获取模板列表
        
        Args:
            tenant_id: 租户ID（可选）
            category: 分类（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[WorkflowTemplate]: 模板列表
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
        激活模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            Optional[WorkflowTemplate]: 更新后的模板对象，不存在返回None
        """
        logger.info(f"激活工作流模板: template_id={template_id}")
        
        template = self.template_repo.get_by_id(template_id)
        if not template:
            return None
        
        template.activate()
        return self.template_repo.update(template)
    
    def deactivate_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """
        停用模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            Optional[WorkflowTemplate]: 更新后的模板对象，不存在返回None
        """
        logger.info(f"停用工作流模板: template_id={template_id}")
        
        template = self.template_repo.get_by_id(template_id)
        if not template:
            return None
        
        template.deactivate()
        return self.template_repo.update(template)
    
    def count_templates(self, tenant_id: Optional[str] = None) -> int:
        """
        统计模板数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 模板数量
        """
        if tenant_id:
            return self.template_repo.count_by_tenant(tenant_id)
        else:
            return self.template_repo.count_all()