"""
Pandas 数据分析助手模块

功能说明：
1. 封装 pandas 的数据库操作方法
2. 提供更简洁易用的接口
3. 支持大数据集分批读取
4. 支持将 DataFrame 写入数据库
5. 自动记录查询日志（SQL语句和参数）

使用示例：
    # 基本使用
    from common.database.pandas_helper import PandasDataHelper
    
    # 创建助手实例
    mysql_helper = PandasDataHelper('mysql')
    oracle_helper = PandasDataHelper('oracle')
    
    # 读取数据
    df = mysql_helper.read_sql("SELECT * FROM users WHERE status = %s", params={'status': 'active'})
    
    # 读取整个表
    df = mysql_helper.read_sql_table('users')
    
    # 批量读取大数据集
    df = mysql_helper.batch_read("SELECT * FROM big_table", batch_size=10000)
    
    # 写入数据
    df.to_sql('new_table', mysql_helper.get_engine(), if_exists='replace')
"""

import pandas as pd
from typing import Optional, Union, List, Dict, Any, Iterator
from sqlalchemy import text
from loguru import logger
from .connection import datasource_manager


class PandasDataHelper:
    """
    Pandas 数据分析助手
    
    功能：
    - 封装 pandas 的数据库操作方法
    - 提供更简洁易用的接口
    - 支持大数据集分批读取
    - 支持将 DataFrame 写入数据库
    - 自动记录查询日志
    
    使用方法：
        # 创建助手实例
        helper = PandasDataHelper('mysql')
        
        # 读取数据
        df = helper.read_sql("SELECT * FROM users")
        
        # 批量读取
        df = helper.batch_read("SELECT * FROM big_table", batch_size=10000)
        
        # 写入数据
        df.to_sql('new_table', helper.get_engine(), if_exists='replace')
    """
    
    def __init__(self, datasource_name: str):
        """
        初始化 Pandas 数据助手
        
        Args:
            datasource_name: 数据源名称（如 'mysql', 'oracle', 'postgresql'）
                           - 必须是已注册的数据源
                           - 使用 datasource_manager.register_datasource() 注册
        
        使用示例：
            # 创建 MySQL 助手
            mysql_helper = PandasDataHelper('mysql')
            
            # 创建 Oracle 助手
            oracle_helper = PandasDataHelper('oracle')
            
            # 创建 PostgreSQL 助手
            postgresql_helper = PandasDataHelper('postgresql')
        """
        self.datasource_name = datasource_name
        
        # 验证数据源是否已注册
        if not datasource_manager.has_datasource(datasource_name):
            raise ValueError(
                f"数据源 [{datasource_name}] 未注册，"
                f"请先使用 datasource_manager.register_datasource() 注册"
            )
        
        logger.info(f"创建 Pandas 数据助手: {datasource_name}")
    
    def read_sql(
        self,
        sql: str,
        params: Optional[dict] = None,
        chunksize: Optional[int] = None,
        **kwargs
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """
        读取 SQL 查询结果（通用方法）
        
        Args:
            sql: SQL 查询语句（可以是 SELECT 查询或表名）
                 - 示例1：SELECT * FROM users WHERE status = %s
                 - 示例2：SELECT * FROM orders WHERE order_date > :start_date
            params: SQL 参数（防止 SQL 注入）
                    - 示例1：{'status': 'active'}
                    - 示例2：{'start_date': '2024-01-01'}
            chunksize: 分块读取大小（用于大数据集）
                      - 如果指定，返回迭代器
                      - 示例：10000（每次读取 10000 条）
            **kwargs: 传递给 pd.read_sql 的其他参数
                    - index_col: 指定索引列
                    - parse_dates: 解析日期列
                    - columns: 指定读取的列
        
        Returns:
            pd.DataFrame 或 Iterator[pd.DataFrame]: 查询结果
            - 如果不指定 chunksize，返回 DataFrame
            - 如果指定 chunksize，返回迭代器
        
        使用示例：
            # 基本查询
            df = helper.read_sql("SELECT * FROM users")
            
            # 带参数的查询（推荐，防止 SQL 注入）
            df = helper.read_sql(
                "SELECT * FROM users WHERE status = %s AND age > %s",
                params={'status': 'active', 'age': 18}
            )
            
            # 使用命名参数
            df = helper.read_sql(
                "SELECT * FROM orders WHERE order_date > :start_date AND order_date < :end_date",
                params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
            )
            
            # 解析日期列
            df = helper.read_sql(
                "SELECT * FROM orders",
                parse_dates=['order_date', 'created_at']
            )
            
            # 分块读取大数据集（返回迭代器）
            for chunk in helper.read_sql("SELECT * FROM big_table", chunksize=10000):
                process_chunk(chunk)
        """
        logger.info(f"[{self.datasource_name}] 执行 SQL 查询")
        logger.info(f"SQL 语句: {sql}")
        if params:
            logger.info(f"查询参数: {params}")
        if chunksize:
            logger.info(f"分块读取，每块大小: {chunksize}")
        
        result = datasource_manager.read_sql(
            sql, 
            self.datasource_name, 
            params=params, 
            chunksize=chunksize,
            **kwargs
        )
        
        if not chunksize:
            logger.success(f"查询成功，返回 {len(result)} 条记录")
        else:
            logger.success(f"查询成功，返回分块迭代器")
        
        return result
    
    def read_sql_query(
        self,
        query: str,
        params: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        读取 SQL 查询结果（仅查询语句）
        
        与 read_sql 的区别：
        - read_sql_query: 只能执行 SELECT 查询
        - read_sql: 可以执行 SELECT 查询或读取表名
        
        Args:
            query: SQL 查询语句（必须是 SELECT 语句）
                   - 示例：SELECT id, username, email FROM users WHERE status = %s
            params: SQL 参数（防止 SQL 注入）
            **kwargs: 传递给 pd.read_sql_query 的其他参数
        
        Returns:
            pd.DataFrame: 查询结果
        
        使用示例：
            # 简单查询
            df = helper.read_sql_query("SELECT id, username FROM users")
            
            # 复杂查询（JOIN）
            df = helper.read_sql_query(
                \"\"\"
                SELECT u.id, u.username, o.order_id, o.amount
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                WHERE u.status = %s
                \"\"\",
                params={'status': 'active'}
            )
            
            # 聚合查询
            df = helper.read_sql_query(
                \"\"\"
                SELECT user_id, COUNT(*) as order_count, SUM(amount) as total_amount
                FROM orders
                WHERE order_date > :start_date
                GROUP BY user_id
                \"\"\",
                params={'start_date': '2024-01-01'}
            )
        """
        logger.info(f"[{self.datasource_name}] 执行 SQL 查询（仅查询）")
        logger.info(f"SQL 语句: {query}")
        if params:
            logger.info(f"查询参数: {params}")
        
        result = datasource_manager.read_sql_query(
            query, 
            self.datasource_name, 
            params=params,
            **kwargs
        )
        
        logger.success(f"查询成功，返回 {len(result)} 条记录")
        return result
    
    def read_sql_table(
        self,
        table_name: str,
        columns: Optional[List[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        读取整个表
        
        Args:
            table_name: 表名
                       - 示例：'users', 'orders', 'products'
            columns: 指定读取的列（可选）
                     - 示例：['id', 'username', 'email']
                     - 如果不指定，则读取所有列
            **kwargs: 传递给 pd.read_sql_table 的其他参数
                    - parse_dates: 解析日期列
        
        Returns:
            pd.DataFrame: 表数据
        
        使用示例：
            # 读取整个表
            df = helper.read_sql_table('users')
            
            # 只读取指定列
            df = helper.read_sql_table(
                'users',
                columns=['id', 'username', 'email']
            )
            
            # 解析日期列
            df = helper.read_sql_table(
                'orders',
                parse_dates=['order_date', 'created_at']
            )
        """
        logger.info(f"[{self.datasource_name}] 读取表: {table_name}")
        if columns:
            logger.info(f"指定列: {columns}")
        
        result = datasource_manager.read_sql_table(
            table_name, 
            self.datasource_name, 
            columns=columns,
            **kwargs
        )
        
        logger.success(f"读取成功，返回 {len(result)} 条记录")
        return result
    
    def batch_read(
        self,
        query: str,
        batch_size: int = 10000,
        params: Optional[dict] = None
    ) -> pd.DataFrame:
        """
        批量读取大数据集（自动合并）
        
        适用于数据量很大的情况，避免内存溢出
        
        Args:
            query: SQL 查询语句
                   - 示例：SELECT * FROM big_table WHERE created_at > '2024-01-01'
            batch_size: 批次大小（默认 10000）
                      - 根据数据量和内存情况调整
                      - 建议：10000-100000
            params: SQL 参数（防止 SQL 注入）
        
        Returns:
            pd.DataFrame: 合并后的完整数据
        
        使用示例：
            # 读取大数据集（100万条记录）
            df = helper.batch_read(
                "SELECT * FROM big_table WHERE created_at > %s",
                batch_size=10000,
                params={'created_at': '2024-01-01'}
            )
            
            # 调整批次大小（数据量更大时）
            df = helper.batch_read(
                "SELECT * FROM huge_table",
                batch_size=50000
            )
        """
        logger.info(f"[{self.datasource_name}] 批量读取大数据集")
        logger.info(f"SQL 语句: {query}")
        logger.info(f"批次大小: {batch_size}")
        if params:
            logger.info(f"查询参数: {params}")
        
        chunks = []
        total_rows = 0
        
        for i, chunk in enumerate(self.read_sql(query, params=params, chunksize=batch_size)):
            chunks.append(chunk)
            total_rows += len(chunk)
            logger.debug(f"已读取批次 {i+1}, 当前累计: {total_rows} 条记录")
        
        # 合并所有批次
        if chunks:
            result = pd.concat(chunks, ignore_index=True)
            logger.success(f"批量读取完成，共 {len(result)} 条记录")
            return result
        else:
            logger.warning("未读取到任何数据")
            return pd.DataFrame()
    
    def to_sql(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = 'fail',
        index: bool = False,
        chunksize: Optional[int] = None,
        **kwargs
    ) -> Optional[int]:
        """
        将 DataFrame 写入数据库
        
        Args:
            df: 要写入的 DataFrame
            table_name: 目标表名
                      - 示例：'new_table', 'backup_users'
            if_exists: 表存在时的处理方式
                      - 'fail': 抛出异常（默认）
                      - 'replace': 删除原表，创建新表
                      - 'append': 追加数据到原表
            index: 是否写入索引列（默认 False）
            chunksize: 分块写入大小（用于大数据集）
                      - 示例：10000（每次写入 10000 条）
            **kwargs: 其他参数（如 dtype, method）
        
        Returns:
            Optional[int]: 写入的行数（如果支持）
        
        使用示例：
            # 创建新表（如果表不存在）
            df.to_sql('new_table', helper.get_engine(), if_exists='fail')
            
            # 替换表（删除原表，创建新表）
            df.to_sql('users_backup', helper.get_engine(), if_exists='replace')
            
            # 追加数据
            df.to_sql('users', helper.get_engine(), if_exists='append')
            
            # 分块写入大数据集
            df.to_sql('big_table', helper.get_engine(), if_exists='append', chunksize=10000)
        """
        logger.info(f"[{self.datasource_name}] 写入数据到表: {table_name}")
        logger.info(f"数据行数: {len(df)}")
        logger.info(f"表存在时处理方式: {if_exists}")
        logger.info(f"是否写入索引: {index}")
        if chunksize:
            logger.info(f"分块写入，每块大小: {chunksize}")
        
        engine = self.get_engine()
        result = df.to_sql(
            table_name, 
            engine, 
            if_exists=if_exists, 
            index=index,
            chunksize=chunksize,
            **kwargs
        )
        
        logger.success(f"数据写入成功")
        return result
    
    def execute_query(self, query: str, params: Optional[dict] = None) -> pd.DataFrame:
        """
        执行查询并返回 DataFrame（简化版）
        
        这是 read_sql 的简化版本，更简洁
        
        Args:
            query: SQL 查询语句
            params: SQL 参数
        
        Returns:
            pd.DataFrame: 查询结果
        
        使用示例：
            # 简单查询
            df = helper.execute_query("SELECT * FROM users")
            
            # 带参数的查询
            df = helper.execute_query(
                "SELECT * FROM users WHERE status = %s",
                params={'status': 'active'}
            )
        """
        return self.read_sql(query, params=params)
    
    def get_engine(self):
        """
        获取数据库引擎
        
        Returns:
            Engine: SQLAlchemy 数据库引擎
        
        使用示例：
            engine = helper.get_engine()
            # 直接使用引擎
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM users"))
        """
        return datasource_manager.get_engine(self.datasource_name)
    
    def get_session(self):
        """
        获取数据库会话
        
        Returns:
            Session: SQLAlchemy 数据库会话
        
        使用示例：
            session = helper.get_session()
            users = session.query(User).all()
            session.close()
        """
        return datasource_manager.get_session(self.datasource_name)
    
    def get_datasource_name(self) -> str:
        """
        获取数据源名称
        
        Returns:
            str: 数据源名称
        
        使用示例：
            name = helper.get_datasource_name()
            print(f"当前使用的数据源: {name}")
        """
        return self.datasource_name
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"PandasDataHelper(datasource_name='{self.datasource_name}')"


# 便捷函数
def create_helper(datasource_name: str) -> PandasDataHelper:
    """
    创建 Pandas 数据助手（便捷函数）
    
    Args:
        datasource_name: 数据源名称
    
    Returns:
        PandasDataHelper: 数据助手实例
    
    使用示例：
        helper = create_helper('mysql')
        df = helper.read_sql("SELECT * FROM users")
    """
    return PandasDataHelper(datasource_name)