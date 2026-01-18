# -*- coding: utf-8 -*-
"""
瑙掕壊鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 瑙掕壊CRUD鎿嶄綔
2. 瑙掕壊鏉冮檺绠＄悊
3. 瑙掕壊鑿滃崟绠＄悊

浣跨敤绀轰緥锛?    from app.repositories.role_repository import RoleRepository
    
    role_repo = RoleRepository(db)
    role = role_repo.get_by_code("admin")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.user import Role


class RoleRepository:
    """
    瑙掕壊鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 瑙掕壊CRUD鎿嶄綔
    - 瑙掕壊鏉冮檺绠＄悊
    - 瑙掕壊鑿滃崟绠＄悊
    
    浣跨敤鏂规硶锛?        role_repo = RoleRepository(db)
        role = role_repo.get_by_code("admin")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栬鑹叉暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, role: Role) -> Role:
        """
        创建瑙掕壊
        
        Args:
            role: 瑙掕壊瀵硅薄
        
        Returns:
            Role: 创建鐨勮鑹插璞?        """
        logger.info(f"创建瑙掕壊: name={role.name}, code={role.code}, tenant_id={role.tenant_id}")
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def get_by_id(self, role_id: str) -> Optional[Role]:
        """
        根据ID鑾峰彇瑙掕壊
        
        Args:
            role_id: 角色ID
        
        Returns:
            Optional[Role]: 瑙掕壊瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_by_code(self, code: str) -> Optional[Role]:
        """
        根据编码鑾峰彇瑙掕壊
        
        Args:
            code: 角色编码
        
        Returns:
            Optional[Role]: 瑙掕壊瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Role).filter(Role.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        根据租户ID鑾峰彇瑙掕壊鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Role]: 瑙掕壊鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Role).filter(Role.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_user_id(self, user_id: str) -> List[Role]:
        """
        根据用户ID鑾峰彇瑙掕壊鍒楄〃
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Role]: 瑙掕壊鍒楄〃
        """
        return self.db.query(Role).join("users").filter(users.id == user_id).all()
    
    def get_system_roles(self, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        鑾峰彇绯荤粺瑙掕壊
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Role]: 瑙掕壊鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Role).filter(Role.is_system == "1").offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Role]:
        """
        鎼滅储瑙掕壊
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Role]: 瑙掕壊鍒楄〃
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
        鑾峰彇鎵€鏈夎鑹?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Role]: 瑙掕壊鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Role).offset(offset).limit(page_size).all()
    
    def update(self, role: Role) -> Role:
        """
        更新瑙掕壊
        
        Args:
            role: 瑙掕壊瀵硅薄
        
        Returns:
            Role: 更新鍚庣殑瑙掕壊瀵硅薄
        """
        logger.info(f"更新瑙掕壊: role_id={role.id}")
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def delete(self, role_id: str) -> bool:
        """
        删除瑙掕壊
        
        Args:
            role_id: 角色ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除瑙掕壊: role_id={role_id}")
        role = self.get_by_id(role_id)
        if not role:
            return False
        
        # 妫€鏌ユ槸鍚︿负绯荤粺瑙掕壊
        if role.is_system == "1":
            raise ValueError("鏃犳硶删除绯荤粺瑙掕壊")
        
        # 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        if role.users:
            raise ValueError("鏃犳硶删除瑙掕壊锛氳瑙掕壊涓嬪瓨鍦ㄧ敤鎴?)
        
        self.db.delete(role)
        self.db.commit()
        return True
    
    def assign_permissions(self, role_id: str, permission_ids: List[str]) -> Role:
        """
        鍒嗛厤鏉冮檺
        
        Args:
            role_id: 角色ID
            permission_ids: 鏉冮檺ID鍒楄〃
        
        Returns:
            Role: 更新鍚庣殑瑙掕壊瀵硅薄
        """
        logger.info(f"鍒嗛厤鏉冮檺: role_id={role_id}, permission_count={len(permission_ids)}")
        role = self.get_by_id(role_id)
        if not role:
            raise ValueError("瑙掕壊涓嶅瓨鍦?)
        
        # 娓呯┖鐜版湁鏉冮檺
        role.permissions.clear()
        
        # 娣诲姞鏂版潈闄?        from common.database.models.permission import Permission
        for permission_id in permission_ids:
            permission = self.db.query(Permission).filter(Permission.id == permission_id).first()
            if permission:
                role.permissions.append(permission)
        
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def assign_menus(self, role_id: str, menu_ids: List[str]) -> Role:
        """
        鍒嗛厤鑿滃崟
        
        Args:
            role_id: 角色ID
            menu_ids: 鑿滃崟ID鍒楄〃
        
        Returns:
            Role: 更新鍚庣殑瑙掕壊瀵硅薄
        """
        logger.info(f"鍒嗛厤鑿滃崟: role_id={role_id}, menu_count={len(menu_ids)}")
        role = self.get_by_id(role_id)
        if not role:
            raise ValueError("瑙掕壊涓嶅瓨鍦?)
        
        # 娓呯┖鐜版湁鑿滃崟
        role.menus.clear()
        
        # 娣诲姞鏂拌彍鍗?        from common.database.models.permission import Menu
        for menu_id in menu_ids:
            menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
            if menu:
                role.menus.append(menu)
        
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛瑙掕壊数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 瑙掕壊数量
        """
        return self.db.query(Role).filter(Role.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夎鑹叉暟閲?        
        Returns:
            int: 瑙掕壊数量
        """
        return self.db.query(Role).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€查询鑹茬紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 角色编码
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Role).filter(Role.code == code).first() is not None
    
    def exists_by_name_in_tenant(self, name: str, tenant_id: str) -> bool:
        """
        妫€鏌ョ鎴峰唴角色名称鏄惁瀛樺湪
        
        Args:
            name: 角色名称
            tenant_id: 租户ID
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Role).filter(
            and_(
                Role.name == name,
                Role.tenant_id == tenant_id
            )
        ).first() is not None
