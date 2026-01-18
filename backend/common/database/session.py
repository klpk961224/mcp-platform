# -*- coding: utf-8 -*-
"""
鏁版嵁搴撲細璇濈鐞嗘ā鍧?
鍔熻兘璇存槑锛?1. 鎻愪緵鏁版嵁搴撲細璇濈殑涓婁笅鏂囩鐞嗗櫒
2. 鑷姩澶勭悊浜嬪姟鎻愪氦鍜屽洖婊?3. 鏀寔澶氭暟鎹簮鐨勪細璇濈鐞?4. 鎻愪緵浼氳瘽姹犵鐞?
浣跨敤绀轰緥锛?    from common.database.session import get_session, SessionManager
    from common.database.connection import datasource_manager
    
    # 鏂瑰紡1锛氫娇鐢ㄤ笂涓嬫枃绠＄悊鍣紙鎺ㄨ崘锛?    with get_session('mysql') as session:
        users = session.query(User).all()
        # 鑷姩鎻愪氦鍜屽叧闂?    
    # 鏂瑰紡2锛氫娇鐢?SessionManager
    session_manager = SessionManager()
    with session_manager.get_session('mysql') as session:
        users = session.query(User).all()
"""

from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
from loguru import logger
from .connection import datasource_manager


@contextmanager
def get_session(datasource_name: str) -> Generator[Session, None, None]:
    """
    鑾峰彇鏁版嵁搴撲細璇濓紙涓婁笅鏂囩鐞嗗櫒锛?    
    Args:
        datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle', 'postgresql'锛?    
    Yields:
        Session: SQLAlchemy 鏁版嵁搴撲細璇濆璞?    
    Raises:
        ValueError: 鏁版嵁婧愭湭娉ㄥ唽鏃舵姏鍑哄紓甯?    
    浣跨敤绀轰緥锛?        # 鍩烘湰浣跨敤
        with get_session('mysql') as session:
            users = session.query(User).all()
            # 閫€鍑轰笂涓嬫枃鏃惰嚜鍔ㄦ彁浜ゅ拰鍏抽棴
        
        # 甯﹀紓甯稿鐞?        try:
            with get_session('mysql') as session:
                user = User(username='test')
                session.add(user)
                # 濡傛灉鎶涘嚭寮傚父锛岃嚜鍔ㄥ洖婊?        except Exception as e:
            logger.error(f"鎿嶄綔澶辫触: {e}")
    """
    logger.debug(f"鎵撳紑鏁版嵁婧?[{datasource_name}] 鐨勪細璇?)
    
    session = None
    try:
        session = datasource_manager.get_session(datasource_name)
        yield session
        session.commit()
        logger.debug(f"鏁版嵁婧?[{datasource_name}] 浼氳瘽鎻愪氦鎴愬姛")
    except Exception as e:
        if session:
            session.rollback()
            logger.error(f"鏁版嵁婧?[{datasource_name}] 浼氳瘽鍥炴粴: {e}")
        raise
    finally:
        if session:
            session.close()
            logger.debug(f"鍏抽棴鏁版嵁婧?[{datasource_name}] 鐨勪細璇?)


class SessionManager:
    """
    浼氳瘽绠＄悊鍣?    
    鍔熻兘锛?    - 绠＄悊澶氫釜鏁版嵁婧愮殑浼氳瘽
    - 鎻愪緵浼氳瘽姹犵鐞?    - 鏀寔浼氳瘽澶嶇敤
    
    浣跨敤鏂规硶锛?        session_manager = SessionManager()
        
        # 鑾峰彇浼氳瘽
        with session_manager.get_session('mysql') as session:
            users = session.query(User).all()
        
        # 鑾峰彇澶氫釜浼氳瘽
        with session_manager.get_session('mysql') as mysql_session, \
             session_manager.get_session('oracle') as oracle_session:
            # 浣跨敤澶氫釜浼氳瘽
            pass
    """
    
    def __init__(self):
        """鍒濆鍖栦細璇濈鐞嗗櫒"""
        self._sessions: dict = {}
        logger.info("浼氳瘽绠＄悊鍣ㄥ垵濮嬪寲瀹屾垚")
    
    def get_session(self, datasource_name: str) -> Session:
        """
        鑾峰彇鏁版嵁婧愮殑浼氳瘽
        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉?        
        Returns:
            Session: 鏁版嵁搴撲細璇濆璞?        
        浣跨敤绀轰緥锛?            session_manager = SessionManager()
            session = session_manager.get_session('mysql')
            users = session.query(User).all()
            session.close()
        """
        return datasource_manager.get_session(datasource_name)
    
    @contextmanager
    def get_session_context(self, datasource_name: str):
        """
        鑾峰彇鏁版嵁婧愮殑浼氳瘽锛堜笂涓嬫枃绠＄悊鍣級
        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉?        
        Yields:
            Session: 鏁版嵁搴撲細璇濆璞?        
        浣跨敤绀轰緥锛?            session_manager = SessionManager()
            with session_manager.get_session_context('mysql') as session:
                users = session.query(User).all()
        """
        with get_session(datasource_name) as session:
            yield session
    
    def close_all_sessions(self):
        """
        鍏抽棴鎵€鏈変細璇?        
        浣跨敤绀轰緥锛?            session_manager = SessionManager()
            # ... 浣跨敤浼氳瘽 ...
            session_manager.close_all_sessions()
        """
        for session in self._sessions.values():
            if session:
                session.close()
        self._sessions.clear()
        logger.info("鎵€鏈変細璇濆凡鍏抽棴")
    
    def __enter__(self):
        """鏀寔 with 璇彞"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """閫€鍑?with 璇彞鏃跺叧闂墍鏈変細璇?""
        self.close_all_sessions()


class TransactionManager:
    """
    浜嬪姟绠＄悊鍣?    
    鍔熻兘锛?    - 绠＄悊鏁版嵁搴撲簨鍔?    - 鏀寔宓屽浜嬪姟
    - 鏀寔浜嬪姟鍥炴粴
    
    浣跨敤鏂规硶锛?        transaction_manager = TransactionManager()
        
        # 鍩烘湰浜嬪姟
        with transaction_manager.transaction('mysql') as session:
            user = User(username='test')
            session.add(user)
            # 鑷姩鎻愪氦
        
        # 鎵嬪姩鍥炴粴
        with transaction_manager.transaction('mysql') as session:
            user = User(username='test')
            session.add(user)
            if some_condition:
                transaction_manager.rollback()
    """
    
    def __init__(self):
        """鍒濆鍖栦簨鍔＄鐞嗗櫒"""
        self._current_transaction: Optional[Session] = None
        logger.info("浜嬪姟绠＄悊鍣ㄥ垵濮嬪寲瀹屾垚")
    
    @contextmanager
    def transaction(self, datasource_name: str, autocommit: bool = True):
        """
        浜嬪姟涓婁笅鏂囩鐞嗗櫒
        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉?            autocommit: 鏄惁鑷姩鎻愪氦锛堥粯璁?True锛?        
        Yields:
            Session: 鏁版嵁搴撲細璇濆璞?        
        浣跨敤绀轰緥锛?            transaction_manager = TransactionManager()
            
            # 鑷姩鎻愪氦
            with transaction_manager.transaction('mysql') as session:
                user = User(username='test')
                session.add(user)
                # 鑷姩鎻愪氦
            
            # 鎵嬪姩鎻愪氦
            with transaction_manager.transaction('mysql', autocommit=False) as session:
                user = User(username='test')
                session.add(user)
                session.commit()
        """
        session = datasource_manager.get_session(datasource_name)
        self._current_transaction = session
        
        try:
            logger.debug(f"寮€濮嬩簨鍔?[鏁版嵁婧? {datasource_name}]")
            yield session
            
            if autocommit:
                session.commit()
                logger.debug(f"浜嬪姟鎻愪氦鎴愬姛 [鏁版嵁婧? {datasource_name}]")
        except Exception as e:
            session.rollback()
            logger.error(f"浜嬪姟鍥炴粴 [鏁版嵁婧? {datasource_name}]: {e}")
            raise
        finally:
            session.close()
            self._current_transaction = None
            logger.debug(f"浜嬪姟缁撴潫 [鏁版嵁婧? {datasource_name}]")
    
    def rollback(self):
        """
        鎵嬪姩鍥炴粴褰撳墠浜嬪姟
        
        浣跨敤绀轰緥锛?            transaction_manager = TransactionManager()
            with transaction_manager.transaction('mysql') as session:
                user = User(username='test')
                session.add(user)
                if some_error:
                    transaction_manager.rollback()
        """
        if self._current_transaction:
            self._current_transaction.rollback()
            logger.warning("浜嬪姟宸叉墜鍔ㄥ洖婊?)
    
    def commit(self):
        """
        鎵嬪姩鎻愪氦褰撳墠浜嬪姟
        
        浣跨敤绀轰緥锛?            transaction_manager = TransactionManager()
            with transaction_manager.transaction('mysql', autocommit=False) as session:
                user = User(username='test')
                session.add(user)
                transaction_manager.commit()
        """
        if self._current_transaction:
            self._current_transaction.commit()
            logger.info("浜嬪姟宸叉墜鍔ㄦ彁浜?)


# 鍏ㄥ眬瀹炰緥
session_manager = SessionManager()
transaction_manager = TransactionManager()
