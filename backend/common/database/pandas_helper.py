"""
Pandas 鏁版嵁鍒嗘瀽鍔╂墜妯″潡

鍔熻兘璇存槑锛?1. 灏佽 pandas 鐨勬暟鎹簱鎿嶄綔鏂规硶
2. 鎻愪緵鏇寸畝娲佹槗鐢ㄧ殑鎺ュ彛
3. 鏀寔澶ф暟鎹泦鍒嗘壒璇诲彇
4. 鏀寔灏?DataFrame 鍐欏叆鏁版嵁搴?5. 鑷姩璁板綍鏌ヨ鏃ュ織锛圫QL璇彞鍜屽弬鏁帮級

浣跨敤绀轰緥锛?    # 鍩烘湰浣跨敤
    from common.database.pandas_helper import PandasDataHelper
    
    # 鍒涘缓鍔╂墜瀹炰緥
    mysql_helper = PandasDataHelper('mysql')
    oracle_helper = PandasDataHelper('oracle')
    
    # 璇诲彇鏁版嵁
    df = mysql_helper.read_sql("SELECT * FROM users WHERE status = %s", params={'status': 'active'})
    
    # 璇诲彇鏁翠釜琛?    df = mysql_helper.read_sql_table('users')
    
    # 鎵归噺璇诲彇澶ф暟鎹泦
    df = mysql_helper.batch_read("SELECT * FROM big_table", batch_size=10000)
    
    # 鍐欏叆鏁版嵁
    df.to_sql('new_table', mysql_helper.get_engine(), if_exists='replace')
"""

import pandas as pd
from typing import Optional, Union, List, Dict, Any, Iterator
from sqlalchemy import text
from loguru import logger
from .connection import datasource_manager


class PandasDataHelper:
    """
    Pandas 鏁版嵁鍒嗘瀽鍔╂墜
    
    鍔熻兘锛?    - 灏佽 pandas 鐨勬暟鎹簱鎿嶄綔鏂规硶
    - 鎻愪緵鏇寸畝娲佹槗鐢ㄧ殑鎺ュ彛
    - 鏀寔澶ф暟鎹泦鍒嗘壒璇诲彇
    - 鏀寔灏?DataFrame 鍐欏叆鏁版嵁搴?    - 鑷姩璁板綍鏌ヨ鏃ュ織
    
    浣跨敤鏂规硶锛?        # 鍒涘缓鍔╂墜瀹炰緥
        helper = PandasDataHelper('mysql')
        
        # 璇诲彇鏁版嵁
        df = helper.read_sql("SELECT * FROM users")
        
        # 鎵归噺璇诲彇
        df = helper.batch_read("SELECT * FROM big_table", batch_size=10000)
        
        # 鍐欏叆鏁版嵁
        df.to_sql('new_table', helper.get_engine(), if_exists='replace')
    """
    
    def __init__(self, datasource_name: str):
        """
        鍒濆鍖?Pandas 鏁版嵁鍔╂墜
        
        Args:
            datasource_name: 鏁版嵁婧愬悕绉帮紙濡?'mysql', 'oracle', 'postgresql'锛?                           - 蹇呴』鏄凡娉ㄥ唽鐨勬暟鎹簮
                           - 浣跨敤 datasource_manager.register_datasource() 娉ㄥ唽
        
        浣跨敤绀轰緥锛?            # 鍒涘缓 MySQL 鍔╂墜
            mysql_helper = PandasDataHelper('mysql')
            
            # 鍒涘缓 Oracle 鍔╂墜
            oracle_helper = PandasDataHelper('oracle')
            
            # 鍒涘缓 PostgreSQL 鍔╂墜
            postgresql_helper = PandasDataHelper('postgresql')
        """
        self.datasource_name = datasource_name
        
        # 楠岃瘉鏁版嵁婧愭槸鍚﹀凡娉ㄥ唽
        if not datasource_manager.has_datasource(datasource_name):
            raise ValueError(
                f"鏁版嵁婧?[{datasource_name}] 鏈敞鍐岋紝"
                f"璇峰厛浣跨敤 datasource_manager.register_datasource() 娉ㄥ唽"
            )
        
        logger.info(f"鍒涘缓 Pandas 鏁版嵁鍔╂墜: {datasource_name}")
    
    def read_sql(
        self,
        sql: str,
        params: Optional[dict] = None,
        chunksize: Optional[int] = None,
        **kwargs
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """
        璇诲彇 SQL 鏌ヨ缁撴灉锛堥€氱敤鏂规硶锛?        
        Args:
            sql: SQL 鏌ヨ璇彞锛堝彲浠ユ槸 SELECT 鏌ヨ鎴栬〃鍚嶏級
                 - 绀轰緥1锛歋ELECT * FROM users WHERE status = %s
                 - 绀轰緥2锛歋ELECT * FROM orders WHERE order_date > :start_date
            params: SQL 鍙傛暟锛堥槻姝?SQL 娉ㄥ叆锛?                    - 绀轰緥1锛歿'status': 'active'}
                    - 绀轰緥2锛歿'start_date': '2024-01-01'}
            chunksize: 鍒嗗潡璇诲彇澶у皬锛堢敤浜庡ぇ鏁版嵁闆嗭級
                      - 濡傛灉鎸囧畾锛岃繑鍥炶凯浠ｅ櫒
                      - 绀轰緥锛?0000锛堟瘡娆¤鍙?10000 鏉★級
            **kwargs: 浼犻€掔粰 pd.read_sql 鐨勫叾浠栧弬鏁?                    - index_col: 鎸囧畾绱㈠紩鍒?                    - parse_dates: 瑙ｆ瀽鏃ユ湡鍒?                    - columns: 鎸囧畾璇诲彇鐨勫垪
        
        Returns:
            pd.DataFrame 鎴?Iterator[pd.DataFrame]: 鏌ヨ缁撴灉
            - 濡傛灉涓嶆寚瀹?chunksize锛岃繑鍥?DataFrame
            - 濡傛灉鎸囧畾 chunksize锛岃繑鍥炶凯浠ｅ櫒
        
        浣跨敤绀轰緥锛?            # 鍩烘湰鏌ヨ
            df = helper.read_sql("SELECT * FROM users")
            
            # 甯﹀弬鏁扮殑鏌ヨ锛堟帹鑽愶紝闃叉 SQL 娉ㄥ叆锛?            df = helper.read_sql(
                "SELECT * FROM users WHERE status = %s AND age > %s",
                params={'status': 'active', 'age': 18}
            )
            
            # 浣跨敤鍛藉悕鍙傛暟
            df = helper.read_sql(
                "SELECT * FROM orders WHERE order_date > :start_date AND order_date < :end_date",
                params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
            )
            
            # 瑙ｆ瀽鏃ユ湡鍒?            df = helper.read_sql(
                "SELECT * FROM orders",
                parse_dates=['order_date', 'created_at']
            )
            
            # 鍒嗗潡璇诲彇澶ф暟鎹泦锛堣繑鍥炶凯浠ｅ櫒锛?            for chunk in helper.read_sql("SELECT * FROM big_table", chunksize=10000):
                process_chunk(chunk)
        """
        logger.info(f"[{self.datasource_name}] 鎵ц SQL 鏌ヨ")
        logger.info(f"SQL 璇彞: {sql}")
        if params:
            logger.info(f"鏌ヨ鍙傛暟: {params}")
        if chunksize:
            logger.info(f"鍒嗗潡璇诲彇锛屾瘡鍧楀ぇ灏? {chunksize}")
        
        result = datasource_manager.read_sql(
            sql, 
            self.datasource_name, 
            params=params, 
            chunksize=chunksize,
            **kwargs
        )
        
        if not chunksize:
            logger.success(f"鏌ヨ鎴愬姛锛岃繑鍥?{len(result)} 鏉¤褰?)
        else:
            logger.success(f"鏌ヨ鎴愬姛锛岃繑鍥炲垎鍧楄凯浠ｅ櫒")
        
        return result
    
    def read_sql_query(
        self,
        query: str,
        params: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        璇诲彇 SQL 鏌ヨ缁撴灉锛堜粎鏌ヨ璇彞锛?        
        涓?read_sql 鐨勫尯鍒細
        - read_sql_query: 鍙兘鎵ц SELECT 鏌ヨ
        - read_sql: 鍙互鎵ц SELECT 鏌ヨ鎴栬鍙栬〃鍚?        
        Args:
            query: SQL 鏌ヨ璇彞锛堝繀椤绘槸 SELECT 璇彞锛?                   - 绀轰緥锛歋ELECT id, username, email FROM users WHERE status = %s
            params: SQL 鍙傛暟锛堥槻姝?SQL 娉ㄥ叆锛?            **kwargs: 浼犻€掔粰 pd.read_sql_query 鐨勫叾浠栧弬鏁?        
        Returns:
            pd.DataFrame: 鏌ヨ缁撴灉
        
        浣跨敤绀轰緥锛?            # 绠€鍗曟煡璇?            df = helper.read_sql_query("SELECT id, username FROM users")
            
            # 澶嶆潅鏌ヨ锛圝OIN锛?            df = helper.read_sql_query(
                \"\"\"
                SELECT u.id, u.username, o.order_id, o.amount
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                WHERE u.status = %s
                \"\"\",
                params={'status': 'active'}
            )
            
            # 鑱氬悎鏌ヨ
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
        logger.info(f"[{self.datasource_name}] 鎵ц SQL 鏌ヨ锛堜粎鏌ヨ锛?)
        logger.info(f"SQL 璇彞: {query}")
        if params:
            logger.info(f"鏌ヨ鍙傛暟: {params}")
        
        result = datasource_manager.read_sql_query(
            query, 
            self.datasource_name, 
            params=params,
            **kwargs
        )
        
        logger.success(f"鏌ヨ鎴愬姛锛岃繑鍥?{len(result)} 鏉¤褰?)
        return result
    
    def read_sql_table(
        self,
        table_name: str,
        columns: Optional[List[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        璇诲彇鏁翠釜琛?        
        Args:
            table_name: 琛ㄥ悕
                       - 绀轰緥锛?users', 'orders', 'products'
            columns: 鎸囧畾璇诲彇鐨勫垪锛堝彲閫夛級
                     - 绀轰緥锛歔'id', 'username', 'email']
                     - 濡傛灉涓嶆寚瀹氾紝鍒欒鍙栨墍鏈夊垪
            **kwargs: 浼犻€掔粰 pd.read_sql_table 鐨勫叾浠栧弬鏁?                    - parse_dates: 瑙ｆ瀽鏃ユ湡鍒?        
        Returns:
            pd.DataFrame: 琛ㄦ暟鎹?        
        浣跨敤绀轰緥锛?            # 璇诲彇鏁翠釜琛?            df = helper.read_sql_table('users')
            
            # 鍙鍙栨寚瀹氬垪
            df = helper.read_sql_table(
                'users',
                columns=['id', 'username', 'email']
            )
            
            # 瑙ｆ瀽鏃ユ湡鍒?            df = helper.read_sql_table(
                'orders',
                parse_dates=['order_date', 'created_at']
            )
        """
        logger.info(f"[{self.datasource_name}] 璇诲彇琛? {table_name}")
        if columns:
            logger.info(f"鎸囧畾鍒? {columns}")
        
        result = datasource_manager.read_sql_table(
            table_name, 
            self.datasource_name, 
            columns=columns,
            **kwargs
        )
        
        logger.success(f"璇诲彇鎴愬姛锛岃繑鍥?{len(result)} 鏉¤褰?)
        return result
    
    def batch_read(
        self,
        query: str,
        batch_size: int = 10000,
        params: Optional[dict] = None
    ) -> pd.DataFrame:
        """
        鎵归噺璇诲彇澶ф暟鎹泦锛堣嚜鍔ㄥ悎骞讹級
        
        閫傜敤浜庢暟鎹噺寰堝ぇ鐨勬儏鍐碉紝閬垮厤鍐呭瓨婧㈠嚭
        
        Args:
            query: SQL 鏌ヨ璇彞
                   - 绀轰緥锛歋ELECT * FROM big_table WHERE created_at > '2024-01-01'
            batch_size: 鎵规澶у皬锛堥粯璁?10000锛?                      - 鏍规嵁鏁版嵁閲忓拰鍐呭瓨鎯呭喌璋冩暣
                      - 寤鸿锛?0000-100000
            params: SQL 鍙傛暟锛堥槻姝?SQL 娉ㄥ叆锛?        
        Returns:
            pd.DataFrame: 鍚堝苟鍚庣殑瀹屾暣鏁版嵁
        
        浣跨敤绀轰緥锛?            # 璇诲彇澶ф暟鎹泦锛?00涓囨潯璁板綍锛?            df = helper.batch_read(
                "SELECT * FROM big_table WHERE created_at > %s",
                batch_size=10000,
                params={'created_at': '2024-01-01'}
            )
            
            # 璋冩暣鎵规澶у皬锛堟暟鎹噺鏇村ぇ鏃讹級
            df = helper.batch_read(
                "SELECT * FROM huge_table",
                batch_size=50000
            )
        """
        logger.info(f"[{self.datasource_name}] 鎵归噺璇诲彇澶ф暟鎹泦")
        logger.info(f"SQL 璇彞: {query}")
        logger.info(f"鎵规澶у皬: {batch_size}")
        if params:
            logger.info(f"鏌ヨ鍙傛暟: {params}")
        
        chunks = []
        total_rows = 0
        
        for i, chunk in enumerate(self.read_sql(query, params=params, chunksize=batch_size)):
            chunks.append(chunk)
            total_rows += len(chunk)
            logger.debug(f"宸茶鍙栨壒娆?{i+1}, 褰撳墠绱: {total_rows} 鏉¤褰?)
        
        # 鍚堝苟鎵€鏈夋壒娆?        if chunks:
            result = pd.concat(chunks, ignore_index=True)
            logger.success(f"鎵归噺璇诲彇瀹屾垚锛屽叡 {len(result)} 鏉¤褰?)
            return result
        else:
            logger.warning("鏈鍙栧埌浠讳綍鏁版嵁")
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
        灏?DataFrame 鍐欏叆鏁版嵁搴?        
        Args:
            df: 瑕佸啓鍏ョ殑 DataFrame
            table_name: 鐩爣琛ㄥ悕
                      - 绀轰緥锛?new_table', 'backup_users'
            if_exists: 琛ㄥ瓨鍦ㄦ椂鐨勫鐞嗘柟寮?                      - 'fail': 鎶涘嚭寮傚父锛堥粯璁わ級
                      - 'replace': 鍒犻櫎鍘熻〃锛屽垱寤烘柊琛?                      - 'append': 杩藉姞鏁版嵁鍒板師琛?            index: 鏄惁鍐欏叆绱㈠紩鍒楋紙榛樿 False锛?            chunksize: 鍒嗗潡鍐欏叆澶у皬锛堢敤浜庡ぇ鏁版嵁闆嗭級
                      - 绀轰緥锛?0000锛堟瘡娆″啓鍏?10000 鏉★級
            **kwargs: 鍏朵粬鍙傛暟锛堝 dtype, method锛?        
        Returns:
            Optional[int]: 鍐欏叆鐨勮鏁帮紙濡傛灉鏀寔锛?        
        浣跨敤绀轰緥锛?            # 鍒涘缓鏂拌〃锛堝鏋滆〃涓嶅瓨鍦級
            df.to_sql('new_table', helper.get_engine(), if_exists='fail')
            
            # 鏇挎崲琛紙鍒犻櫎鍘熻〃锛屽垱寤烘柊琛級
            df.to_sql('users_backup', helper.get_engine(), if_exists='replace')
            
            # 杩藉姞鏁版嵁
            df.to_sql('users', helper.get_engine(), if_exists='append')
            
            # 鍒嗗潡鍐欏叆澶ф暟鎹泦
            df.to_sql('big_table', helper.get_engine(), if_exists='append', chunksize=10000)
        """
        logger.info(f"[{self.datasource_name}] 鍐欏叆鏁版嵁鍒拌〃: {table_name}")
        logger.info(f"鏁版嵁琛屾暟: {len(df)}")
        logger.info(f"琛ㄥ瓨鍦ㄦ椂澶勭悊鏂瑰紡: {if_exists}")
        logger.info(f"鏄惁鍐欏叆绱㈠紩: {index}")
        if chunksize:
            logger.info(f"鍒嗗潡鍐欏叆锛屾瘡鍧楀ぇ灏? {chunksize}")
        
        engine = self.get_engine()
        result = df.to_sql(
            table_name, 
            engine, 
            if_exists=if_exists, 
            index=index,
            chunksize=chunksize,
            **kwargs
        )
        
        logger.success(f"鏁版嵁鍐欏叆鎴愬姛")
        return result
    
    def execute_query(self, query: str, params: Optional[dict] = None) -> pd.DataFrame:
        """
        鎵ц鏌ヨ骞惰繑鍥?DataFrame锛堢畝鍖栫増锛?        
        杩欐槸 read_sql 鐨勭畝鍖栫増鏈紝鏇寸畝娲?        
        Args:
            query: SQL 鏌ヨ璇彞
            params: SQL 鍙傛暟
        
        Returns:
            pd.DataFrame: 鏌ヨ缁撴灉
        
        浣跨敤绀轰緥锛?            # 绠€鍗曟煡璇?            df = helper.execute_query("SELECT * FROM users")
            
            # 甯﹀弬鏁扮殑鏌ヨ
            df = helper.execute_query(
                "SELECT * FROM users WHERE status = %s",
                params={'status': 'active'}
            )
        """
        return self.read_sql(query, params=params)
    
    def get_engine(self):
        """
        鑾峰彇鏁版嵁搴撳紩鎿?        
        Returns:
            Engine: SQLAlchemy 鏁版嵁搴撳紩鎿?        
        浣跨敤绀轰緥锛?            engine = helper.get_engine()
            # 鐩存帴浣跨敤寮曟搸
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM users"))
        """
        return datasource_manager.get_engine(self.datasource_name)
    
    def get_session(self):
        """
        鑾峰彇鏁版嵁搴撲細璇?        
        Returns:
            Session: SQLAlchemy 鏁版嵁搴撲細璇?        
        浣跨敤绀轰緥锛?            session = helper.get_session()
            users = session.query(User).all()
            session.close()
        """
        return datasource_manager.get_session(self.datasource_name)
    
    def get_datasource_name(self) -> str:
        """
        鑾峰彇鏁版嵁婧愬悕绉?        
        Returns:
            str: 鏁版嵁婧愬悕绉?        
        浣跨敤绀轰緥锛?            name = helper.get_datasource_name()
            print(f"褰撳墠浣跨敤鐨勬暟鎹簮: {name}")
        """
        return self.datasource_name
    
    def __repr__(self) -> str:
        """瀛楃涓茶〃绀?""
        return f"PandasDataHelper(datasource_name='{self.datasource_name}')"


# 渚挎嵎鍑芥暟
def create_helper(datasource_name: str) -> PandasDataHelper:
    """
    鍒涘缓 Pandas 鏁版嵁鍔╂墜锛堜究鎹峰嚱鏁帮級
    
    Args:
        datasource_name: 鏁版嵁婧愬悕绉?    
    Returns:
        PandasDataHelper: 鏁版嵁鍔╂墜瀹炰緥
    
    浣跨敤绀轰緥锛?        helper = create_helper('mysql')
        df = helper.read_sql("SELECT * FROM users")
    """
    return PandasDataHelper(datasource_name)
