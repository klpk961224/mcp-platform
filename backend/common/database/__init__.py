"""
鏁版嵁搴撴ā鍧?
瀵煎嚭锛?- DataSourceManager: 澶氭暟鎹簮绠＄悊鍣?- PandasDataHelper: Pandas 鏁版嵁鍒嗘瀽鍔╂墜
- datasource_manager: 鍏ㄥ眬鏁版嵁婧愮鐞嗗櫒瀹炰緥
- get_session: 鑾峰彇鏁版嵁搴撲細璇?- SessionManager: 浼氳瘽绠＄悊鍣?- TransactionManager: 浜嬪姟绠＄悊鍣?- SagaTransaction: Saga浜嬪姟
- SagaOrchestrator: Saga缂栨帓鍣?- BaseModel: 鏁版嵁搴撴ā鍨嬪熀绫?- TimestampMixin: 鏃堕棿鎴虫贩鍏ョ被
- SoftDeleteMixin: 杞垹闄ゆ贩鍏ョ被
- AuditMixin: 瀹¤娣峰叆绫?- FullModelMixin: 瀹屾暣妯″瀷娣峰叆绫?
浣跨敤绀轰緥锛?    from common.database import (
        datasource_manager, 
        PandasDataHelper,
        get_session,
        BaseModel,
        TimestampMixin,
        SoftDeleteMixin
    )
    
    # 娉ㄥ唽鏁版嵁婧?    datasource_manager.register_datasource(
        name='mysql',
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='12345678',
        database='mcp_platform'
    )
    
    # 浣跨敤 PandasDataHelper
    helper = PandasDataHelper('mysql')
    df = helper.read_sql("SELECT * FROM users")
    
    # 浣跨敤浼氳瘽
    with get_session('mysql') as session:
        users = session.query(User).all()
    
    # 创建妯″瀷
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
    # 杩炴帴绠＄悊
    'DataSourceManager',
    'datasource_manager',
    'PandasDataHelper',
    'create_helper',
    
    # 浼氳瘽绠＄悊
    'get_session',
    'SessionManager',
    'session_manager',
    'TransactionManager',
    'transaction_manager',
    
    # 浜嬪姟绠＄悊
    'SagaTransaction',
    'SagaOrchestrator',
    'saga_orchestrator',
    
    # 妯″瀷鍩虹被
    'BaseModel',
    'TimestampMixin',
    'SoftDeleteMixin',
    'AuditMixin',
    'FullModelMixin',
]
