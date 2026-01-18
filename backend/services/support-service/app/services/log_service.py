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
from sqlalchemy import and_
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from common.database.models.system import LoginLog, OperationLog
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
    
    def create_login_log(self, user_id: str, tenant_id: str,
                         ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                         login_status: str = "success", error_message: Optional[str] = None) -> LoginLog:
        """
        创建登录日志
        
        Args:
            user_id: 用户ID
            tenant_id: 租户ID
            ip_address: IP地址（可选）
            user_agent: 用户代理（可选）
            login_status: 登录状态
            error_message: 错误信息（可选）
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        login_log = LoginLog(
            tenant_id=tenant_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            login_status=login_status,
            error_message=error_message
        )
        return self.log_repo.create_login_log(login_log)
    
    def record_login_success(self, user_id: str, tenant_id: str,
                             ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> LoginLog:
        """
        记录成功登录
        
        Args:
            user_id: 用户ID
            tenant_id: 租户ID
            ip_address: IP地址（可选）
            user_agent: 用户代理（可选）
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        return self.create_login_log(
            user_id=user_id,
            tenant_id=tenant_id,
            ip_address=ip_address,
            user_agent=user_agent,
            login_status="success"
        )
    
    def record_login_failure(self, user_id: str, tenant_id: str,
                             ip_address: Optional[str] = None, error_message: Optional[str] = None) -> LoginLog:
        """
        记录失败登录
        
        Args:
            user_id: 用户ID
            tenant_id: 租户ID
            ip_address: IP地址（可选）
            error_message: 错误信息（可选）
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        return self.create_login_log(
            user_id=user_id,
            tenant_id=tenant_id,
            ip_address=ip_address,
            login_status="failed",
            error_message=error_message
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
        
        # 注意：当前表结构不支持logout_time字段，此方法暂时不实现
        # 如果需要记录登出，需要修改表结构添加logout_time字段
        return False
    
    def create_operation_log(self, user_id: str, tenant_id: str,
                              module: str, operation: str,
                              method: str = "POST", path: Optional[str] = None,
                              request_params: Optional[str] = None, response_data: Optional[str] = None,
                              response_status: Optional[int] = None,
                              response_time: Optional[int] = None) -> OperationLog:
        """
        创建操作日志
        
        Args:
            user_id: 用户ID
            tenant_id: 租户ID
            module: 模块名称
            operation: 操作动作
            method: 请求方法
            path: 请求路径（可选）
            request_params: 请求参数（可选）
            response_data: 响应数据（可选）
            response_status: 响应状态（可选）
            response_time: 响应时间（可选）
        
        Returns:
            OperationLog: 创建的操作日志对象
        """
        operation_log = OperationLog(
            tenant_id=tenant_id,
            user_id=user_id,
            module=module,
            operation=operation,
            method=method,
            path=path,
            request_params=request_params,
            response_data=response_data,
            response_status=response_status,
            response_time=response_time
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