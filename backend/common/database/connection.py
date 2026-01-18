"""
澶氭暟鎹簮杩炴帴绠＄悊妯″潡

鍔熻兘璇存槑锛?1. 鏀寔澶氭暟鎹簮绠＄悊锛圡ySQL銆丳ostgreSQL銆丱racle锛?2. 鎻愪緵 SQLAlchemy Engine 鍜?Session 绠＄悊
3. 闆嗘垚 Pandas read_sql/read_sql_query/read_sql_table 鏂规硶
4. 鑷姩璁板綍鏌ヨ鏃ュ織锛圫QL璇彞鍜屽弬鏁帮級

浣跨敤绀轰緥锛?    # 鍒濆鍖栨暟鎹簮
    from common.database.connection import datasource_manager
    
    datasource_manager.register_datasource(
        name='mysql',
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='12345678',
        database='mcp_platform'
    )
    
    # 鏂瑰紡1锛氫娇鐢?SQLAlchemy ORM
    with datasource_manager.get_session_context('mysql') as session:
        users = session.query(User).all()
    
    # 鏂瑰紡2锛氫娇鐢?Pandas 璇诲彇鏁版嵁
    df = datasource_manager.read_sql(
        "SELECT * FROM users WHERE status = %s",
        datasource_name='mysql',
        params={'status': 'active'}
    )
    
    # 鏂瑰紡3锛氫娇鐢?PandasDataHelper锛堟帹鑽愶級
    from common.database.pandas_helper import PandasDataHelper
    helper = PandasDataHelper('mysql')
    df = helper.read_sql("SELECT * FROM users")
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Dict, Any, Optional
from contextlib import contextmanager
import pandas as pd
from loguru import logger


class DataSourceManager:
    """
    澶氭暟鎹簮绠＄悊鍣?    
    鍔熻兘锛?    - 绠＄悊澶氫釜鏁版嵁婧愮殑杩炴帴
    - 鎻愪緵 Session 鍜?Engine 璁块棶
    - 闆嗘垚 Pandas 鏁版嵁璇诲彇鏂规硶
    - 鑷姩璁板綍鏌ヨ鏃ュ織
    
    浣跨敤鏂规硶锛?        1. 娉ㄥ唽鏁版嵁婧愶細register_datasource()
        2. 鑾峰彇 Session锛歡et_session() 鎴?get_session_context()
        3. 鑾峰彇 Engine锛歡et_engine()
        4. Pandas 璇诲彇锛歳ead_sql(), read_sql_query(), read_sql_table()
    """
    
    def __init__(self):
        """鍒濆鍖栨暟鎹簮绠＄悊鍣?""
        self._engines: Dict[str, Any] = {}
        self._session_makers: Dict[str, Any] = {}
        logger.info("鏁版嵁婧愮鐞嗗櫒鍒濆鍖栧畬鎴?)
    
    def register_datasource(
        self,
        name: str,
        db_type: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        **kwargs
    ):
        """
        娉ㄥ唽鏁版嵁婧?        
        Args:
            name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle', 'postgresql'锛?                  - 浣跨敤绀轰緥锛歞atasource_manager.register_datasource(name='mysql', ...)
            db_type: 鏁版嵁搴撶被鍨嬶紙'mysql', 'postgresql', 'oracle'锛?            host: 涓绘満鍦板潃锛堝 'localhost', '192.168.1.100'锛?            port: 绔彛鍙凤紙MySQL:3306, PostgreSQL:5432, Oracle:1521锛?            username: 鏁版嵁搴撶敤鎴峰悕
            password: 鏁版嵁搴撳瘑鐮?            database: 鏁版嵁搴撳悕锛圤racle 浣跨敤 service_name锛?            **kwargs: 鍏朵粬杩炴帴鍙傛暟锛堝 pool_size, max_overflow, echo 绛夛級
                      - pool_size: 杩炴帴姹犲ぇ灏忥紝榛樿 5
                      - max_overflow: 鏈€澶ф孩鍑鸿繛鎺ユ暟锛岄粯璁?10
                      - echo: 鏄惁鎵撳嵃 SQL 璇彞锛岄粯璁?False锛堝紑鍙戠幆澧冨彲璁句负 True锛?        
        浣跨敤绀轰緥锛?            # 娉ㄥ唽 MySQL 鏁版嵁婧?            datasource_manager.register_datasource(
                name='mysql',
                db_type='mysql',
                host='localhost',
                port=3306,
                username='root',
                password='12345678',
                database='mcp_platform',
                pool_size=10,
                max_overflow=20,
                echo=False
            )
            
            # 娉ㄥ唽 Oracle 鏁版嵁婧?            datasource_manager.register_datasource(
                name='oracle',
                db_type='oracle',
                host='192.168.1.100',
                port=1521,
                username='system',
                password='oracle123',
                database='ORCL',  # Oracle 鐨?service_name
                pool_size=5,
                max_overflow=10
            )
        """
        # 鏍规嵁鏁版嵁搴撶被鍨嬫瀯寤鸿繛鎺RL
        if db_type == 'mysql':
            url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"娉ㄥ唽 MySQL 鏁版嵁婧? {name} -> {host}:{port}/{database}")
        elif db_type == 'postgresql':
            url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"娉ㄥ唽 PostgreSQL 鏁版嵁婧? {name} -> {host}:{port}/{database}")
        elif db_type == 'oracle':
            url = f"oracle+oracledb://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"娉ㄥ唽 Oracle 鏁版嵁婧? {name} -> {host}:{port}/{database}")
        else:
            raise ValueError(f"涓嶆敮鎸佺殑鏁版嵁搴撶被鍨? {db_type}锛屾敮鎸佺殑绫诲瀷锛歮ysql, postgresql, oracle")
        
        # 鍒涘缓寮曟搸
        engine = create_engine(url, **kwargs)
        
        # 鍒涘缓 Session Maker
        session_maker = sessionmaker(bind=engine)
        
        # 淇濆瓨鍒扮鐞嗗櫒
        self._engines[name] = engine
        self._session_makers[name] = session_maker
        
        logger.success(f"鏁版嵁婧?[{name}] 娉ㄥ唽鎴愬姛")
    
    def get_session(self, datasource_name: str) -> Session:
        """
        鑾峰彇鎸囧畾鏁版嵁婧愮殑浼氳瘽
        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle'锛?        
        Returns:
            Session: SQLAlchemy 鏁版嵁搴撲細璇濆璞?        
        浣跨敤绀轰緥锛?            session = datasource_manager.get_session('mysql')
            users = session.query(User).all()
            session.close()  # 闇€瑕佹墜鍔ㄥ叧闂?        """
        session_maker = self._session_makers.get(datasource_name)
        if not session_maker:
            raise ValueError(f"鏈壘鍒版暟鎹簮: {datasource_name}锛岃鍏堜娇鐢?register_datasource() 娉ㄥ唽")
        return session_maker()
    
    def get_engine(self, datasource_name: str):
        """
        鑾峰彇鎸囧畾鏁版嵁婧愮殑寮曟搸
        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle'锛?        
        Returns:
            Engine: SQLAlchemy 鏁版嵁搴撳紩鎿庡璞?        
        浣跨敤绀轰緥锛?            engine = datasource_manager.get_engine('mysql')
            # 鐩存帴浣跨敤寮曟搸鎵ц SQL
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM users"))
        """
        engine = self._engines.get(datasource_name)
        if not engine:
            raise ValueError(f"鏈壘鍒版暟鎹簮: {datasource_name}锛岃鍏堜娇鐢?register_datasource() 娉ㄥ唽")
        return engine
    
    @contextmanager
    def get_session_context(self, datasource_name: str):
        """
        鑾峰彇鎸囧畾鏁版嵁婧愮殑浼氳瘽锛堜笂涓嬫枃绠＄悊鍣紝鎺ㄨ崘浣跨敤锛?        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle'锛?        
        Yields:
            Session: SQLAlchemy 鏁版嵁搴撲細璇濆璞?        
        浣跨敤绀轰緥锛?            # 鏂瑰紡1锛氳嚜鍔ㄦ彁浜ゅ拰鍏抽棴锛堟帹鑽愶級
            with datasource_manager.get_session_context('mysql') as session:
                users = session.query(User).all()
                # 閫€鍑轰笂涓嬫枃鏃惰嚜鍔ㄦ彁浜ゅ拰鍏抽棴
            
            # 鏂瑰紡2锛氭崟鑾峰紓甯稿苟鑷姩鍥炴粴
            try:
                with datasource_manager.get_session_context('mysql') as session:
                    user = User(username='test', email='test@example.com')
                    session.add(user)
                    # 濡傛灉鎶涘嚭寮傚父锛岃嚜鍔ㄥ洖婊?            except Exception as e:
                logger.error(f"鎿嶄綔澶辫触: {e}")
        """
        session = self.get_session(datasource_name)
        try:
            logger.debug(f"鎵撳紑鏁版嵁婧?[{datasource_name}] 鐨勪細璇?)
            yield session
            session.commit()
            logger.debug(f"鏁版嵁婧?[{datasource_name}] 浼氳瘽鎻愪氦鎴愬姛")
        except Exception as e:
            session.rollback()
            logger.error(f"鏁版嵁婧?[{datasource_name}] 浼氳瘽鍥炴粴: {e}")
            raise
        finally:
            session.close()
            logger.debug(f"鍏抽棴鏁版嵁婧?[{datasource_name}] 鐨勪細璇?)
    
    def read_sql(
        self,
        sql: str,
        datasource_name: str,
        params: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        浣跨敤 pandas 璇诲彇 SQL 鏌ヨ缁撴灉锛堥€氱敤鏂规硶锛?        
        Args:
            sql: SQL 鏌ヨ璇彞锛堝彲浠ユ槸 SELECT 鏌ヨ鎴栬〃鍚嶏級
                 - 绀轰緥1锛歋ELECT * FROM users WHERE status = %s
                 - 绀轰緥2锛歋ELECT * FROM orders WHERE order_date > :start_date
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle'锛?            params: SQL 鍙傛暟锛堥槻姝?SQL 娉ㄥ叆锛?                    - 绀轰緥1锛歿'status': 'active'}
                    - 绀轰緥2锛歿'start_date': '2024-01-01'}
            **kwargs: 浼犻€掔粰 pd.read_sql 鐨勫叾浠栧弬鏁?                    - index_col: 鎸囧畾绱㈠紩鍒?                    - parse_dates: 瑙ｆ瀽鏃ユ湡鍒?                    - columns: 鎸囧畾璇诲彇鐨勫垪
        
        Returns:
            pd.DataFrame: 鏌ヨ缁撴灉
        
        浣跨敤绀轰緥锛?            # 鍩烘湰鏌ヨ
            df = datasource_manager.read_sql(
                "SELECT * FROM users",
                datasource_name='mysql'
            )
            
            # 甯﹀弬鏁扮殑鏌ヨ锛堟帹鑽愶紝闃叉 SQL 娉ㄥ叆锛?            df = datasource_manager.read_sql(
                "SELECT * FROM users WHERE status = %s AND age > %s",
                datasource_name='mysql',
                params={'status': 'active', 'age': 18}
            )
            
            # 浣跨敤鍛藉悕鍙傛暟
            df = datasource_manager.read_sql(
                "SELECT * FROM orders WHERE order_date > :start_date AND order_date < :end_date",
                datasource_name='oracle',
                params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
            )
            
            # 瑙ｆ瀽鏃ユ湡鍒?            df = datasource_manager.read_sql(
                "SELECT * FROM orders",
                datasource_name='mysql',
                parse_dates=['order_date', 'created_at']
            )
        """
        # 璁板綍鏌ヨ鏃ュ織
        logger.info(f"鎵ц SQL 鏌ヨ [鏁版嵁婧? {datasource_name}]")
        logger.info(f"SQL 璇彞: {sql}")
        if params:
            logger.info(f"鏌ヨ鍙傛暟: {params}")
        
        engine = self.get_engine(datasource_name)
        df = pd.read_sql(sql, engine, params=params, **kwargs)
        
        logger.success(f"鏌ヨ鎴愬姛锛岃繑鍥?{len(df)} 鏉¤褰?)
        return df
    
    def read_sql_query(
        self,
        sql: str,
        datasource_name: str,
        params: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        浣跨敤 pandas 璇诲彇 SQL 鏌ヨ缁撴灉锛堜粎鏌ヨ璇彞锛?        
        涓?read_sql 鐨勫尯鍒細
        - read_sql_query: 鍙兘鎵ц SELECT 鏌ヨ
        - read_sql: 鍙互鎵ц SELECT 鏌ヨ鎴栬鍙栬〃鍚?        
        Args:
            sql: SQL 鏌ヨ璇彞锛堝繀椤绘槸 SELECT 璇彞锛?                 - 绀轰緥锛歋ELECT id, username, email FROM users WHERE status = %s
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle'锛?            params: SQL 鍙傛暟锛堥槻姝?SQL 娉ㄥ叆锛?            **kwargs: 浼犻€掔粰 pd.read_sql_query 鐨勫叾浠栧弬鏁?        
        Returns:
            pd.DataFrame: 鏌ヨ缁撴灉
        
        浣跨敤绀轰緥锛?            # 绠€鍗曟煡璇?            df = datasource_manager.read_sql_query(
                "SELECT id, username FROM users",
                datasource_name='mysql'
            )
            
            # 澶嶆潅鏌ヨ锛圝OIN锛?            df = datasource_manager.read_sql_query(
                \"\"\"
                SELECT u.id, u.username, o.order_id, o.amount
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                WHERE u.status = %s
                \"\"\",
                datasource_name='mysql',
                params={'status': 'active'}
            )
            
            # 鑱氬悎鏌ヨ
            df = datasource_manager.read_sql_query(
                \"\"\"
                SELECT user_id, COUNT(*) as order_count, SUM(amount) as total_amount
                FROM orders
                WHERE order_date > :start_date
                GROUP BY user_id
                \"\"\",
                datasource_name='oracle',
                params={'start_date': '2024-01-01'}
            )
        """
        # 璁板綍鏌ヨ鏃ュ織
        logger.info(f"鎵ц SQL 鏌ヨ [鏁版嵁婧? {datasource_name}]")
        logger.info(f"SQL 璇彞: {sql}")
        if params:
            logger.info(f"鏌ヨ鍙傛暟: {params}")
        
        engine = self.get_engine(datasource_name)
        df = pd.read_sql_query(sql, engine, params=params, **kwargs)
        
        logger.success(f"鏌ヨ鎴愬姛锛岃繑鍥?{len(df)} 鏉¤褰?)
        return df
    
    def read_sql_table(
        self,
        table_name: str,
        datasource_name: str,
        columns: Optional[list] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        浣跨敤 pandas 璇诲彇鏁翠釜琛?        
        Args:
            table_name: 琛ㄥ悕
                       - 绀轰緥锛?users', 'orders', 'products'
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle'锛?            columns: 鎸囧畾璇诲彇鐨勫垪锛堝彲閫夛級
                     - 绀轰緥锛歔'id', 'username', 'email']
                     - 濡傛灉涓嶆寚瀹氾紝鍒欒鍙栨墍鏈夊垪
            **kwargs: 浼犻€掔粰 pd.read_sql_table 鐨勫叾浠栧弬鏁?                    - parse_dates: 瑙ｆ瀽鏃ユ湡鍒?        
        Returns:
            pd.DataFrame: 琛ㄦ暟鎹?        
        浣跨敤绀轰緥锛?            # 璇诲彇鏁翠釜琛?            df = datasource_manager.read_sql_table(
                'users',
                datasource_name='mysql'
            )
            
            # 鍙鍙栨寚瀹氬垪
            df = datasource_manager.read_sql_table(
                'users',
                datasource_name='mysql',
                columns=['id', 'username', 'email']
            )
            
            # 瑙ｆ瀽鏃ユ湡鍒?            df = datasource_manager.read_sql_table(
                'orders',
                datasource_name='oracle',
                parse_dates=['order_date', 'created_at']
            )
        """
        # 璁板綍鏌ヨ鏃ュ織
        logger.info(f"璇诲彇琛ㄦ暟鎹?[鏁版嵁婧? {datasource_name}, 琛? {table_name}]")
        if columns:
            logger.info(f"鎸囧畾鍒? {columns}")
        
        engine = self.get_engine(datasource_name)
        df = pd.read_sql_table(table_name, engine, columns=columns, **kwargs)
        
        logger.success(f"璇诲彇鎴愬姛锛岃繑鍥?{len(df)} 鏉¤褰?)
        return df
    
    def list_datasources(self) -> list:
        """
        鍒楀嚭鎵€鏈夊凡娉ㄥ唽鐨勬暟鎹簮
        
        Returns:
            list: 鏁版嵁婧愬悕绉板垪琛?        
        浣跨敤绀轰緥锛?            datasources = datasource_manager.list_datasources()
            print(f"宸叉敞鍐岀殑鏁版嵁婧? {datasources}")
        """
        return list(self._engines.keys())
    
    def has_datasource(self, datasource_name: str) -> bool:
        """
        妫€鏌ユ暟鎹簮鏄惁宸叉敞鍐?        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉?        
        Returns:
            bool: 鏄惁宸叉敞鍐?        
        浣跨敤绀轰緥锛?            if datasource_manager.has_datasource('oracle'):
                df = datasource_manager.read_sql("SELECT * FROM orders", 'oracle')
        """
        return datasource_name in self._engines


# 鍏ㄥ眬鏁版嵁婧愮鐞嗗櫒瀹炰緥
datasource_manager = DataSourceManager()
