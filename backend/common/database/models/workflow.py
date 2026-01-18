"""
宸ヤ綔娴佺浉鍏虫ā鍨?
鍖呭惈锛?- WorkflowDefinition: 宸ヤ綔娴佸畾涔夎〃
- WorkflowInstance: 宸ヤ綔娴佸疄渚嬭〃
- WorkflowNode: 宸ヤ綔娴佽妭鐐硅〃
- WorkflowTask: 宸ヤ綔娴佷换鍔¤〃
- WorkflowLog: 宸ヤ綔娴佹棩蹇楄〃
- WorkflowTemplate: 宸ヤ綔娴佹ā鏉胯〃
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel, FullModelMixin, TimestampMixin, CreatedAtMixin


class WorkflowDefinition(BaseModel, FullModelMixin):
    """宸ヤ綔娴佸畾涔夎〃"""

    __tablename__ = 'workflow_definitions'

    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(50), nullable=False)
    definition_json = Column(JSON, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(20), nullable=False, default='active')


class WorkflowInstance(BaseModel, FullModelMixin):
    """宸ヤ綔娴佸疄渚嬭〃"""

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


class WorkflowNode(BaseModel, TimestampMixin):
    """宸ヤ綔娴佽妭鐐硅〃"""

    __tablename__ = 'workflow_nodes'

    definition_id = Column(String(50), ForeignKey('workflow_definitions.id', ondelete='CASCADE'), nullable=False)
    node_key = Column(String(50), nullable=False)
    node_type = Column(String(50), nullable=False)
    node_name = Column(String(100), nullable=False)
    node_config = Column(JSON)
    sort_order = Column(Integer, nullable=False, default=0)

    definition = relationship('WorkflowDefinition')


class WorkflowTask(BaseModel, TimestampMixin):
    """宸ヤ綔娴佷换鍔¤〃"""

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


class WorkflowLog(BaseModel, CreatedAtMixin):
    """宸ヤ綔娴佹棩蹇楄〃"""

    __tablename__ = 'workflow_logs'

    instance_id = Column(String(50), ForeignKey('workflow_instances.id', ondelete='CASCADE'), nullable=False)
    task_id = Column(String(50), ForeignKey('workflow_tasks.id', ondelete='SET NULL'))
    user_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))
    action = Column(String(50), nullable=False)
    comment = Column(Text)
    log_data = Column(JSON)


class WorkflowTemplate(BaseModel, FullModelMixin):
    """宸ヤ綔娴佹ā鏉胯〃"""

    __tablename__ = 'workflow_templates'

    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    template_type = Column(String(50), nullable=False)
    definition_json = Column(JSON, nullable=False)
    is_system = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default='active')
