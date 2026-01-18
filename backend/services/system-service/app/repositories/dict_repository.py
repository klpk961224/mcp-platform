# -*- coding: utf-8 -*-
"""
瀛楀吀鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 瀛楀吀CRUD鎿嶄綔
2. 瀛楀吀椤笴RUD鎿嶄綔
3. 瀛楀吀查询鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.dict_repository import DictRepository
    
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
    瀛楀吀鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 瀛楀吀CRUD鎿嶄綔
    - 瀛楀吀查询鎿嶄綔
    
    浣跨敤鏂规硶锛?        dict_repo = DictRepository(db)
        dicts = dict_repo.get_by_type("user_status")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧瓧鍏告暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, dict_obj: Dict) -> Dict:
        """
        创建瀛楀吀
        
        Args:
            dict_obj: 瀛楀吀瀵硅薄
        
        Returns:
            Dict: 创建鐨勫瓧鍏稿璞?        """
        logger.info(f"创建瀛楀吀: type={dict_obj.type}, name={dict_obj.name}")
        self.db.add(dict_obj)
        self.db.commit()
        self.db.refresh(dict_obj)
        return dict_obj
    
    def get_by_id(self, dict_id: str) -> Optional[Dict]:
        """
        根据ID鑾峰彇瀛楀吀
        
        Args:
            dict_id: 瀛楀吀ID
        
        Returns:
            Optional[Dict]: 瀛楀吀瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Dict).filter(Dict.id == dict_id).first()
    
    def get_by_type(self, dict_type: str) -> Optional[Dict]:
        """
        根据类型鑾峰彇瀛楀吀
        
        Args:
            dict_type: 瀛楀吀类型
        
        Returns:
            Optional[Dict]: 瀛楀吀瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Dict).filter(Dict.type == dict_type).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Dict]:
        """
        根据租户ID鑾峰彇瀛楀吀鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Dict]: 瀛楀吀鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Dict).filter(Dict.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Dict]:
        """
        鎼滅储瀛楀吀
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Dict]: 瀛楀吀鍒楄〃
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
        鑾峰彇鎵€鏈夊瓧鍏?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Dict]: 瀛楀吀鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Dict).offset(offset).limit(page_size).all()
    
    def update(self, dict_obj: Dict) -> Dict:
        """
        更新瀛楀吀
        
        Args:
            dict_obj: 瀛楀吀瀵硅薄
        
        Returns:
            Dict: 更新鍚庣殑瀛楀吀瀵硅薄
        """
        logger.info(f"更新瀛楀吀: dict_id={dict_obj.id}")
        self.db.commit()
        self.db.refresh(dict_obj)
        return dict_obj
    
    def delete(self, dict_id: str) -> bool:
        """
        删除瀛楀吀
        
        Args:
            dict_id: 瀛楀吀ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除瀛楀吀: dict_id={dict_id}")
        dict_obj = self.get_by_id(dict_id)
        if not dict_obj:
            return False
        
        # 妫€鏌ユ槸鍚︽湁瀛楀吀椤?        if dict_obj.items:
            raise ValueError("鏃犳硶删除瀛楀吀锛氳瀛楀吀涓嬪瓨鍦ㄥ瓧鍏搁」")
        
        self.db.delete(dict_obj)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛瀛楀吀数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 瀛楀吀数量
        """
        return self.db.query(Dict).filter(Dict.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夊瓧鍏告暟閲?        
        Returns:
            int: 瀛楀吀数量
        """
        return self.db.query(Dict).count()


class DictItemRepository:
    """
    瀛楀吀椤规暟鎹闂眰
    
    鍔熻兘锛?    - 瀛楀吀椤笴RUD鎿嶄綔
    - 瀛楀吀椤规煡璇㈡搷浣?    
    浣跨敤鏂规硶锛?        dict_item_repo = DictItemRepository(db)
        items = dict_item_repo.get_by_dict_id("dict_001")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧瓧鍏搁」鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, dict_item: DictItem) -> DictItem:
        """
        创建瀛楀吀椤?        
        Args:
            dict_item: 瀛楀吀椤瑰璞?        
        Returns:
            DictItem: 创建鐨勫瓧鍏搁」瀵硅薄
        """
        logger.info(f"创建瀛楀吀椤? label={dict_item.label}, value={dict_item.value}")
        self.db.add(dict_item)
        self.db.commit()
        self.db.refresh(dict_item)
        return dict_item
    
    def get_by_id(self, dict_item_id: str) -> Optional[DictItem]:
        """
        根据ID鑾峰彇瀛楀吀椤?        
        Args:
            dict_item_id: 瀛楀吀椤笽D
        
        Returns:
            Optional[DictItem]: 瀛楀吀椤瑰璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.db.query(DictItem).filter(DictItem.id == dict_item_id).first()
    
    def get_by_dict_id(self, dict_id: str, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        根据瀛楀吀ID鑾峰彇瀛楀吀椤瑰垪琛?        
        Args:
            dict_id: 瀛楀吀ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DictItem]: 瀛楀吀椤瑰垪琛?        """
        offset = (page - 1) * page_size
        return self.db.query(DictItem).filter(
            DictItem.dict_id == dict_id
        ).order_by(DictItem.sort_order).offset(offset).limit(page_size).all()
    
    def get_by_dict_type(self, dict_type: str) -> List[DictItem]:
        """
        根据瀛楀吀类型鑾峰彇瀛楀吀椤瑰垪琛?        
        Args:
            dict_type: 瀛楀吀类型
        
        Returns:
            List[DictItem]: 瀛楀吀椤瑰垪琛?        """
        dict_obj = self.db.query(Dict).filter(Dict.type == dict_type).first()
        if not dict_obj:
            return []
        
        return self.db.query(DictItem).filter(
            DictItem.dict_id == dict_obj.id,
            DictItem.status == "active"
        ).order_by(DictItem.sort_order).all()
    
    def search(self, keyword: str, dict_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        鎼滅储瀛楀吀椤?        
        Args:
            keyword: 鍏抽敭璇?            dict_id: 瀛楀吀ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DictItem]: 瀛楀吀椤瑰垪琛?        """
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
        更新瀛楀吀椤?        
        Args:
            dict_item: 瀛楀吀椤瑰璞?        
        Returns:
            DictItem: 更新鍚庣殑瀛楀吀椤瑰璞?        """
        logger.info(f"更新瀛楀吀椤? dict_item_id={dict_item.id}")
        self.db.commit()
        self.db.refresh(dict_item)
        return dict_item
    
    def delete(self, dict_item_id: str) -> bool:
        """
        删除瀛楀吀椤?        
        Args:
            dict_item_id: 瀛楀吀椤笽D
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除瀛楀吀椤? dict_item_id={dict_item_id}")
        dict_item = self.get_by_id(dict_item_id)
        if not dict_item:
            return False
        
        self.db.delete(dict_item)
        self.db.commit()
        return True
    
    def count_by_dict(self, dict_id: str) -> int:
        """
        缁熻瀛楀吀鐨勫瓧鍏搁」数量
        
        Args:
            dict_id: 瀛楀吀ID
        
        Returns:
            int: 瀛楀吀椤规暟閲?        """
        return self.db.query(DictItem).filter(DictItem.dict_id == dict_id).count()
