# -*- coding: utf-8 -*-
"""
数据源数据访问层

功能说明：
1. 数据源CRUD操作
2. 数据源查询操作
3. 数据源统计操作

使用示例：
    from app.repositories.datasource_repository import DataSourceRepository
    
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
    数据源数据访问层
    
    功能：
    - 数据源CRUD操作
    - 数据源查询操作
    - 数据源统计操作
    
    使用方法：
        datasource_repo = DataSourceRepository(db)
        datasource = datasource_repo.get_default_datasource()
    """
    
    def __init__(self, db: Session):
        """
        初始化数据源数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, datasource: DataSource) -> DataSource:
        """
        创建数据源
        
        Args:
            datasource: 数据源对象
        
        Returns:
            DataSource: 创建的数据源对象
        """
        logger.info(f"创建数据源: name={datasource.name}, type={datasource.type}")
        self.db.add(datasource)
        self.db.commit()
        self.db.refresh(datasource)
        return datasource
    
    def get_by_id(self, datasource_id: str) -> Optional[DataSource]:
        """
        根据ID获取数据源
        
        Args:
            datasource_id: 数据源ID
        
        Returns:
            Optional[DataSource]: 数据源对象，不存在返回None
        """
        return self.db.query(DataSource).filter(DataSource.id == datasource_id).first()
    
    def get_by_name(self, name: str, tenant_id: str) -> Optional[DataSource]:
        """
        根据名称获取数据源
        
        Args:
            name: 数据源名称
            tenant_id: 租户ID
        
        Returns:
            Optional[DataSource]: 数据源对象，不存在返回None
        """
        return self.db.query(DataSource).filter(
            and_(
                DataSource.name == name,
                DataSource.tenant_id == tenant_id
            )
        ).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        根据租户ID获取数据源列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataSource]: 数据源列表
        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).filter(DataSource.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_type(self, data_type: str, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        根据类型获取数据源列表
        
        Args:
            data_type: 数据源类型
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataSource]: 数据源列表
        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).filter(DataSource.type == data_type).offset(offset).limit(page_size).all()
    
    def get_default_datasource(self, tenant_id: str) -> Optional[DataSource]:
        """
        获取租户的默认数据源
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Optional[DataSource]: 数据源对象，不存在返回None
        """
        return self.db.query(DataSource).filter(
            and_(
                DataSource.tenant_id == tenant_id,
                DataSource.is_default == True
            )
        ).first()
    
    def get_active_datasources(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        获取租户的活跃数据源列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataSource]: 数据源列表
        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).filter(
            and_(
                DataSource.tenant_id == tenant_id,
                DataSource.status == "active"
            )
        ).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        搜索数据源
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataSource]: 数据源列表
        """
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
        获取所有数据源
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataSource]: 数据源列表
        """
        offset = (page - 1) * page_size
        return self.db.query(DataSource).offset(offset).limit(page_size).all()
    
    def update(self, datasource: DataSource) -> DataSource:
        """
        更新数据源
        
        Args:
            datasource: 数据源对象
        
        Returns:
            DataSource: 更新后的数据源对象
        """
        logger.info(f"更新数据源: datasource_id={datasource.id}")
        self.db.commit()
        self.db.refresh(datasource)
        return datasource
    
    def delete(self, datasource_id: str) -> bool:
        """
        删除数据源
        
        Args:
            datasource_id: 数据源ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除数据源: datasource_id={datasource_id}")
        datasource = self.get_by_id(datasource_id)
        if not datasource:
            return False
        
        # 检查是否为默认数据源
        if datasource.is_default:
            raise ValueError("无法删除默认数据源")
        
        self.db.delete(datasource)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户数据源数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 数据源数量
        """
        return self.db.query(DataSource).filter(DataSource.tenant_id == tenant_id).count()
    
    def count_by_type(self, data_type: str) -> int:
        """
        统计数据源类型的数量
        
        Args:
            data_type: 数据源类型
        
        Returns:
            int: 数据源数量
        """
        return self.db.query(DataSource).filter(DataSource.type == data_type).count()
    
    def count_all(self) -> int:
        """
        统计所有数据源数量
        
        Returns:
            int: 数据源数量
        """
        return self.db.query(DataSource).count()
    
    def exists_by_name(self, name: str, tenant_id: str) -> bool:
        """
        检查数据源名称是否存在
        
        Args:
            name: 数据源名称
            tenant_id: 租户ID
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(DataSource).filter(
            and_(
                DataSource.name == name,
                DataSource.tenant_id == tenant_id
            )
        ).first() is not None