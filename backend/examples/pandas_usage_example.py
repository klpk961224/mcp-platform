"""
Pandas 数据分析使用示例

本文件展示了如何使用 PandasDataHelper 进行数据分析，
包括：
1. 基本查询
2. 参数化查询
3. 跨数据源查询
4. 数据分析
5. 数据写入
"""

import pandas as pd
from typing import Dict, Any
from common.database import datasource_manager, PandasDataHelper
from loguru import logger


class DataAnalysisService:
    """
    数据分析服务
    
    功能：
    - 从多个数据源查询数据
    - 使用 pandas 进行数据分析
    - 生成分析报告
    """
    
    def __init__(self):
        """初始化服务，为每个数据源创建助手"""
        self.mysql = PandasDataHelper('mysql')
        self.oracle = PandasDataHelper('oracle')
        self.postgresql = PandasDataHelper('postgresql')
        
        logger.info("数据分析服务初始化完成")
    
    def example_1_basic_query(self):
        """
        示例1：基本查询
        
        功能：
        - 从 MySQL 读取用户数据
        - 从 Oracle 读取订单数据
        - 从 PostgreSQL 读取产品数据
        """
        logger.info("=" * 50)
        logger.info("示例1：基本查询")
        logger.info("=" * 50)
        
        # 从 MySQL 读取用户数据
        users_df = self.mysql.read_sql("SELECT * FROM users LIMIT 10")
        logger.info(f"MySQL 用户数据: {len(users_df)} 条")
        print(users_df)
        
        # 从 Oracle 读取订单数据
        orders_df = self.oracle.read_sql("SELECT * FROM orders LIMIT 10")
        logger.info(f"Oracle 订单数据: {len(orders_df)} 条")
        print(orders_df)
        
        # 从 PostgreSQL 读取产品数据
        products_df = self.postgresql.read_sql("SELECT * FROM products LIMIT 10")
        logger.info(f"PostgreSQL 产品数据: {len(products_df)} 条")
        print(products_df)
    
    def example_2_parameterized_query(self):
        """
        示例2：参数化查询（防止 SQL 注入）
        
        功能：
        - 使用参数化查询
        - 防止 SQL 注入
        """
        logger.info("=" * 50)
        logger.info("示例2：参数化查询")
        logger.info("=" * 50)
        
        # ✅ 正确：使用参数化查询
        users_df = self.mysql.read_sql(
            "SELECT * FROM users WHERE status = %s AND age > %s",
            params={'status': 'active', 'age': 18}
        )
        logger.info(f"查询结果: {len(users_df)} 条")
        print(users_df)
        
        # ✅ 正确：使用命名参数（Oracle）
        orders_df = self.oracle.read_sql(
            """
            SELECT * FROM orders 
            WHERE order_date > TO_DATE(:start_date, 'YYYY-MM-DD') 
              AND order_date < TO_DATE(:end_date, 'YYYY-MM-DD')
            """,
            params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
        )
        logger.info(f"查询结果: {len(orders_df)} 条")
        print(orders_df)
        
        # ❌ 错误：不要使用字符串拼接（SQL 注入风险）
        # users_df = self.mysql.read_sql(f"SELECT * FROM users WHERE status = '{user_input}'")
    
    def example_3_cross_datasource_analysis(self):
        """
        示例3：跨数据源分析
        
        功能：
        - 从多个数据源查询数据
        - 在应用层进行数据整合
        - 使用 pandas 进行分析
        """
        logger.info("=" * 50)
        logger.info("示例3：跨数据源分析")
        logger.info("=" * 50)
        
        # 1. 从 MySQL 获取用户数据
        users_df = self.mysql.read_sql(
            """
            SELECT 
                id, username, email, created_at
            FROM users
            WHERE status = %s
            """,
            params={'status': 'active'}
        )
        logger.info(f"MySQL 用户数据: {len(users_df)} 条")
        
        # 2. 从 Oracle 获取订单数据
        orders_df = self.oracle.read_sql(
            """
            SELECT 
                order_id, user_id, amount, order_date
            FROM orders
            WHERE order_date > TO_DATE(:start_date, 'YYYY-MM-DD')
            """,
            params={'start_date': '2024-01-01'}
        )
        logger.info(f"Oracle 订单数据: {len(orders_df)} 条")
        
        # 3. 从 PostgreSQL 获取产品数据
        products_df = self.postgresql.read_sql_table(
            'products',
            columns=['product_id', 'name', 'price', 'category']
        )
        logger.info(f"PostgreSQL 产品数据: {len(products_df)} 条")
        
        # 4. 数据分析
        report = self._analyze_data(users_df, orders_df, products_df)
        
        logger.info("分析报告生成完成")
        return report
    
    def _analyze_data(
        self,
        users_df: pd.DataFrame,
        orders_df: pd.DataFrame,
        products_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        数据分析（私有方法）
        
        Args:
            users_df: 用户数据
            orders_df: 订单数据
            products_df: 产品数据
        
        Returns:
            Dict[str, Any]: 分析报告
        """
        report = {}
        
        # 用户统计
        report['user_stats'] = {
            'total_users': len(users_df),
            'new_users_per_day': users_df.groupby(users_df['created_at'].dt.date).size().to_dict(),
        }
        
        # 订单统计
        report['order_stats'] = {
            'total_orders': len(orders_df),
            'total_revenue': float(orders_df['amount'].sum()),
            'avg_order_value': float(orders_df['amount'].mean()),
            'revenue_by_day': orders_df.groupby(orders_df['order_date'].dt.date)['amount'].sum().to_dict(),
        }
        
        # 产品统计
        report['product_stats'] = {
            'total_products': len(products_df),
            'products_by_category': products_df.groupby('category').size().to_dict(),
            'avg_price': float(products_df['price'].mean()),
        }
        
        # 跨数据源分析
        merged_df = pd.merge(
            orders_df,
            users_df,
            left_on='user_id',
            right_on='id',
            how='left'
        )
        
        report['cross_analysis'] = {
            'users_with_orders': int(merged_df['user_id'].nunique()),
            'orders_per_user': float(merged_df.groupby('user_id').size().mean()),
            'top_users_by_revenue': merged_df.groupby('username')['amount'].sum().nlargest(10).to_dict(),
        }
        
        return report
    
    def example_4_batch_read(self):
        """
        示例4：批量读取大数据集
        
        功能：
        - 使用 batch_read 读取大数据集
        - 避免内存溢出
        """
        logger.info("=" * 50)
        logger.info("示例4：批量读取大数据集")
        logger.info("=" * 50)
        
        # 批量读取大数据集
        big_df = self.mysql.batch_read(
            "SELECT * FROM big_table WHERE created_at > %s",
            batch_size=10000,
            params={'created_at': '2024-01-01'}
        )
        
        logger.info(f"批量读取完成，共 {len(big_df)} 条记录")
        print(big_df.head())
    
    def example_5_write_data(self):
        """
        示例5：写入数据
        
        功能：
        - 将 DataFrame 写入数据库
        - 支持创建新表、追加数据、替换表
        """
        logger.info("=" * 50)
        logger.info("示例5：写入数据")
        logger.info("=" * 50)
        
        # 创建测试数据
        test_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
        })
        
        logger.info("测试数据:")
        print(test_df)
        
        # 方式1：创建新表
        self.mysql.to_sql(
            test_df,
            'test_table',
            if_exists='fail'  # 表存在时失败
        )
        logger.info("创建新表成功")
        
        # 方式2：追加数据
        new_df = pd.DataFrame({
            'id': [4, 5],
            'name': ['David', 'Eve'],
            'age': [40, 45],
        })
        self.mysql.to_sql(
            new_df,
            'test_table',
            if_exists='append'  # 追加数据
        )
        logger.info("追加数据成功")
        
        # 方式3：替换表
        self.mysql.to_sql(
            test_df,
            'test_table',
            if_exists='replace'  # 替换表
        )
        logger.info("替换表成功")
    
    def example_6_complex_analysis(self):
        """
        示例6：复杂分析
        
        功能：
        - 复杂的 SQL 查询（JOIN、聚合）
        - 多维度数据分析
        """
        logger.info("=" * 50)
        logger.info("示例6：复杂分析")
        logger.info("=" * 50)
        
        # 复杂查询：用户订单分析
        user_order_df = self.mysql.read_sql_query(
            """
            SELECT 
                u.id,
                u.username,
                COUNT(o.order_id) as order_count,
                SUM(o.amount) as total_amount,
                AVG(o.amount) as avg_amount,
                MAX(o.amount) as max_amount,
                MIN(o.amount) as min_amount
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.status = %s
            GROUP BY u.id, u.username
            ORDER BY total_amount DESC
            LIMIT 10
            """,
            params={'status': 'active'}
        )
        
        logger.info(f"用户订单分析结果: {len(user_order_df)} 条")
        print(user_order_df)
        
        # 复杂查询：产品类别销售分析
        category_sales_df = self.oracle.read_sql_query(
            """
            SELECT 
                p.category,
                COUNT(DISTINCT o.order_id) as order_count,
                SUM(oi.quantity) as total_quantity,
                SUM(oi.quantity * oi.price) as total_revenue
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_date > TO_DATE(:start_date, 'YYYY-MM-DD')
            GROUP BY p.category
            ORDER BY total_revenue DESC
            """,
            params={'start_date': '2024-01-01'}
        )
        
        logger.info(f"产品类别销售分析: {len(category_sales_df)} 条")
        print(category_sales_df)
    
    def example_7_read_table(self):
        """
        示例7：读取整个表
        
        功能：
        - 使用 read_sql_table 读取整个表
        - 指定读取的列
        - 解析日期列
        """
        logger.info("=" * 50)
        logger.info("示例7：读取整个表")
        logger.info("=" * 50)
        
        # 读取整个表
        users_df = self.mysql.read_sql_table('users')
        logger.info(f"读取 users 表: {len(users_df)} 条")
        
        # 只读取指定列
        users_simple_df = self.mysql.read_sql_table(
            'users',
            columns=['id', 'username', 'email']
        )
        logger.info(f"读取指定列: {len(users_simple_df)} 条")
        print(users_simple_df)
        
        # 解析日期列
        orders_df = self.oracle.read_sql_table(
            'orders',
            parse_dates=['order_date', 'created_at']
        )
        logger.info(f"读取 orders 表（解析日期）: {len(orders_df)} 条")
        print(orders_df.dtypes)


# 主程序
if __name__ == '__main__':
    # 配置日志
    logger.add(
        "logs/pandas_usage.log",
        rotation="100 MB",
        retention="30 days",
        level="INFO"
    )
    
    logger.info("开始 Pandas 数据分析示例")
    
    # 初始化数据源（示例）
    # 注意：实际使用时需要先注册数据源
    # datasource_manager.register_datasource(...)
    
    # 创建服务实例
    service = DataAnalysisService()
    
    # 运行示例
    try:
        # 示例1：基本查询
        service.example_1_basic_query()
        
        # 示例2：参数化查询
        service.example_2_parameterized_query()
        
        # 示例3：跨数据源分析
        report = service.example_3_cross_datasource_analysis()
        print("\n分析报告:")
        print(report)
        
        # 示例4：批量读取大数据集
        # service.example_4_batch_read()
        
        # 示例5：写入数据
        # service.example_5_write_data()
        
        # 示例6：复杂分析
        # service.example_6_complex_analysis()
        
        # 示例7：读取整个表
        # service.example_7_read_table()
        
    except Exception as e:
        logger.error(f"执行示例时出错: {e}")
        raise
    
    logger.info("Pandas 数据分析示例完成")
"""