# -*- coding: utf-8 -*-
"""
日志服务

功能说明：
1. 登录日志管理
2. 操作日志管理
3. 日志查询和统计

使用示例：
    from app.services.log_service import LogService
    
    log_service = LogService(db)
    log = log_service.create_login_log(user_id="123", username="admin")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.log import LoginLog, OperationLog
from app.repositories.log_repository import LogRepository


class LogService:
    """
    日志服务
    
    功能：
    - 登录日志管理
    - 操作日志管理
    - 日志查询和统计
    
    使用方法：
        log_service = LogService(db)
        log = log_service.create_login_log(user_id="123", username="admin")
    """
    
    def __init__(self, db: Session):
        """
        初始化日志服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.log_repo = LogRepository(db)
    
    def create_login_log(self, user_id: str, username: str, tenant_id: str,
                         ip: Optional[str] = None, user_agent: Optional[str] = None,
                         status: str = "success", failure_reason: Optional[str] = None,
                         device_type: Optional[str] = None, device_info: Optional[str] = None,
                         location: Optional[str] = None) -> LoginLog:
        """
        创建登录日志
        
        Args:
            user_id: 用户ID
            username: 用户名
            tenant_id: 租户ID
            ip: IP地址（可选）
            user_agent: 用户代理（可选）
            status: 状态
            failure_reason: 失败原因（可选）
            device_type: 设备类型（可选）
            device_info: 设备信息（可选）
            location: 地理位置（可选）
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        login_log = LoginLog(
            tenant_id=tenant_id,
            user_id=user_id,
            username=username,
            ip=ip,
            user_agent=user_agent,
            status=status,
            failure_reason=failure_reason,
            device_type=device_type,
            device_info=device_info,
            location=location,
            login_time=datetime.now()
        )
        return self.log_repo.create_login_log(login_log)
    
    def record_login_success(self, user_id: str, username: str, tenant_id: str,
                             ip: Optional[str] = None, user_agent: Optional[str] = None,
                             device_type: Optional[str] = None) -> LoginLog:
        """
        记录成功登录
        
        Args:
            user_id: 用户ID
            username: 用户名
            tenant_id: 租户ID
            ip: IP地址（可选）
            user_agent: 用户代理（可选）
            device_type: 设备类型（可选）
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        return self.create_login_log(
            user_id=user_id,
            username=username,
            tenant_id=tenant_id,
            ip=ip,
            user_agent=user_agent,
            status="success",
            device_type=device_type
        )
    
    def record_login_failure(self, user_id: str, username: str, tenant_id: str,
                             ip: Optional[str] = None, failure_reason: Optional[str] = None) -> LoginLog:
        """
        记录失败登录
        
        Args:
            user_id: 用户ID
            username: 用户名
            tenant_id: 租户ID
            ip: IP地址（可选）
            failure_reason: 失败原因（可选）
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        return self.create_login_log(
            user_id=user_id,
            username=username,
            tenant_id=tenant_id,
            ip=ip,
            status="failed",
            failure_reason=failure_reason
        )
    
    def record_logout(self, user_id: str) -> bool:
        """
        记录登出
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否成功
        """
        logger.info(f"记录登出: user_id={user_id}")
        
        # 获取最新的成功登录日志
        login_log = self.db.query(LoginLog).filter(
            and_(
                LoginLog.user_id == user_id,
                LoginLog.status == "success",
                LoginLog.logout_time.is_(None)
            )
        ).order_by(LoginLog.login_time.desc()).first()
        
        if login_log:
            login_log.logout_time = datetime.now()
            self.log_repo.update_login_log(login_log)
            return True
        
        return False
    
    def create_operation_log(self, user_id: str, username: str, tenant_id: str,
                              module: str, action: str, description: Optional[str] = None,
                              method: str = "POST", url: Optional[str] = None,
                              params: Optional[str] = None, result: Optional[str] = None,
                              status: str = "success", error_message: Optional[str] = None,
                              ip: Optional[str] = None, user_agent: Optional[str] = None,
                              execution_time: Optional[int] = None) -> OperationLog:
        """
        创建操作日志
        
        Args:
            user_id: 用户ID
            username: 用户名
            tenant_id: 租户ID
            module: 模块名称
            action: 操作动作
            description: 操作描述（可选）
            method: 请求方法
            url: 请求URL（可选）
            params: 请求参数（可选）
            result: 操作结果（可选）
            status: 状态
            error_message: 错误信息（可选）
            ip: IP地址（可选）
            user_agent: 用户代理（可选）
            execution_time: 执行时间（可选）
        
        Returns:
            OperationLog: 创建的操作日志对象
        """
        operation_log = OperationLog(
            tenant_id=tenant_id,
            user_id=user_id,
            username=username,
            module=module,
            action=action,
            description=description,
            method=method,
            url=url,
            params=params,
            result=result,
            status=status,
            error_message=error_message,
            ip=ip,
            user_agent=user_agent,
            execution_time=execution_time
        )
        return self.log_repo.create_operation_log(operation_log)
    
    def get_user_login_logs(self, user_id: str, page: int = 1, page_size: int = 10) -> List[LoginLog]:
        """
        获取用户登录日志
        
        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[LoginLog]: 登录日志列表
        """
        return self.log_repo.get_user_login_logs(user_id, page, page_size)
    
    def get_user_operation_logs(self, user_id: str, page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        获取用户操作日志
        
        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[OperationLog]: 操作日志列表
        """
        return self.log_repo.get_user_operation_logs(user_id, page, page_size)
    
    def check_failed_logins(self, user_id: str, threshold: int = 5, hours: int = 24) -> bool:
        """
        检查用户失败登录次数是否超过阈值
        
        Args:
            user_id: 用户ID
            threshold: 阈值
            hours: 小时数
        
        Returns:
            bool: 是否超过阈值
        """
        failed_count = self.log_repo.count_failed_logins_by_user(user_id, hours)
        return failed_count >= threshold
    
    def get_login_statistics(self, tenant_id: str, days: int = 7) -> Dict[str, Any]:
        """
        获取登录统计信息
        
        Args:
            tenant_id: 租户ID
            days: 天数
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        return self.log_repo.get_login_statistics(tenant_id, days)