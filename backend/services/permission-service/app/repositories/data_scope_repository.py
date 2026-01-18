# -*- coding: utf-8 -*-
"""
数据范围权限数据访问层

功能说明：
1. 数据范围CRUD操作
2. 用户数据范围权限操作
3. 数据范围权限查询

使用示例：
    from app.repositories.data_scope_repository import DataScopeRepository
    
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
    数据范围数据访问层
    
    功能：
    - 数据范围CRUD操作
    - 数据范围查询操作
    
    使用方法：
        data_scope_repo = DataScopeRepository(db)
        data_scope = data_scope_repo.get_by_code("department")
    """
    
    def __init__(self, db: Session):
        """
        初始化数据范围数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, data_scope: DataScope) -> DataScope:
        """
        创建数据范围
        
        Args:
            data_scope: 数据范围对象
        
        Returns:
            DataScope: 创建的数据范围对象
        """
        logger.info(f"创建数据范围: name={data_scope.name}, code={data_scope.code}")
        self.db.add(data_scope)
        self.db.commit()
        self.db.refresh(data_scope)
        return data_scope
    
    def get_by_id(self, data_scope_id: str) -> Optional[DataScope]:
        """
        根据ID获取数据范围
        
        Args:
            data_scope_id: 数据范围ID
        
        Returns:
            Optional[DataScope]: 数据范围对象，不存在返回None
        """
        return self.db.query(DataScope).filter(DataScope.id == data_scope_id).first()
    
    def get_by_code(self, code: str) -> Optional[DataScope]:
        """
        根据编码获取数据范围
        
        Args:
            code: 数据范围编码
        
        Returns:
            Optional[DataScope]: 数据范围对象，不存在返回None
        """
        return self.db.query(DataScope).filter(DataScope.code == code).first()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[DataScope]:
        """
        获取所有数据范围
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataScope]: 数据范围列表
        """
        offset = (page - 1) * page_size
        return self.db.query(DataScope).order_by(DataScope.level).offset(offset).limit(page_size).all()
    
    def update(self, data_scope: DataScope) -> DataScope:
        """
        更新数据范围
        
        Args:
            data_scope: 数据范围对象
        
        Returns:
            DataScope: 更新后的数据范围对象
        """
        logger.info(f"更新数据范围: data_scope_id={data_scope.id}")
        self.db.commit()
        self.db.refresh(data_scope)
        return data_scope
    
    def delete(self, data_scope_id: str) -> bool:
        """
        删除数据范围
        
        Args:
            data_scope_id: 数据范围ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除数据范围: data_scope_id={data_scope_id}")
        data_scope = self.get_by_id(data_scope_id)
        if not data_scope:
            return False
        
        # 检查是否有用户使用
        if data_scope.user_data_scopes:
            raise ValueError("无法删除数据范围：该数据范围被用户使用")
        
        self.db.delete(data_scope)
        self.db.commit()
        return True
    
    def count_all(self) -> int:
        """
        统计所有数据范围数量
        
        Returns:
            int: 数据范围数量
        """
        return self.db.query(DataScope).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查数据范围编码是否存在
        
        Args:
            code: 数据范围编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(DataScope).filter(DataScope.code == code).first() is not None


class UserDataScopeRepository:
    """
    用户数据范围数据访问层
    
    功能：
    - 用户数据范围CRUD操作
    - 用户数据范围查询操作
    
    使用方法：
        user_data_scope_repo = UserDataScopeRepository(db)
        user_data_scope = user_data_scope_repo.get_by_user_module("user_001", "user")
    """
    
    def __init__(self, db: Session):
        """
        初始化用户数据范围数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, user_data_scope: UserDataScope) -> UserDataScope:
        """
        创建用户数据范围
        
        Args:
            user_data_scope: 用户数据范围对象
        
        Returns:
            UserDataScope: 创建的用户数据范围对象
        """
        logger.info(f"创建用户数据范围: user_id={user_data_scope.user_id}, module={user_data_scope.module}")
        self.db.add(user_data_scope)
        self.db.commit()
        self.db.refresh(user_data_scope)
        return user_data_scope
    
    def get_by_id(self, user_data_scope_id: str) -> Optional[UserDataScope]:
        """
        根据ID获取用户数据范围
        
        Args:
            user_data_scope_id: 用户数据范围ID
        
        Returns:
            Optional[UserDataScope]: 用户数据范围对象，不存在返回None
        """
        return self.db.query(UserDataScope).filter(UserDataScope.id == user_data_scope_id).first()
    
    def get_by_user_module(self, user_id: str, module: str) -> Optional[UserDataScope]:
        """
        根据用户ID和模块获取用户数据范围
        
        Args:
            user_id: 用户ID
            module: 模块
        
        Returns:
            Optional[UserDataScope]: 用户数据范围对象，不存在返回None
        """
        return self.db.query(UserDataScope).filter(
            and_(
                UserDataScope.user_id == user_id,
                UserDataScope.module == module
            )
        ).first()
    
    def get_by_user_id(self, user_id: str) -> List[UserDataScope]:
        """
        根据用户ID获取所有数据范围
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[UserDataScope]: 用户数据范围列表
        """
        return self.db.query(UserDataScope).filter(UserDataScope.user_id == user_id).all()
    
    def update(self, user_data_scope: UserDataScope) -> UserDataScope:
        """
        更新用户数据范围
        
        Args:
            user_data_scope: 用户数据范围对象
        
        Returns:
            UserDataScope: 更新后的用户数据范围对象
        """
        logger.info(f"更新用户数据范围: user_data_scope_id={user_data_scope.id}")
        self.db.commit()
        self.db.refresh(user_data_scope)
        return user_data_scope
    
    def delete(self, user_data_scope_id: str) -> bool:
        """
        删除用户数据范围
        
        Args:
            user_data_scope_id: 用户数据范围ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除用户数据范围: user_data_scope_id={user_data_scope_id}")
        user_data_scope = self.get_by_id(user_data_scope_id)
        if not user_data_scope:
            return False
        
        self.db.delete(user_data_scope)
        self.db.commit()
        return True
    
    def count_by_user(self, user_id: str) -> int:
        """
        统计用户的数据范围数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 数据范围数量
        """
        return self.db.query(UserDataScope).filter(UserDataScope.user_id == user_id).count()