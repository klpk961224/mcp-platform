# -*- coding: utf-8 -*-
"""
角色数据访问层

功能说明：
1. 角色CRUD操作
2. 角色权限管理
3. 角色菜单管理

使用示例：
    from app.repositories.role_repository import RoleRepository
    
    role_repo = RoleRepository(db)
    role = role_repo.get_by_code("admin")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from app.models.role import Role


class RoleRepository:
    """
    角色数据访问层
    
    功能：
    - 角色CRUD操作
    - 角色权限管理
    - 角色菜单管理
    
    使用方法：
        role_repo = RoleRepository(db)
        role = role_repo.get_by_code("admin")
    """
    
    def __init__(self, db: Session):
        """
        初始化角色数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, role: Role) -> Role:
        """
        创建角色
        
        Args:
            role: 角色对象
        
        Returns:
            Role: 创建的角色对象
        """
        logger.info(f"创建角色: name={role.name}, code={role.code}, tenant_id={role.tenant_id}")
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def get_by_id(self, role_id: str) -> Optional[Role]:
        """
        根据ID获取角色
        
        Args:
            role_id: 角色ID
        
        Returns:
            Optional[Role]: 角色对象，不存在返回None
        """
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_by_code(self, code: str) -> Optional[Role]:
        """
        根据编码获取角色
        
        Args:
            code: 角色编码
        
        Returns:
            Optional[Role]: 角色对象，不存在返回None
        """
        return self.db.query(Role).filter(Role.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        根据租户ID获取角色列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Role]: 角色列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Role).filter(Role.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_user_id(self, user_id: str) -> List[Role]:
        """
        根据用户ID获取角色列表
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Role]: 角色列表
        """
        return self.db.query(Role).join("users").filter(users.id == user_id).all()
    
    def get_system_roles(self, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        获取系统角色
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Role]: 角色列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Role).filter(Role.is_system == "1").offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        搜索角色
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Role]: 角色列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(Role).filter(
            or_(
                Role.name.like(f"%{keyword}%"),
                Role.code.like(f"%{keyword}%"),
                Role.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Role.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        获取所有角色
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Role]: 角色列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Role).offset(offset).limit(page_size).all()
    
    def update(self, role: Role) -> Role:
        """
        更新角色
        
        Args:
            role: 角色对象
        
        Returns:
            Role: 更新后的角色对象
        """
        logger.info(f"更新角色: role_id={role.id}")
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def delete(self, role_id: str) -> bool:
        """
        删除角色
        
        Args:
            role_id: 角色ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除角色: role_id={role_id}")
        role = self.get_by_id(role_id)
        if not role:
            return False
        
        # 检查是否为系统角色
        if role.is_system == "1":
            raise ValueError("无法删除系统角色")
        
        # 检查是否有用户
        if role.users:
            raise ValueError("无法删除角色：该角色下存在用户")
        
        self.db.delete(role)
        self.db.commit()
        return True
    
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
        role = self.get_by_id(role_id)
        if not role:
            raise ValueError("角色不存在")
        
        # 清空现有权限
        role.permissions.clear()
        
        # 添加新权限
        from app.models.permission import Permission
        for permission_id in permission_ids:
            permission = self.db.query(Permission).filter(Permission.id == permission_id).first()
            if permission:
                role.permissions.append(permission)
        
        self.db.commit()
        self.db.refresh(role)
        return role
    
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
        role = self.get_by_id(role_id)
        if not role:
            raise ValueError("角色不存在")
        
        # 清空现有菜单
        role.menus.clear()
        
        # 添加新菜单
        from app.models.menu import Menu
        for menu_id in menu_ids:
            menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
            if menu:
                role.menus.append(menu)
        
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户角色数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 角色数量
        """
        return self.db.query(Role).filter(Role.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        统计所有角色数量
        
        Returns:
            int: 角色数量
        """
        return self.db.query(Role).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查角色编码是否存在
        
        Args:
            code: 角色编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Role).filter(Role.code == code).first() is not None
    
    def exists_by_name_in_tenant(self, name: str, tenant_id: str) -> bool:
        """
        检查租户内角色名称是否存在
        
        Args:
            name: 角色名称
            tenant_id: 租户ID
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Role).filter(
            and_(
                Role.name == name,
                Role.tenant_id == tenant_id
            )
        ).first() is not None