# -*- coding: utf-8 -*-
"""
鐢ㄦ埛鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 鐢ㄦ埛CRUD鎿嶄綔
2. 鐢ㄦ埛查询鎿嶄綔
3. 鐢ㄦ埛缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.user_repository import UserRepository
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_username("admin")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.user import User


class UserRepository:
    """
    鐢ㄦ埛鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鐢ㄦ埛CRUD鎿嶄綔
    - 鐢ㄦ埛查询鎿嶄綔
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
        创建鐢ㄦ埛
        
        Args:
            user: 鐢ㄦ埛瀵硅薄
        
        Returns:
            User: 创建鐨勭敤鎴峰璞?        """
        logger.info(f"创建鐢ㄦ埛: username={user.username}, tenant_id={user.tenant_id}")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        根据ID鑾峰彇鐢ㄦ埛
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名嶈幏鍙栫敤鎴?        
        Args:
            username: 用户名?        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱鑾峰彇鐢ㄦ埛
        
        Args:
            email: 邮箱
        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[User]:
        """
        根据租户ID鑾峰彇鐢ㄦ埛鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(User).filter(User.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_department_id(self, department_id: str, page: int = 1, page_size: int = 10) -> List[User]:
        """
        根据部门ID鑾峰彇鐢ㄦ埛鍒楄〃
        
        Args:
            department_id: 部门ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(User).filter(User.dept_id == department_id).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[User]:
        """
        鎼滅储鐢ㄦ埛
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        offset = (page - 1) * page_size
        query = self.db.query(User).filter(
            or_(
                User.username.like(f"%{keyword}%"),
                User.email.like(f"%{keyword}%"),
                User.full_name.like(f"%{keyword}%"),
                User.phone.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(User.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[User]:
        """
        鑾峰彇鎵€鏈夌敤鎴?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(User).offset(offset).limit(page_size).all()
    
    def update(self, user: User) -> User:
        """
        更新鐢ㄦ埛
        
        Args:
            user: 鐢ㄦ埛瀵硅薄
        
        Returns:
            User: 更新鍚庣殑鐢ㄦ埛瀵硅薄
        """
        logger.info(f"更新鐢ㄦ埛: user_id={user.id}")
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str) -> bool:
        """
        删除鐢ㄦ埛
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除鐢ㄦ埛: user_id={user_id}")
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛鐢ㄦ埛数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 鐢ㄦ埛数量
        """
        return self.db.query(User).filter(User.tenant_id == tenant_id).count()
    
    def count_by_department(self, department_id: str) -> int:
        """
        缁熻閮ㄩ棬鐢ㄦ埛数量
        
        Args:
            department_id: 部门ID
        
        Returns:
            int: 鐢ㄦ埛数量
        """
        return self.db.query(User).filter(User.department_id == department_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夌敤鎴锋暟閲?        
        Returns:
            int: 鐢ㄦ埛数量
        """
        return self.db.query(User).count()
    
    def exists_by_username(self, username: str) -> bool:
        """
        妫€鏌ョ敤鎴峰悕鏄惁瀛樺湪
        
        Args:
            username: 用户名?        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(User).filter(User.username == username).first() is not None
    
    def exists_by_email(self, email: str) -> bool:
        """
        妫€鏌ラ偖绠辨槸鍚﹀瓨鍦?        
        Args:
            email: 邮箱
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(User).filter(User.email == email).first() is not None
