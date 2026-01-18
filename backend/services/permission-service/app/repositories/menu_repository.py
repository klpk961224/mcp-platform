# -*- coding: utf-8 -*-
"""
鑿滃崟鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 鑿滃崟CRUD鎿嶄綔
2. 鑿滃崟鏍戝舰缁撴瀯查询
3. 鑿滃崟缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.menu_repository import MenuRepository
    
    menu_repo = MenuRepository(db)
    menu = menu_repo.get_by_code("user_manage")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.permission import Menu


class MenuRepository:
    """
    鑿滃崟鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 鑿滃崟CRUD鎿嶄綔
    - 鑿滃崟鏍戝舰缁撴瀯查询
    - 鑿滃崟缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        menu_repo = MenuRepository(db)
        menu = menu_repo.get_by_code("user_manage")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栬彍鍗曟暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, menu: Menu) -> Menu:
        """
        创建鑿滃崟
        
        Args:
            menu: 鑿滃崟瀵硅薄
        
        Returns:
            Menu: 创建鐨勮彍鍗曞璞?        """
        logger.info(f"创建鑿滃崟: name={menu.name}, code={menu.code}, tenant_id={menu.tenant_id}")
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        """
        根据ID鑾峰彇鑿滃崟
        
        Args:
            menu_id: 鑿滃崟ID
        
        Returns:
            Optional[Menu]: 鑿滃崟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Menu).filter(Menu.id == menu_id).first()
    
    def get_by_code(self, code: str) -> Optional[Menu]:
        """
        根据编码鑾峰彇鑿滃崟
        
        Args:
            code: 鑿滃崟编码
        
        Returns:
            Optional[Menu]: 鑿滃崟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Menu).filter(Menu.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        根据租户ID鑾峰彇鑿滃崟鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).filter(Menu.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_parent_id(self, parent_id: str, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        根据鐖惰彍鍗旾D鑾峰彇瀛愯彍鍗曞垪琛?        
        Args:
            parent_id: 鐖惰彍鍗旾D
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).filter(Menu.parent_id == parent_id).offset(offset).limit(page_size).all()
    
    def get_root_menus(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        鑾峰彇绉熸埛鐨勬牴鑿滃崟锛堟病鏈夌埗鑿滃崟鐨勮彍鍗曪級
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).filter(
            and_(
                Menu.tenant_id == tenant_id,
                Menu.parent_id.is_(None)
            )
        ).offset(offset).limit(page_size).all()
    
    def get_tree(self, tenant_id: str) -> List[Menu]:
        """
        鑾峰彇绉熸埛鐨勮彍鍗曟爲
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Menu]: 鑿滃崟鏍?        """
        root_menus = self.get_root_menus(tenant_id, page=1, page_size=1000)
        return root_menus
    
    def get_visible_menus(self, tenant_id: str) -> List[Menu]:
        """
        鑾峰彇绉熸埛鐨勫彲瑙佽彍鍗?        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        return self.db.query(Menu).filter(
            and_(
                Menu.tenant_id == tenant_id,
                Menu.is_visible == "1",
                Menu.menu_type == "menu"
            )
        ).order_by(Menu.sort_order).all()
    
    def get_by_role_id(self, role_id: str) -> List[Menu]:
        """
        根据角色ID鑾峰彇鑿滃崟鍒楄〃
        
        Args:
            role_id: 角色ID
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        return self.db.query(Menu).join("roles").filter(roles.id == role_id).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        鎼滅储鑿滃崟
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        offset = (page - 1) * page_size
        query = self.db.query(Menu).filter(
            or_(
                Menu.name.like(f"%{keyword}%"),
                Menu.code.like(f"%{keyword}%"),
                Menu.title.like(f"%{keyword}%"),
                Menu.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Menu.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        鑾峰彇鎵€鏈夎彍鍗?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Menu]: 鑿滃崟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).offset(offset).limit(page_size).all()
    
    def update(self, menu: Menu) -> Menu:
        """
        更新鑿滃崟
        
        Args:
            menu: 鑿滃崟瀵硅薄
        
        Returns:
            Menu: 更新鍚庣殑鑿滃崟瀵硅薄
        """
        logger.info(f"更新鑿滃崟: menu_id={menu.id}")
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def delete(self, menu_id: str) -> bool:
        """
        删除鑿滃崟
        
        Args:
            menu_id: 鑿滃崟ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除鑿滃崟: menu_id={menu_id}")
        menu = self.get_by_id(menu_id)
        if not menu:
            return False
        
        # 妫€鏌ユ槸鍚︽湁瀛愯彍鍗?        if menu.children:
            raise ValueError("鏃犳硶删除鑿滃崟锛氳鑿滃崟涓嬪瓨鍦ㄥ瓙鑿滃崟")
        
        # 妫€鏌ユ槸鍚︽湁瑙掕壊浣跨敤
        if menu.roles:
            raise ValueError("鏃犳硶删除鑿滃崟锛氳鑿滃崟琚鑹蹭娇鐢?)
        
        self.db.delete(menu)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛鑿滃崟数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 鑿滃崟数量
        """
        return self.db.query(Menu).filter(Menu.tenant_id == tenant_id).count()
    
    def count_by_parent(self, parent_id: str) -> int:
        """
        缁熻瀛愯彍鍗曟暟閲?        
        Args:
            parent_id: 鐖惰彍鍗旾D
        
        Returns:
            int: 瀛愯彍鍗曟暟閲?        """
        return self.db.query(Menu).filter(Menu.parent_id == parent_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夎彍鍗曟暟閲?        
        Returns:
            int: 鑿滃崟数量
        """
        return self.db.query(Menu).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€查询彍鍗曠紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 鑿滃崟编码
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Menu).filter(Menu.code == code).first() is not None
    
    def exists_by_path_in_tenant(self, path: str, tenant_id: str) -> bool:
        """
        妫€鏌ョ鎴峰唴鑿滃崟璺緞鏄惁瀛樺湪
        
        Args:
            path: 鑿滃崟璺緞
            tenant_id: 租户ID
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Menu).filter(
            and_(
                Menu.path == path,
                Menu.tenant_id == tenant_id
            )
        ).first() is not None
