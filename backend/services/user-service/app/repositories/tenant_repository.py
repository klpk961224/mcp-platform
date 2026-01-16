# -*- coding: utf-8 -*-
"""
租户数据访问层

功能说明：
1. 租户CRUD操作
2. 租户查询操作
3. 租户统计操作

使用示例：
    from app.repositories.tenant_repository import TenantRepository
    
    tenant_repo = TenantRepository(db)
    tenant = tenant_repo.get_by_code("example")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from app.models.tenant import Tenant


class TenantRepository:
    """
    租户数据访问层
    
    功能：
    - 租户CRUD操作
    - 租户查询操作
    - 租户统计操作
    
    使用方法：
        tenant_repo = TenantRepository(db)
        tenant = tenant_repo.get_by_code("example")
    """
    
    def __init__(self, db: Session):
        """
        初始化租户数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, tenant: Tenant) -> Tenant:
        """
        创建租户
        
        Args:
            tenant: 租户对象
        
        Returns:
            Tenant: 创建的租户对象
        """
        logger.info(f"创建租户: name={tenant.name}, code={tenant.code}")
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def get_by_id(self, tenant_id: str) -> Optional[Tenant]:
        """
        根据ID获取租户
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Optional[Tenant]: 租户对象，不存在返回None
        """
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    def get_by_code(self, code: str) -> Optional[Tenant]:
        """
        根据编码获取租户
        
        Args:
            code: 租户编码
        
        Returns:
            Optional[Tenant]: 租户对象，不存在返回None
        """
        return self.db.query(Tenant).filter(Tenant.code == code).first()
    
    def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        根据名称获取租户
        
        Args:
            name: 租户名称
        
        Returns:
            Optional[Tenant]: 租户对象，不存在返回None
        """
        return self.db.query(Tenant).filter(Tenant.name == name).first()
    
    def get_by_package_id(self, package_id: str, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        根据套餐ID获取租户列表
        
        Args:
            package_id: 套餐ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Tenant]: 租户列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(Tenant.package_id == package_id).offset(offset).limit(page_size).all()
    
    def get_active_tenants(self, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        获取激活的租户列表
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Tenant]: 租户列表
        """
        from datetime import datetime
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(
            and_(
                Tenant.status == "active",
                or_(
                    Tenant.expires_at.is_(None),
                    Tenant.expires_at > datetime.now()
                )
            )
        ).offset(offset).limit(page_size).all()
    
    def get_expired_tenants(self, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        获取过期的租户列表
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Tenant]: 租户列表
        """
        from datetime import datetime
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(
            and_(
                Tenant.expires_at.isnot(None),
                Tenant.expires_at < datetime.now()
            )
        ).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        搜索租户
        
        Args:
            keyword: 关键词
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Tenant]: 租户列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(
            or_(
                Tenant.name.like(f"%{keyword}%"),
                Tenant.code.like(f"%{keyword}%"),
                Tenant.description.like(f"%{keyword}%")
            )
        ).offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        获取所有租户
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Tenant]: 租户列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Tenant).offset(offset).limit(page_size).all()
    
    def update(self, tenant: Tenant) -> Tenant:
        """
        更新租户
        
        Args:
            tenant: 租户对象
        
        Returns:
            Tenant: 更新后的租户对象
        """
        logger.info(f"更新租户: tenant_id={tenant.id}")
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def delete(self, tenant_id: str) -> bool:
        """
        删除租户
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除租户: tenant_id={tenant_id}")
        tenant = self.get_by_id(tenant_id)
        if not tenant:
            return False
        
        # 检查是否有用户
        if tenant.users:
            raise ValueError("无法删除租户：该租户下存在用户")
        
        # 检查是否有部门
        if tenant.departments:
            raise ValueError("无法删除租户：该租户下存在部门")
        
        self.db.delete(tenant)
        self.db.commit()
        return True
    
    def count_by_package(self, package_id: str) -> int:
        """
        统计套餐租户数量
        
        Args:
            package_id: 套餐ID
        
        Returns:
            int: 租户数量
        """
        return self.db.query(Tenant).filter(Tenant.package_id == package_id).count()
    
    def count_active(self) -> int:
        """
        统计激活的租户数量
        
        Returns:
            int: 租户数量
        """
        from datetime import datetime
        return self.db.query(Tenant).filter(
            and_(
                Tenant.status == "active",
                or_(
                    Tenant.expires_at.is_(None),
                    Tenant.expires_at > datetime.now()
                )
            )
        ).count()
    
    def count_expired(self) -> int:
        """
        统计过期的租户数量
        
        Returns:
            int: 租户数量
        """
        from datetime import datetime
        return self.db.query(Tenant).filter(
            and_(
                Tenant.expires_at.isnot(None),
                Tenant.expires_at < datetime.now()
            )
        ).count()
    
    def count_all(self) -> int:
        """
        统计所有租户数量
        
        Returns:
            int: 租户数量
        """
        return self.db.query(Tenant).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查租户编码是否存在
        
        Args:
            code: 租户编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Tenant).filter(Tenant.code == code).first() is not None
    
    def exists_by_name(self, name: str) -> bool:
        """
        检查租户名称是否存在
        
        Args:
            name: 租户名称
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Tenant).filter(Tenant.name == name).first() is not None