# -*- coding: utf-8 -*-
"""
工作流模型

功能说明：
1. 工作流实例管理
2. 工作流状态管理
3. 工作流历史记录

使用示例：
    from app.models.workflow import Workflow
    
    workflow = Workflow(
        name="请假审批",
        template_id="template_123",
        initiator_id="user_123"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional

from common.database.base import BaseModel


class Workflow(BaseModel):
    """
    工作流模型
    
    功能：
    - 工作流实例管理
    - 工作流状态管理
    - 工作流历史记录
    
    属性说明：
    - id: 工作流ID（主键）
    - tenant_id: 租户ID
    - name: 工作流名称
    - template_id: 模板ID（外键）
    - initiator_id: 发起人ID
    - initiator_name: 发起人名称
    - status: 状态
    - current_node_id: 当前节点ID
    - current_node_name: 当前节点名称
    - business_data: 业务数据（JSON）
    - variables: 变量（JSON）
    - started_at: 开始时间
    - finished_at: 结束时间
    - duration: 持续时间（秒）
    - created_at: 创建时间
    """
    
    __tablename__ = "workflows"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="工作流名称")
    template_id = Column(String(64), ForeignKey("workflow_templates.id"), nullable=True, comment="模板ID")
    
    # 发起人信息
    initiator_id = Column(String(64), nullable=False, index=True, comment="发起人ID")
    initiator_name = Column(String(50), nullable=False, comment="发起人名称")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="running", comment="状态")
    current_node_id = Column(String(64), nullable=True, comment="当前节点ID")
    current_node_name = Column(String(100), nullable=True, comment="当前节点名称")
    
    # 数据信息
    business_data = Column(Text, nullable=True, comment="业务数据（JSON）")
    variables = Column(Text, nullable=True, comment="变量（JSON）")
    
    # 时间信息
    started_at = Column(DateTime, nullable=False, default=datetime.now, comment="开始时间")
    finished_at = Column(DateTime, nullable=True, comment="结束时间")
    duration = Column(Integer, nullable=True, comment="持续时间（秒）")
    
    # 关系
    tasks = relationship("WorkflowTask", back_populates="workflow", cascade="all, delete-orphan")
    template = relationship("WorkflowTemplate", back_populates="workflows")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name={self.name}, status={self.status})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "template_id": self.template_id,
            "initiator_id": self.initiator_id,
            "initiator_name": self.initiator_name,
            "status": self.status,
            "current_node_id": self.current_node_id,
            "current_node_name": self.current_node_name,
            "business_data": self.business_data,
            "variables": self.variables,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration": self.duration,
            "task_count": len(self.tasks) if self.tasks else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def start(self):
        """启动工作流"""
        self.status = "running"
        self.started_at = datetime.now()
    
    def finish(self):
        """结束工作流"""
        self.status = "completed"
        self.finished_at = datetime.now()
        if self.started_at:
            self.duration = int((self.finished_at - self.started_at).total_seconds())
    
    def terminate(self):
        """终止工作流"""
        self.status = "terminated"
        self.finished_at = datetime.now()
        if self.started_at:
            self.duration = int((self.finished_at - self.started_at).total_seconds())
    
    def is_running(self) -> bool:
        """检查是否运行中"""
        return self.status == "running"
    
    def is_completed(self) -> bool:
        """检查是否已完成"""
        return self.status == "completed"
    
    def is_terminated(self) -> bool:
        """检查是否已终止"""
        return self.status == "terminated"