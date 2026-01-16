# -*- coding: utf-8 -*-
"""
MCP工具模型

功能说明：
1. MCP工具注册
2. MCP工具配置
3. MCP工具调用日志

使用示例：
    from app.models.mcp_tool import MCPTool
    
    tool = MCPTool(
        name="数据分析",
        code="data_analysis",
        api_endpoint="http://localhost:8000/api/analyze"
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from common.database.base import BaseModel


class MCPTool(BaseModel):
    """
    MCP工具模型
    
    功能：
    - MCP工具注册
    - MCP工具配置
    - MCP工具调用日志
    
    属性说明：
    - id: 工具ID（主键）
    - tenant_id: 租户ID
    - name: 工具名称
    - code: 工具编码（唯一）
    - description: 工具描述
    - api_endpoint: API端点
    - api_method: API方法（GET/POST/PUT/DELETE）
    - api_timeout: API超时时间（秒）
    - api_retry_count: API重试次数
    - status: 状态（active/inactive）
    - is_public: 是否公开（所有租户可用）
    - required_permissions: 所需权限（JSON数组）
    - rate_limit: 速率限制（次/分钟）
    - call_count: 调用次数
    - success_count: 成功次数
    - fail_count: 失败次数
    - last_called_at: 最后调用时间
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "mcp_tools"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="工具名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="工具编码")
    description = Column(Text, nullable=True, comment="工具描述")
    
    # API配置
    api_endpoint = Column(String(255), nullable=False, comment="API端点")
    api_method = Column(String(10), nullable=False, default="POST", comment="API方法")
    api_timeout = Column(Integer, nullable=False, default=30, comment="API超时时间（秒）")
    api_retry_count = Column(Integer, nullable=False, default=3, comment="API重试次数")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="active", comment="状态")
    is_public = Column(Boolean, nullable=False, default=False, comment="是否公开")
    
    # 权限配置
    required_permissions = Column(Text, nullable=True, comment="所需权限（JSON数组）")
    
    # 限流配置
    rate_limit = Column(Integer, nullable=False, default=60, comment="速率限制（次/分钟）")
    
    # 统计信息
    call_count = Column(Integer, nullable=False, default=0, comment="调用次数")
    success_count = Column(Integer, nullable=False, default=0, comment="成功次数")
    fail_count = Column(Integer, nullable=False, default=0, comment="失败次数")
    last_called_at = Column(DateTime, nullable=True, comment="最后调用时间")
    
    # 扩展信息
    config = Column(Text, nullable=True, comment="工具配置（JSON）")
    
    def __repr__(self):
        return f"<MCPTool(id={self.id}, name={self.name}, code={self.code})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "api_endpoint": self.api_endpoint,
            "api_method": self.api_method,
            "api_timeout": self.api_timeout,
            "api_retry_count": self.api_retry_count,
            "status": self.status,
            "is_public": self.is_public,
            "required_permissions": self.required_permissions,
            "rate_limit": self.rate_limit,
            "call_count": self.call_count,
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "success_rate": self.get_success_rate(),
            "last_called_at": self.last_called_at.isoformat() if self.last_called_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.call_count == 0:
            return 0.0
        return round(self.success_count / self.call_count * 100, 2)
    
    def increment_call_count(self, success: bool = True):
        """增加调用次数"""
        self.call_count += 1
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
        self.last_called_at = datetime.now()
    
    def is_available(self) -> bool:
        """检查工具是否可用"""
        return self.status == "active"