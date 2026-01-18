# -*- coding: utf-8 -*-
"""
数据源服务

功能说明：
1. 数据源管理
2. 数据源连接
3. 数据源健康检查

使用示例：
    from app.services.datasource_service import DataSourceService
    
    datasource_service = DataSourceService(db)
    datasource = datasource_service.create_datasource(name="主数据库", type="mysql")
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
    数据源服务
    
    功能：
    - 数据源管理
    - 数据源连接
    - 数据源健康检查
    
    使用方法：
        datasource_service = DataSourceService(db)
        datasource = datasource_service.create_datasource(name="主数据库", type="mysql")
    """
    
    def __init__(self, db: Session):
        """
        初始化数据源服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.datasource_repo = DataSourceRepository(db)
    
    def create_datasource(self, datasource_data: Dict[str, Any]) -> DataSource:
        """
        创建数据源
        
        Args:
            datasource_data: 数据源数据
        
        Returns:
            DataSource: 创建的数据源对象
        
        Raises:
            ValueError: 数据源名称已存在
        """
        logger.info(f"创建数据源: name={datasource_data.get('name')}, type={datasource_data.get('type')}")
        
        # 检查数据源名称是否已存在
        if self.datasource_repo.exists_by_name(datasource_data.get("name"), datasource_data.get("tenant_id")):
            raise ValueError("数据源名称已存在")
        
        # 创建数据源
        datasource = DataSource(**datasource_data)
        datasource = self.datasource_repo.create(datasource)
        
        # 注册到数据源管理器
        self._register_datasource(datasource)
        
        return datasource
    
    def get_datasource(self, datasource_id: str) -> Optional[DataSource]:
        """
        获取数据源
        
        Args:
            datasource_id: 数据源ID
        
        Returns:
            Optional[DataSource]: 数据源对象，不存在返回None
        """
        return self.datasource_repo.get_by_id(datasource_id)
    
    def get_default_datasource(self, tenant_id: str) -> Optional[DataSource]:
        """
        获取默认数据源
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Optional[DataSource]: 数据源对象，不存在返回None
        """
        return self.datasource_repo.get_default_datasource(tenant_id)
    
    def update_datasource(self, datasource_id: str, datasource_data: Dict[str, Any]) -> Optional[DataSource]:
        """
        更新数据源
        
        Args:
            datasource_id: 数据源ID
            datasource_data: 数据源数据
        
        Returns:
            Optional[DataSource]: 更新后的数据源对象，不存在返回None
        """
        logger.info(f"更新数据源: datasource_id={datasource_id}")
        
        datasource = self.datasource_repo.get_by_id(datasource_id)
        if not datasource:
            return None
        
        # 更新数据源
        for key, value in datasource_data.items():
            if hasattr(datasource, key):
                setattr(datasource, key, value)
        
        datasource = self.datasource_repo.update(datasource)
        
        # 重新注册到数据源管理器
        self._register_datasource(datasource)
        
        return datasource
    
    def delete_datasource(self, datasource_id: str) -> bool:
        """
        删除数据源
        
        Args:
            datasource_id: 数据源ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除数据源: datasource_id={datasource_id}")
        return self.datasource_repo.delete(datasource_id)
    
    def list_datasources(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                         page: int = 1, page_size: int = 10) -> List[DataSource]:
        """
        获取数据源列表
        
        Args:
            tenant_id: 租户ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataSource]: 数据源列表
        """
        if keyword:
            return self.datasource_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.datasource_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.datasource_repo.get_all(page, page_size)
    
    def test_connection(self, datasource_id: str) -> Dict[str, Any]:
        """
        测试数据源连接
        
        Args:
            datasource_id: 数据源ID
        
        Returns:
            Dict[str, Any]: 连接测试结果
        """
        logger.info(f"测试数据源连接: datasource_id={datasource_id}")
        
        datasource = self.datasource_repo.get_by_id(datasource_id)
        if not datasource:
            return {"success": False, "message": "数据源不存在"}
        
        try:
            # 测试连接
            session = datasource_manager.get_session(datasource.id)
            session.execute("SELECT 1")
            session.close()
            
            # 更新健康状态
            datasource.update_health_status(is_healthy=True)
            self.datasource_repo.update(datasource)
            
            return {"success": True, "message": "连接成功"}
            
        except Exception as e:
            logger.error(f"数据源连接测试失败: {e}")
            
            # 更新健康状态
            datasource.update_health_status(is_healthy=False)
            self.datasource_repo.update(datasource)
            
            return {"success": False, "message": f"连接失败: {str(e)}"}
    
    def _register_datasource(self, datasource: DataSource):
        """
        注册数据源到数据源管理器
        
        Args:
            datasource: 数据源对象
        """
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
            logger.info(f"数据源注册成功: {datasource.id}")
        except Exception as e:
            logger.error(f"数据源注册失败: {e}")
            raise
    
    def count_datasources(self, tenant_id: Optional[str] = None) -> int:
        """
        统计数据源数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 数据源数量
        """
        if tenant_id:
            return self.datasource_repo.count_by_tenant(tenant_id)
        else:
            return self.datasource_repo.count_all()