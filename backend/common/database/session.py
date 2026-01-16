# -*- coding: utf-8 -*-
"""
数据库会话管理模块

功能说明：
1. 提供数据库会话的上下文管理器
2. 自动处理事务提交和回滚
3. 支持多数据源的会话管理
4. 提供会话池管理

使用示例：
    from common.database.session import get_session, SessionManager
    from common.database.connection import datasource_manager
    
    # 方式1：使用上下文管理器（推荐）
    with get_session('mysql') as session:
        users = session.query(User).all()
        # 自动提交和关闭
    
    # 方式2：使用 SessionManager
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
    获取数据库会话（上下文管理器）
    
    Args:
        datasource_name: 数据源名称（如 'mysql', 'oracle', 'postgresql'）
    
    Yields:
        Session: SQLAlchemy 数据库会话对象
    
    Raises:
        ValueError: 数据源未注册时抛出异常
    
    使用示例：
        # 基本使用
        with get_session('mysql') as session:
            users = session.query(User).all()
            # 退出上下文时自动提交和关闭
        
        # 带异常处理
        try:
            with get_session('mysql') as session:
                user = User(username='test')
                session.add(user)
                # 如果抛出异常，自动回滚
        except Exception as e:
            logger.error(f"操作失败: {e}")
    """
    logger.debug(f"打开数据源 [{datasource_name}] 的会话")
    
    session = None
    try:
        session = datasource_manager.get_session(datasource_name)
        yield session
        session.commit()
        logger.debug(f"数据源 [{datasource_name}] 会话提交成功")
    except Exception as e:
        if session:
            session.rollback()
            logger.error(f"数据源 [{datasource_name}] 会话回滚: {e}")
        raise
    finally:
        if session:
            session.close()
            logger.debug(f"关闭数据源 [{datasource_name}] 的会话")


class SessionManager:
    """
    会话管理器
    
    功能：
    - 管理多个数据源的会话
    - 提供会话池管理
    - 支持会话复用
    
    使用方法：
        session_manager = SessionManager()
        
        # 获取会话
        with session_manager.get_session('mysql') as session:
            users = session.query(User).all()
        
        # 获取多个会话
        with session_manager.get_session('mysql') as mysql_session, \
             session_manager.get_session('oracle') as oracle_session:
            # 使用多个会话
            pass
    """
    
    def __init__(self):
        """初始化会话管理器"""
        self._sessions: dict = {}
        logger.info("会话管理器初始化完成")
    
    def get_session(self, datasource_name: str) -> Session:
        """
        获取数据源的会话
        
        Args:
            datasource_name: 数据源名称
        
        Returns:
            Session: 数据库会话对象
        
        使用示例：
            session_manager = SessionManager()
            session = session_manager.get_session('mysql')
            users = session.query(User).all()
            session.close()
        """
        return datasource_manager.get_session(datasource_name)
    
    @contextmanager
    def get_session_context(self, datasource_name: str):
        """
        获取数据源的会话（上下文管理器）
        
        Args:
            datasource_name: 数据源名称
        
        Yields:
            Session: 数据库会话对象
        
        使用示例：
            session_manager = SessionManager()
            with session_manager.get_session_context('mysql') as session:
                users = session.query(User).all()
        """
        with get_session(datasource_name) as session:
            yield session
    
    def close_all_sessions(self):
        """
        关闭所有会话
        
        使用示例：
            session_manager = SessionManager()
            # ... 使用会话 ...
            session_manager.close_all_sessions()
        """
        for session in self._sessions.values():
            if session:
                session.close()
        self._sessions.clear()
        logger.info("所有会话已关闭")
    
    def __enter__(self):
        """支持 with 语句"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 语句时关闭所有会话"""
        self.close_all_sessions()


class TransactionManager:
    """
    事务管理器
    
    功能：
    - 管理数据库事务
    - 支持嵌套事务
    - 支持事务回滚
    
    使用方法：
        transaction_manager = TransactionManager()
        
        # 基本事务
        with transaction_manager.transaction('mysql') as session:
            user = User(username='test')
            session.add(user)
            # 自动提交
        
        # 手动回滚
        with transaction_manager.transaction('mysql') as session:
            user = User(username='test')
            session.add(user)
            if some_condition:
                transaction_manager.rollback()
    """
    
    def __init__(self):
        """初始化事务管理器"""
        self._current_transaction: Optional[Session] = None
        logger.info("事务管理器初始化完成")
    
    @contextmanager
    def transaction(self, datasource_name: str, autocommit: bool = True):
        """
        事务上下文管理器
        
        Args:
            datasource_name: 数据源名称
            autocommit: 是否自动提交（默认 True）
        
        Yields:
            Session: 数据库会话对象
        
        使用示例：
            transaction_manager = TransactionManager()
            
            # 自动提交
            with transaction_manager.transaction('mysql') as session:
                user = User(username='test')
                session.add(user)
                # 自动提交
            
            # 手动提交
            with transaction_manager.transaction('mysql', autocommit=False) as session:
                user = User(username='test')
                session.add(user)
                session.commit()
        """
        session = datasource_manager.get_session(datasource_name)
        self._current_transaction = session
        
        try:
            logger.debug(f"开始事务 [数据源: {datasource_name}]")
            yield session
            
            if autocommit:
                session.commit()
                logger.debug(f"事务提交成功 [数据源: {datasource_name}]")
        except Exception as e:
            session.rollback()
            logger.error(f"事务回滚 [数据源: {datasource_name}]: {e}")
            raise
        finally:
            session.close()
            self._current_transaction = None
            logger.debug(f"事务结束 [数据源: {datasource_name}]")
    
    def rollback(self):
        """
        手动回滚当前事务
        
        使用示例：
            transaction_manager = TransactionManager()
            with transaction_manager.transaction('mysql') as session:
                user = User(username='test')
                session.add(user)
                if some_error:
                    transaction_manager.rollback()
        """
        if self._current_transaction:
            self._current_transaction.rollback()
            logger.warning("事务已手动回滚")
    
    def commit(self):
        """
        手动提交当前事务
        
        使用示例：
            transaction_manager = TransactionManager()
            with transaction_manager.transaction('mysql', autocommit=False) as session:
                user = User(username='test')
                session.add(user)
                transaction_manager.commit()
        """
        if self._current_transaction:
            self._current_transaction.commit()
            logger.info("事务已手动提交")


# 全局实例
session_manager = SessionManager()
transaction_manager = TransactionManager()