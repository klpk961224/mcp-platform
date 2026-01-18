# -*- coding: utf-8 -*-
"""
数据范围权限服务

功能说明：
1. 数据范围CRUD操作
2. 用户数据范围权限配置
3. 数据范围权限检查

使用示例：
    from app.services.data_scope_service import DataScopeService
    
    data_scope_service = DataScopeService(db)
    # 检查用户是否有权限访问部门数据
    has_access = data_scope_service.check_data_scope("user_001", "department", "dept_001")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.data_scope import DataScope, UserDataScope
from app.repositories.data_scope_repository import DataScopeRepository, UserDataScopeRepository


class DataScopeService:
    """
    数据范围权限服务
    
    功能：
    - 数据范围CRUD操作
    - 用户数据范围权限配置
    - 数据范围权限检查
    
    使用方法：
        data_scope_service = DataScopeService(db)
        has_access = data_scope_service.check_data_scope("user_001", "department", "dept_001")
    """
    
    # 数据范围类型常量
    DATA_SCOPE_ALL = "all"  # 全部数据
    DATA_SCOPE_DEPARTMENT = "department"  # 本部门数据
    DATA_SCOPE_DEPARTMENT_AND_BELOW = "department_and_below"  # 本部门及以下数据
    DATA_SCOPE_SELF = "self"  # 仅本人数据
    
    def __init__(self, db: Session):
        """
        初始化数据范围权限服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.data_scope_repo = DataScopeRepository(db)
        self.user_data_scope_repo = UserDataScopeRepository(db)
    
    def create_data_scope(self, data_scope_data: Dict[str, Any]) -> DataScope:
        """
        创建数据范围
        
        Args:
            data_scope_data: 数据范围数据
        
        Returns:
            DataScope: 创建的数据范围对象
        
        Raises:
            ValueError: 数据范围编码已存在
        """
        logger.info(f"创建数据范围: name={data_scope_data.get('name')}, code={data_scope_data.get('code')}")
        
        # 检查数据范围编码是否已存在
        if self.data_scope_repo.exists_by_code(data_scope_data.get("code")):
            raise ValueError("数据范围编码已存在")
        
        # 创建数据范围
        data_scope = DataScope(**data_scope_data)
        return self.data_scope_repo.create(data_scope)
    
    def get_data_scope(self, data_scope_id: str) -> Optional[DataScope]:
        """
        获取数据范围
        
        Args:
            data_scope_id: 数据范围ID
        
        Returns:
            Optional[DataScope]: 数据范围对象，不存在返回None
        """
        return self.data_scope_repo.get_by_id(data_scope_id)
    
    def get_data_scope_by_code(self, code: str) -> Optional[DataScope]:
        """
        根据编码获取数据范围
        
        Args:
            code: 数据范围编码
        
        Returns:
            Optional[DataScope]: 数据范围对象，不存在返回None
        """
        return self.data_scope_repo.get_by_code(code)
    
    def list_data_scopes(self, page: int = 1, page_size: int = 10) -> List[DataScope]:
        """
        获取数据范围列表
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DataScope]: 数据范围列表
        """
        return self.data_scope_repo.get_all(page, page_size)
    
    def set_user_data_scope(self, user_id: str, module: str, data_scope_code: str) -> UserDataScope:
        """
        设置用户的数据范围权限
        
        Args:
            user_id: 用户ID
            module: 模块
            data_scope_code: 数据范围编码
        
        Returns:
            UserDataScope: 创建的用户数据范围对象
        
        Raises:
            ValueError: 数据范围不存在
        """
        logger.info(f"设置用户数据范围: user_id={user_id}, module={module}, data_scope_code={data_scope_code}")
        
        # 获取数据范围
        data_scope = self.data_scope_repo.get_by_code(data_scope_code)
        if not data_scope:
            raise ValueError("数据范围不存在")
        
        # 检查是否已存在
        existing = self.user_data_scope_repo.get_by_user_module(user_id, module)
        if existing:
            # 更新
            existing.data_scope_id = data_scope.id
            return self.user_data_scope_repo.update(existing)
        else:
            # 创建
            user_data_scope = UserDataScope(
                user_id=user_id,
                module=module,
                data_scope_id=data_scope.id
            )
            return self.user_data_scope_repo.create(user_data_scope)
    
    def get_user_data_scope(self, user_id: str, module: str) -> Optional[UserDataScope]:
        """
        获取用户的数据范围权限
        
        Args:
            user_id: 用户ID
            module: 模块
        
        Returns:
            Optional[UserDataScope]: 用户数据范围对象，不存在返回None
        """
        return self.user_data_scope_repo.get_by_user_module(user_id, module)
    
    def check_data_scope(self, user_id: str, module: str, target_id: str, user_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        检查用户是否有权限访问目标数据
        
        Args:
            user_id: 用户ID
            module: 模块
            target_id: 目标数据ID
            user_info: 用户信息（包含department_id等）
        
        Returns:
            bool: 是否有权限
        """
        logger.debug(f"检查数据范围权限: user_id={user_id}, module={module}, target_id={target_id}")
        
        # 获取用户的数据范围
        user_data_scope = self.get_user_data_scope(user_id, module)
        if not user_data_scope:
            # 默认为仅本人数据
            data_scope_code = self.DATA_SCOPE_SELF
        else:
            data_scope_code = user_data_scope.data_scope.code
        
        # 根据数据范围类型检查权限
        if data_scope_code == self.DATA_SCOPE_ALL:
            # 全部数据：有权限
            return True
        elif data_scope_code == self.DATA_SCOPE_DEPARTMENT:
            # 本部门数据：检查是否属于同一部门
            if not user_info:
                return False
            user_department_id = user_info.get("department_id")
            if not user_department_id:
                return False
            return self._check_same_department(target_id, user_department_id, module)
        elif data_scope_code == self.DATA_SCOPE_DEPARTMENT_AND_BELOW:
            # 本部门及以下数据：检查是否属于本部门或子部门
            if not user_info:
                return False
            user_department_id = user_info.get("department_id")
            if not user_department_id:
                return False
            return self._check_department_and_below(target_id, user_department_id, module)
        elif data_scope_code == self.DATA_SCOPE_SELF:
            # 仅本人数据：检查是否是本人
            return target_id == user_id
        else:
            # 未知数据范围类型：默认无权限
            return False
    
    def _check_same_department(self, target_id: str, user_department_id: str, module: str) -> bool:
        """
        检查目标是否属于同一部门
        
        Args:
            target_id: 目标ID
            user_department_id: 用户部门ID
            module: 模块
        
        Returns:
            bool: 是否属于同一部门
        """
        # 根据模块查询目标数据的部门ID
        target_department_id = self._get_target_department_id(target_id, module)
        if not target_department_id:
            return False
        return target_department_id == user_department_id
    
    def _check_department_and_below(self, target_id: str, user_department_id: str, module: str) -> bool:
        """
        检查目标是否属于本部门或子部门
        
        Args:
            target_id: 目标ID
            user_department_id: 用户部门ID
            module: 模块
        
        Returns:
            bool: 是否属于本部门或子部门
        """
        # 根据模块查询目标数据的部门ID
        target_department_id = self._get_target_department_id(target_id, module)
        if not target_department_id:
            return False
        
        # 如果是同一部门，有权限
        if target_department_id == user_department_id:
            return True
        
        # 检查是否是子部门
        return self._is_child_department(target_department_id, user_department_id)
    
    def _is_child_department(self, child_id: str, parent_id: str) -> bool:
        """
        检查是否是子部门
        
        Args:
            child_id: 子部门ID
            parent_id: 父部门ID
        
        Returns:
            bool: 是否是子部门
        """
        from common.database.models.user import Department
        
        # 获取父部门的所有子部门
        child_departments = self.db.query(Department).filter(
            Department.parent_id == parent_id
        ).all()
        
        # 检查是否是直接子部门
        if any(dept.id == child_id for dept in child_departments):
            return True
        
        # 递归检查子部门的子部门
        for dept in child_departments:
            if self._is_child_department(child_id, dept.id):
                return True
        
        return False
    
    def _get_target_department_id(self, target_id: str, module: str) -> Optional[str]:
        """
        获取目标数据的部门ID
        
        Args:
            target_id: 目标ID
            module: 模块
        
        Returns:
            Optional[str]: 部门ID
        """
        if module == "user":
            # 查询用户的部门ID
            from common.database.models.user import User
            user = self.db.query(User).filter(User.id == target_id).first()
            return user.department_id if user else None
        elif module == "department":
            # 查询部门的父部门ID
            from common.database.models.user import Department
            department = self.db.query(Department).filter(Department.id == target_id).first()
            return department.parent_id if department else None
        else:
            return None