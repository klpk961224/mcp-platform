# -*- coding: utf-8 -*-
"""
权限数据访问层

功能说明：
1. 权限CRUD操作
2. 权限查询操作
3. 权限统计操作

使用示例：
    from app.repositories.permission_repository import PermissionRepository
    
    perm_repo = PermissionRepository(db)
    perm = perm_repo.get_by_code("user:manage")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.permission import Permission


class PermissionRepository:
    """
    权限数据访问层
    
    功能：
    - 权限CRUD操作
    - 权限查询操作
    - 权限统计操作
    
    使用方法：
        perm_repo = PermissionRepository(db)
        perm = perm_repo.get_by_code("user:manage")
    """
    
    def __init__(self, db: Session):
        """
        初始化权限数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, permission: Permission) -> Permission:
        """
        创建权限
        
        Args:
            permission: 权限对象
        
        Returns:
            Permission: 创建的权限对象
        """
        logger.info(f"创建权限: name={permission.name}, code={permission.code}, tenant_id={permission.tenant_id}")
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def get_by_id(self, permission_id: str) -> Optional[Permission]:
        """
        根据ID获取权限
        
        Args:
            permission_id: 权限ID
        
        Returns:
            Optional[Permission]: 权限对象，不存在返回None
        """
        return self.db.query(Permission).filter(Permission.id == permission_id).first()
    
    def get_by_code(self, code: str) -> Optional[Permission]:
        """
        根据编码获取权限
        
        Args:
            code: 权限编码
        
        Returns:
            Optional[Permission]: 权限对象，不存在返回None
        """
        return self.db.query(Permission).filter(Permission.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        根据租户ID获取权限列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Permission]: 权限列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).filter(Permission.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_resource(self, resource: str, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        根据资源类型获取权限列表
        
        Args:
            resource: 资源类型
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Permission]: 权限列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).filter(Permission.resource == resource).offset(offset).limit(page_size).all()
    
    def get_by_type(self, permission_type: str, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        根据权限类型获取权限列表
        
        Args:
            permission_type: 权限类型
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Permission]: 权限列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).filter(Permission.type == permission_type).offset(offset).limit(page_size).all()
    
    def get_by_role_id(self, role_id: str) -> List[Permission]:
        """
        根据角色ID获取权限列表
        
        Args:
            role_id: 角色ID
        
        Returns:
            List[Permission]: 权限列表
        """
        return self.db.query(Permission).join("roles").filter(roles.id == role_id).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        搜索权限
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Permission]: 权限列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(Permission).filter(
            or_(
                Permission.name.like(f"%{keyword}%"),
                Permission.code.like(f"%{keyword}%"),
                Permission.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Permission.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        获取所有权限
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Permission]: 权限列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).offset(offset).limit(page_size).all()
    
    def update(self, permission: Permission) -> Permission:
        """
        更新权限
        
        Args:
            permission: 权限对象
        
        Returns:
            Permission: 更新后的权限对象
        """
        logger.info(f"更新权限: permission_id={permission.id}")
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def delete(self, permission_id: str) -> bool:
        """
        删除权限
        
        Args:
            permission_id: 权限ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除权限: permission_id={permission_id}")
        permission = self.get_by_id(permission_id)
        if not permission:
            return False
        
        # 检查是否有角色使用
        if permission.roles:
            raise ValueError("无法删除权限：该权限被角色使用")
        
        self.db.delete(permission)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户权限数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 权限数量
        """
        return self.db.query(Permission).filter(Permission.tenant_id == tenant_id).count()
    
    def count_by_resource(self, resource: str) -> int:
        """
        统计资源权限数量
        
        Args:
            resource: 资源类型
        
        Returns:
            int: 权限数量
        """
        return self.db.query(Permission).filter(Permission.resource == resource).count()
    
    def count_all(self) -> int:
        """
        统计所有权限数量
        
        Returns:
            int: 权限数量
        """
        return self.db.query(Permission).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查权限编码是否存在
        
        Args:
            code: 权限编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Permission).filter(Permission.code == code).first() is not None