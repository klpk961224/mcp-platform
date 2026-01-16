"""
系统相关模型

包含：
- MCPTool: MCP工具表
- LoginLog: 登录日志表
- OperationLog: 操作日志表
- Dict: 字典表
- DictItem: 字典项表
- Notification: 通知表
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class MCPTool(BaseModel):
    """MCP工具表"""
    
    __tablename__ = 'mcp_tools'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    api_path = Column(String(255), nullable=False)
    api_method = Column(String(10), nullable=False)
    tool_type = Column(String(50), nullable=False)
    auth_type = Column(String(50), nullable=False)
    timeout = Column(Integer, nullable=False, default=30)
    max_retries = Column(Integer, nullable=False, default=3)
    status = Column(String(20), nullable=False, default='active')
    call_count = Column(Integer, nullable=False, default=0)
    success_count = Column(Integer, nullable=False, default=0)
    failure_count = Column(Integer, nullable=False, default=0)
    avg_response_time = Column(Integer)
    
    tenant = relationship('Tenant', back_populates='mcp_tools')


class LoginLog(BaseModel):
    """登录日志表"""
    
    __tablename__ = 'login_logs'
    
    user_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    login_status = Column(String(20), nullable=False)
    error_message = Column(Text)


class OperationLog(BaseModel):
    """操作日志表"""
    
    __tablename__ = 'operation_logs'
    
    user_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    module = Column(String(50), nullable=False)
    operation = Column(String(50), nullable=False)
    method = Column(String(10), nullable=False)
    path = Column(String(255), nullable=False)
    request_params = Column(JSON)
    response_data = Column(JSON)
    response_status = Column(Integer)
    response_time = Column(Integer)


class Dict(BaseModel):
    """字典表"""
    
    __tablename__ = 'dicts'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False, default='active')


class DictItem(BaseModel):
    """字典项表"""
    
    __tablename__ = 'dict_items'
    
    dict_id = Column(String(50), ForeignKey('dicts.id', ondelete='CASCADE'), nullable=False)
    label = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default='active')


class Notification(BaseModel):
    """通知表"""

    __tablename__ = 'notifications'

    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    sender_id = Column(String(50))
    receiver_ids = Column(JSON)
    status = Column(String(20), nullable=False, default='unread')


class ErrorCode(BaseModel):
    """错误码表"""

    __tablename__ = 'error_codes'

    code = Column(String(50), unique=True, nullable=False, comment='错误码')
    message = Column(String(500), nullable=False, comment='错误信息')
    level = Column(String(20), nullable=False, default='error', comment='错误级别')
    module = Column(String(50), nullable=False, comment='模块')
    description = Column(Text, comment='描述')
    status = Column(String(20), nullable=False, default='active', comment='状态')