# -*- coding: utf-8 -*-
"""
字典数据访问层

功能说明：
1. 字典CRUD操作
2. 字典项CRUD操作
3. 字典查询操作

使用示例：
    from app.repositories.dict_repository import DictRepository
    
    dict_repo = DictRepository(db)
    dicts = dict_repo.get_by_type("user_status")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.system import Dict, DictItem


class DictRepository:
    """
    字典数据访问层
    
    功能：
    - 字典CRUD操作
    - 字典查询操作
    
    使用方法：
        dict_repo = DictRepository(db)
        dicts = dict_repo.get_by_type("user_status")
    """
    
    def __init__(self, db: Session):
        """
        初始化字典数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, dict_obj: Dict) -> Dict:
        """
        创建字典
        
        Args:
            dict_obj: 字典对象
        
        Returns:
            Dict: 创建的字典对象
        """
        logger.info(f"创建字典: type={dict_obj.type}, name={dict_obj.name}")
        self.db.add(dict_obj)
        self.db.commit()
        self.db.refresh(dict_obj)
        return dict_obj
    
    def get_by_id(self, dict_id: str) -> Optional[Dict]:
        """
        根据ID获取字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            Optional[Dict]: 字典对象，不存在返回None
        """
        return self.db.query(Dict).filter(Dict.id == dict_id).first()
    
    def get_by_type(self, dict_type: str) -> Optional[Dict]:
        """
        根据类型获取字典
        
        Args:
            dict_type: 字典类型
        
        Returns:
            Optional[Dict]: 字典对象，不存在返回None
        """
        return self.db.query(Dict).filter(Dict.type == dict_type).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Dict]:
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
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Dict]:
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
                Dict.type.like(f"%{keyword}%"),
                Dict.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Dict.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Dict]:
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
    
    def update(self, dict_obj: Dict) -> Dict:
        """
        更新字典
        
        Args:
            dict_obj: 字典对象
        
        Returns:
            Dict: 更新后的字典对象
        """
        logger.info(f"更新字典: dict_id={dict_obj.id}")
        self.db.commit()
        self.db.refresh(dict_obj)
        return dict_obj
    
    def delete(self, dict_id: str) -> bool:
        """
        删除字典
        
        Args:
            dict_id: 字典ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典: dict_id={dict_id}")
        dict_obj = self.get_by_id(dict_id)
        if not dict_obj:
            return False
        
        # 检查是否有字典项
        if dict_obj.items:
            raise ValueError("无法删除字典：该字典下存在字典项")
        
        self.db.delete(dict_obj)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户字典数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 字典数量
        """
        return self.db.query(Dict).filter(Dict.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        统计所有字典数量
        
        Returns:
            int: 字典数量
        """
        return self.db.query(Dict).count()


class DictItemRepository:
    """
    字典项数据访问层
    
    功能：
    - 字典项CRUD操作
    - 字典项查询操作
    
    使用方法：
        dict_item_repo = DictItemRepository(db)
        items = dict_item_repo.get_by_dict_id("dict_001")
    """
    
    def __init__(self, db: Session):
        """
        初始化字典项数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, dict_item: DictItem) -> DictItem:
        """
        创建字典项
        
        Args:
            dict_item: 字典项对象
        
        Returns:
            DictItem: 创建的字典项对象
        """
        logger.info(f"创建字典项: label={dict_item.label}, value={dict_item.value}")
        self.db.add(dict_item)
        self.db.commit()
        self.db.refresh(dict_item)
        return dict_item
    
    def get_by_id(self, dict_item_id: str) -> Optional[DictItem]:
        """
        根据ID获取字典项
        
        Args:
            dict_item_id: 字典项ID
        
        Returns:
            Optional[DictItem]: 字典项对象，不存在返回None
        """
        return self.db.query(DictItem).filter(DictItem.id == dict_item_id).first()
    
    def get_by_dict_id(self, dict_id: str, page: int = 1, page_size: int = 10) -> List[DictItem]:
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
        return self.db.query(DictItem).filter(
            DictItem.dict_id == dict_id
        ).order_by(DictItem.sort_order).offset(offset).limit(page_size).all()
    
    def get_by_dict_type(self, dict_type: str) -> List[DictItem]:
        """
        根据字典类型获取字典项列表
        
        Args:
            dict_type: 字典类型
        
        Returns:
            List[DictItem]: 字典项列表
        """
        dict_obj = self.db.query(Dict).filter(Dict.type == dict_type).first()
        if not dict_obj:
            return []
        
        return self.db.query(DictItem).filter(
            DictItem.dict_id == dict_obj.id,
            DictItem.status == "active"
        ).order_by(DictItem.sort_order).all()
    
    def search(self, keyword: str, dict_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        搜索字典项
        
        Args:
            keyword: 关键词
            dict_id: 字典ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DictItem]: 字典项列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(DictItem).filter(
            or_(
                DictItem.label.like(f"%{keyword}%"),
                DictItem.value.like(f"%{keyword}%")
            )
        )
        
        if dict_id:
            query = query.filter(DictItem.dict_id == dict_id)
        
        return query.order_by(DictItem.sort_order).offset(offset).limit(page_size).all()
    
    def update(self, dict_item: DictItem) -> DictItem:
        """
        更新字典项
        
        Args:
            dict_item: 字典项对象
        
        Returns:
            DictItem: 更新后的字典项对象
        """
        logger.info(f"更新字典项: dict_item_id={dict_item.id}")
        self.db.commit()
        self.db.refresh(dict_item)
        return dict_item
    
    def delete(self, dict_item_id: str) -> bool:
        """
        删除字典项
        
        Args:
            dict_item_id: 字典项ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除字典项: dict_item_id={dict_item_id}")
        dict_item = self.get_by_id(dict_item_id)
        if not dict_item:
            return False
        
        self.db.delete(dict_item)
        self.db.commit()
        return True
    
    def count_by_dict(self, dict_id: str) -> int:
        """
        统计字典的字典项数量
        
        Args:
            dict_id: 字典ID
        
        Returns:
            int: 字典项数量
        """
        return self.db.query(DictItem).filter(DictItem.dict_id == dict_id).count()