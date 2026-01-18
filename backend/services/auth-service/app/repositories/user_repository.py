# -*- coding: utf-8 -*-
"""
鐢ㄦ埛鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 鐢ㄦ埛CRUD鎿嶄綔
2. 鐢ㄦ埛鏌ヨ鎿嶄綔
3. 鐢ㄦ埛缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.user_repository import UserRepository
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_username("admin")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from loguru import logger
from common.database.models.user import User


class UserRepository:
    """
    鐢ㄦ埛鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鐢ㄦ埛CRUD鎿嶄綔
    - 鐢ㄦ埛鏌ヨ鎿嶄綔
    - 鐢ㄦ埛缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        user_repo = UserRepository(db)
        user = user_repo.get_by_username("admin")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栫敤鎴锋暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, user: User) -> User:
        """
        鍒涘缓鐢ㄦ埛
        
        Args:
            user: 鐢ㄦ埛瀵硅薄
        
        Returns:
            User: 鍒涘缓鐨勭敤鎴峰璞?        """
        logger.info(f"鍒涘缓鐢ㄦ埛: username={user.username}")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        鏍规嵁ID鑾峰彇鐢ㄦ埛
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        鏍规嵁鐢ㄦ埛鍚嶈幏鍙栫敤鎴?        
        Args:
            username: 鐢ㄦ埛鍚?        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        鏍规嵁閭鑾峰彇鐢ㄦ埛
        
        Args:
            email: 閭
        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_phone(self, phone: str) -> Optional[User]:
        """
        鏍规嵁鎵嬫満鍙疯幏鍙栫敤鎴?        
        Args:
            phone: 鎵嬫満鍙?        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.phone == phone).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[User]:
        """
        鏍规嵁绉熸埛ID鑾峰彇鐢ㄦ埛鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(User).filter(User.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[User]:
        """
        鑾峰彇鎵€鏈夌敤鎴?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(User).offset(offset).limit(page_size).all()
    
    def update(self, user: User) -> User:
        """
        鏇存柊鐢ㄦ埛
        
        Args:
            user: 鐢ㄦ埛瀵硅薄
        
        Returns:
            User: 鏇存柊鍚庣殑鐢ㄦ埛瀵硅薄
        """
        logger.info(f"鏇存柊鐢ㄦ埛: user_id={user.id}")
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str) -> bool:
        """
        鍒犻櫎鐢ㄦ埛
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎鐢ㄦ埛: user_id={user_id}")
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛鐢ㄦ埛鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            int: 鐢ㄦ埛鏁伴噺
        """
        return self.db.query(User).filter(User.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夌敤鎴锋暟閲?        
        Returns:
            int: 鐢ㄦ埛鏁伴噺
        """
        return self.db.query(User).count()
