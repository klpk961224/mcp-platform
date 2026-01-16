# -*- coding: utf-8 -*-
"""
待办任务模型

功能说明：
1. 个人待办任务管理
2. 每日计划管理
3. 任务提醒

使用示例：
    from app.models.todo import TodoTask, DailyPlan
    
    # 创建待办任务
    todo = TodoTask(
        title="完成项目文档",
        description="编写项目设计文档",
        priority="high"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date

from common.database.base import BaseModel


class TodoTask(BaseModel):
    """
    待办任务模型
    
    功能：
    - 个人待办任务管理
    - 任务优先级管理
    - 任务截止时间
    
    属性说明：
    - id: 任务ID（主键）
    - tenant_id: 租户ID
    - user_id: 用户ID
    - username: 用户名
    - title: 任务标题
    - description: 任务描述
    - task_type: 任务类型
    - priority: 优先级
    - status: 状态
    - due_date: 截止日期
    - due_time: 截止时间
    - tags: 标签（JSON数组）
    - attachment: 附件URL
    - completed_at: 完成时间
    - is_overdue: 是否逾期
    - reminder_sent: 是否已发送提醒
    - created_at: 创建时间
    """
    
    __tablename__ = "todo_tasks"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    
    # 内容信息
    title = Column(String(255), nullable=False, comment="任务标题")
    description = Column(Text, nullable=True, comment="任务描述")
    
    # 类型信息
    task_type = Column(String(20), nullable=False, default="personal", comment="任务类型")
    priority = Column(String(20), nullable=False, default="medium", comment="优先级")
    status = Column(String(20), nullable=False, default="pending", comment="状态")
    
    # 时间信息
    due_date = Column(DateTime, nullable=True, comment="截止日期")
    due_time = Column(String(10), nullable=True, comment="截止时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    
    # 扩展信息
    tags = Column(Text, nullable=True, comment="标签（JSON数组）")
    attachment = Column(String(255), nullable=True, comment="附件URL")
    
    # 状态信息
    is_overdue = Column(Boolean, nullable=False, default=False, comment="是否逾期")
    reminder_sent = Column(Boolean, nullable=False, default=False, comment="是否已发送提醒")
    
    def __repr__(self):
        return f"<TodoTask(id={self.id}, title={self.title}, status={self.status})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "username": self.username,
            "title": self.title,
            "description": self.description,
            "task_type": self.task_type,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "due_time": self.due_time,
            "tags": self.tags,
            "attachment": self.attachment,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_overdue": self.is_overdue,
            "reminder_sent": self.reminder_sent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def mark_completed(self):
        """标记为已完成"""
        self.status = "completed"
        self.completed_at = datetime.now()
    
    def mark_pending(self):
        """标记为待处理"""
        self.status = "pending"
        self.completed_at = None
    
    def is_completed(self) -> bool:
        """检查是否已完成"""
        return self.status == "completed"
    
    def is_overdue_task(self) -> bool:
        """检查是否逾期"""
        if self.due_date and not self.is_completed():
            return datetime.now() > self.due_date
        return False
    
    def update_overdue_status(self):
        """更新逾期状态"""
        self.is_overdue = self.is_overdue_task()


class DailyPlan(BaseModel):
    """
    每日计划模型
    
    功能：
    - 每日计划管理
    - 每日计划统计
    - 每日计划历史
    
    属性说明：
    - id: 计划ID（主键）
    - tenant_id: 租户ID
    - user_id: 用户ID
    - username: 用户名
    - plan_date: 计划日期
    - tasks: 任务列表（JSON）
    - total_tasks: 总任务数
    - completed_tasks: 已完成任务数
    - completion_rate: 完成率
    - notes: 备注
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "daily_plans"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    
    # 计划信息
    plan_date = Column(DateTime, nullable=False, index=True, comment="计划日期")
    tasks = Column(Text, nullable=True, comment="任务列表（JSON）")
    notes = Column(Text, nullable=True, comment="备注")
    
    # 统计信息
    total_tasks = Column(Integer, nullable=False, default=0, comment="总任务数")
    completed_tasks = Column(Integer, nullable=False, default=0, comment="已完成任务数")
    completion_rate = Column(Integer, nullable=False, default=0, comment="完成率")
    
    def __repr__(self):
        return f"<DailyPlan(id={self.id}, user_id={self.user_id}, plan_date={self.plan_date})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "username": self.username,
            "plan_date": self.plan_date.isoformat() if self.plan_date else None,
            "tasks": self.tasks,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "completion_rate": self.completion_rate,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_statistics(self):
        """更新统计信息"""
        if self.total_tasks == 0:
            self.completion_rate = 0
        else:
            self.completion_rate = int(self.completed_tasks / self.total_tasks * 100)
    
    def add_task(self):
        """添加任务"""
        self.total_tasks += 1
        self.update_statistics()
    
    def complete_task(self):
        """完成任务"""
        self.completed_tasks += 1
        self.update_statistics()
    
    def is_all_completed(self) -> bool:
        """检查是否全部完成"""
        return self.completed_tasks >= self.total_tasks and self.total_tasks > 0