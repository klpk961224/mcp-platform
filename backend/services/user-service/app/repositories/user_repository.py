# -*- coding: utf-8 -*-
"""
用户数据访问层

功能说明：
1. 用户CRUD操作
2. 用户查询操作
3. 用户统计操作

使用示例：
    from app.repositories.user_repository import UserRepository
    
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
    用户数据访问层
    
    功能：
    - 用户CRUD操作
    - 用户查询操作
    - 用户统计操作
    
    使用方法：
        user_repo = UserRepository(db)
        user = user_repo.get_by_username("admin")
    """
    
    def __init__(self, db: Session):
        """
        初始化用户数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, user: User) -> User:
        """
        创建用户
        
        Args:
            user: 用户对象
        
        Returns:
            User: 创建的用户对象
        """
        logger.info(f"创建用户: username={user.username}, tenant_id={user.tenant_id}")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        根据ID获取用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 用户对象，不存在返回None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            Optional[User]: 用户对象，不存在返回None
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            email: 邮箱
        
        Returns:
            Optional[User]: 用户对象，不存在返回None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[User]:
        """
        根据租户ID获取用户列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[User]: 用户列表
        """
        offset = (page - 1) * page_size
        return self.db.query(User).filter(User.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_department_id(self, department_id: str, page: int = 1, page_size: int = 10) -> List[User]:
        """
        根据部门ID获取用户列表
        
        Args:
            department_id: 部门ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[User]: 用户列表
        """
        offset = (page - 1) * page_size
        return self.db.query(User).filter(User.dept_id == department_id).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[User]:
        """
        搜索用户
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[User]: 用户列表
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
        获取所有用户
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[User]: 用户列表
        """
        offset = (page - 1) * page_size
        return self.db.query(User).offset(offset).limit(page_size).all()
    
    def update(self, user: User) -> User:
        """
        更新用户
        
        Args:
            user: 用户对象
        
        Returns:
            User: 更新后的用户对象
        """
        logger.info(f"更新用户: user_id={user.id}")
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除用户: user_id={user_id}")
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户用户数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 用户数量
        """
        return self.db.query(User).filter(User.tenant_id == tenant_id).count()
    
    def count_by_department(self, department_id: str) -> int:
        """
        统计部门用户数量
        
        Args:
            department_id: 部门ID
        
        Returns:
            int: 用户数量
        """
        return self.db.query(User).filter(User.department_id == department_id).count()
    
    def count_all(self) -> int:
        """
        统计所有用户数量
        
        Returns:
            int: 用户数量
        """
        return self.db.query(User).count()
    
    def exists_by_username(self, username: str) -> bool:
        """
        检查用户名是否存在
        
        Args:
            username: 用户名
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(User).filter(User.username == username).first() is not None
    
    def exists_by_email(self, email: str) -> bool:
        """
        检查邮箱是否存在
        
        Args:
            email: 邮箱
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(User).filter(User.email == email).first() is not None