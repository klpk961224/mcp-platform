"""
待办任务相关模型

包含：
- TodoTask: 待办任务表
- TodoTag: 待办任务标签表
- TodoAttachment: 待办任务附件表
- DailyPlan: 每日计划表
- DailyPlanTask: 每日计划任务关联表
- TodoReminder: 任务提醒表
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime, Table, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel


# 待办任务标签关联表
todo_task_tags = Table(
    'todo_task_tags',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True),
    Column('todo_task_id', String(50), ForeignKey('todo_tasks.id', ondelete='CASCADE'), nullable=False),
    Column('tag_id', String(50), ForeignKey('todo_tags.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime, nullable=False, default=datetime.now)
)


# 每日计划任务关联表
daily_plan_tasks = Table(
    'daily_plan_tasks',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True),
    Column('daily_plan_id', String(50), ForeignKey('daily_plans.id', ondelete='CASCADE'), nullable=False),
    Column('todo_task_id', String(50), ForeignKey('todo_tasks.id', ondelete='CASCADE'), nullable=False),
    Column('sort_order', Integer, nullable=False, default=0),
    Column('created_at', DateTime, nullable=False, default=datetime.now)
)


class TodoTask(BaseModel):
    """待办任务表"""
    
    __tablename__ = 'todo_tasks'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    task_type = Column(String(20), nullable=False)
    priority = Column(String(20), nullable=False, default='medium')
    status = Column(String(20), nullable=False, default='pending')
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    workflow_instance_id = Column(String(50), ForeignKey('workflow_instances.id', ondelete='SET NULL'))
    workflow_task_id = Column(String(50), ForeignKey('workflow_tasks.id', ondelete='SET NULL'))
    
    user = relationship('User')
    tags = relationship('TodoTag', secondary=todo_task_tags, back_populates='tasks')
    attachments = relationship('TodoAttachment', back_populates='task')


class TodoTag(BaseModel):
    """待办任务标签表"""
    
    __tablename__ = 'todo_tags'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    color = Column(String(20))
    
    tasks = relationship('TodoTask', secondary=todo_task_tags, back_populates='tags')


class TodoAttachment(BaseModel):
    """待办任务附件表"""
    
    __tablename__ = 'todo_attachments'
    
    todo_task_id = Column(String(50), ForeignKey('todo_tasks.id', ondelete='CASCADE'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    
    task = relationship('TodoTask', back_populates='attachments')


class DailyPlan(BaseModel):
    """每日计划表"""
    
    __tablename__ = 'daily_plans'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    plan_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default='active')
    
    user = relationship('User')
    tasks = relationship('TodoTask', secondary=daily_plan_tasks)


class TodoReminder(BaseModel):
    """任务提醒表"""
    
    __tablename__ = 'todo_reminders'
    
    todo_task_id = Column(String(50), ForeignKey('todo_tasks.id', ondelete='CASCADE'), nullable=False)
    reminder_type = Column(String(20), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)
    sent_at = Column(DateTime)