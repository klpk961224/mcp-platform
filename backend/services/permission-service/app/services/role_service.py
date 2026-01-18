# -*- coding: utf-8 -*-
"""
角色服务

功能说明：
1. 角色CRUD操作
2. 角色权限管理
3. 角色菜单管理

使用示例：
    from app.services.role_service import RoleService
    
    role_service = RoleService(db)
    role = role_service.create_role(name="管理员", code="admin")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.user import Role
from app.repositories.role_repository import RoleRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.menu_repository import MenuRepository


class RoleService:
    """
    角色服务
    
    功能：
    - 角色CRUD操作
    - 角色权限管理
    - 角色菜单管理
    
    使用方法：
        role_service = RoleService(db)
        role = role_service.create_role(name="管理员", code="admin")
    """
    
    def __init__(self, db: Session):
        """
        初始化角色服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.role_repo = RoleRepository(db)
        self.perm_repo = PermissionRepository(db)
        self.menu_repo = MenuRepository(db)
    
    def create_role(self, role_data: Dict[str, Any]) -> Role:
        """
        创建角色
        
        Args:
            role_data: 角色数据
        
        Returns:
            Role: 创建的角色对象
        
        Raises:
            ValueError: 角色编码已存在
            ValueError: 角色名称已存在
        """
        logger.info(f"创建角色: name={role_data.get('name')}, code={role_data.get('code')}")
        
        # 检查角色编码是否已存在
        if self.role_repo.exists_by_code(role_data.get("code")):
            raise ValueError("角色编码已存在")
        
        # 检查角色名称是否已存在
        tenant_id = role_data.get("tenant_id")
        if tenant_id and self.role_repo.exists_by_name_in_tenant(role_data.get("name"), tenant_id):
            raise ValueError("角色名称已存在")
        
        # 创建角色
        role = Role(**role_data)
        return self.role_repo.create(role)
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """
        获取角色
        
        Args:
            role_id: 角色ID
        
        Returns:
            Optional[Role]: 角色对象，不存在返回None
        """
        return self.role_repo.get_by_id(role_id)
    
    def get_role_by_code(self, code: str) -> Optional[Role]:
        """
        根据编码获取角色
        
        Args:
            code: 角色编码
        
        Returns:
            Optional[Role]: 角色对象，不存在返回None
        """
        return self.role_repo.get_by_code(code)
    
    def update_role(self, role_id: str, role_data: Dict[str, Any]) -> Optional[Role]:
        """
        更新角色
        
        Args:
            role_id: 角色ID
            role_data: 角色数据
        
        Returns:
            Optional[Role]: 更新后的角色对象，不存在返回None
        
        Raises:
            ValueError: 角色名称已被其他角色使用
        """
        logger.info(f"更新角色: role_id={role_id}")
        
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return None
        
        # 检查角色名称是否被其他角色使用
        if "name" in role_data and role_data["name"] != role.name:
            if self.role_repo.exists_by_name_in_tenant(role_data["name"], role.tenant_id):
                raise ValueError("角色名称已被其他角色使用")
        
        # 更新角色
        for key, value in role_data.items():
            if hasattr(role, key):
                setattr(role, key, value)
        
        return self.role_repo.update(role)
    
    def delete_role(self, role_id: str) -> bool:
        """
        删除角色
        
        Args:
            role_id: 角色ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除角色: role_id={role_id}")
        return self.role_repo.delete(role_id)
    
    def list_roles(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None, 
                   page: int = 1, page_size: int = 10) -> List[Role]:
        """
        获取角色列表
        
        Args:
            tenant_id: 租户ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Role]: 角色列表
        """
        if keyword:
            return self.role_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.role_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.role_repo.get_all(page, page_size)
    
    def assign_permissions(self, role_id: str, permission_ids: List[str]) -> Role:
        """
        分配权限
        
        Args:
            role_id: 角色ID
            permission_ids: 权限ID列表
        
        Returns:
            Role: 更新后的角色对象
        """
        logger.info(f"分配权限: role_id={role_id}, permission_count={len(permission_ids)}")
        return self.role_repo.assign_permissions(role_id, permission_ids)
    
    def assign_menus(self, role_id: str, menu_ids: List[str]) -> Role:
        """
        分配菜单
        
        Args:
            role_id: 角色ID
            menu_ids: 菜单ID列表
        
        Returns:
            Role: 更新后的角色对象
        """
        logger.info(f"分配菜单: role_id={role_id}, menu_count={len(menu_ids)}")
        return self.role_repo.assign_menus(role_id, menu_ids)
    
    def get_role_permissions(self, role_id: str) -> List:
        """
        获取角色权限
        
        Args:
            role_id: 角色ID
        
        Returns:
            List: 权限列表
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return []
        return role.permissions
    
    def get_role_menus(self, role_id: str) -> List:
        """
        获取角色菜单
        
        Args:
            role_id: 角色ID
        
        Returns:
            List: 菜单列表
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return []
        return role.menus
    
    def check_permission(self, role_id: str, permission_code: str) -> bool:
        """
        检查角色是否拥有指定权限
        
        Args:
            role_id: 角色ID
            permission_code: 权限编码
        
        Returns:
            bool: 是否拥有权限
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return False
        return role.has_permission(permission_code)
    
    def count_roles(self, tenant_id: Optional[str] = None) -> int:
        """
        统计角色数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 角色数量
        """
        if tenant_id:
            return self.role_repo.count_by_tenant(tenant_id)
        else:
            return self.role_repo.count_all()