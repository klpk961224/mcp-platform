# -*- coding: utf-8 -*-
"""
菜单服务

功能说明：
1. 菜单CRUD操作
2. 菜单树形结构管理
3. 菜单权限管理

使用示例：
    from app.services.menu_service import MenuService
    
    menu_service = MenuService(db)
    menu = menu_service.create_menu(name="用户管理", code="user_manage")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.permission import Menu
from app.repositories.menu_repository import MenuRepository


class MenuService:
    """
    菜单服务
    
    功能：
    - 菜单CRUD操作
    - 菜单树形结构管理
    - 菜单权限管理
    
    使用方法：
        menu_service = MenuService(db)
        menu = menu_service.create_menu(name="用户管理", code="user_manage")
    """
    
    def __init__(self, db: Session):
        """
        初始化菜单服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.menu_repo = MenuRepository(db)
    
    def create_menu(self, menu_data: Dict[str, Any]) -> Menu:
        """
        创建菜单
        
        Args:
            menu_data: 菜单数据
        
        Returns:
            Menu: 创建的菜单对象
        
        Raises:
            ValueError: 菜单编码已存在
            ValueError: 父菜单不存在
            ValueError: 父菜单不属于该租户
            ValueError: 菜单路径已存在
        """
        logger.info(f"创建菜单: name={menu_data.get('name')}, code={menu_data.get('code')}")
        
        # 检查菜单编码是否已存在
        if self.menu_repo.exists_by_code(menu_data.get("code")):
            raise ValueError("菜单编码已存在")
        
        # 验证父菜单
        parent_id = menu_data.get("parent_id")
        tenant_id = menu_data.get("tenant_id")
        if parent_id:
            parent_menu = self.menu_repo.get_by_id(parent_id)
            if not parent_menu:
                raise ValueError("父菜单不存在")
            if tenant_id and parent_menu.tenant_id != tenant_id:
                raise ValueError("父菜单不属于该租户")
            # 设置层级
            menu_data["level"] = parent_menu.level + 1
        
        # 检查菜单路径是否已存在
        path = menu_data.get("path")
        if path and tenant_id:
            if self.menu_repo.exists_by_path_in_tenant(path, tenant_id):
                raise ValueError("菜单路径已存在")
        
        # 创建菜单
        menu = Menu(**menu_data)
        return self.menu_repo.create(menu)
    
    def get_menu(self, menu_id: str) -> Optional[Menu]:
        """
        获取菜单
        
        Args:
            menu_id: 菜单ID
        
        Returns:
            Optional[Menu]: 菜单对象，不存在返回None
        """
        return self.menu_repo.get_by_id(menu_id)
    
    def get_menu_by_code(self, code: str) -> Optional[Menu]:
        """
        根据编码获取菜单
        
        Args:
            code: 菜单编码
        
        Returns:
            Optional[Menu]: 菜单对象，不存在返回None
        """
        return self.menu_repo.get_by_code(code)
    
    def update_menu(self, menu_id: str, menu_data: Dict[str, Any]) -> Optional[Menu]:
        """
        更新菜单
        
        Args:
            menu_id: 菜单ID
            menu_data: 菜单数据
        
        Returns:
            Optional[Menu]: 更新后的菜单对象，不存在返回None
        
        Raises:
            ValueError: 父菜单不存在
            ValueError: 父菜单不属于该租户
            ValueError: 不能将菜单设置为自己的子菜单
            ValueError: 菜单路径已被其他菜单使用
        """
        logger.info(f"更新菜单: menu_id={menu_id}")
        
        menu = self.menu_repo.get_by_id(menu_id)
        if not menu:
            return None
        
        # 验证父菜单
        if "parent_id" in menu_data:
            parent_id = menu_data["parent_id"]
            if parent_id:
                parent_menu = self.menu_repo.get_by_id(parent_id)
                if not parent_menu:
                    raise ValueError("父菜单不存在")
                if parent_menu.tenant_id != menu.tenant_id:
                    raise ValueError("父菜单不属于该租户")
                # 检查是否将菜单设置为自己的子菜单
                if parent_id == menu_id:
                    raise ValueError("不能将菜单设置为自己的子菜单")
                # 设置层级
                menu_data["level"] = parent_menu.level + 1
        
        # 检查菜单路径是否被其他菜单使用
        if "path" in menu_data and menu_data["path"]:
            existing_menu = self.menu_repo.exists_by_path_in_tenant(menu_data["path"], menu.tenant_id)
            if existing_menu and existing_menu.id != menu_id:
                raise ValueError("菜单路径已被其他菜单使用")
        
        # 更新菜单
        for key, value in menu_data.items():
            if hasattr(menu, key):
                setattr(menu, key, value)
        
        return self.menu_repo.update(menu)
    
    def delete_menu(self, menu_id: str) -> bool:
        """
        删除菜单
        
        Args:
            menu_id: 菜单ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除菜单: menu_id={menu_id}")
        return self.menu_repo.delete(menu_id)
    
    def list_menus(self, tenant_id: Optional[str] = None, parent_id: Optional[str] = None,
                   keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Menu]:
        """
        获取菜单列表
        
        Args:
            tenant_id: 租户ID（可选）
            parent_id: 父菜单ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Menu]: 菜单列表
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
        获取菜单树
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Menu]: 菜单树
        """
        return self.menu_repo.get_tree(tenant_id)
    
    def get_visible_menus(self, tenant_id: str) -> List[Menu]:
        """
        获取可见菜单
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Menu]: 可见菜单列表
        """
        return self.menu_repo.get_visible_menus(tenant_id)
    
    def get_user_menus(self, user_id: str) -> List[Menu]:
        """
        获取用户菜单
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Menu]: 用户菜单列表
        """
        # 获取用户的所有角色
        from common.database.models.user import Role
        roles = self.db.query(Role).join("users").filter(users.id == user_id).all()
        
        # 收集所有菜单ID
        menu_ids = set()
        for role in roles:
            for menu in role.menus:
                menu_ids.add(menu.id)
        
        # 获取菜单
        menus = []
        for menu_id in menu_ids:
            menu = self.menu_repo.get_by_id(menu_id)
            if menu and menu.is_visible_menu():
                menus.append(menu)
        
        return menus
    
    def count_menus(self, tenant_id: Optional[str] = None, parent_id: Optional[str] = None) -> int:
        """
        统计菜单数量
        
        Args:
            tenant_id: 租户ID（可选）
            parent_id: 父菜单ID（可选）
        
        Returns:
            int: 菜单数量
        """
        if parent_id:
            return self.menu_repo.count_by_parent(parent_id)
        elif tenant_id:
            return self.menu_repo.count_by_tenant(tenant_id)
        else:
            return self.menu_repo.count_all()
    
    def search_menus(self, query_params: Dict[str, Any], offset: int = 0, limit: int = 10) -> tuple:
        """
        搜索菜单
        
        Args:
            query_params: 查询参数
            offset: 偏移量
            limit: 限制数量
        
        Returns:
            tuple: (菜单列表, 总数)
        """
        from sqlalchemy import and_
        
        query = self.db.query(Menu)
        
        # 租户ID过滤
        if query_params.get("tenant_id"):
            query = query.filter(Menu.tenant_id == query_params["tenant_id"])
        
        # 状态过滤
        if query_params.get("status"):
            query = query.filter(Menu.status == query_params["status"])
        
        # 统计总数
        total = query.count()
        
        # 分页
        menus = query.offset(offset).limit(limit).all()
        
        return menus, total