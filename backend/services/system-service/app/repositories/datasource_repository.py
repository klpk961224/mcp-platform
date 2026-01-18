# -*- coding: utf-8 -*-
"""
鏁版嵁婧愭暟鎹闂眰

鍔熻兘璇存槑锛?1. 鏁版嵁婧怌RUD鎿嶄綔
2. 鏁版嵁婧愭煡璇㈡搷浣?3. 鏁版嵁婧愮粺璁℃搷浣?
浣跨敤绀轰緥锛?    from app.repositories.datasource_repository import DataSourceRepository
    
    datasource_repo = DataSourceRepository(db)
    datasource = datasource_repo.get_default_datasource()
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from app.models.datasource import DataSource


class DataSourceRepository:
    """
    鏁版嵁婧愭暟鎹闂眰
    
    鍔熻兘锛?    - 鏁版嵁婧怌RUD鎿嶄綔
    - 鏁版嵁婧愭煡璇㈡搷浣?    - 鏁版嵁婧愮粺璁℃搷浣?    
    浣跨敤鏂规硶锛?        datasource_repo = DataSourceRepository(db)
        datasource = datasource_repo.get_default_datasource()
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨暟鎹簮鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, datasource: DataSource) -> DataSource:
        """
        创建鏁版嵁婧?        
        Args:
            datasource: 鏁版嵁婧愬璞?        
        Returns:
            DataSource: 创建鐨勬暟鎹簮瀵硅薄
        """
        logger.info(f"创建鏁版嵁婧? name={datasource.name}, type={datasource.type}")
        self.db.add(datasource)
        self.db.commit()
        self.db.refresh(datasource)
        return datasource
    
    def get_by_id(self, datasource_id: str) -> Optional[DataSource]:
        """
        根据ID鑾峰彇鏁版嵁婧?        
        Args:
            datasource_id: 鏁版嵁婧怚D
        
        Returns:
            Optional[DataSource]: 鏁版嵁婧愬璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(DataSource).filter(DataSource.id == datasource_id).first()
    
    def get_by_name(self, name: str, tenant_id: str) -> Optional[DataSource]:
        """
        根据名称鑾峰彇鏁版嵁婧?        
        Args:
            name: 鏁版嵁婧愬悕绉?            tenant_id: 租户ID
        
        Returns:
            Optional[DataSource]: 鏁版嵁婧愬璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(DataSource).filter(
            and_(
                DataSource.name == name,
                DataSource.tenant_id == tenant_id
            )
        ).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        根据租户ID鑾峰彇鏁版嵁婧愬垪琛?        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DataSource]: 鏁版嵁婧愬垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).filter(DataSource.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_type(self, data_type: str, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        根据类型鑾峰彇鏁版嵁婧愬垪琛?        
        Args:
            data_type: 鏁版嵁婧愮被鍨?            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DataSource]: 鏁版嵁婧愬垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).filter(DataSource.type == data_type).offset(offset).limit(page_size).all()
    
    def get_default_datasource(self, tenant_id: str) -> Optional[DataSource]:
        """
        鑾峰彇绉熸埛鐨勯粯璁ゆ暟鎹簮
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Optional[DataSource]: 鏁版嵁婧愬璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(DataSource).filter(
            and_(
                DataSource.tenant_id == tenant_id,
                DataSource.is_default == True
            )
        ).first()
    
    def get_active_datasources(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        鑾峰彇绉熸埛鐨勬椿璺冩暟鎹簮鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DataSource]: 鏁版嵁婧愬垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).filter(
            and_(
                DataSource.tenant_id == tenant_id,
                DataSource.status == "active"
            )
        ).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        鎼滅储鏁版嵁婧?        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DataSource]: 鏁版嵁婧愬垪琛?        """
        offset = (page - 1) * page_size
        query = self.db.query(DataSource).filter(
            or_(
                DataSource.name.like(f"%{keyword}%"),
                DataSource.host.like(f"%{keyword}%"),
                DataSource.database.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(DataSource.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        鑾峰彇鎵€鏈夋暟鎹簮
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DataSource]: 鏁版嵁婧愬垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).offset(offset).limit(page_size).all()
    
    def update(self, datasource: DataSource) -> DataSource:
        """
        更新鏁版嵁婧?        
        Args:
            datasource: 鏁版嵁婧愬璞?        
        Returns:
            DataSource: 更新鍚庣殑鏁版嵁婧愬璞?        """
        logger.info(f"更新鏁版嵁婧? datasource_id={datasource.id}")
        self.db.commit()
        self.db.refresh(datasource)
        return datasource
    
    def delete(self, datasource_id: str) -> bool:
        """
        删除鏁版嵁婧?        
        Args:
            datasource_id: 鏁版嵁婧怚D
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除鏁版嵁婧? datasource_id={datasource_id}")
        datasource = self.get_by_id(datasource_id)
        if not datasource:
            return False
        
        # 妫€鏌ユ槸鍚︿负默认鏁版嵁婧?        if datasource.is_default:
            raise ValueError("鏃犳硶删除默认鏁版嵁婧?)
        
        self.db.delete(datasource)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛鏁版嵁婧愭暟閲?        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 鏁版嵁婧愭暟閲?        """
        return self.db.query(DataSource).filter(DataSource.tenant_id == tenant_id).count()
    
    def count_by_type(self, data_type: str) -> int:
        """
        缁熻鏁版嵁婧愮被鍨嬬殑数量
        
        Args:
            data_type: 鏁版嵁婧愮被鍨?        
        Returns:
            int: 鏁版嵁婧愭暟閲?        """
        return self.db.query(DataSource).filter(DataSource.type == data_type).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夋暟鎹簮数量
        
        Returns:
            int: 鏁版嵁婧愭暟閲?        """
        return self.db.query(DataSource).count()
    
    def exists_by_name(self, name: str, tenant_id: str) -> bool:
        """
        妫€鏌ユ暟鎹簮名称鏄惁瀛樺湪
        
        Args:
            name: 鏁版嵁婧愬悕绉?            tenant_id: 租户ID
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(DataSource).filter(
            and_(
                DataSource.name == name,
                DataSource.tenant_id == tenant_id
            )
        ).first() is not None
