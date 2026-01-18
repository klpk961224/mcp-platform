# -*- coding: utf-8 -*-
"""
鏁版嵁婧愭湇鍔?
鍔熻兘璇存槑锛?1. 鏁版嵁婧愮鐞?2. 鏁版嵁婧愯繛鎺?3. 鏁版嵁婧愬仴搴锋鏌?
浣跨敤绀轰緥锛?    from app.services.datasource_service import DataSourceService
    
    datasource_service = DataSourceService(db)
    datasource = datasource_service.create_datasource(name="涓绘暟鎹簱", type="mysql")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.datasource import DataSource
from app.repositories.datasource_repository import DataSourceRepository
from common.database.connection import datasource_manager


class DataSourceService:
    """
    鏁版嵁婧愭湇鍔?    
    鍔熻兘锛?    - 鏁版嵁婧愮鐞?    - 鏁版嵁婧愯繛鎺?    - 鏁版嵁婧愬仴搴锋鏌?    
    浣跨敤鏂规硶锛?        datasource_service = DataSourceService(db)
        datasource = datasource_service.create_datasource(name="涓绘暟鎹簱", type="mysql")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨暟鎹簮鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.datasource_repo = DataSourceRepository(db)
    
    def create_datasource(self, datasource_data: Dict[str, Any]) -> DataSource:
        """
        鍒涘缓鏁版嵁婧?        
        Args:
            datasource_data: 鏁版嵁婧愭暟鎹?        
        Returns:
            DataSource: 鍒涘缓鐨勬暟鎹簮瀵硅薄
        
        Raises:
            ValueError: 鏁版嵁婧愬悕绉板凡瀛樺湪
        """
        logger.info(f"鍒涘缓鏁版嵁婧? name={datasource_data.get('name')}, type={datasource_data.get('type')}")
        
        # 妫€鏌ユ暟鎹簮鍚嶇О鏄惁宸插瓨鍦?        if self.datasource_repo.exists_by_name(datasource_data.get("name"), datasource_data.get("tenant_id")):
            raise ValueError("鏁版嵁婧愬悕绉板凡瀛樺湪")
        
        # 鍒涘缓鏁版嵁婧?        datasource = DataSource(**datasource_data)
        datasource = self.datasource_repo.create(datasource)
        
        # 娉ㄥ唽鍒版暟鎹簮绠＄悊鍣?        self._register_datasource(datasource)
        
        return datasource
    
    def get_datasource(self, datasource_id: str) -> Optional[DataSource]:
        """
        鑾峰彇鏁版嵁婧?        
        Args:
            datasource_id: 鏁版嵁婧怚D
        
        Returns:
            Optional[DataSource]: 鏁版嵁婧愬璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.datasource_repo.get_by_id(datasource_id)
    
    def get_default_datasource(self, tenant_id: str) -> Optional[DataSource]:
        """
        鑾峰彇榛樿鏁版嵁婧?        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            Optional[DataSource]: 鏁版嵁婧愬璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.datasource_repo.get_default_datasource(tenant_id)
    
    def update_datasource(self, datasource_id: str, datasource_data: Dict[str, Any]) -> Optional[DataSource]:
        """
        鏇存柊鏁版嵁婧?        
        Args:
            datasource_id: 鏁版嵁婧怚D
            datasource_data: 鏁版嵁婧愭暟鎹?        
        Returns:
            Optional[DataSource]: 鏇存柊鍚庣殑鏁版嵁婧愬璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        logger.info(f"鏇存柊鏁版嵁婧? datasource_id={datasource_id}")
        
        datasource = self.datasource_repo.get_by_id(datasource_id)
        if not datasource:
            return None
        
        # 鏇存柊鏁版嵁婧?        for key, value in datasource_data.items():
            if hasattr(datasource, key):
                setattr(datasource, key, value)
        
        datasource = self.datasource_repo.update(datasource)
        
        # 閲嶆柊娉ㄥ唽鍒版暟鎹簮绠＄悊鍣?        self._register_datasource(datasource)
        
        return datasource
    
    def delete_datasource(self, datasource_id: str) -> bool:
        """
        鍒犻櫎鏁版嵁婧?        
        Args:
            datasource_id: 鏁版嵁婧怚D
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎鏁版嵁婧? datasource_id={datasource_id}")
        return self.datasource_repo.delete(datasource_id)
    
    def list_datasources(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                         page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        鑾峰彇鏁版嵁婧愬垪琛?        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[DataSource]: 鏁版嵁婧愬垪琛?        """
        if keyword:
            return self.datasource_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.datasource_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.datasource_repo.get_all(page, page_size)
    
    def test_connection(self, datasource_id: str) -> Dict[str, Any]:
        """
        娴嬭瘯鏁版嵁婧愯繛鎺?        
        Args:
            datasource_id: 鏁版嵁婧怚D
        
        Returns:
            Dict[str, Any]: 杩炴帴娴嬭瘯缁撴灉
        """
        logger.info(f"娴嬭瘯鏁版嵁婧愯繛鎺? datasource_id={datasource_id}")
        
        datasource = self.datasource_repo.get_by_id(datasource_id)
        if not datasource:
            return {"success": False, "message": "鏁版嵁婧愪笉瀛樺湪"}
        
        try:
            # 娴嬭瘯杩炴帴
            session = datasource_manager.get_session(datasource.id)
            session.execute("SELECT 1")
            session.close()
            
            # 鏇存柊鍋ュ悍鐘舵€?            datasource.update_health_status(is_healthy=True)
            self.datasource_repo.update(datasource)
            
            return {"success": True, "message": "杩炴帴鎴愬姛"}
            
        except Exception as e:
            logger.error(f"鏁版嵁婧愯繛鎺ユ祴璇曞け璐? {e}")
            
            # 鏇存柊鍋ュ悍鐘舵€?            datasource.update_health_status(is_healthy=False)
            self.datasource_repo.update(datasource)
            
            return {"success": False, "message": f"杩炴帴澶辫触: {str(e)}"}
    
    def _register_datasource(self, datasource: DataSource):
        """
        娉ㄥ唽鏁版嵁婧愬埌鏁版嵁婧愮鐞嗗櫒
        
        Args:
            datasource: 鏁版嵁婧愬璞?        """
        try:
            datasource_manager.register_datasource(
                name=datasource.id,
                db_type=datasource.type,
                host=datasource.host,
                port=datasource.port,
                username=datasource.username,
                password=datasource.password,
                database=datasource.database,
                pool_size=datasource.pool_size,
                max_overflow=datasource.max_overflow,
                echo=False
            )
            logger.info(f"鏁版嵁婧愭敞鍐屾垚鍔? {datasource.id}")
        except Exception as e:
            logger.error(f"鏁版嵁婧愭敞鍐屽け璐? {e}")
            raise
    
    def count_datasources(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻鏁版嵁婧愭暟閲?        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 鏁版嵁婧愭暟閲?        """
        if tenant_id:
            return self.datasource_repo.count_by_tenant(tenant_id)
        else:
            return self.datasource_repo.count_all()
