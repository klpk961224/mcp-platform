# -*- coding: utf-8 -*-
"""
宀椾綅鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 宀椾綅CRUD鎿嶄綔
2. 宀椾綅查询鎿嶄綔
3. 宀椾綅缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.position_repository import PositionRepository
    
    position_repo = PositionRepository(db)
    position = position_repo.get_by_code("developer")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.position import Position


class PositionRepository:
    """
    宀椾綅鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 宀椾綅CRUD鎿嶄綔
    - 宀椾綅查询鎿嶄綔
    - 宀椾綅缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        position_repo = PositionRepository(db)
        position = position_repo.get_by_code("developer")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧矖浣嶆暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, position: Position) -> Position:
        """
        创建宀椾綅
        
        Args:
            position: 宀椾綅瀵硅薄
        
        Returns:
            Position: 创建鐨勫矖浣嶅璞?        """
        logger.info(f"创建宀椾綅: name={position.name}, code={position.code}, tenant_id={position.tenant_id}")
        self.db.add(position)
        self.db.commit()
        self.db.refresh(position)
        return position
    
    def get_by_id(self, position_id: str) -> Optional[Position]:
        """
        根据ID鑾峰彇宀椾綅
        
        Args:
            position_id: 岗位ID
        
        Returns:
            Optional[Position]: 宀椾綅瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Position).filter(Position.id == position_id).first()
    
    def get_by_code(self, code: str) -> Optional[Position]:
        """
        根据编码鑾峰彇宀椾綅
        
        Args:
            code: 宀椾綅编码
        
        Returns:
            Optional[Position]: 宀椾綅瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Position).filter(Position.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Position]:
        """
        根据租户ID鑾峰彇宀椾綅鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Position]: 宀椾綅鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Position).filter(Position.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Position]:
        """
        鎼滅储宀椾綅
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Position]: 宀椾綅鍒楄〃
        """
        offset = (page - 1) * page_size
        query = self.db.query(Position).filter(
            or_(
                Position.name.like(f"%{keyword}%"),
                Position.code.like(f"%{keyword}%"),
                Position.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Position.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Position]:
        """
        鑾峰彇鎵€鏈夊矖浣?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Position]: 宀椾綅鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Position).offset(offset).limit(page_size).all()
    
    def update(self, position: Position) -> Position:
        """
        更新宀椾綅
        
        Args:
            position: 宀椾綅瀵硅薄
        
        Returns:
            Position: 更新鍚庣殑宀椾綅瀵硅薄
        """
        logger.info(f"更新宀椾綅: position_id={position.id}")
        self.db.commit()
        self.db.refresh(position)
        return position
    
    def delete(self, position_id: str) -> bool:
        """
        删除宀椾綅
        
        Args:
            position_id: 岗位ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除宀椾綅: position_id={position_id}")
        position = self.get_by_id(position_id)
        if not position:
            return False
        
        self.db.delete(position)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛宀椾綅数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 宀椾綅数量
        """
        return self.db.query(Position).filter(Position.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夊矖浣嶆暟閲?        
        Returns:
            int: 宀椾綅数量
        """
        return self.db.query(Position).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€鏌ュ矖浣嶇紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 宀椾綅编码
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Position).filter(Position.code == code).first() is not None
