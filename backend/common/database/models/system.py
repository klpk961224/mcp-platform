"""
绯荤粺鐩稿叧妯″瀷

鍖呭惈锛?- MCPTool: MCP宸ュ叿琛?- LoginLog: 鐧诲綍鏃ュ織琛?- OperationLog: 鎿嶄綔鏃ュ織琛?- Dict: 瀛楀吀琛?- DictItem: 瀛楀吀椤硅〃
- SystemNotification: 绯荤粺閫氱煡琛?"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel, FullModelMixin, CreatedAtMixin, TimestampMixin


class MCPTool(BaseModel, FullModelMixin):
    """MCP宸ュ叿琛?""

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


class LoginLog(BaseModel, CreatedAtMixin):
    """鐧诲綍鏃ュ織琛?""

    __tablename__ = 'login_logs'

    user_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'))
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    login_status = Column(String(20), nullable=False)
    error_message = Column(Text)


class OperationLog(BaseModel, CreatedAtMixin):
    """鎿嶄綔鏃ュ織琛?""

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


class Dict(BaseModel, TimestampMixin):
    """瀛楀吀琛?""

    __tablename__ = 'dicts'

    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False, default='active')


class DictItem(BaseModel, TimestampMixin):
    """瀛楀吀椤硅〃"""

    __tablename__ = 'dict_items'

    dict_id = Column(String(50), ForeignKey('dicts.id', ondelete='CASCADE'), nullable=False)
    label = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default='active')


class SystemNotification(BaseModel, TimestampMixin):
    """绯荤粺閫氱煡琛?""

    __tablename__ = 'notifications'

    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    sender_id = Column(String(50))
    receiver_ids = Column(JSON)
    status = Column(String(20), nullable=False, default='unread')


class ErrorCode(BaseModel, TimestampMixin):
    """閿欒鐮佽〃"""

    __tablename__ = 'error_codes'

    code = Column(String(50), unique=True, nullable=False, comment='閿欒鐮?)
    message = Column(String(500), nullable=False, comment='閿欒淇℃伅')
    level = Column(String(20), nullable=False, default='error', comment='閿欒绾у埆')
    module = Column(String(50), nullable=False, comment='妯″潡')
    description = Column(Text, comment='鎻忚堪')
    status = Column(String(20), nullable=False, default='active', comment='鐘舵€?)
