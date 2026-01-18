# -*- coding: utf-8 -*-
"""
鐢ㄦ埛鏈嶅姟

鍔熻兘璇存槑锛?1. 鐢ㄦ埛CRUD鎿嶄綔
2. 鐢ㄦ埛查询鎿嶄綔
3. 鐢ㄦ埛状态佺鐞?
浣跨敤绀轰緥锛?    from app.services.user_service import UserService
    
    user_service = UserService(db)
    user = user_service.create_user(username="admin", email="admin@example.com")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.tenant_repository import TenantRepository


class UserService:
    """
    鐢ㄦ埛鏈嶅姟
    
    鍔熻兘锛?    - 鐢ㄦ埛CRUD鎿嶄綔
    - 鐢ㄦ埛查询鎿嶄綔
    - 鐢ㄦ埛状态佺鐞?    
    浣跨敤鏂规硶锛?        user_service = UserService(db)
        user = user_service.create_user(username="admin", email="admin@example.com")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栫敤鎴锋湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.tenant_repo = TenantRepository(db)
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        创建鐢ㄦ埛
        
        Args:
            user_data: 鐢ㄦ埛鏁版嵁
        
        Returns:
            User: 创建鐨勭敤鎴峰璞?        
        Raises:
            ValueError: 用户名嶆垨邮箱宸插瓨鍦?            ValueError: 閮ㄩ棬涓嶅瓨鍦?            ValueError: 绉熸埛涓嶅瓨鍦?            ValueError: 绉熸埛宸茶繃鏈?            ValueError: 绉熸埛鐢ㄦ埛鏁板凡杈句笂闄?        """
        logger.info(f"创建鐢ㄦ埛: username={user_data.get('username')}")
        
        # 妫€鏌ョ敤鎴峰悕鏄惁宸插瓨鍦?        if self.user_repo.exists_by_username(user_data.get("username")):
            raise ValueError("用户名嶅凡瀛樺湪")
        
        # 妫€鏌ラ偖绠辨槸鍚﹀凡瀛樺湪
        if self.user_repo.exists_by_email(user_data.get("email")):
            raise ValueError("邮箱宸插瓨鍦?)
        
        # 楠岃瘉绉熸埛
        tenant_id = user_data.get("tenant_id")
        if tenant_id:
            tenant = self.tenant_repo.get_by_id(tenant_id)
            if not tenant:
                raise ValueError("绉熸埛涓嶅瓨鍦?)
            if tenant.is_expired():
                raise ValueError("绉熸埛宸茶繃鏈?)
            if not tenant.can_add_user():
                raise ValueError("绉熸埛鐢ㄦ埛鏁板凡杈句笂闄?)
        
        # 楠岃瘉閮ㄩ棬
        dept_id = user_data.get("dept_id")
        if dept_id:
            department = self.dept_repo.get_by_id(dept_id)
            if not department:
                raise ValueError("閮ㄩ棬涓嶅瓨鍦?)
            if tenant_id and department.tenant_id != tenant_id:
                raise ValueError("閮ㄩ棬涓嶅睘浜庤绉熸埛")
        
        # 创建鐢ㄦ埛
        user = User(**user_data)
        return self.user_repo.create(user)
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        鑾峰彇鐢ㄦ埛
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名嶈幏鍙栫敤鎴?        
        Args:
            username: 用户名?        
        Returns:
            Optional[User]: 鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.user_repo.get_by_username(username)
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        """
        更新鐢ㄦ埛
        
        Args:
            user_id: 用户ID
            user_data: 鐢ㄦ埛鏁版嵁
        
        Returns:
            Optional[User]: 更新鍚庣殑鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        
        Raises:
            ValueError: 邮箱宸茶鍏朵粬鐢ㄦ埛浣跨敤
            ValueError: 閮ㄩ棬涓嶅瓨鍦?            ValueError: 閮ㄩ棬涓嶅睘浜庤绉熸埛
        """
        logger.info(f"更新鐢ㄦ埛: user_id={user_id}")
        
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        # 妫€鏌ラ偖绠辨槸鍚﹁鍏朵粬鐢ㄦ埛浣跨敤
        if "email" in user_data and user_data["email"] != user.email:
            if self.user_repo.exists_by_email(user_data["email"]):
                raise ValueError("邮箱宸茶鍏朵粬鐢ㄦ埛浣跨敤")
        
        # 楠岃瘉閮ㄩ棬
        if "department_id" in user_data and user_data["department_id"]:
            department = self.dept_repo.get_by_id(user_data["department_id"])
            if not department:
                raise ValueError("閮ㄩ棬涓嶅瓨鍦?)
            if department.tenant_id != user.tenant_id:
                raise ValueError("閮ㄩ棬涓嶅睘浜庤绉熸埛")
        
        # 更新鐢ㄦ埛
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return self.user_repo.update(user)
    
    def delete_user(self, user_id: str) -> bool:
        """
        删除鐢ㄦ埛
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除鐢ㄦ埛: user_id={user_id}")
        return self.user_repo.delete(user_id)
    
    def list_users(self, tenant_id: Optional[str] = None, department_id: Optional[str] = None, 
                   keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[User]:
        """
        鑾峰彇鐢ㄦ埛鍒楄〃
        
        Args:
            tenant_id: 租户ID锛堝彲閫夛級
            department_id: 部门ID锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[User]: 鐢ㄦ埛鍒楄〃
        """
        if keyword:
            return self.user_repo.search(keyword, tenant_id, page, page_size)
        elif department_id:
            return self.user_repo.get_by_department_id(department_id, page, page_size)
        elif tenant_id:
            return self.user_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.user_repo.get_all(page, page_size)
    
    def activate_user(self, user_id: str) -> Optional[User]:
        """
        婵€娲荤敤鎴?        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 更新鍚庣殑鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"婵€娲荤敤鎴? user_id={user_id}")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        user.is_active = True
        user.status = "active"
        return self.user_repo.update(user)
    
    def deactivate_user(self, user_id: str) -> Optional[User]:
        """
        鍋滅敤鐢ㄦ埛
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 更新鍚庣殑鐢ㄦ埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鍋滅敤鐢ㄦ埛: user_id={user_id}")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        user.is_active = False
        user.status = "inactive"
        return self.user_repo.update(user)
    
    def count_users(self, tenant_id: Optional[str] = None, department_id: Optional[str] = None) -> int:
        """
        缁熻鐢ㄦ埛数量
        
        Args:
            tenant_id: 租户ID锛堝彲閫夛級
            department_id: 部门ID锛堝彲閫夛級
        
        Returns:
            int: 鐢ㄦ埛数量
        """
        if department_id:
            return self.user_repo.count_by_department(department_id)
        elif tenant_id:
            return self.user_repo.count_by_tenant(tenant_id)
        else:
            return self.user_repo.count_all()
