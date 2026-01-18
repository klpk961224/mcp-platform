# -*- coding: utf-8 -*-
"""
鑿滃崟鏈嶅姟

鍔熻兘璇存槑锛?1. 鑿滃崟CRUD鎿嶄綔
2. 鑿滃崟鏍戝舰缁撴瀯绠＄悊
3. 鑿滃崟鏉冮檺绠＄悊

浣跨敤绀轰緥锛?    from app.services.menu_service import MenuService
    
    menu_service = MenuService(db)
    menu = menu_service.create_menu(name="鐢ㄦ埛绠＄悊", code="user_manage")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.permission import Menu
from app.repositories.menu_repository import MenuRepository


class MenuService:
    """
    鑿滃崟鏈嶅姟
    
    鍔熻兘锛?    - 鑿滃崟CRUD鎿嶄綔
    - 鑿滃崟鏍戝舰缁撴瀯绠＄悊
    - 鑿滃崟鏉冮檺绠＄悊
    
    浣跨敤鏂规硶锛?        menu_service = MenuService(db)
        menu = menu_service.create_menu(name="鐢ㄦ埛绠＄悊", code="user_manage")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栬彍鍗曟湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.menu_repo = MenuRepository(db)
    
    def create_menu(self, menu_data: Dict[str, Any]) -> Menu:
        """
        鍒涘缓鑿滃崟
        
        Args:
            menu_data: 鑿滃崟鏁版嵁
        
        Returns:
            Menu: 鍒涘缓鐨勮彍鍗曞璞?        
        Raises:
            ValueError: 鑿滃崟缂栫爜宸插瓨鍦?            ValueError: 鐖惰彍鍗曚笉瀛樺湪
            ValueError: 鐖惰彍鍗曚笉灞炰簬璇ョ鎴?            ValueError: 鑿滃崟璺緞宸插瓨鍦?        """
        logger.info(f"鍒涘缓鑿滃崟: name={menu_data.get('name')}, code={menu_data.get('code')}")
        
        # 妫€鏌ヨ彍鍗曠紪鐮佹槸鍚﹀凡瀛樺湪
        if self.menu_repo.exists_by_code(menu_data.get("code")):
            raise ValueError("鑿滃崟缂栫爜宸插瓨鍦?)
        
        # 楠岃瘉鐖惰彍鍗?        parent_id = menu_data.get("parent_id")
        tenant_id = menu_data.get("tenant_id")
        if parent_id:
            parent_menu = self.menu_repo.get_by_id(parent_id)
            if not parent_menu:
                raise ValueError("鐖惰彍鍗曚笉瀛樺湪")
            if tenant_id and parent_menu.tenant_id != tenant_id:
                raise ValueError("鐖惰彍鍗曚笉灞炰簬璇ョ鎴?)
            # 璁剧疆灞傜骇
            menu_data["level"] = parent_menu.level + 1
        
        # 妫€鏌ヨ彍鍗曡矾寰勬槸鍚﹀凡瀛樺湪
        path = menu_data.get("path")
        if path and tenant_id:
            if self.menu_repo.exists_by_path_in_tenant(path, tenant_id):
                raise ValueError("鑿滃崟璺緞宸插瓨鍦?)
        
        # 鍒涘缓鑿滃崟
        menu = Menu(**menu_data)
        return self.menu_repo.create(menu)
    
    def get_menu(self, menu_id: str) -> Optional[Menu]:
        """
        鑾峰彇鑿滃崟
        
        Args:
            menu_id: 鑿滃崟ID
        
        Returns:
            Optional[Menu]: 鑿滃崟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.menu_repo.get_by_id(menu_id)
    
    def get_menu_by_code(self, code: str) -> Optional[Menu]:
        """
        鏍规嵁缂栫爜鑾峰彇鑿滃崟
        
        Args:
            code: 鑿滃崟缂栫爜
        
        Returns:
            Optional[Menu]: 鑿滃崟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.menu_repo.get_by_code(code)
    
    def update_menu(self, menu_id: str, menu_data: Dict[str, Any]) -> Optional[Menu]:
        """
        鏇存柊鑿滃崟
        
        Args:
            menu_id: 鑿滃崟ID
            menu_data: 鑿滃崟鏁版嵁
        
        Returns:
            Optional[Menu]: 鏇存柊鍚庣殑鑿滃崟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        
        Raises:
            ValueError: 鐖惰彍鍗曚笉瀛樺湪
            ValueError: 鐖惰彍鍗曚笉灞炰簬璇ョ鎴?            ValueError: 涓嶈兘灏嗚彍鍗曡缃负鑷繁鐨勫瓙鑿滃崟
            ValueError: 鑿滃崟璺緞宸茶鍏朵粬鑿滃崟浣跨敤
        """
        logger.info(f"鏇存柊鑿滃崟: menu_id={menu_id}")
        
        menu = self.menu_repo.get_by_id(menu_id)
        if not menu:
            return None
        
        # 楠岃瘉鐖惰彍鍗?        if "parent_id" in menu_data:
            parent_id = menu_data["parent_id"]
            if parent_id:
                parent_menu = self.menu_repo.get_by_id(parent_id)
                if not parent_menu:
                    raise ValueError("鐖惰彍鍗曚笉瀛樺湪")
                if parent_menu.tenant_id != menu.tenant_id:
                    raise ValueError("鐖惰彍鍗曚笉灞炰簬璇ョ鎴?)
                # 妫€鏌ユ槸鍚﹀皢鑿滃崟璁剧疆涓鸿嚜宸辩殑瀛愯彍鍗?                if parent_id == menu_id:
                    raise ValueError("涓嶈兘灏嗚彍鍗曡缃负鑷繁鐨勫瓙鑿滃崟")
                # 璁剧疆灞傜骇
                menu_data["level"] = parent_menu.level + 1
        
        # 妫€鏌ヨ彍鍗曡矾寰勬槸鍚﹁鍏朵粬鑿滃崟浣跨敤
        if "path" in menu_data and menu_data["path"]:
            existing_menu = self.menu_repo.exists_by_path_in_tenant(menu_data["path"], menu.tenant_id)
            if existing_menu and existing_menu.id != menu_id:
                raise ValueError("鑿滃崟璺緞宸茶鍏朵粬鑿滃崟浣跨敤")
        
        # 鏇存柊鑿滃崟
        for key, value in menu_data.items():
            if hasattr(menu, key):
                setattr(menu, key, value)
        
        return self.menu_repo.update(menu)
    
    def delete_menu(self, menu_id: str) -> bool:
        """
        鍒犻櫎鑿滃崟
        
        Args:
            menu_id: 鑿滃崟ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎鑿滃崟: menu_id={menu_id}")
        return self.menu_repo.delete(menu_id)
    
    def list_menus(self, tenant_id: Optional[str] = None, parent_id: Optional[str] = None,
                   keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        鑾峰彇鑿滃崟鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            parent_id: 鐖惰彍鍗旾D锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        if keyword:
            return self.menu_repo.search(keyword, tenant_id, page, page_size)
        elif parent_id:
            return self.menu_repo.get_by_parent_id(parent_id, page, page_size)
        elif tenant_id:
            return self.menu_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.menu_repo.get_all(page, page_size)
    
    def get_menu_tree(self, tenant_id: str) -> List[Menu]:
        """
        鑾峰彇鑿滃崟鏍?        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            List[Menu]: 鑿滃崟鏍?        """
        return self.menu_repo.get_tree(tenant_id)
    
    def get_visible_menus(self, tenant_id: str) -> List[Menu]:
        """
        鑾峰彇鍙鑿滃崟
        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            List[Menu]: 鍙鑿滃崟鍒楄〃
        """
        return self.menu_repo.get_visible_menus(tenant_id)
    
    def get_user_menus(self, user_id: str) -> List[Menu]:
        """
        鑾峰彇鐢ㄦ埛鑿滃崟
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            List[Menu]: 鐢ㄦ埛鑿滃崟鍒楄〃
        """
        # 鑾峰彇鐢ㄦ埛鐨勬墍鏈夎鑹?        from common.database.models.user import Role
        roles = self.db.query(Role).join("users").filter(users.id == user_id).all()
        
        # 鏀堕泦鎵€鏈夎彍鍗旾D
        menu_ids = set()
        for role in roles:
            for menu in role.menus:
                menu_ids.add(menu.id)
        
        # 鑾峰彇鑿滃崟
        menus = []
        for menu_id in menu_ids:
            menu = self.menu_repo.get_by_id(menu_id)
            if menu and menu.is_visible_menu():
                menus.append(menu)
        
        return menus
    
    def count_menus(self, tenant_id: Optional[str] = None, parent_id: Optional[str] = None) -> int:
        """
        缁熻鑿滃崟鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            parent_id: 鐖惰彍鍗旾D锛堝彲閫夛級
        
        Returns:
            int: 鑿滃崟鏁伴噺
        """
        if parent_id:
            return self.menu_repo.count_by_parent(parent_id)
        elif tenant_id:
            return self.menu_repo.count_by_tenant(tenant_id)
        else:
            return self.menu_repo.count_all()
    
    def search_menus(self, query_params: Dict[str, Any], offset: int = 0, limit: int = 10) -> tuple:
        """
        鎼滅储鑿滃崟
        
        Args:
            query_params: 鏌ヨ鍙傛暟
            offset: 鍋忕Щ閲?            limit: 闄愬埗鏁伴噺
        
        Returns:
            tuple: (鑿滃崟鍒楄〃, 鎬绘暟)
        """
        from sqlalchemy import and_
        
        query = self.db.query(Menu)
        
        # 绉熸埛ID杩囨护
        if query_params.get("tenant_id"):
            query = query.filter(Menu.tenant_id == query_params["tenant_id"])
        
        # 鐘舵€佽繃婊?        if query_params.get("status"):
            query = query.filter(Menu.status == query_params["status"])
        
        # 缁熻鎬绘暟
        total = query.count()
        
        # 鍒嗛〉
        menus = query.offset(offset).limit(limit).all()
        
        return menus, total
