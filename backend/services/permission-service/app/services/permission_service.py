# -*- coding: utf-8 -*-
"""
权限服务

功能说明：
1. 权限CRUD操作
2. 权限查询操作
3. 权限验证操作

使用示例：
    from app.services.permission_service import PermissionService
    
    perm_service = PermissionService(db)
    perm = perm_service.create_permission(name="用户管理", code="user:manage")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository


class PermissionService:
    """
    权限服务
    
    功能：
    - 权限CRUD操作
    - 权限查询操作
    - 权限验证操作
    
    使用方法：
        perm_service = PermissionService(db)
        perm = perm_service.create_permission(name="用户管理", code="user:manage")
    """
    
    def __init__(self, db: Session):
        """
        初始化权限服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.perm_repo = PermissionRepository(db)
    
    def create_permission(self, permission_data: Dict[str, Any]) -> Permission:
        """
        创建权限
        
        Args:
            permission_data: 权限数据
        
        Returns:
            Permission: 创建的权限对象
        
        Raises:
            ValueError: 权限编码已存在
        """
        logger.info(f"创建权限: name={permission_data.get('name')}, code={permission_data.get('code')}")
        
        # 检查权限编码是否已存在
        if self.perm_repo.exists_by_code(permission_data.get("code")):
            raise ValueError("权限编码已存在")
        
        # 创建权限
        permission = Permission(**permission_data)
        return self.perm_repo.create(permission)
    
    def get_permission(self, permission_id: str) -> Optional[Permission]:
        """
        获取权限
        
        Args:
            permission_id: 权限ID
        
        Returns:
            Optional[Permission]: 权限对象，不存在返回None
        """
        return self.perm_repo.get_by_id(permission_id)
    
    def get_permission_by_code(self, code: str) -> Optional[Permission]:
        """
        根据编码获取权限
        
        Args:
            code: 权限编码
        
        Returns:
            Optional[Permission]: 权限对象，不存在返回None
        """
        return self.perm_repo.get_by_code(code)
    
    def update_permission(self, permission_id: str, permission_data: Dict[str, Any]) -> Optional[Permission]:
        """
        更新权限
        
        Args:
            permission_id: 权限ID
            permission_data: 权限数据
        
        Returns:
            Optional[Permission]: 更新后的权限对象，不存在返回None
        """
        logger.info(f"更新权限: permission_id={permission_id}")
        
        permission = self.perm_repo.get_by_id(permission_id)
        if not permission:
            return None
        
        # 更新权限
        for key, value in permission_data.items():
            if hasattr(permission, key):
                setattr(permission, key, value)
        
        return self.perm_repo.update(permission)
    
    def delete_permission(self, permission_id: str) -> bool:
        """
        删除权限
        
        Args:
            permission_id: 权限ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除权限: permission_id={permission_id}")
        return self.perm_repo.delete(permission_id)
    
    def list_permissions(self, tenant_id: Optional[str] = None, resource: Optional[str] = None,
                         permission_type: Optional[str] = None, keyword: Optional[str] = None,
                         page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        获取权限列表
        
        Args:
            tenant_id: 租户ID（可选）
            resource: 资源类型（可选）
            permission_type: 权限类型（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Permission]: 权限列表
        """
        if keyword:
            return self.perm_repo.search(keyword, tenant_id, page, page_size)
        elif resource:
            return self.perm_repo.get_by_resource(resource, page, page_size)
        elif permission_type:
            return self.perm_repo.get_by_type(permission_type, page, page_size)
        elif tenant_id:
            return self.perm_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.perm_repo.get_all(page, page_size)
    
    def count_permissions(self, tenant_id: Optional[str] = None, resource: Optional[str] = None) -> int:
        """
        统计权限数量
        
        Args:
            tenant_id: 租户ID（可选）
            resource: 资源类型（可选）
        
        Returns:
            int: 权限数量
        """
        if resource:
            return self.perm_repo.count_by_resource(resource)
        elif tenant_id:
            return self.perm_repo.count_by_tenant(tenant_id)
        else:
            return self.perm_repo.count_all()
    
    def check_user_permission(self, user_id: str, permission_code: str) -> bool:
        """
        检查用户是否拥有指定权限
        
        Args:
            user_id: 用户ID
            permission_code: 权限编码
        
        Returns:
            bool: 是否拥有权限
        """
        # 获取用户的所有角色
        from common.database.models.user import Role
        roles = self.db.query(Role).join("users").filter(users.id == user_id).all()
        
        # 检查任一角色是否拥有该权限
        for role in roles:
            if role.has_permission(permission_code):
                return True
        
        return False