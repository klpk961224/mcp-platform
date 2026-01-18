# -*- coding: utf-8 -*-
"""
菜单数据访问层

功能说明：
1. 菜单CRUD操作
2. 菜单树形结构查询
3. 菜单统计操作

使用示例：
    from app.repositories.menu_repository import MenuRepository
    
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
    菜单数据访问层
    
    功能：
    - 菜单CRUD操作
    - 菜单树形结构查询
    - 菜单统计操作
    
    使用方法：
        menu_repo = MenuRepository(db)
        menu = menu_repo.get_by_code("user_manage")
    """
    
    def __init__(self, db: Session):
        """
        初始化菜单数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, menu: Menu) -> Menu:
        """
        创建菜单
        
        Args:
            menu: 菜单对象
        
        Returns:
            Menu: 创建的菜单对象
        """
        logger.info(f"创建菜单: name={menu.name}, code={menu.code}, tenant_id={menu.tenant_id}")
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        """
        根据ID获取菜单
        
        Args:
            menu_id: 菜单ID
        
        Returns:
            Optional[Menu]: 菜单对象，不存在返回None
        """
        return self.db.query(Menu).filter(Menu.id == menu_id).first()
    
    def get_by_code(self, code: str) -> Optional[Menu]:
        """
        根据编码获取菜单
        
        Args:
            code: 菜单编码
        
        Returns:
            Optional[Menu]: 菜单对象，不存在返回None
        """
        return self.db.query(Menu).filter(Menu.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        根据租户ID获取菜单列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Menu]: 菜单列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).filter(Menu.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_parent_id(self, parent_id: str, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        根据父菜单ID获取子菜单列表
        
        Args:
            parent_id: 父菜单ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Menu]: 菜单列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).filter(Menu.parent_id == parent_id).offset(offset).limit(page_size).all()
    
    def get_root_menus(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        获取租户的根菜单（没有父菜单的菜单）
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Menu]: 菜单列表
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
        获取租户的菜单树
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Menu]: 菜单树
        """
        root_menus = self.get_root_menus(tenant_id, page=1, page_size=1000)
        return root_menus
    
    def get_visible_menus(self, tenant_id: str) -> List[Menu]:
        """
        获取租户的可见菜单
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Menu]: 菜单列表
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
        根据角色ID获取菜单列表
        
        Args:
            role_id: 角色ID
        
        Returns:
            List[Menu]: 菜单列表
        """
        return self.db.query(Menu).join("roles").filter(roles.id == role_id).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        搜索菜单
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Menu]: 菜单列表
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
        获取所有菜单
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Menu]: 菜单列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Menu).offset(offset).limit(page_size).all()
    
    def update(self, menu: Menu) -> Menu:
        """
        更新菜单
        
        Args:
            menu: 菜单对象
        
        Returns:
            Menu: 更新后的菜单对象
        """
        logger.info(f"更新菜单: menu_id={menu.id}")
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def delete(self, menu_id: str) -> bool:
        """
        删除菜单
        
        Args:
            menu_id: 菜单ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除菜单: menu_id={menu_id}")
        menu = self.get_by_id(menu_id)
        if not menu:
            return False
        
        # 检查是否有子菜单
        if menu.children:
            raise ValueError("无法删除菜单：该菜单下存在子菜单")
        
        # 检查是否有角色使用
        if menu.roles:
            raise ValueError("无法删除菜单：该菜单被角色使用")
        
        self.db.delete(menu)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户菜单数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 菜单数量
        """
        return self.db.query(Menu).filter(Menu.tenant_id == tenant_id).count()
    
    def count_by_parent(self, parent_id: str) -> int:
        """
        统计子菜单数量
        
        Args:
            parent_id: 父菜单ID
        
        Returns:
            int: 子菜单数量
        """
        return self.db.query(Menu).filter(Menu.parent_id == parent_id).count()
    
    def count_all(self) -> int:
        """
        统计所有菜单数量
        
        Returns:
            int: 菜单数量
        """
        return self.db.query(Menu).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查菜单编码是否存在
        
        Args:
            code: 菜单编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Menu).filter(Menu.code == code).first() is not None
    
    def exists_by_path_in_tenant(self, path: str, tenant_id: str) -> bool:
        """
        检查租户内菜单路径是否存在
        
        Args:
            path: 菜单路径
            tenant_id: 租户ID
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Menu).filter(
            and_(
                Menu.path == path,
                Menu.tenant_id == tenant_id
            )
        ).first() is not None