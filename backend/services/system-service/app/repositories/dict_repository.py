# -*- coding: utf-8 -*-
"""
字典数据访问层

功能说明：
1. 字典CRUD操作
2. 字典查询操作
3. 字典统计操作

使用示例：
    from app.repositories.dict_repository import DictRepository
    
    dict_repo = DictRepository(db)
    dict = dict_repo.get_by_code("user_status")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from app.models.dict import Dict, DictItem


class DictRepository:
    """
    字典数据访问层
    
    功能：
    - 字典CRUD操作
    - 字典查询操作
    - 字典统计操作
    
    使用方法：
        dict_repo = DictRepository(db)
        dict = dict_repo.get_by_code("user_status")
    """
    
    def __init__(self, db: Session):
        """
        初始化字典数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create_dict(self, dict: Dict) -> Dict:
        """
        创建字典
        
        Args:
            dict: 字典对象
        
        Returns:
            Dict: 创建的字典对象
        """
        logger.info(f"创建字典: name={dict.name}, code={dict.code}")
        self.db.add(dict)
        self.db.commit()
        self.db.refresh(dict)
        return dict
    
    def get_dict_by_id(self, dict_id: str) -> Optional[Dict]:
        """
        根据ID获取字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            Optional[Dict]: 字典对象，不存在返回None
        """
        return self.db.query(Dict).filter(Dict.id == dict_id).first()
    
    def get_dict_by_code(self, code: str) -> Optional[Dict]:
        """
        根据编码获取字典
        
        Args:
            code: 字典编码
        
        Returns:
            Optional[Dict]: 字典对象，不存在返回None
        """
        return self.db.query(Dict).filter(Dict.code == code).first()
    
    def get_dicts_by_tenant(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Dict]:
        """
        根据租户ID获取字典列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Dict]: 字典列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Dict).filter(Dict.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def search_dicts(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Dict]:
        """
        搜索字典
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Dict]: 字典列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(Dict).filter(
            or_(
                Dict.name.like(f"%{keyword}%"),
                Dict.code.like(f"%{keyword}%"),
                Dict.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Dict.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all_dicts(self, page: int = 1, page_size: int = 10) -> List[Dict]:
        """
        获取所有字典
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Dict]: 字典列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Dict).offset(offset).limit(page_size).all()
    
    def update_dict(self, dict: Dict) -> Dict:
        """
        更新字典
        
        Args:
            dict: 字典对象
        
        Returns:
            Dict: 更新后的字典对象
        """
        logger.info(f"更新字典: dict_id={dict.id}")
        self.db.commit()
        self.db.refresh(dict)
        return dict
    
    def delete_dict(self, dict_id: str) -> bool:
        """
        删除字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典: dict_id={dict_id}")
        dict = self.get_dict_by_id(dict_id)
        if not dict:
            return False
        
        # 检查是否为系统字典
        if dict.is_system:
            raise ValueError("无法删除系统字典")
        
        self.db.delete(dict)
        self.db.commit()
        return True
    
    # 字典项相关方法
    def create_dict_item(self, item: DictItem) -> DictItem:
        """
        创建字典项
        
        Args:
            item: 字典项对象
        
        Returns:
            DictItem: 创建的字典项对象
        """
        logger.info(f"创建字典项: label={item.label}, value={item.value}")
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def get_dict_item_by_id(self, item_id: str) -> Optional[DictItem]:
        """
        根据ID获取字典项
        
        Args:
            item_id: 字典项ID
        
        Returns:
            Optional[DictItem]: 字典项对象，不存在返回None
        """
        return self.db.query(DictItem).filter(DictItem.id == item_id).first()
    
    def get_dict_items(self, dict_id: str, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        根据字典ID获取字典项列表
        
        Args:
            dict_id: 字典ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DictItem]: 字典项列表
        """
        offset = (page - 1) * page_size
        return self.db.query(DictItem).filter(DictItem.dict_id == dict_id).order_by(DictItem.sort_order).offset(offset).limit(page_size).all()
    
    def get_all_dict_items(self, dict_id: str) -> List[DictItem]:
        """
        获取字典的所有字典项
        
        Args:
            dict_id: 字典ID
        
        Returns:
            List[DictItem]: 字典项列表
        """
        return self.db.query(DictItem).filter(DictItem.dict_id == dict_id).order_by(DictItem.sort_order).all()
    
    def get_default_dict_item(self, dict_id: str) -> Optional[DictItem]:
        """
        获取字典的默认项
        
        Args:
            dict_id: 字典ID
        
        Returns:
            Optional[DictItem]: 字典项对象，不存在返回None
        """
        return self.db.query(DictItem).filter(
            and_(
                DictItem.dict_id == dict_id,
                DictItem.is_default == True
            )
        ).first()
    
    def update_dict_item(self, item: DictItem) -> DictItem:
        """
        更新字典项
        
        Args:
            item: 字典项对象
        
        Returns:
            DictItem: 更新后的字典项对象
        """
        logger.info(f"更新字典项: item_id={item.id}")
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_dict_item(self, item_id: str) -> bool:
        """
        删除字典项
        
        Args:
            item_id: 字典项ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典项: item_id={item_id}")
        item = self.get_dict_item_by_id(item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    # 统计方法
    def count_dicts_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户字典数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 字典数量
        """
        return self.db.query(Dict).filter(Dict.tenant_id == tenant_id).count()
    
    def count_dict_items(self, dict_id: str) -> int:
        """
        统计字典项数量
        
        Args:
            dict_id: 字典ID
        
        Returns:
            int: 字典项数量
        """
        return self.db.query(DictItem).filter(DictItem.dict_id == dict_id).count()
    
    def count_all_dicts(self) -> int:
        """
        统计所有字典数量
        
        Returns:
            int: 字典数量
        """
        return self.db.query(Dict).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查字典编码是否存在
        
        Args:
            code: 字典编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Dict).filter(Dict.code == code).first() is not None