# -*- coding: utf-8 -*-
"""
用户服务

功能说明：
1. 用户CRUD操作
2. 用户查询操作
3. 用户状态管理

使用示例：
    from app.services.user_service import UserService
    
    user_service = UserService(db)
    user = user_service.create_user(username="admin", email="admin@example.com")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.tenant_repository import TenantRepository


class UserService:
    """
    用户服务
    
    功能：
    - 用户CRUD操作
    - 用户查询操作
    - 用户状态管理
    
    使用方法：
        user_service = UserService(db)
        user = user_service.create_user(username="admin", email="admin@example.com")
    """
    
    def __init__(self, db: Session):
        """
        初始化用户服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.tenant_repo = TenantRepository(db)
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        创建用户
        
        Args:
            user_data: 用户数据
        
        Returns:
            User: 创建的用户对象
        
        Raises:
            ValueError: 用户名或邮箱已存在
            ValueError: 部门不存在
            ValueError: 租户不存在
            ValueError: 租户已过期
            ValueError: 租户用户数已达上限
        """
        logger.info(f"创建用户: username={user_data.get('username')}")
        
        # 检查用户名是否已存在
        if self.user_repo.exists_by_username(user_data.get("username")):
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        if self.user_repo.exists_by_email(user_data.get("email")):
            raise ValueError("邮箱已存在")
        
        # 验证租户
        tenant_id = user_data.get("tenant_id")
        if tenant_id:
            tenant = self.tenant_repo.get_by_id(tenant_id)
            if not tenant:
                raise ValueError("租户不存在")
            if tenant.is_expired():
                raise ValueError("租户已过期")
            if not tenant.can_add_user():
                raise ValueError("租户用户数已达上限")
        
        # 验证部门
        dept_id = user_data.get("dept_id")
        if dept_id:
            department = self.dept_repo.get_by_id(dept_id)
            if not department:
                raise ValueError("部门不存在")
            if tenant_id and department.tenant_id != tenant_id:
                raise ValueError("部门不属于该租户")
        
        # 创建用户
        user = User(**user_data)
        return self.user_repo.create(user)
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        获取用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 用户对象，不存在返回None
        """
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            Optional[User]: 用户对象，不存在返回None
        """
        return self.user_repo.get_by_username(username)
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        """
        更新用户
        
        Args:
            user_id: 用户ID
            user_data: 用户数据
        
        Returns:
            Optional[User]: 更新后的用户对象，不存在返回None
        
        Raises:
            ValueError: 邮箱已被其他用户使用
            ValueError: 部门不存在
            ValueError: 部门不属于该租户
        """
        logger.info(f"更新用户: user_id={user_id}")
        
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        # 检查邮箱是否被其他用户使用
        if "email" in user_data and user_data["email"] != user.email:
            if self.user_repo.exists_by_email(user_data["email"]):
                raise ValueError("邮箱已被其他用户使用")
        
        # 验证部门
        if "department_id" in user_data and user_data["department_id"]:
            department = self.dept_repo.get_by_id(user_data["department_id"])
            if not department:
                raise ValueError("部门不存在")
            if department.tenant_id != user.tenant_id:
                raise ValueError("部门不属于该租户")
        
        # 更新用户
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return self.user_repo.update(user)
    
    def delete_user(self, user_id: str) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除用户: user_id={user_id}")
        return self.user_repo.delete(user_id)
    
    def list_users(self, tenant_id: Optional[str] = None, department_id: Optional[str] = None, 
                   keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[User]:
        """
        获取用户列表
        
        Args:
            tenant_id: 租户ID（可选）
            department_id: 部门ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[User]: 用户列表
        """
        if keyword:
            return self.user_repo.search(keyword, tenant_id, page, page_size)
        elif department_id:
            return self.user_repo.get_by_department_id(department_id, page, page_size)
        elif tenant_id:
            return self.user_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.user_repo.get_all(page, page_size)
    
    def activate_user(self, user_id: str) -> Optional[User]:
        """
        激活用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 更新后的用户对象，不存在返回None
        """
        logger.info(f"激活用户: user_id={user_id}")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        user.is_active = True
        user.status = "active"
        return self.user_repo.update(user)
    
    def deactivate_user(self, user_id: str) -> Optional[User]:
        """
        停用用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 更新后的用户对象，不存在返回None
        """
        logger.info(f"停用用户: user_id={user_id}")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        user.is_active = False
        user.status = "inactive"
        return self.user_repo.update(user)
    
    def count_users(self, tenant_id: Optional[str] = None, department_id: Optional[str] = None) -> int:
        """
        统计用户数量
        
        Args:
            tenant_id: 租户ID（可选）
            department_id: 部门ID（可选）
        
        Returns:
            int: 用户数量
        """
        if department_id:
            return self.user_repo.count_by_department(department_id)
        elif tenant_id:
            return self.user_repo.count_by_tenant(tenant_id)
        else:
            return self.user_repo.count_all()