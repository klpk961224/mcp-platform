# -*- coding: utf-8 -*-
"""
字典服务

功能说明：
1. 字典CRUD操作
2. 字典项CRUD操作
3. 字典查询操作

使用示例：
    from app.services.dict_service import DictService
    
    dict_service = DictService(db)
    dicts = dict_service.get_dict_by_type("user_status")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict as DictType, Any, List

from common.database.models.system import Dict as DictModel, DictItem
from app.repositories.dict_repository import DictRepository, DictItemRepository


class DictService:
    """
    字典服务
    
    功能：
    - 字典CRUD操作
    - 字典项CRUD操作
    - 字典查询操作
    
    使用方法：
        dict_service = DictService(db)
        dicts = dict_service.get_dict_by_type("user_status")
    """
    
    def __init__(self, db: Session):
        """
        初始化字典服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.dict_repo = DictRepository(db)
        self.dict_item_repo = DictItemRepository(db)
    
    def create_dict(self, dict_data: DictType[str, Any]) -> DictModel:
        """
        创建字典
        
        Args:
            dict_data: 字典数据
        
        Returns:
            DictModel: 创建的字典对象
        
        Raises:
            ValueError: 字典类型已存在
        """
        logger.info(f"创建字典: type={dict_data.get('type')}, name={dict_data.get('name')}")
        
        # 检查字典类型是否已存在
        existing = self.dict_repo.get_by_type(dict_data.get("type"))
        if existing:
            raise ValueError("字典类型已存在")
        
        # 创建字典
        dict_obj = DictModel(**dict_data)
        return self.dict_repo.create(dict_obj)
    
    def get_dict(self, dict_id: str) -> Optional[DictModel]:
        """
        获取字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            Optional[DictModel]: 字典对象，不存在返回None
        """
        return self.dict_repo.get_by_id(dict_id)
    
    def get_dict_by_type(self, dict_type: str) -> Optional[DictModel]:
        """
        根据类型获取字典
        
        Args:
            dict_type: 字典类型
        
        Returns:
            Optional[DictModel]: 字典对象，不存在返回None
        """
        return self.dict_repo.get_by_type(dict_type)
    
    def update_dict(self, dict_id: str, dict_data: DictType[str, Any]) -> Optional[DictModel]:
        """
        更新字典
        
        Args:
            dict_id: 字典ID
            dict_data: 字典数据
        
        Returns:
            Optional[DictModel]: 更新后的字典对象，不存在返回None
        """
        logger.info(f"更新字典: dict_id={dict_id}")
        
        dict_obj = self.dict_repo.get_by_id(dict_id)
        if not dict_obj:
            return None
        
        # 更新字典
        for key, value in dict_data.items():
            if hasattr(dict_obj, key):
                setattr(dict_obj, key, value)
        
        return self.dict_repo.update(dict_obj)
    
    def delete_dict(self, dict_id: str) -> bool:
        """
        删除字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典: dict_id={dict_id}")
        return self.dict_repo.delete(dict_id)
    
    def list_dicts(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                   page: int = 1, page_size: int = 10) -> List[DictModel]:
        """
        获取字典列表
        
        Args:
            tenant_id: 租户ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DictModel]: 字典列表
        """
        if keyword:
            return self.dict_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.dict_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.dict_repo.get_all(page, page_size)
    
    def count_dicts(self, tenant_id: Optional[str] = None) -> int:
        """
        统计字典数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 字典数量
        """
        if tenant_id:
            return self.dict_repo.count_by_tenant(tenant_id)
        else:
            return self.dict_repo.count_all()
    
    def create_dict_item(self, dict_id: str, dict_item_data: DictType[str, Any]) -> DictItem:
        """
        创建字典项
        
        Args:
            dict_id: 字典ID
            dict_item_data: 字典项数据
        
        Returns:
            DictItem: 创建的字典项对象
        
        Raises:
            ValueError: 字典不存在
        """
        logger.info(f"创建字典项: dict_id={dict_id}, label={dict_item_data.get('label')}")
        
        # 检查字典是否存在
        dict_obj = self.dict_repo.get_by_id(dict_id)
        if not dict_obj:
            raise ValueError("字典不存在")
        
        # 创建字典项
        dict_item_data["dict_id"] = dict_id
        dict_item = DictItem(**dict_item_data)
        return self.dict_item_repo.create(dict_item)
    
    def get_dict_item(self, dict_item_id: str) -> Optional[DictItem]:
        """
        获取字典项
        
        Args:
            dict_item_id: 字典项ID
        
        Returns:
            Optional[DictItem]: 字典项对象，不存在返回None
        """
        return self.dict_item_repo.get_by_id(dict_item_id)
    
    def get_dict_items(self, dict_id: str, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        获取字典的字典项列表
        
        Args:
            dict_id: 字典ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DictItem]: 字典项列表
        """
        return self.dict_item_repo.get_by_dict_id(dict_id, page, page_size)
    
    def get_dict_items_by_type(self, dict_type: str) -> List[DictItem]:
        """
        根据字典类型获取字典项列表
        
        Args:
            dict_type: 字典类型
        
        Returns:
            List[DictItem]: 字典项列表
        """
        return self.dict_item_repo.get_by_dict_type(dict_type)
    
    def update_dict_item(self, dict_item_id: str, dict_item_data: DictType[str, Any]) -> Optional[DictItem]:
        """
        更新字典项
        
        Args:
            dict_item_id: 字典项ID
            dict_item_data: 字典项数据
        
        Returns:
            Optional[DictItem]: 更新后的字典项对象，不存在返回None
        """
        logger.info(f"更新字典项: dict_item_id={dict_item_id}")
        
        dict_item = self.dict_item_repo.get_by_id(dict_item_id)
        if not dict_item:
            return None
        
        # 更新字典项
        for key, value in dict_item_data.items():
            if hasattr(dict_item, key):
                setattr(dict_item, key, value)
        
        return self.dict_item_repo.update(dict_item)
    
    def delete_dict_item(self, dict_item_id: str) -> bool:
        """
        删除字典项
        
        Args:
            dict_item_id: 字典项ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典项: dict_item_id={dict_item_id}")
        return self.dict_item_repo.delete(dict_item_id)
    
    def count_dict_items(self, dict_id: str) -> int:
        """
        统计字典的字典项数量
        
        Args:
            dict_id: 字典ID
        
        Returns:
            int: 字典项数量
        """
        return self.dict_item_repo.count_by_dict(dict_id)