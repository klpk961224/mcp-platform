# -*- coding: utf-8 -*-
"""
宀椾綅鏈嶅姟

鍔熻兘璇存槑锛?1. 宀椾綅CRUD鎿嶄綔
2. 宀椾綅查询鎿嶄綔
3. 宀椾綅缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.services.position_service import PositionService
    
    position_service = PositionService(db)
    position = position_service.create_position(name="寮€鍙戝伐绋嬪笀", code="developer")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.position import Position
from app.repositories.position_repository import PositionRepository


class PositionService:
    """
    宀椾綅鏈嶅姟
    
    鍔熻兘锛?    - 宀椾綅CRUD鎿嶄綔
    - 宀椾綅查询鎿嶄綔
    - 宀椾綅缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        position_service = PositionService(db)
        position = position_service.create_position(name="寮€鍙戝伐绋嬪笀", code="developer")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧矖浣嶆湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.position_repo = PositionRepository(db)
    
    def create_position(self, position_data: Dict[str, Any]) -> Position:
        """
        创建宀椾綅
        
        Args:
            position_data: 宀椾綅鏁版嵁
        
        Returns:
            Position: 创建鐨勫矖浣嶅璞?        
        Raises:
            ValueError: 宀椾綅编码宸插瓨鍦?        """
        logger.info(f"创建宀椾綅: name={position_data.get('name')}, code={position_data.get('code')}")
        
        # 妫€鏌ュ矖浣嶇紪鐮佹槸鍚﹀凡瀛樺湪
        if self.position_repo.exists_by_code(position_data.get("code")):
            raise ValueError("宀椾綅编码宸插瓨鍦?)
        
        # 创建宀椾綅
        position = Position(**position_data)
        return self.position_repo.create(position)
    
    def get_position(self, position_id: str) -> Optional[Position]:
        """
        鑾峰彇宀椾綅
        
        Args:
            position_id: 岗位ID
        
        Returns:
            Optional[Position]: 宀椾綅瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.position_repo.get_by_id(position_id)
    
    def get_position_by_code(self, code: str) -> Optional[Position]:
        """
        根据编码鑾峰彇宀椾綅
        
        Args:
            code: 宀椾綅编码
        
        Returns:
            Optional[Position]: 宀椾綅瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.position_repo.get_by_code(code)
    
    def update_position(self, position_id: str, position_data: Dict[str, Any]) -> Optional[Position]:
        """
        更新宀椾綅
        
        Args:
            position_id: 岗位ID
            position_data: 宀椾綅鏁版嵁
        
        Returns:
            Optional[Position]: 更新鍚庣殑宀椾綅瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"更新宀椾綅: position_id={position_id}")
        
        position = self.position_repo.get_by_id(position_id)
        if not position:
            return None
        
        # 更新宀椾綅
        for key, value in position_data.items():
            if hasattr(position, key):
                setattr(position, key, value)
        
        return self.position_repo.update(position)
    
    def delete_position(self, position_id: str) -> bool:
        """
        删除宀椾綅
        
        Args:
            position_id: 岗位ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除宀椾綅: position_id={position_id}")
        return self.position_repo.delete(position_id)
    
    def list_positions(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                      page: int = 1, page_size: int = 10) -> List[Position]:
        """
        鑾峰彇宀椾綅鍒楄〃
        
        Args:
            tenant_id: 租户ID锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Position]: 宀椾綅鍒楄〃
        """
        if keyword:
            return self.position_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.position_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.position_repo.get_all(page, page_size)
    
    def count_positions(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻宀椾綅数量
        
        Args:
            tenant_id: 租户ID锛堝彲閫夛級
        
        Returns:
            int: 宀椾綅数量
        """
        if tenant_id:
            return self.position_repo.count_by_tenant(tenant_id)
        else:
            return self.position_repo.count_all()
