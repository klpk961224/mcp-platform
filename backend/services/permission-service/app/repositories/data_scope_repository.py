# -*- coding: utf-8 -*-
"""
鏁版嵁鑼冨洿鏉冮檺鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 鏁版嵁鑼冨洿CRUD鎿嶄綔
2. 鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺鎿嶄綔
3. 鏁版嵁鑼冨洿鏉冮檺鏌ヨ

浣跨敤绀轰緥锛?    from app.repositories.data_scope_repository import DataScopeRepository
    
    data_scope_repo = DataScopeRepository(db)
    data_scope = data_scope_repo.get_by_code("department")
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from loguru import logger

from common.database.models.data_scope import DataScope, UserDataScope


class DataScopeRepository:
    """
    鏁版嵁鑼冨洿鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鏁版嵁鑼冨洿CRUD鎿嶄綔
    - 鏁版嵁鑼冨洿鏌ヨ鎿嶄綔
    
    浣跨敤鏂规硶锛?        data_scope_repo = DataScopeRepository(db)
        data_scope = data_scope_repo.get_by_code("department")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨暟鎹寖鍥存暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, data_scope: DataScope) -> DataScope:
        """
        鍒涘缓鏁版嵁鑼冨洿
        
        Args:
            data_scope: 鏁版嵁鑼冨洿瀵硅薄
        
        Returns:
            DataScope: 鍒涘缓鐨勬暟鎹寖鍥村璞?        """
        logger.info(f"鍒涘缓鏁版嵁鑼冨洿: name={data_scope.name}, code={data_scope.code}")
        self.db.add(data_scope)
        self.db.commit()
        self.db.refresh(data_scope)
        return data_scope
    
    def get_by_id(self, data_scope_id: str) -> Optional[DataScope]:
        """
        鏍规嵁ID鑾峰彇鏁版嵁鑼冨洿
        
        Args:
            data_scope_id: 鏁版嵁鑼冨洿ID
        
        Returns:
            Optional[DataScope]: 鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(DataScope).filter(DataScope.id == data_scope_id).first()
    
    def get_by_code(self, code: str) -> Optional[DataScope]:
        """
        鏍规嵁缂栫爜鑾峰彇鏁版嵁鑼冨洿
        
        Args:
            code: 鏁版嵁鑼冨洿缂栫爜
        
        Returns:
            Optional[DataScope]: 鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(DataScope).filter(DataScope.code == code).first()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[DataScope]:
        """
        鑾峰彇鎵€鏈夋暟鎹寖鍥?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[DataScope]: 鏁版嵁鑼冨洿鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(DataScope).order_by(DataScope.level).offset(offset).limit(page_size).all()
    
    def update(self, data_scope: DataScope) -> DataScope:
        """
        鏇存柊鏁版嵁鑼冨洿
        
        Args:
            data_scope: 鏁版嵁鑼冨洿瀵硅薄
        
        Returns:
            DataScope: 鏇存柊鍚庣殑鏁版嵁鑼冨洿瀵硅薄
        """
        logger.info(f"鏇存柊鏁版嵁鑼冨洿: data_scope_id={data_scope.id}")
        self.db.commit()
        self.db.refresh(data_scope)
        return data_scope
    
    def delete(self, data_scope_id: str) -> bool:
        """
        鍒犻櫎鏁版嵁鑼冨洿
        
        Args:
            data_scope_id: 鏁版嵁鑼冨洿ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎鏁版嵁鑼冨洿: data_scope_id={data_scope_id}")
        data_scope = self.get_by_id(data_scope_id)
        if not data_scope:
            return False
        
        # 妫€鏌ユ槸鍚︽湁鐢ㄦ埛浣跨敤
        if data_scope.user_data_scopes:
            raise ValueError("鏃犳硶鍒犻櫎鏁版嵁鑼冨洿锛氳鏁版嵁鑼冨洿琚敤鎴蜂娇鐢?)
        
        self.db.delete(data_scope)
        self.db.commit()
        return True
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夋暟鎹寖鍥存暟閲?        
        Returns:
            int: 鏁版嵁鑼冨洿鏁伴噺
        """
        return self.db.query(DataScope).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€鏌ユ暟鎹寖鍥寸紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 鏁版嵁鑼冨洿缂栫爜
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(DataScope).filter(DataScope.code == code).first() is not None


class UserDataScopeRepository:
    """
    鐢ㄦ埛鏁版嵁鑼冨洿鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鐢ㄦ埛鏁版嵁鑼冨洿CRUD鎿嶄綔
    - 鐢ㄦ埛鏁版嵁鑼冨洿鏌ヨ鎿嶄綔
    
    浣跨敤鏂规硶锛?        user_data_scope_repo = UserDataScopeRepository(db)
        user_data_scope = user_data_scope_repo.get_by_user_module("user_001", "user")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栫敤鎴锋暟鎹寖鍥存暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, user_data_scope: UserDataScope) -> UserDataScope:
        """
        鍒涘缓鐢ㄦ埛鏁版嵁鑼冨洿
        
        Args:
            user_data_scope: 鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄
        
        Returns:
            UserDataScope: 鍒涘缓鐨勭敤鎴锋暟鎹寖鍥村璞?        """
        logger.info(f"鍒涘缓鐢ㄦ埛鏁版嵁鑼冨洿: user_id={user_data_scope.user_id}, module={user_data_scope.module}")
        self.db.add(user_data_scope)
        self.db.commit()
        self.db.refresh(user_data_scope)
        return user_data_scope
    
    def get_by_id(self, user_data_scope_id: str) -> Optional[UserDataScope]:
        """
        鏍规嵁ID鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿
        
        Args:
            user_data_scope_id: 鐢ㄦ埛鏁版嵁鑼冨洿ID
        
        Returns:
            Optional[UserDataScope]: 鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(UserDataScope).filter(UserDataScope.id == user_data_scope_id).first()
    
    def get_by_user_module(self, user_id: str, module: str) -> Optional[UserDataScope]:
        """
        鏍规嵁鐢ㄦ埛ID鍜屾ā鍧楄幏鍙栫敤鎴锋暟鎹寖鍥?        
        Args:
            user_id: 鐢ㄦ埛ID
            module: 妯″潡
        
        Returns:
            Optional[UserDataScope]: 鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(UserDataScope).filter(
            and_(
                UserDataScope.user_id == user_id,
                UserDataScope.module == module
            )
        ).first()
    
    def get_by_user_id(self, user_id: str) -> List[UserDataScope]:
        """
        鏍规嵁鐢ㄦ埛ID鑾峰彇鎵€鏈夋暟鎹寖鍥?        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            List[UserDataScope]: 鐢ㄦ埛鏁版嵁鑼冨洿鍒楄〃
        """
        return self.db.query(UserDataScope).filter(UserDataScope.user_id == user_id).all()
    
    def update(self, user_data_scope: UserDataScope) -> UserDataScope:
        """
        鏇存柊鐢ㄦ埛鏁版嵁鑼冨洿
        
        Args:
            user_data_scope: 鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄
        
        Returns:
            UserDataScope: 鏇存柊鍚庣殑鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄
        """
        logger.info(f"鏇存柊鐢ㄦ埛鏁版嵁鑼冨洿: user_data_scope_id={user_data_scope.id}")
        self.db.commit()
        self.db.refresh(user_data_scope)
        return user_data_scope
    
    def delete(self, user_data_scope_id: str) -> bool:
        """
        鍒犻櫎鐢ㄦ埛鏁版嵁鑼冨洿
        
        Args:
            user_data_scope_id: 鐢ㄦ埛鏁版嵁鑼冨洿ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎鐢ㄦ埛鏁版嵁鑼冨洿: user_data_scope_id={user_data_scope_id}")
        user_data_scope = self.get_by_id(user_data_scope_id)
        if not user_data_scope:
            return False
        
        self.db.delete(user_data_scope)
        self.db.commit()
        return True
    
    def count_by_user(self, user_id: str) -> int:
        """
        缁熻鐢ㄦ埛鐨勬暟鎹寖鍥存暟閲?        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            int: 鏁版嵁鑼冨洿鏁伴噺
        """
        return self.db.query(UserDataScope).filter(UserDataScope.user_id == user_id).count()
