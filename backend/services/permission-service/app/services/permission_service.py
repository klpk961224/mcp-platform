# -*- coding: utf-8 -*-
"""
鏉冮檺鏈嶅姟

鍔熻兘璇存槑锛?1. 鏉冮檺CRUD鎿嶄綔
2. 鏉冮檺鏌ヨ鎿嶄綔
3. 鏉冮檺楠岃瘉鎿嶄綔

浣跨敤绀轰緥锛?    from app.services.permission_service import PermissionService
    
    perm_service = PermissionService(db)
    perm = perm_service.create_permission(name="鐢ㄦ埛绠＄悊", code="user:manage")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository


class PermissionService:
    """
    鏉冮檺鏈嶅姟
    
    鍔熻兘锛?    - 鏉冮檺CRUD鎿嶄綔
    - 鏉冮檺鏌ヨ鎿嶄綔
    - 鏉冮檺楠岃瘉鎿嶄綔
    
    浣跨敤鏂规硶锛?        perm_service = PermissionService(db)
        perm = perm_service.create_permission(name="鐢ㄦ埛绠＄悊", code="user:manage")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨潈闄愭湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.perm_repo = PermissionRepository(db)
    
    def create_permission(self, permission_data: Dict[str, Any]) -> Permission:
        """
        鍒涘缓鏉冮檺
        
        Args:
            permission_data: 鏉冮檺鏁版嵁
        
        Returns:
            Permission: 鍒涘缓鐨勬潈闄愬璞?        
        Raises:
            ValueError: 鏉冮檺缂栫爜宸插瓨鍦?        """
        logger.info(f"鍒涘缓鏉冮檺: name={permission_data.get('name')}, code={permission_data.get('code')}")
        
        # 妫€鏌ユ潈闄愮紪鐮佹槸鍚﹀凡瀛樺湪
        if self.perm_repo.exists_by_code(permission_data.get("code")):
            raise ValueError("鏉冮檺缂栫爜宸插瓨鍦?)
        
        # 鍒涘缓鏉冮檺
        permission = Permission(**permission_data)
        return self.perm_repo.create(permission)
    
    def get_permission(self, permission_id: str) -> Optional[Permission]:
        """
        鑾峰彇鏉冮檺
        
        Args:
            permission_id: 鏉冮檺ID
        
        Returns:
            Optional[Permission]: 鏉冮檺瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.perm_repo.get_by_id(permission_id)
    
    def get_permission_by_code(self, code: str) -> Optional[Permission]:
        """
        鏍规嵁缂栫爜鑾峰彇鏉冮檺
        
        Args:
            code: 鏉冮檺缂栫爜
        
        Returns:
            Optional[Permission]: 鏉冮檺瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.perm_repo.get_by_code(code)
    
    def update_permission(self, permission_id: str, permission_data: Dict[str, Any]) -> Optional[Permission]:
        """
        鏇存柊鏉冮檺
        
        Args:
            permission_id: 鏉冮檺ID
            permission_data: 鏉冮檺鏁版嵁
        
        Returns:
            Optional[Permission]: 鏇存柊鍚庣殑鏉冮檺瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鏇存柊鏉冮檺: permission_id={permission_id}")
        
        permission = self.perm_repo.get_by_id(permission_id)
        if not permission:
            return None
        
        # 鏇存柊鏉冮檺
        for key, value in permission_data.items():
            if hasattr(permission, key):
                setattr(permission, key, value)
        
        return self.perm_repo.update(permission)
    
    def delete_permission(self, permission_id: str) -> bool:
        """
        鍒犻櫎鏉冮檺
        
        Args:
            permission_id: 鏉冮檺ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎鏉冮檺: permission_id={permission_id}")
        return self.perm_repo.delete(permission_id)
    
    def list_permissions(self, tenant_id: Optional[str] = None, resource: Optional[str] = None,
                         permission_type: Optional[str] = None, keyword: Optional[str] = None,
                         page: int = 1, page_size: int = 10) -> List[Permission]:
        """
        鑾峰彇鏉冮檺鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            resource: 璧勬簮绫诲瀷锛堝彲閫夛級
            permission_type: 鏉冮檺绫诲瀷锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Permission]: 鏉冮檺鍒楄〃
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
        缁熻鏉冮檺鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            resource: 璧勬簮绫诲瀷锛堝彲閫夛級
        
        Returns:
            int: 鏉冮檺鏁伴噺
        """
        if resource:
            return self.perm_repo.count_by_resource(resource)
        elif tenant_id:
            return self.perm_repo.count_by_tenant(tenant_id)
        else:
            return self.perm_repo.count_all()
    
    def check_user_permission(self, user_id: str, permission_code: str) -> bool:
        """
        妫€鏌ョ敤鎴锋槸鍚︽嫢鏈夋寚瀹氭潈闄?        
        Args:
            user_id: 鐢ㄦ埛ID
            permission_code: 鏉冮檺缂栫爜
        
        Returns:
            bool: 鏄惁鎷ユ湁鏉冮檺
        """
        # 鑾峰彇鐢ㄦ埛鐨勬墍鏈夎鑹?        from common.database.models.user import Role
        roles = self.db.query(Role).join("users").filter(users.id == user_id).all()
        
        # 妫€鏌ヤ换涓€瑙掕壊鏄惁鎷ユ湁璇ユ潈闄?        for role in roles:
            if role.has_permission(permission_code):
                return True
        
        return False
