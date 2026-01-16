"""
多数据源连接管理模块

功能说明：
1. 支持多数据源管理（MySQL、PostgreSQL、Oracle）
2. 提供 SQLAlchemy Engine 和 Session 管理
3. 集成 Pandas read_sql/read_sql_query/read_sql_table 方法
4. 自动记录查询日志（SQL语句和参数）

使用示例：
    # 初始化数据源
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
    
    # 方式1：使用 SQLAlchemy ORM
    with datasource_manager.get_session_context('mysql') as session:
        users = session.query(User).all()
    
    # 方式2：使用 Pandas 读取数据
    df = datasource_manager.read_sql(
        "SELECT * FROM users WHERE status = %s",
        datasource_name='mysql',
        params={'status': 'active'}
    )
    
    # 方式3：使用 PandasDataHelper（推荐）
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
    多数据源管理器
    
    功能：
    - 管理多个数据源的连接
    - 提供 Session 和 Engine 访问
    - 集成 Pandas 数据读取方法
    - 自动记录查询日志
    
    使用方法：
        1. 注册数据源：register_datasource()
        2. 获取 Session：get_session() 或 get_session_context()
        3. 获取 Engine：get_engine()
        4. Pandas 读取：read_sql(), read_sql_query(), read_sql_table()
    """
    
    def __init__(self):
        """初始化数据源管理器"""
        self._engines: Dict[str, Any] = {}
        self._session_makers: Dict[str, Any] = {}
        logger.info("数据源管理器初始化完成")
    
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
        注册数据源
        
        Args:
            name: 数据源名称（如 'mysql', 'oracle', 'postgresql'）
                  - 使用示例：datasource_manager.register_datasource(name='mysql', ...)
            db_type: 数据库类型（'mysql', 'postgresql', 'oracle'）
            host: 主机地址（如 'localhost', '192.168.1.100'）
            port: 端口号（MySQL:3306, PostgreSQL:5432, Oracle:1521）
            username: 数据库用户名
            password: 数据库密码
            database: 数据库名（Oracle 使用 service_name）
            **kwargs: 其他连接参数（如 pool_size, max_overflow, echo 等）
                      - pool_size: 连接池大小，默认 5
                      - max_overflow: 最大溢出连接数，默认 10
                      - echo: 是否打印 SQL 语句，默认 False（开发环境可设为 True）
        
        使用示例：
            # 注册 MySQL 数据源
            datasource_manager.register_datasource(
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
            
            # 注册 Oracle 数据源
            datasource_manager.register_datasource(
                name='oracle',
                db_type='oracle',
                host='192.168.1.100',
                port=1521,
                username='system',
                password='oracle123',
                database='ORCL',  # Oracle 的 service_name
                pool_size=5,
                max_overflow=10
            )
        """
        # 根据数据库类型构建连接URL
        if db_type == 'mysql':
            url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"注册 MySQL 数据源: {name} -> {host}:{port}/{database}")
        elif db_type == 'postgresql':
            url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"注册 PostgreSQL 数据源: {name} -> {host}:{port}/{database}")
        elif db_type == 'oracle':
            url = f"oracle+oracledb://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"注册 Oracle 数据源: {name} -> {host}:{port}/{database}")
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}，支持的类型：mysql, postgresql, oracle")
        
        # 创建引擎
        engine = create_engine(url, **kwargs)
        
        # 创建 Session Maker
        session_maker = sessionmaker(bind=engine)
        
        # 保存到管理器
        self._engines[name] = engine
        self._session_makers[name] = session_maker
        
        logger.success(f"数据源 [{name}] 注册成功")
    
    def get_session(self, datasource_name: str) -> Session:
        """
        获取指定数据源的会话
        
        Args:
            datasource_name: 数据源名称（如 'mysql', 'oracle'）
        
        Returns:
            Session: SQLAlchemy 数据库会话对象
        
        使用示例：
            session = datasource_manager.get_session('mysql')
            users = session.query(User).all()
            session.close()  # 需要手动关闭
        """
        session_maker = self._session_makers.get(datasource_name)
        if not session_maker:
            raise ValueError(f"未找到数据源: {datasource_name}，请先使用 register_datasource() 注册")
        return session_maker()
    
    def get_engine(self, datasource_name: str):
        """
        获取指定数据源的引擎
        
        Args:
            datasource_name: 数据源名称（如 'mysql', 'oracle'）
        
        Returns:
            Engine: SQLAlchemy 数据库引擎对象
        
        使用示例：
            engine = datasource_manager.get_engine('mysql')
            # 直接使用引擎执行 SQL
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM users"))
        """
        engine = self._engines.get(datasource_name)
        if not engine:
            raise ValueError(f"未找到数据源: {datasource_name}，请先使用 register_datasource() 注册")
        return engine
    
    @contextmanager
    def get_session_context(self, datasource_name: str):
        """
        获取指定数据源的会话（上下文管理器，推荐使用）
        
        Args:
            datasource_name: 数据源名称（如 'mysql', 'oracle'）
        
        Yields:
            Session: SQLAlchemy 数据库会话对象
        
        使用示例：
            # 方式1：自动提交和关闭（推荐）
            with datasource_manager.get_session_context('mysql') as session:
                users = session.query(User).all()
                # 退出上下文时自动提交和关闭
            
            # 方式2：捕获异常并自动回滚
            try:
                with datasource_manager.get_session_context('mysql') as session:
                    user = User(username='test', email='test@example.com')
                    session.add(user)
                    # 如果抛出异常，自动回滚
            except Exception as e:
                logger.error(f"操作失败: {e}")
        """
        session = self.get_session(datasource_name)
        try:
            logger.debug(f"打开数据源 [{datasource_name}] 的会话")
            yield session
            session.commit()
            logger.debug(f"数据源 [{datasource_name}] 会话提交成功")
        except Exception as e:
            session.rollback()
            logger.error(f"数据源 [{datasource_name}] 会话回滚: {e}")
            raise
        finally:
            session.close()
            logger.debug(f"关闭数据源 [{datasource_name}] 的会话")
    
    def read_sql(
        self,
        sql: str,
        datasource_name: str,
        params: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        使用 pandas 读取 SQL 查询结果（通用方法）
        
        Args:
            sql: SQL 查询语句（可以是 SELECT 查询或表名）
                 - 示例1：SELECT * FROM users WHERE status = %s
                 - 示例2：SELECT * FROM orders WHERE order_date > :start_date
            datasource_name: 数据源名称（如 'mysql', 'oracle'）
            params: SQL 参数（防止 SQL 注入）
                    - 示例1：{'status': 'active'}
                    - 示例2：{'start_date': '2024-01-01'}
            **kwargs: 传递给 pd.read_sql 的其他参数
                    - index_col: 指定索引列
                    - parse_dates: 解析日期列
                    - columns: 指定读取的列
        
        Returns:
            pd.DataFrame: 查询结果
        
        使用示例：
            # 基本查询
            df = datasource_manager.read_sql(
                "SELECT * FROM users",
                datasource_name='mysql'
            )
            
            # 带参数的查询（推荐，防止 SQL 注入）
            df = datasource_manager.read_sql(
                "SELECT * FROM users WHERE status = %s AND age > %s",
                datasource_name='mysql',
                params={'status': 'active', 'age': 18}
            )
            
            # 使用命名参数
            df = datasource_manager.read_sql(
                "SELECT * FROM orders WHERE order_date > :start_date AND order_date < :end_date",
                datasource_name='oracle',
                params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
            )
            
            # 解析日期列
            df = datasource_manager.read_sql(
                "SELECT * FROM orders",
                datasource_name='mysql',
                parse_dates=['order_date', 'created_at']
            )
        """
        # 记录查询日志
        logger.info(f"执行 SQL 查询 [数据源: {datasource_name}]")
        logger.info(f"SQL 语句: {sql}")
        if params:
            logger.info(f"查询参数: {params}")
        
        engine = self.get_engine(datasource_name)
        df = pd.read_sql(sql, engine, params=params, **kwargs)
        
        logger.success(f"查询成功，返回 {len(df)} 条记录")
        return df
    
    def read_sql_query(
        self,
        sql: str,
        datasource_name: str,
        params: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        使用 pandas 读取 SQL 查询结果（仅查询语句）
        
        与 read_sql 的区别：
        - read_sql_query: 只能执行 SELECT 查询
        - read_sql: 可以执行 SELECT 查询或读取表名
        
        Args:
            sql: SQL 查询语句（必须是 SELECT 语句）
                 - 示例：SELECT id, username, email FROM users WHERE status = %s
            datasource_name: 数据源名称（如 'mysql', 'oracle'）
            params: SQL 参数（防止 SQL 注入）
            **kwargs: 传递给 pd.read_sql_query 的其他参数
        
        Returns:
            pd.DataFrame: 查询结果
        
        使用示例：
            # 简单查询
            df = datasource_manager.read_sql_query(
                "SELECT id, username FROM users",
                datasource_name='mysql'
            )
            
            # 复杂查询（JOIN）
            df = datasource_manager.read_sql_query(
                \"\"\"
                SELECT u.id, u.username, o.order_id, o.amount
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                WHERE u.status = %s
                \"\"\",
                datasource_name='mysql',
                params={'status': 'active'}
            )
            
            # 聚合查询
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
        # 记录查询日志
        logger.info(f"执行 SQL 查询 [数据源: {datasource_name}]")
        logger.info(f"SQL 语句: {sql}")
        if params:
            logger.info(f"查询参数: {params}")
        
        engine = self.get_engine(datasource_name)
        df = pd.read_sql_query(sql, engine, params=params, **kwargs)
        
        logger.success(f"查询成功，返回 {len(df)} 条记录")
        return df
    
    def read_sql_table(
        self,
        table_name: str,
        datasource_name: str,
        columns: Optional[list] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        使用 pandas 读取整个表
        
        Args:
            table_name: 表名
                       - 示例：'users', 'orders', 'products'
            datasource_name: 数据源名称（如 'mysql', 'oracle'）
            columns: 指定读取的列（可选）
                     - 示例：['id', 'username', 'email']
                     - 如果不指定，则读取所有列
            **kwargs: 传递给 pd.read_sql_table 的其他参数
                    - parse_dates: 解析日期列
        
        Returns:
            pd.DataFrame: 表数据
        
        使用示例：
            # 读取整个表
            df = datasource_manager.read_sql_table(
                'users',
                datasource_name='mysql'
            )
            
            # 只读取指定列
            df = datasource_manager.read_sql_table(
                'users',
                datasource_name='mysql',
                columns=['id', 'username', 'email']
            )
            
            # 解析日期列
            df = datasource_manager.read_sql_table(
                'orders',
                datasource_name='oracle',
                parse_dates=['order_date', 'created_at']
            )
        """
        # 记录查询日志
        logger.info(f"读取表数据 [数据源: {datasource_name}, 表: {table_name}]")
        if columns:
            logger.info(f"指定列: {columns}")
        
        engine = self.get_engine(datasource_name)
        df = pd.read_sql_table(table_name, engine, columns=columns, **kwargs)
        
        logger.success(f"读取成功，返回 {len(df)} 条记录")
        return df
    
    def list_datasources(self) -> list:
        """
        列出所有已注册的数据源
        
        Returns:
            list: 数据源名称列表
        
        使用示例：
            datasources = datasource_manager.list_datasources()
            print(f"已注册的数据源: {datasources}")
        """
        return list(self._engines.keys())
    
    def has_datasource(self, datasource_name: str) -> bool:
        """
        检查数据源是否已注册
        
        Args:
            datasource_name: 数据源名称
        
        Returns:
            bool: 是否已注册
        
        使用示例：
            if datasource_manager.has_datasource('oracle'):
                df = datasource_manager.read_sql("SELECT * FROM orders", 'oracle')
        """
        return datasource_name in self._engines


# 全局数据源管理器实例
datasource_manager = DataSourceManager()