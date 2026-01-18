"""
数据库模块

导出：
- DataSourceManager: 多数据源管理器
- PandasDataHelper: Pandas 数据分析助手
- datasource_manager: 全局数据源管理器实例
- get_session: 获取数据库会话
- SessionManager: 会话管理器
- TransactionManager: 事务管理器
- SagaTransaction: Saga事务
- SagaOrchestrator: Saga编排器
- BaseModel: 数据库模型基类
- TimestampMixin: 时间戳混入类
- SoftDeleteMixin: 软删除混入类
- AuditMixin: 审计混入类
- FullModelMixin: 完整模型混入类

使用示例：
    from common.database import (
        datasource_manager, 
        PandasDataHelper,
        get_session,
        BaseModel,
        TimestampMixin,
        SoftDeleteMixin
    )
    
    # 注册数据源
    datasource_manager.register_datasource(
        name='mysql',
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='12345678',
        database='mcp_platform'
    )
    
    # 使用 PandasDataHelper
    helper = PandasDataHelper('mysql')
    df = helper.read_sql("SELECT * FROM users")
    
    # 使用会话
    with get_session('mysql') as session:
        users = session.query(User).all()
    
    # 创建模型
    class User(BaseModel, TimestampMixin, SoftDeleteMixin):
        __tablename__ = 'users'
        username = Column(String(50))
"""

from .connection import DataSourceManager, datasource_manager
from .pandas_helper import PandasDataHelper, create_helper
from .session import get_session, SessionManager, TransactionManager, session_manager, transaction_manager
from .transaction import SagaTransaction, SagaOrchestrator, saga_orchestrator
from .base import (
    BaseModel,
    TimestampMixin,
    SoftDeleteMixin,
    AuditMixin,
    FullModelMixin
)

__all__ = [
    # 连接管理
    'DataSourceManager',
    'datasource_manager',
    'PandasDataHelper',
    'create_helper',
    
    # 会话管理
    'get_session',
    'SessionManager',
    'session_manager',
    'TransactionManager',
    'transaction_manager',
    
    # 事务管理
    'SagaTransaction',
    'SagaOrchestrator',
    'saga_orchestrator',
    
    # 模型基类
    'BaseModel',
    'TimestampMixin',
    'SoftDeleteMixin',
    'AuditMixin',
    'FullModelMixin',
]