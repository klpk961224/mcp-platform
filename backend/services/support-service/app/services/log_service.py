# -*- coding: utf-8 -*-
"""
鏃ュ織鏈嶅姟

鍔熻兘璇存槑锛?1. 鐧诲綍鏃ュ織绠＄悊
2. 鎿嶄綔鏃ュ織绠＄悊
3. 鏃ュ織鏌ヨ鍜岀粺璁?
浣跨敤绀轰緥锛?    from app.services.log_service import LogService
    
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
    鏃ュ織鏈嶅姟
    
    鍔熻兘锛?    - 鐧诲綍鏃ュ織绠＄悊
    - 鎿嶄綔鏃ュ織绠＄悊
    - 鏃ュ織鏌ヨ鍜岀粺璁?    
    浣跨敤鏂规硶锛?        log_service = LogService(db)
        log = log_service.create_login_log(user_id="123", username="admin")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨棩蹇楁湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.log_repo = LogRepository(db)
    
    def create_login_log(self, user_id: str, tenant_id: str,
                         ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                         login_status: str = "success", error_message: Optional[str] = None) -> LoginLog:
        """
        鍒涘缓鐧诲綍鏃ュ織
        
        Args:
            user_id: 鐢ㄦ埛ID
            tenant_id: 绉熸埛ID
            ip_address: IP鍦板潃锛堝彲閫夛級
            user_agent: 鐢ㄦ埛浠ｇ悊锛堝彲閫夛級
            login_status: 鐧诲綍鐘舵€?            error_message: 閿欒淇℃伅锛堝彲閫夛級
        
        Returns:
            LoginLog: 鍒涘缓鐨勭櫥褰曟棩蹇楀璞?        """
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
        璁板綍鎴愬姛鐧诲綍
        
        Args:
            user_id: 鐢ㄦ埛ID
            tenant_id: 绉熸埛ID
            ip_address: IP鍦板潃锛堝彲閫夛級
            user_agent: 鐢ㄦ埛浠ｇ悊锛堝彲閫夛級
        
        Returns:
            LoginLog: 鍒涘缓鐨勭櫥褰曟棩蹇楀璞?        """
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
        璁板綍澶辫触鐧诲綍
        
        Args:
            user_id: 鐢ㄦ埛ID
            tenant_id: 绉熸埛ID
            ip_address: IP鍦板潃锛堝彲閫夛級
            error_message: 閿欒淇℃伅锛堝彲閫夛級
        
        Returns:
            LoginLog: 鍒涘缓鐨勭櫥褰曟棩蹇楀璞?        """
        return self.create_login_log(
            user_id=user_id,
            tenant_id=tenant_id,
            ip_address=ip_address,
            login_status="failed",
            error_message=error_message
        )
    
    def record_logout(self, user_id: str) -> bool:
        """
        璁板綍鐧诲嚭
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        logger.info(f"璁板綍鐧诲嚭: user_id={user_id}")
        
        # 娉ㄦ剰锛氬綋鍓嶈〃缁撴瀯涓嶆敮鎸乴ogout_time瀛楁锛屾鏂规硶鏆傛椂涓嶅疄鐜?        # 濡傛灉闇€瑕佽褰曠櫥鍑猴紝闇€瑕佷慨鏀硅〃缁撴瀯娣诲姞logout_time瀛楁
        return False
    
    def create_operation_log(self, user_id: str, tenant_id: str,
                              module: str, operation: str,
                              method: str = "POST", path: Optional[str] = None,
                              request_params: Optional[str] = None, response_data: Optional[str] = None,
                              response_status: Optional[int] = None,
                              response_time: Optional[int] = None) -> OperationLog:
        """
        鍒涘缓鎿嶄綔鏃ュ織
        
        Args:
            user_id: 鐢ㄦ埛ID
            tenant_id: 绉熸埛ID
            module: 妯″潡鍚嶇О
            operation: 鎿嶄綔鍔ㄤ綔
            method: 璇锋眰鏂规硶
            path: 璇锋眰璺緞锛堝彲閫夛級
            request_params: 璇锋眰鍙傛暟锛堝彲閫夛級
            response_data: 鍝嶅簲鏁版嵁锛堝彲閫夛級
            response_status: 鍝嶅簲鐘舵€侊紙鍙€夛級
            response_time: 鍝嶅簲鏃堕棿锛堝彲閫夛級
        
        Returns:
            OperationLog: 鍒涘缓鐨勬搷浣滄棩蹇楀璞?        """
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
        鑾峰彇鐢ㄦ埛鐧诲綍鏃ュ織
        
        Args:
            user_id: 鐢ㄦ埛ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[LoginLog]: 鐧诲綍鏃ュ織鍒楄〃
        """
        return self.log_repo.get_user_login_logs(user_id, page, page_size)
    
    def get_user_operation_logs(self, user_id: str, page: int = 1, page_size: int = 10) -> List[OperationLog]:
        """
        鑾峰彇鐢ㄦ埛鎿嶄綔鏃ュ織
        
        Args:
            user_id: 鐢ㄦ埛ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[OperationLog]: 鎿嶄綔鏃ュ織鍒楄〃
        """
        return self.log_repo.get_user_operation_logs(user_id, page, page_size)
    
    def check_failed_logins(self, user_id: str, threshold: int = 5, hours: int = 24) -> bool:
        """
        妫€鏌ョ敤鎴峰け璐ョ櫥褰曟鏁版槸鍚﹁秴杩囬槇鍊?        
        Args:
            user_id: 鐢ㄦ埛ID
            threshold: 闃堝€?            hours: 灏忔椂鏁?        
        Returns:
            bool: 鏄惁瓒呰繃闃堝€?        """
        failed_count = self.log_repo.count_failed_logins_by_user(user_id, hours)
        return failed_count >= threshold
    
    def get_login_statistics(self, tenant_id: str, days: int = 7) -> Dict[str, Any]:
        """
        鑾峰彇鐧诲綍缁熻淇℃伅
        
        Args:
            tenant_id: 绉熸埛ID
            days: 澶╂暟
        
        Returns:
            Dict[str, Any]: 缁熻淇℃伅
        """
        return self.log_repo.get_login_statistics(tenant_id, days)
