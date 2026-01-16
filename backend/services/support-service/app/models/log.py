# -*- coding: utf-8 -*-
"""
日志模型

功能说明：
1. 登录日志记录
2. 操作日志记录
3. 日志查询和统计

使用示例：
    from app.models.log import LoginLog, OperationLog
    
    # 创建登录日志
    login_log = LoginLog(
        user_id="123",
        username="admin",
        ip="192.168.1.1",
        user_agent="Mozilla/5.0..."
    )
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from datetime import datetime

from common.database.base import BaseModel


class LoginLog(BaseModel):
    """
    登录日志模型
    
    功能：
    - 登录日志记录
    - 登录失败记录
    - 登录统计
    
    属性说明：
    - id: 日志ID（主键）
    - tenant_id: 租户ID
    - user_id: 用户ID
    - username: 用户名
    - ip: IP地址
    - user_agent: 用户代理
    - login_time: 登录时间
    - logout_time: 登出时间
    - status: 状态（success/failed）
    - failure_reason: 失败原因
    - device_type: 设备类型
    - device_info: 设备信息（JSON）
    - location: 地理位置
    - created_at: 创建时间
    """
    
    __tablename__ = "login_logs"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    
    # 连接信息
    ip = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 时间信息
    login_time = Column(DateTime, nullable=False, default=datetime.now, comment="登录时间")
    logout_time = Column(DateTime, nullable=True, comment="登出时间")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="success", comment="状态")
    failure_reason = Column(String(255), nullable=True, comment="失败原因")
    
    # 设备信息
    device_type = Column(String(20), nullable=True, comment="设备类型")
    device_info = Column(Text, nullable=True, comment="设备信息（JSON）")
    location = Column(String(255), nullable=True, comment="地理位置")
    
    def __repr__(self):
        return f"<LoginLog(id={self.id}, username={self.username}, status={self.status})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "username": self.username,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "login_time": self.login_time.isoformat() if self.login_time else None,
            "logout_time": self.logout_time.isoformat() if self.logout_time else None,
            "status": self.status,
            "failure_reason": self.failure_reason,
            "device_type": self.device_type,
            "device_info": self.device_info,
            "location": self.location,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def is_success(self) -> bool:
        """检查是否登录成功"""
        return self.status == "success"
    
    def get_session_duration(self) -> int:
        """获取会话时长（秒）"""
        if self.logout_time and self.login_time:
            return int((self.logout_time - self.login_time).total_seconds())
        return 0


class OperationLog(BaseModel):
    """
    操作日志模型
    
    功能：
    - 操作日志记录
    - 操作审计
    - 操作统计
    
    属性说明：
    - id: 日志ID（主键）
    - tenant_id: 租户ID
    - user_id: 用户ID
    - username: 用户名
    - module: 模块名称
    - action: 操作动作
    - description: 操作描述
    - method: 请求方法
    - url: 请求URL
    - params: 请求参数
    - result: 操作结果
    - status: 状态（success/failed）
    - error_message: 错误信息
    - ip: IP地址
    - user_agent: 用户代理
    - execution_time: 执行时间（毫秒）
    - created_at: 创建时间
    """
    
    __tablename__ = "operation_logs"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    
    # 操作信息
    module = Column(String(50), nullable=False, comment="模块名称")
    action = Column(String(50), nullable=False, comment="操作动作")
    description = Column(String(255), nullable=True, comment="操作描述")
    
    # 请求信息
    method = Column(String(10), nullable=False, comment="请求方法")
    url = Column(String(255), nullable=False, comment="请求URL")
    params = Column(Text, nullable=True, comment="请求参数")
    
    # 结果信息
    result = Column(Text, nullable=True, comment="操作结果")
    status = Column(String(20), nullable=False, default="success", comment="状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    
    # 连接信息
    ip = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 性能信息
    execution_time = Column(Integer, nullable=True, comment="执行时间（毫秒）")
    
    def __repr__(self):
        return f"<OperationLog(id={self.id}, username={self.username}, action={self.action}, status={self.status})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "username": self.username,
            "module": self.module,
            "action": self.action,
            "description": self.description,
            "method": self.method,
            "url": self.url,
            "params": self.params,
            "result": self.result,
            "status": self.status,
            "error_message": self.error_message,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "execution_time": self.execution_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def is_success(self) -> bool:
        """检查操作是否成功"""
        return self.status == "success"
    
    def is_slow_query(self, threshold: int = 1000) -> bool:
        """检查是否为慢查询"""
        return self.execution_time and self.execution_time > threshold