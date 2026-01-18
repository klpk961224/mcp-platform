# -*- coding: utf-8 -*-
"""
瀛楀吀鏈嶅姟

鍔熻兘璇存槑锛?1. 瀛楀吀CRUD鎿嶄綔
2. 瀛楀吀椤笴RUD鎿嶄綔
3. 瀛楀吀鏌ヨ鎿嶄綔

浣跨敤绀轰緥锛?    from app.services.dict_service import DictService
    
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
    瀛楀吀鏈嶅姟
    
    鍔熻兘锛?    - 瀛楀吀CRUD鎿嶄綔
    - 瀛楀吀椤笴RUD鎿嶄綔
    - 瀛楀吀鏌ヨ鎿嶄綔
    
    浣跨敤鏂规硶锛?        dict_service = DictService(db)
        dicts = dict_service.get_dict_by_type("user_status")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧瓧鍏告湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.dict_repo = DictRepository(db)
        self.dict_item_repo = DictItemRepository(db)
    
    def create_dict(self, dict_data: DictType[str, Any]) -> DictModel:
        """
        鍒涘缓瀛楀吀
        
        Args:
            dict_data: 瀛楀吀鏁版嵁
        
        Returns:
            DictModel: 鍒涘缓鐨勫瓧鍏稿璞?        
        Raises:
            ValueError: 瀛楀吀绫诲瀷宸插瓨鍦?        """
        logger.info(f"鍒涘缓瀛楀吀: type={dict_data.get('type')}, name={dict_data.get('name')}")
        
        # 妫€鏌ュ瓧鍏哥被鍨嬫槸鍚﹀凡瀛樺湪
        existing = self.dict_repo.get_by_type(dict_data.get("type"))
        if existing:
            raise ValueError("瀛楀吀绫诲瀷宸插瓨鍦?)
        
        # 鍒涘缓瀛楀吀
        dict_obj = DictModel(**dict_data)
        return self.dict_repo.create(dict_obj)
    
    def get_dict(self, dict_id: str) -> Optional[DictModel]:
        """
        鑾峰彇瀛楀吀
        
        Args:
            dict_id: 瀛楀吀ID
        
        Returns:
            Optional[DictModel]: 瀛楀吀瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.dict_repo.get_by_id(dict_id)
    
    def get_dict_by_type(self, dict_type: str) -> Optional[DictModel]:
        """
        鏍规嵁绫诲瀷鑾峰彇瀛楀吀
        
        Args:
            dict_type: 瀛楀吀绫诲瀷
        
        Returns:
            Optional[DictModel]: 瀛楀吀瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.dict_repo.get_by_type(dict_type)
    
    def update_dict(self, dict_id: str, dict_data: DictType[str, Any]) -> Optional[DictModel]:
        """
        鏇存柊瀛楀吀
        
        Args:
            dict_id: 瀛楀吀ID
            dict_data: 瀛楀吀鏁版嵁
        
        Returns:
            Optional[DictModel]: 鏇存柊鍚庣殑瀛楀吀瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鏇存柊瀛楀吀: dict_id={dict_id}")
        
        dict_obj = self.dict_repo.get_by_id(dict_id)
        if not dict_obj:
            return None
        
        # 鏇存柊瀛楀吀
        for key, value in dict_data.items():
            if hasattr(dict_obj, key):
                setattr(dict_obj, key, value)
        
        return self.dict_repo.update(dict_obj)
    
    def delete_dict(self, dict_id: str) -> bool:
        """
        鍒犻櫎瀛楀吀
        
        Args:
            dict_id: 瀛楀吀ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎瀛楀吀: dict_id={dict_id}")
        return self.dict_repo.delete(dict_id)
    
    def list_dicts(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                   page: int = 1, page_size: int = 10) -> List[DictModel]:
        """
        鑾峰彇瀛楀吀鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[DictModel]: 瀛楀吀鍒楄〃
        """
        if keyword:
            return self.dict_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.dict_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.dict_repo.get_all(page, page_size)
    
    def count_dicts(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻瀛楀吀鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 瀛楀吀鏁伴噺
        """
        if tenant_id:
            return self.dict_repo.count_by_tenant(tenant_id)
        else:
            return self.dict_repo.count_all()
    
    def create_dict_item(self, dict_id: str, dict_item_data: DictType[str, Any]) -> DictItem:
        """
        鍒涘缓瀛楀吀椤?        
        Args:
            dict_id: 瀛楀吀ID
            dict_item_data: 瀛楀吀椤规暟鎹?        
        Returns:
            DictItem: 鍒涘缓鐨勫瓧鍏搁」瀵硅薄
        
        Raises:
            ValueError: 瀛楀吀涓嶅瓨鍦?        """
        logger.info(f"鍒涘缓瀛楀吀椤? dict_id={dict_id}, label={dict_item_data.get('label')}")
        
        # 妫€鏌ュ瓧鍏告槸鍚﹀瓨鍦?        dict_obj = self.dict_repo.get_by_id(dict_id)
        if not dict_obj:
            raise ValueError("瀛楀吀涓嶅瓨鍦?)
        
        # 鍒涘缓瀛楀吀椤?        dict_item_data["dict_id"] = dict_id
        dict_item = DictItem(**dict_item_data)
        return self.dict_item_repo.create(dict_item)
    
    def get_dict_item(self, dict_item_id: str) -> Optional[DictItem]:
        """
        鑾峰彇瀛楀吀椤?        
        Args:
            dict_item_id: 瀛楀吀椤笽D
        
        Returns:
            Optional[DictItem]: 瀛楀吀椤瑰璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        return self.dict_item_repo.get_by_id(dict_item_id)
    
    def get_dict_items(self, dict_id: str, page: int = 1, page_size: int = 10) -> List[DictItem]:
        """
        鑾峰彇瀛楀吀鐨勫瓧鍏搁」鍒楄〃
        
        Args:
            dict_id: 瀛楀吀ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[DictItem]: 瀛楀吀椤瑰垪琛?        """
        return self.dict_item_repo.get_by_dict_id(dict_id, page, page_size)
    
    def get_dict_items_by_type(self, dict_type: str) -> List[DictItem]:
        """
        鏍规嵁瀛楀吀绫诲瀷鑾峰彇瀛楀吀椤瑰垪琛?        
        Args:
            dict_type: 瀛楀吀绫诲瀷
        
        Returns:
            List[DictItem]: 瀛楀吀椤瑰垪琛?        """
        return self.dict_item_repo.get_by_dict_type(dict_type)
    
    def update_dict_item(self, dict_item_id: str, dict_item_data: DictType[str, Any]) -> Optional[DictItem]:
        """
        鏇存柊瀛楀吀椤?        
        Args:
            dict_item_id: 瀛楀吀椤笽D
            dict_item_data: 瀛楀吀椤规暟鎹?        
        Returns:
            Optional[DictItem]: 鏇存柊鍚庣殑瀛楀吀椤瑰璞★紝涓嶅瓨鍦ㄨ繑鍥濶one
        """
        logger.info(f"鏇存柊瀛楀吀椤? dict_item_id={dict_item_id}")
        
        dict_item = self.dict_item_repo.get_by_id(dict_item_id)
        if not dict_item:
            return None
        
        # 鏇存柊瀛楀吀椤?        for key, value in dict_item_data.items():
            if hasattr(dict_item, key):
                setattr(dict_item, key, value)
        
        return self.dict_item_repo.update(dict_item)
    
    def delete_dict_item(self, dict_item_id: str) -> bool:
        """
        鍒犻櫎瀛楀吀椤?        
        Args:
            dict_item_id: 瀛楀吀椤笽D
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎瀛楀吀椤? dict_item_id={dict_item_id}")
        return self.dict_item_repo.delete(dict_item_id)
    
    def count_dict_items(self, dict_id: str) -> int:
        """
        缁熻瀛楀吀鐨勫瓧鍏搁」鏁伴噺
        
        Args:
            dict_id: 瀛楀吀ID
        
        Returns:
            int: 瀛楀吀椤规暟閲?        """
        return self.dict_item_repo.count_by_dict(dict_id)
