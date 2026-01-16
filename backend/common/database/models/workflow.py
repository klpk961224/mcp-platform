"""
工作流相关模型

包含：
- WorkflowDefinition: 工作流定义表
- WorkflowInstance: 工作流实例表
- WorkflowNode: 工作流节点表
- WorkflowTask: 工作流任务表
- WorkflowLog: 工作流日志表
- WorkflowTemplate: 工作流模板表
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class WorkflowDefinition(BaseModel):
    """工作流定义表"""
    
    __tablename__ = 'workflow_definitions'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(50), nullable=False)
    definition_json = Column(JSON, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(20), nullable=False, default='active')
    created_by = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))


class WorkflowInstance(BaseModel):
    """工作流实例表"""
    
    __tablename__ = 'workflow_instances'
    
    instance_no = Column(String(50), nullable=False, unique=True)
    definition_id = Column(String(50), ForeignKey('workflow_definitions.id', ondelete='CASCADE'), nullable=False)
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(20), nullable=False, default='running')
    current_node_id = Column(String(50))
    initiator_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    business_key = Column(String(100))
    title = Column(String(200))
    variables = Column(JSON)
    started_at = Column(DateTime, nullable=False, default=datetime.now)
    completed_at = Column(DateTime)
    
    definition = relationship('WorkflowDefinition')
    initiator = relationship('User')
    tasks = relationship('WorkflowTask', back_populates='instance')


class WorkflowNode(BaseModel):
    """工作流节点表"""
    
    __tablename__ = 'workflow_nodes'
    
    definition_id = Column(String(50), ForeignKey('workflow_definitions.id', ondelete='CASCADE'), nullable=False)
    node_key = Column(String(50), nullable=False)
    node_type = Column(String(50), nullable=False)
    node_name = Column(String(100), nullable=False)
    node_config = Column(JSON)
    sort_order = Column(Integer, nullable=False, default=0)
    
    definition = relationship('WorkflowDefinition')


class WorkflowTask(BaseModel):
    """工作流任务表"""
    
    __tablename__ = 'workflow_tasks'
    
    instance_id = Column(String(50), ForeignKey('workflow_instances.id', ondelete='CASCADE'), nullable=False)
    node_id = Column(String(50), ForeignKey('workflow_nodes.id', ondelete='CASCADE'), nullable=False)
    task_key = Column(String(50), nullable=False)
    task_name = Column(String(100), nullable=False)
    assignee_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))
    status = Column(String(20), nullable=False, default='pending')
    action = Column(String(20))
    comment = Column(Text)
    completed_at = Column(DateTime)
    
    instance = relationship('WorkflowInstance', back_populates='tasks')
    assignee = relationship('User')


class WorkflowLog(BaseModel):
    """工作流日志表"""
    
    __tablename__ = 'workflow_logs'
    
    instance_id = Column(String(50), ForeignKey('workflow_instances.id', ondelete='CASCADE'), nullable=False)
    task_id = Column(String(50), ForeignKey('workflow_tasks.id', ondelete='SET NULL'))
    user_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))
    action = Column(String(50), nullable=False)
    comment = Column(Text)
    log_data = Column(JSON)


class WorkflowTemplate(BaseModel):
    """工作流模板表"""
    
    __tablename__ = 'workflow_templates'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    template_type = Column(String(50), nullable=False)
    definition_json = Column(JSON, nullable=False)
    is_system = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default='active')