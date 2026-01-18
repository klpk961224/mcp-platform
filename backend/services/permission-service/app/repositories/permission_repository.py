# -*- coding: utf-8 -*-
"""
鏉冮檺鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 鏉冮檺CRUD鎿嶄綔
2. 鏉冮檺查询鎿嶄綔
3. 鏉冮檺缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.permission_repository import PermissionRepository
    
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
    鏉冮檺鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鏉冮檺CRUD鎿嶄綔
    - 鏉冮檺查询鎿嶄綔
    - 鏉冮檺缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        perm_repo = PermissionRepository(db)
        perm = perm_repo.get_by_code("user:manage")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨潈闄愭暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, permission: Permission) -> Permission:
        """
        创建鏉冮檺
        
        Args:
            permission: 鏉冮檺瀵硅薄
        
        Returns:
            Permission: 创建鐨勬潈闄愬璞?        """
        logger.info(f"创建鏉冮檺: name={permission.name}, code={permission.code}, tenant_id={permission.tenant_id}")
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def get_by_id(self, permission_id: str) -> Optional[Permission]:
        """
        根据ID鑾峰彇鏉冮檺
        
        Args:
            permission_id: 鏉冮檺ID
        
        Returns:
            Optional[Permission]: 鏉冮檺瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Permission).filter(Permission.id == permission_id).first()
    
    def get_by_code(self, code: str) -> Optional[Permission]:
        """
        根据编码鑾峰彇鏉冮檺
        
        Args:
            code: 鏉冮檺编码
        
        Returns:
            Optional[Permission]: 鏉冮檺瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Permission).filter(Permission.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        根据租户ID鑾峰彇鏉冮檺鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).filter(Permission.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_resource(self, resource: str, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        根据资源类型鑾峰彇鏉冮檺鍒楄〃
        
        Args:
            resource: 资源类型
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).filter(Permission.resource == resource).offset(offset).limit(page_size).all()
    
    def get_by_type(self, permission_type: str, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        根据鏉冮檺类型鑾峰彇鏉冮檺鍒楄〃
        
        Args:
            permission_type: 鏉冮檺类型
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).filter(Permission.type == permission_type).offset(offset).limit(page_size).all()
    
    def get_by_role_id(self, role_id: str) -> List[Permission]:
        """
        根据角色ID鑾峰彇鏉冮檺鍒楄〃
        
        Args:
            role_id: 角色ID
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
        """
        return self.db.query(Permission).join("roles").filter(roles.id == role_id).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        鎼滅储鏉冮檺
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
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
        鑾峰彇鎵€鏈夋潈闄?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Permission).offset(offset).limit(page_size).all()
    
    def update(self, permission: Permission) -> Permission:
        """
        更新鏉冮檺
        
        Args:
            permission: 鏉冮檺瀵硅薄
        
        Returns:
            Permission: 更新鍚庣殑鏉冮檺瀵硅薄
        """
        logger.info(f"更新鏉冮檺: permission_id={permission.id}")
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def delete(self, permission_id: str) -> bool:
        """
        删除鏉冮檺
        
        Args:
            permission_id: 鏉冮檺ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除鏉冮檺: permission_id={permission_id}")
        permission = self.get_by_id(permission_id)
        if not permission:
            return False
        
        # 妫€鏌ユ槸鍚︽湁瑙掕壊浣跨敤
        if permission.roles:
            raise ValueError("鏃犳硶删除鏉冮檺锛氳鏉冮檺琚鑹蹭娇鐢?)
        
        self.db.delete(permission)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛鏉冮檺数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 鏉冮檺数量
        """
        return self.db.query(Permission).filter(Permission.tenant_id == tenant_id).count()
    
    def count_by_resource(self, resource: str) -> int:
        """
        缁熻资源鏉冮檺数量
        
        Args:
            resource: 资源类型
        
        Returns:
            int: 鏉冮檺数量
        """
        return self.db.query(Permission).filter(Permission.resource == resource).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夋潈闄愭暟閲?        
        Returns:
            int: 鏉冮檺数量
        """
        return self.db.query(Permission).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€鏌ユ潈闄愮紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 鏉冮檺编码
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Permission).filter(Permission.code == code).first() is not None
