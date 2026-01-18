"""
寰呭姙浠诲姟鐩稿叧妯″瀷

鍖呭惈锛?- TodoTask: 寰呭姙浠诲姟琛?- TodoTag: 寰呭姙浠诲姟鏍囩琛?- TodoAttachment: 寰呭姙浠诲姟闄勪欢琛?- DailyPlan: 姣忔棩璁″垝琛?- DailyPlanTask: 姣忔棩璁″垝浠诲姟鍏宠仈琛?- TodoReminder: 浠诲姟鎻愰啋琛?"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime, Table, Date, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from ..base import BaseModel, FullModelMixin, TimestampMixin


# 寰呭姙浠诲姟鏍囩鍏宠仈琛?todo_task_tags = Table(
    'todo_task_tags',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True),
    Column('todo_task_id', String(50), ForeignKey('todo_tasks.id', ondelete='CASCADE'), nullable=False),
    Column('tag_id', String(50), ForeignKey('todo_tags.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime, nullable=False, default=datetime.now),
    keep_existing=True
)


# 姣忔棩璁″垝浠诲姟鍏宠仈琛?daily_plan_tasks = Table(
    'daily_plan_tasks',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True),
    Column('daily_plan_id', String(50), ForeignKey('daily_plans.id', ondelete='CASCADE'), nullable=False),
    Column('todo_task_id', String(50), ForeignKey('todo_tasks.id', ondelete='CASCADE'), nullable=False),
    Column('sort_order', Integer, nullable=False, default=0),
    Column('created_at', DateTime, nullable=False, default=datetime.now),
    keep_existing=True
)


class TodoTask(BaseModel, FullModelMixin):
    """寰呭姙浠诲姟琛?""

    __tablename__ = 'todo_tasks'

    tenant_id: Mapped[str] = mapped_column(String(50), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    task_type: Mapped[str] = mapped_column(String(20), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default='medium')
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    workflow_instance_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("workflow_instances.id", ondelete="SET NULL"))
    workflow_task_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("workflow_tasks.id", ondelete="SET NULL"))

    user = relationship('User')
    tags = relationship('TodoTag', secondary=todo_task_tags, back_populates='tasks')
    attachments = relationship('TodoAttachment', back_populates='task')


class TodoTag(BaseModel, TimestampMixin):
    """寰呭姙浠诲姟鏍囩琛?""

    __tablename__ = 'todo_tags'

    tenant_id: Mapped[str] = mapped_column(String(50), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(20))

    tasks = relationship('TodoTask', secondary=todo_task_tags, back_populates='tags')


class TodoAttachment(BaseModel, TimestampMixin):
    """寰呭姙浠诲姟闄勪欢琛?""

    __tablename__ = 'todo_attachments'

    todo_task_id: Mapped[str] = mapped_column(String(50), ForeignKey("todo_tasks.id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    file_type: Mapped[Optional[str]] = mapped_column(String(50))

    task = relationship('TodoTask', back_populates='attachments')


class DailyPlan(BaseModel, TimestampMixin):
    """姣忔棩璁″垝琛?""

    __tablename__ = 'daily_plans'

    tenant_id: Mapped[str] = mapped_column(String(50), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='active')

    user = relationship('User')
    tasks = relationship('TodoTask', secondary=daily_plan_tasks)


class TodoReminder(BaseModel, TimestampMixin):
    """浠诲姟鎻愰啋琛?""

    __tablename__ = 'todo_reminders'

    todo_task_id: Mapped[str] = mapped_column(String(50), ForeignKey("todo_tasks.id", ondelete="CASCADE"), nullable=False)
    reminder_type: Mapped[str] = mapped_column(String(20), nullable=False)
    reminder_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
