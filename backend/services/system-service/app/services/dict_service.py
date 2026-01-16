# -*- coding: utf-8 -*-
"""
字典服务

功能说明：
1. 字典管理
2. 字典项管理
3. 字典缓存

使用示例：
    from app.services.dict_service import DictService
    
    dict_service = DictService(db)
    dict = dict_service.create_dict(name="用户状态", code="user_status")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from app.models.dict import Dict, DictItem
from app.repositories.dict_repository import DictRepository


class DictService:
    """
    字典服务
    
    功能：
    - 字典管理
    - 字典项管理
    - 字典缓存
    
    使用方法：
        dict_service = DictService(db)
        dict = dict_service.create_dict(name="用户状态", code="user_status")
    """
    
    def __init__(self, db: Session):
        """
        初始化字典服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.dict_repo = DictRepository(db)
    
    def create_dict(self, dict_data: Dict[str, Any]) -> Dict:
        """
        创建字典
        
        Args:
            dict_data: 字典数据
        
        Returns:
            Dict: 创建的字典对象
        
        Raises:
            ValueError: 字典编码已存在
        """
        logger.info(f"创建字典: name={dict_data.get('name')}, code={dict_data.get('code')}")
        
        # 检查字典编码是否已存在
        if self.dict_repo.exists_by_code(dict_data.get("code")):
            raise ValueError("字典编码已存在")
        
        # 创建字典
        dict = Dict(**dict_data)
        return self.dict_repo.create_dict(dict)
    
    def get_dict(self, dict_id: str) -> Optional[Dict]:
        """
        获取字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            Optional[Dict]: 字典对象，不存在返回None
        """
        return self.dict_repo.get_dict_by_id(dict_id)
    
    def get_dict_by_code(self, code: str) -> Optional[Dict]:
        """
        根据编码获取字典
        
        Args:
            code: 字典编码
        
        Returns:
            Optional[Dict]: 字典对象，不存在返回None
        """
        return self.dict_repo.get_dict_by_code(code)
    
    def update_dict(self, dict_id: str, dict_data: Dict[str, Any]) -> Optional[Dict]:
        """
        更新字典
        
        Args:
            dict_id: 字典ID
            dict_data: 字典数据
        
        Returns:
            Optional[Dict]: 更新后的字典对象，不存在返回None
        """
        logger.info(f"更新字典: dict_id={dict_id}")
        
        dict = self.dict_repo.get_dict_by_id(dict_id)
        if not dict:
            return None
        
        # 更新字典
        for key, value in dict_data.items():
            if hasattr(dict, key):
                setattr(dict, key, value)
        
        return self.dict_repo.update_dict(dict)
    
    def delete_dict(self, dict_id: str) -> bool:
        """
        删除字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典: dict_id={dict_id}")
        return self.dict_repo.delete_dict(dict_id)
    
    def list_dicts(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                   page: int = 1, page_size: int = 10) -> List[Dict]:
        """
        获取字典列表
        
        Args:
            tenant_id: 租户ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Dict]: 字典列表
        """
        if keyword:
            return self.dict_repo.search_dicts(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.dict_repo.get_dicts_by_tenant(tenant_id, page, page_size)
        else:
            return self.dict_repo.get_all_dicts(page, page_size)
    
    # 字典项相关方法
    def create_dict_item(self, item_data: Dict[str, Any]) -> DictItem:
        """
        创建字典项
        
        Args:
            item_data: 字典项数据
        
        Returns:
            DictItem: 创建的字典项对象
        """
        logger.info(f"创建字典项: label={item_data.get('label')}, value={item_data.get('value')}")
        
        # 创建字典项
        item = DictItem(**item_data)
        return self.dict_repo.create_dict_item(item)
    
    def get_dict_item(self, item_id: str) -> Optional[DictItem]:
        """
        获取字典项
        
        Args:
            item_id: 字典项ID
        
        Returns:
            Optional[DictItem]: 字典项对象，不存在返回None
        """
        return self.dict_repo.get_dict_item_by_id(item_id)
    
    def get_dict_items(self, dict_id: str, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        获取字典项列表
        
        Args:
            dict_id: 字典ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DictItem]: 字典项列表
        """
        return self.dict_repo.get_dict_items(dict_id, page, page_size)
    
    def get_all_dict_items(self, dict_id: str) -> List[DictItem]:
        """
        获取字典的所有字典项
        
        Args:
            dict_id: 字典ID
        
        Returns:
            List[DictItem]: 字典项列表
        """
        return self.dict_repo.get_all_dict_items(dict_id)
    
    def get_default_dict_item(self, dict_id: str) -> Optional[DictItem]:
        """
        获取字典的默认项
        
        Args:
            dict_id: 字典ID
        
        Returns:
            Optional[DictItem]: 字典项对象，不存在返回None
        """
        return self.dict_repo.get_default_dict_item(dict_id)
    
    def update_dict_item(self, item_id: str, item_data: Dict[str, Any]) -> Optional[DictItem]:
        """
        更新字典项
        
        Args:
            item_id: 字典项ID
            item_data: 字典项数据
        
        Returns:
            Optional[DictItem]: 更新后的字典项对象，不存在返回None
        """
        logger.info(f"更新字典项: item_id={item_id}")
        
        item = self.dict_repo.get_dict_item_by_id(item_id)
        if not item:
            return None
        
        # 更新字典项
        for key, value in item_data.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        return self.dict_repo.update_dict_item(item)
    
    def delete_dict_item(self, item_id: str) -> bool:
        """
        删除字典项
        
        Args:
            item_id: 字典项ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典项: item_id={item_id}")
        return self.dict_repo.delete_dict_item(item_id)
    
    def get_dict_value_label(self, dict_code: str, value: str) -> Optional[str]:
        """
        根据字典编码和值获取标签
        
        Args:
            dict_code: 字典编码
            value: 值
        
        Returns:
            Optional[str]: 标签，不存在返回None
        """
        dict = self.dict_repo.get_dict_by_code(dict_code)
        if not dict:
            return None
        
        for item in dict.items:
            if item.value == value:
                return item.label
        
        return None
    
    def count_dicts(self, tenant_id: Optional[str] = None) -> int:
        """
        统计字典数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 字典数量
        """
        if tenant_id:
            return self.dict_repo.count_dicts_by_tenant(tenant_id)
        else:
            return self.dict_repo.count_all_dicts()
    
    def count_dict_items(self, dict_id: str) -> int:
        """
        统计字典项数量
        
        Args:
            dict_id: 字典ID
        
        Returns:
            int: 字典项数量
        """
        return self.dict_repo.count_dict_items(dict_id)