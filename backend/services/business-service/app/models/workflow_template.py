# -*- coding: utf-8 -*-
"""
工作流模板模型

功能说明：
1. 工作流模板管理
2. 预置审批模板
3. 可视化设计器

使用示例：
    from app.models.workflow_template import WorkflowTemplate
    
    template = WorkflowTemplate(
        name="请假审批",
        description="员工请假审批流程",
        category="hr"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class WorkflowTemplate(BaseModel):
    """
    工作流模板模型
    
    功能：
    - 工作流模板管理
    - 预置审批模板
    - 可视化设计器
    
    属性说明：
    - id: 模板ID（主键）
    - tenant_id: 租户ID
    - name: 模板名称
    - code: 模板编码（唯一）
    - description: 模板描述
    - category: 分类
    - version: 版本
    - definition: 流程定义（JSON）
    - is_system: 是否系统模板
    - is_active: 是否激活
    - usage_count: 使用次数
    - created_at: 创建时间
    """
    
    __tablename__ = "workflow_templates"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="模板名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="模板编码")
    description = Column(Text, nullable=True, comment="模板描述")
    category = Column(String(50), nullable=False, comment="分类")
    
    # 版本信息
    version = Column(String(20), nullable=False, default="1.0", comment="版本")
    
    # 流程定义
    definition = Column(Text, nullable=False, comment="流程定义（JSON）")
    
    # 状态信息
    is_system = Column(Boolean, nullable=False, default=False, comment="是否系统模板")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否激活")
    
    # 统计信息
    usage_count = Column(Integer, nullable=False, default=0, comment="使用次数")
    
    # 关系
    workflows = relationship("Workflow", back_populates="template")
    
    def __repr__(self):
        return f"<WorkflowTemplate(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "definition": self.definition,
            "is_system": self.is_system,
            "is_active": self.is_active,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def activate(self):
        """激活模板"""
        self.is_active = True
    
    def deactivate(self):
        """停用模板"""
        self.is_active = False
    
    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.is_active