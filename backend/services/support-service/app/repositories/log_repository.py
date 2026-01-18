# -*- coding: utf-8 -*-
"""
日志数据访问层

功能说明：
1. 登录日志CRUD操作
2. 操作日志CRUD操作
3. 日志查询和统计

使用示例：
    from app.repositories.log_repository import LogRepository
    
    log_repo = LogRepository(db)
    logs = log_repo.get_user_login_logs(user_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import Optional, List, Dict, Any
from loguru import logger
from datetime import datetime, timedelta

from common.database.models.system import LoginLog, OperationLog


class LogRepository:
    """
    日志数据访问层
    
    功能：
    - 登录日志CRUD操作
    - 操作日志CRUD操作
    - 日志查询和统计
    
    使用方法：
        log_repo = LogRepository(db)
        logs = log_repo.get_user_login_logs(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        初始化日志数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    # 登录日志相关方法
    def create_login_log(self, login_log: LoginLog) -> LoginLog:
        """
        创建登录日志
        
        Args:
            login_log: 登录日志对象
        
        Returns:
            LoginLog: 创建的登录日志对象
        """
        logger.info(f"创建登录日志: user_id={login_log.user_id}, login_status={login_log.login_status}")
        self.db.add(login_log)
        self.db.commit()
        self.db.refresh(login_log)
        return login_log
    
    def get_login_log_by_id(self, log_id: str) -> Optional[LoginLog]:
        """
        根据ID获取登录日志
        
        Args:
            log_id: 日志ID
        
        Returns:
            Optional[LoginLog]: 登录日志对象，不存在返回None
        """
        return self.db.query(LoginLog).filter(LoginLog.id == log_id).first()
    
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
        offset = (page - 1) * page_size
        return self.db.query(LoginLog).filter(
            LoginLog.user_id == user_id
        ).order_by(LoginLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_login_logs(self, tenant_id: str, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None, page: int = 1, page_size: int = 10) -> List[LoginLog]:
        """
        获取租户登录日志
        
        Args:
            tenant_id: 租户ID
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[LoginLog]: 登录日志列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(LoginLog).filter(LoginLog.tenant_id == tenant_id)
        
        if start_date:
            query = query.filter(LoginLog.created_at >= start_date)
        if end_date:
            query = query.filter(LoginLog.created_at <= end_date)
        
        return query.order_by(LoginLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_failed_login_logs(self, start_date: Optional[datetime] = None, 
                              end_date: Optional[datetime] = None, page: int = 1, page_size: int = 10) -> List[LoginLog]:
        """
        获取失败的登录日志
        
        Args:
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[LoginLog]: 失败的登录日志列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(LoginLog).filter(LoginLog.login_status == "failed")
        
        if start_date:
            query = query.filter(LoginLog.created_at >= start_date)
        if end_date:
            query = query.filter(LoginLog.created_at <= end_date)
        
        return query.order_by(LoginLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def search_login_logs(self, keyword: str, tenant_id: Optional[str] = None,
                          page: int = 1, page_size: int = 10) -> List[LoginLog]:
        """
        搜索登录日志
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[LoginLog]: 登录日志列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(LoginLog).filter(
            or_(
                LoginLog.user_id.like(f"%{keyword}%"),
                LoginLog.ip_address.like(f"%{keyword}%"),
                LoginLog.user_agent.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(LoginLog.tenant_id == tenant_id)
        
        return query.order_by(LoginLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def update_login_log(self, login_log: LoginLog) -> LoginLog:
        """
        更新登录日志
        
        Args:
            login_log: 登录日志对象
        
        Returns:
            LoginLog: 更新后的登录日志对象
        """
        logger.info(f"更新登录日志: log_id={login_log.id}")
        self.db.commit()
        self.db.refresh(login_log)
        return login_log
    
    # 操作日志相关方法
    def create_operation_log(self, operation_log: OperationLog) -> OperationLog:
        """
        创建操作日志
        
        Args:
            operation_log: 操作日志对象
        
        Returns:
            OperationLog: 创建的操作日志对象
        """
        logger.info(f"创建操作日志: user_id={operation_log.user_id}, operation={operation_log.operation}")
        self.db.add(operation_log)
        self.db.commit()
        self.db.refresh(operation_log)
        return operation_log
    
    def get_operation_log_by_id(self, log_id: str) -> Optional[OperationLog]:
        """
        根据ID获取操作日志
        
        Args:
            log_id: 日志ID
        
        Returns:
            Optional[OperationLog]: 操作日志对象，不存在返回None
        """
        return self.db.query(OperationLog).filter(OperationLog.id == log_id).first()
    
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
        offset = (page - 1) * page_size
        return self.db.query(OperationLog).filter(
            OperationLog.user_id == user_id
        ).order_by(OperationLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_operation_logs(self, tenant_id: str, start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None, page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        获取租户操作日志
        
        Args:
            tenant_id: 租户ID
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[OperationLog]: 操作日志列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(OperationLog).filter(OperationLog.tenant_id == tenant_id)
        
        if start_date:
            query = query.filter(OperationLog.created_at >= start_date)
        if end_date:
            query = query.filter(OperationLog.created_at <= end_date)
        
        return query.order_by(OperationLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def search_operation_logs(self, keyword: str, tenant_id: Optional[str] = None,
                              page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        搜索操作日志
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[OperationLog]: 操作日志列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(OperationLog).filter(
            or_(
                OperationLog.user_id.like(f"%{keyword}%"),
                OperationLog.module.like(f"%{keyword}%"),
                OperationLog.operation.like(f"%{keyword}%"),
                OperationLog.path.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(OperationLog.tenant_id == tenant_id)
        
        return query.order_by(OperationLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_slow_queries(self, threshold: int = 1000, page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        获取慢查询日志
        
        Args:
            threshold: 阈值（毫秒）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[OperationLog]: 慢查询日志列表
        """
        offset = (page - 1) * page_size
        return self.db.query(OperationLog).filter(
            OperationLog.response_time > threshold
        ).order_by(OperationLog.response_time.desc()).offset(offset).limit(page_size).all()
    
    # 统计方法
    def count_login_logs_by_date(self, date: datetime) -> int:
        """
        统计指定日期的登录日志数量
        
        Args:
            date: 日期
        
        Returns:
            int: 登录日志数量
        """
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return self.db.query(LoginLog).filter(
            and_(
                LoginLog.created_at >= start_date,
                LoginLog.created_at < end_date
            )
        ).count()
    
    def count_failed_logins_by_user(self, user_id: str, hours: int = 24) -> int:
        """
        统计用户在指定小时内的失败登录次数
        
        Args:
            user_id: 用户ID
            hours: 小时数
        
        Returns:
            int: 失败登录次数
        """
        start_time = datetime.now() - timedelta(hours=hours)
        return self.db.query(LoginLog).filter(
            and_(
                LoginLog.user_id == user_id,
                LoginLog.login_status == "failed",
                LoginLog.created_at >= start_time
            )
        ).count()
    
    def count_operation_logs_by_date(self, date: datetime) -> int:
        """
        统计指定日期的操作日志数量
        
        Args:
            date: 日期
        
        Returns:
            int: 操作日志数量
        """
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return self.db.query(OperationLog).filter(
            and_(
                OperationLog.created_at >= start_date,
                OperationLog.created_at < end_date
            )
        ).count()
    
    def get_login_statistics(self, tenant_id: str, days: int = 7) -> Dict[str, Any]:
        """
        获取登录统计信息
        
        Args:
            tenant_id: 租户ID
            days: 天数
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # 总登录次数
        total_logins = self.db.query(LoginLog).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.created_at >= start_date
            )
        ).count()
        
        # 成功登录次数
        success_logins = self.db.query(LoginLog).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.login_status == "success",
                LoginLog.created_at >= start_date
            )
        ).count()
        
        # 失败登录次数
        failed_logins = self.db.query(LoginLog).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.login_status == "failed",
                LoginLog.created_at >= start_date
            )
        ).count()
        
        # 每日登录统计
        daily_stats = self.db.query(
            func.date(LoginLog.created_at).label('date'),
            func.count(LoginLog.id).label('count')
        ).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.created_at >= start_date
            )
        ).group_by(func.date(LoginLog.created_at)).all()
        
        return {
            "total_logins": total_logins,
            "success_logins": success_logins,
            "failed_logins": failed_logins,
            "success_rate": round(success_logins / total_logins * 100, 2) if total_logins > 0 else 0,
            "daily_stats": [{"date": str(stat.date), "count": stat.count} for stat in daily_stats]
        }