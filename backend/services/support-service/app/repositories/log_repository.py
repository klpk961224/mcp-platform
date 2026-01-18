# -*- coding: utf-8 -*-
"""
鏃ュ織鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 鐧诲綍鏃ュ織CRUD鎿嶄綔
2. 鎿嶄綔鏃ュ織CRUD鎿嶄綔
3. 鏃ュ織查询鍜岀粺璁?
浣跨敤绀轰緥锛?    from app.repositories.log_repository import LogRepository
    
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
    鏃ュ織鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鐧诲綍鏃ュ織CRUD鎿嶄綔
    - 鎿嶄綔鏃ュ織CRUD鎿嶄綔
    - 鏃ュ織查询鍜岀粺璁?    
    浣跨敤鏂规硶锛?        log_repo = LogRepository(db)
        logs = log_repo.get_user_login_logs(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨棩蹇楁暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    # 鐧诲綍鏃ュ織鐩稿叧鏂规硶
    def create_login_log(self, login_log: LoginLog) -> LoginLog:
        """
        创建鐧诲綍鏃ュ織
        
        Args:
            login_log: 鐧诲綍鏃ュ織瀵硅薄
        
        Returns:
            LoginLog: 创建鐨勭櫥褰曟棩蹇楀璞?        """
        logger.info(f"创建鐧诲綍鏃ュ織: user_id={login_log.user_id}, login_status={login_log.login_status}")
        self.db.add(login_log)
        self.db.commit()
        self.db.refresh(login_log)
        return login_log
    
    def get_login_log_by_id(self, log_id: str) -> Optional[LoginLog]:
        """
        根据ID鑾峰彇鐧诲綍鏃ュ織
        
        Args:
            log_id: 鏃ュ織ID
        
        Returns:
            Optional[LoginLog]: 鐧诲綍鏃ュ織瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(LoginLog).filter(LoginLog.id == log_id).first()
    
    def get_user_login_logs(self, user_id: str, page: int = 1, page_size: int = 10) -> List[LoginLog]:
        """
        鑾峰彇鐢ㄦ埛鐧诲綍鏃ュ織
        
        Args:
            user_id: 用户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[LoginLog]: 鐧诲綍鏃ュ織鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(LoginLog).filter(
            LoginLog.user_id == user_id
        ).order_by(LoginLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_login_logs(self, tenant_id: str, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None, page: int = 1, page_size: int = 10) -> List[LoginLog]:
        """
        鑾峰彇绉熸埛鐧诲綍鏃ュ織
        
        Args:
            tenant_id: 租户ID
            start_date: 寮€濮嬫棩鏈燂紙鍙€夛級
            end_date: 缁撴潫鏃ユ湡锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[LoginLog]: 鐧诲綍鏃ュ織鍒楄〃
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
        鑾峰彇澶辫触鐨勭櫥褰曟棩蹇?        
        Args:
            start_date: 寮€濮嬫棩鏈燂紙鍙€夛級
            end_date: 缁撴潫鏃ユ湡锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[LoginLog]: 澶辫触鐨勭櫥褰曟棩蹇楀垪琛?        """
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
        鎼滅储鐧诲綍鏃ュ織
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[LoginLog]: 鐧诲綍鏃ュ織鍒楄〃
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
        更新鐧诲綍鏃ュ織
        
        Args:
            login_log: 鐧诲綍鏃ュ織瀵硅薄
        
        Returns:
            LoginLog: 更新鍚庣殑鐧诲綍鏃ュ織瀵硅薄
        """
        logger.info(f"更新鐧诲綍鏃ュ織: log_id={login_log.id}")
        self.db.commit()
        self.db.refresh(login_log)
        return login_log
    
    # 鎿嶄綔鏃ュ織鐩稿叧鏂规硶
    def create_operation_log(self, operation_log: OperationLog) -> OperationLog:
        """
        创建鎿嶄綔鏃ュ織
        
        Args:
            operation_log: 鎿嶄綔鏃ュ織瀵硅薄
        
        Returns:
            OperationLog: 创建鐨勬搷浣滄棩蹇楀璞?        """
        logger.info(f"创建鎿嶄綔鏃ュ織: user_id={operation_log.user_id}, operation={operation_log.operation}")
        self.db.add(operation_log)
        self.db.commit()
        self.db.refresh(operation_log)
        return operation_log
    
    def get_operation_log_by_id(self, log_id: str) -> Optional[OperationLog]:
        """
        根据ID鑾峰彇鎿嶄綔鏃ュ織
        
        Args:
            log_id: 鏃ュ織ID
        
        Returns:
            Optional[OperationLog]: 鎿嶄綔鏃ュ織瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(OperationLog).filter(OperationLog.id == log_id).first()
    
    def get_user_operation_logs(self, user_id: str, page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        鑾峰彇鐢ㄦ埛鎿嶄綔鏃ュ織
        
        Args:
            user_id: 用户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[OperationLog]: 鎿嶄綔鏃ュ織鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(OperationLog).filter(
            OperationLog.user_id == user_id
        ).order_by(OperationLog.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_operation_logs(self, tenant_id: str, start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None, page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        鑾峰彇绉熸埛鎿嶄綔鏃ュ織
        
        Args:
            tenant_id: 租户ID
            start_date: 寮€濮嬫棩鏈燂紙鍙€夛級
            end_date: 缁撴潫鏃ユ湡锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[OperationLog]: 鎿嶄綔鏃ュ織鍒楄〃
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
        鎼滅储鎿嶄綔鏃ュ織
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[OperationLog]: 鎿嶄綔鏃ュ織鍒楄〃
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
        鑾峰彇鎱㈡煡璇㈡棩蹇?        
        Args:
            threshold: 闃堝€硷紙姣锛?            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[OperationLog]: 鎱㈡煡璇㈡棩蹇楀垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(OperationLog).filter(
            OperationLog.response_time > threshold
        ).order_by(OperationLog.response_time.desc()).offset(offset).limit(page_size).all()
    
    # 缁熻鏂规硶
    def count_login_logs_by_date(self, date: datetime) -> int:
        """
        缁熻鎸囧畾鏃ユ湡鐨勭櫥褰曟棩蹇楁暟閲?        
        Args:
            date: 鏃ユ湡
        
        Returns:
            int: 鐧诲綍鏃ュ織数量
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
        缁熻鐢ㄦ埛鍦ㄦ寚瀹氬皬鏃跺唴鐨勫け璐ョ櫥褰曟鏁?        
        Args:
            user_id: 用户ID
            hours: 灏忔椂鏁?        
        Returns:
            int: 澶辫触鐧诲綍娆℃暟
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
        缁熻鎸囧畾鏃ユ湡鐨勬搷浣滄棩蹇楁暟閲?        
        Args:
            date: 鏃ユ湡
        
        Returns:
            int: 鎿嶄綔鏃ュ織数量
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
        鑾峰彇鐧诲綍缁熻淇℃伅
        
        Args:
            tenant_id: 租户ID
            days: 澶╂暟
        
        Returns:
            Dict[str, Any]: 缁熻淇℃伅
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # 鎬荤櫥褰曟鏁?        total_logins = self.db.query(LoginLog).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.created_at >= start_date
            )
        ).count()
        
        # 鎴愬姛鐧诲綍娆℃暟
        success_logins = self.db.query(LoginLog).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.login_status == "success",
                LoginLog.created_at >= start_date
            )
        ).count()
        
        # 澶辫触鐧诲綍娆℃暟
        failed_logins = self.db.query(LoginLog).filter(
            and_(
                LoginLog.tenant_id == tenant_id,
                LoginLog.login_status == "failed",
                LoginLog.created_at >= start_date
            )
        ).count()
        
        # 姣忔棩鐧诲綍缁熻
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
