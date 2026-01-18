# -*- coding: utf-8 -*-
"""
瑙掕壊鏈嶅姟

鍔熻兘璇存槑锛?1. 瑙掕壊CRUD鎿嶄綔
2. 瑙掕壊鏉冮檺绠＄悊
3. 瑙掕壊鑿滃崟绠＄悊

浣跨敤绀轰緥锛?    from app.services.role_service import RoleService
    
    role_service = RoleService(db)
    role = role_service.create_role(name="绠＄悊鍛?, code="admin")
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
    瑙掕壊鏈嶅姟
    
    鍔熻兘锛?    - 瑙掕壊CRUD鎿嶄綔
    - 瑙掕壊鏉冮檺绠＄悊
    - 瑙掕壊鑿滃崟绠＄悊
    
    浣跨敤鏂规硶锛?        role_service = RoleService(db)
        role = role_service.create_role(name="绠＄悊鍛?, code="admin")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栬鑹叉湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.role_repo = RoleRepository(db)
        self.perm_repo = PermissionRepository(db)
        self.menu_repo = MenuRepository(db)
    
    def create_role(self, role_data: Dict[str, Any]) -> Role:
        """
        鍒涘缓瑙掕壊
        
        Args:
            role_data: 瑙掕壊鏁版嵁
        
        Returns:
            Role: 鍒涘缓鐨勮鑹插璞?        
        Raises:
            ValueError: 瑙掕壊缂栫爜宸插瓨鍦?            ValueError: 瑙掕壊鍚嶇О宸插瓨鍦?        """
        logger.info(f"鍒涘缓瑙掕壊: name={role_data.get('name')}, code={role_data.get('code')}")
        
        # 妫€鏌ヨ鑹茬紪鐮佹槸鍚﹀凡瀛樺湪
        if self.role_repo.exists_by_code(role_data.get("code")):
            raise ValueError("瑙掕壊缂栫爜宸插瓨鍦?)
        
        # 妫€鏌ヨ鑹插悕绉版槸鍚﹀凡瀛樺湪
        tenant_id = role_data.get("tenant_id")
        if tenant_id and self.role_repo.exists_by_name_in_tenant(role_data.get("name"), tenant_id):
            raise ValueError("瑙掕壊鍚嶇О宸插瓨鍦?)
        
        # 鍒涘缓瑙掕壊
        role = Role(**role_data)
        return self.role_repo.create(role)
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """
        鑾峰彇瑙掕壊
        
        Args:
            role_id: 瑙掕壊ID
        
        Returns:
            Optional[Role]: 瑙掕壊瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.role_repo.get_by_id(role_id)
    
    def get_role_by_code(self, code: str) -> Optional[Role]:
        """
        鏍规嵁缂栫爜鑾峰彇瑙掕壊
        
        Args:
            code: 瑙掕壊缂栫爜
        
        Returns:
            Optional[Role]: 瑙掕壊瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.role_repo.get_by_code(code)
    
    def update_role(self, role_id: str, role_data: Dict[str, Any]) -> Optional[Role]:
        """
        鏇存柊瑙掕壊
        
        Args:
            role_id: 瑙掕壊ID
            role_data: 瑙掕壊鏁版嵁
        
        Returns:
            Optional[Role]: 鏇存柊鍚庣殑瑙掕壊瀵硅薄锛屼笉瀛樺湪杩斿洖None
        
        Raises:
            ValueError: 瑙掕壊鍚嶇О宸茶鍏朵粬瑙掕壊浣跨敤
        """
        logger.info(f"鏇存柊瑙掕壊: role_id={role_id}")
        
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return None
        
        # 妫€鏌ヨ鑹插悕绉版槸鍚﹁鍏朵粬瑙掕壊浣跨敤
        if "name" in role_data and role_data["name"] != role.name:
            if self.role_repo.exists_by_name_in_tenant(role_data["name"], role.tenant_id):
                raise ValueError("瑙掕壊鍚嶇О宸茶鍏朵粬瑙掕壊浣跨敤")
        
        # 鏇存柊瑙掕壊
        for key, value in role_data.items():
            if hasattr(role, key):
                setattr(role, key, value)
        
        return self.role_repo.update(role)
    
    def delete_role(self, role_id: str) -> bool:
        """
        鍒犻櫎瑙掕壊
        
        Args:
            role_id: 瑙掕壊ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎瑙掕壊: role_id={role_id}")
        return self.role_repo.delete(role_id)
    
    def list_roles(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None, 
                   page: int = 1, page_size: int = 10) -> List[Role]:
        """
        鑾峰彇瑙掕壊鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Role]: 瑙掕壊鍒楄〃
        """
        if keyword:
            return self.role_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.role_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.role_repo.get_all(page, page_size)
    
    def assign_permissions(self, role_id: str, permission_ids: List[str]) -> Role:
        """
        鍒嗛厤鏉冮檺
        
        Args:
            role_id: 瑙掕壊ID
            permission_ids: 鏉冮檺ID鍒楄〃
        
        Returns:
            Role: 鏇存柊鍚庣殑瑙掕壊瀵硅薄
        """
        logger.info(f"鍒嗛厤鏉冮檺: role_id={role_id}, permission_count={len(permission_ids)}")
        return self.role_repo.assign_permissions(role_id, permission_ids)
    
    def assign_menus(self, role_id: str, menu_ids: List[str]) -> Role:
        """
        鍒嗛厤鑿滃崟
        
        Args:
            role_id: 瑙掕壊ID
            menu_ids: 鑿滃崟ID鍒楄〃
        
        Returns:
            Role: 鏇存柊鍚庣殑瑙掕壊瀵硅薄
        """
        logger.info(f"鍒嗛厤鑿滃崟: role_id={role_id}, menu_count={len(menu_ids)}")
        return self.role_repo.assign_menus(role_id, menu_ids)
    
    def get_role_permissions(self, role_id: str) -> List:
        """
        鑾峰彇瑙掕壊鏉冮檺
        
        Args:
            role_id: 瑙掕壊ID
        
        Returns:
            List: 鏉冮檺鍒楄〃
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return []
        return role.permissions
    
    def get_role_menus(self, role_id: str) -> List:
        """
        鑾峰彇瑙掕壊鑿滃崟
        
        Args:
            role_id: 瑙掕壊ID
        
        Returns:
            List: 鑿滃崟鍒楄〃
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return []
        return role.menus
    
    def check_permission(self, role_id: str, permission_code: str) -> bool:
        """
        妫€鏌ヨ鑹叉槸鍚︽嫢鏈夋寚瀹氭潈闄?        
        Args:
            role_id: 瑙掕壊ID
            permission_code: 鏉冮檺缂栫爜
        
        Returns:
            bool: 鏄惁鎷ユ湁鏉冮檺
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return False
        return role.has_permission(permission_code)
    
    def count_roles(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻瑙掕壊鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 瑙掕壊鏁伴噺
        """
        if tenant_id:
            return self.role_repo.count_by_tenant(tenant_id)
        else:
            return self.role_repo.count_all()
