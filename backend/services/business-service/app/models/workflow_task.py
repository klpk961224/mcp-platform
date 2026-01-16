# -*- coding: utf-8 -*-
"""
工作流任务模型

功能说明：
1. 工作流任务管理
2. 审批任务处理
3. 任务评论管理

使用示例：
    from app.models.workflow_task import WorkflowTask
    
    task = WorkflowTask(
        workflow_id="workflow_123",
        node_id="node_123",
        node_name="经理审批",
        assignee_id="user_123"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class WorkflowTask(BaseModel):
    """
    工作流任务模型
    
    功能：
    - 工作流任务管理
    - 审批任务处理
    - 任务评论管理
    
    属性说明：
    - id: 任务ID（主键）
    - workflow_id: 工作流ID（外键）
    - node_id: 节点ID
    - node_name: 节点名称
    - node_type: 节点类型
    - assignee_id: 受理人ID
    - assignee_name: 受理人名称
    - status: 状态
    - result: 审批结果
    - comment: 审批意见
    - business_data: 业务数据（JSON）
    - started_at: 开始时间
    - finished_at: 结束时间
    - duration: 处理时长（秒）
    - created_at: 创建时间
    """
    
    __tablename__ = "workflow_tasks"
    
    # 基本信息
    workflow_id = Column(String(64), ForeignKey("workflows.id"), nullable=False, index=True, comment="工作流ID")
    node_id = Column(String(64), nullable=False, comment="节点ID")
    node_name = Column(String(100), nullable=False, comment="节点名称")
    node_type = Column(String(20), nullable=False, comment="节点类型")
    
    # 受理人信息
    assignee_id = Column(String(64), nullable=False, index=True, comment="受理人ID")
    assignee_name = Column(String(50), nullable=False, comment="受理人名称")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="pending", comment="状态")
    result = Column(String(20), nullable=True, comment="审批结果")
    comment = Column(Text, nullable=True, comment="审批意见")
    
    # 数据信息
    business_data = Column(Text, nullable=True, comment="业务数据（JSON）")
    
    # 时间信息
    started_at = Column(DateTime, nullable=False, default=datetime.now, comment="开始时间")
    finished_at = Column(DateTime, nullable=True, comment="结束时间")
    duration = Column(Integer, nullable=True, comment="处理时长（秒）")
    
    # 关系
    workflow = relationship("Workflow", back_populates="tasks")
    
    def __repr__(self):
        return f"<WorkflowTask(id={self.id}, node_name={self.node_name}, status={self.status})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "node_id": self.node_id,
            "node_name": self.node_name,
            "node_type": self.node_type,
            "assignee_id": self.assignee_id,
            "assignee_name": self.assignee_name,
            "status": self.status,
            "result": self.result,
            "comment": self.comment,
            "business_data": self.business_data,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration": self.duration,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def approve(self, comment: Optional[str] = None):
        """通过审批"""
        self.status = "approved"
        self.result = "approved"
        self.comment = comment
        self.finished_at = datetime.now()
        if self.started_at:
            self.duration = int((self.finished_at - self.started_at).total_seconds())
    
    def reject(self, comment: Optional[str] = None):
        """拒绝审批"""
        self.status = "rejected"
        self.result = "rejected"
        self.comment = comment
        self.finished_at = datetime.now()
        if self.started_at:
            self.duration = int((self.finished_at - self.started_at).total_seconds())
    
    def transfer(self, new_assignee_id: str, new_assignee_name: str):
        """转交任务"""
        self.assignee_id = new_assignee_id
        self.assignee_name = new_assignee_name
        self.status = "transferred"
    
    def is_pending(self) -> bool:
        """检查是否待处理"""
        return self.status == "pending"
    
    def is_approved(self) -> bool:
        """检查是否已通过"""
        return self.status == "approved"
    
    def is_rejected(self) -> bool:
        """检查是否已拒绝"""
        return self.status == "rejected"
    
    def is_finished(self) -> bool:
        """检查是否已完成"""
        return self.status in ["approved", "rejected", "transferred"]