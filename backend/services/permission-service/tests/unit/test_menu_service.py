# -*- coding: utf-8 -*-
"""
MenuService单元测试

测试内容：
1. 创建菜单
2. 获取菜单
3. 更新菜单
4. 删除菜单
5. 获取菜单列表
6. 获取菜单树
7. 获取可见菜单
8. 获取用户菜单
9. 统计菜单数量
10. 搜索菜单
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.menu_service import MenuService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_menu():
    """模拟菜单对象"""
    menu = Mock()
    menu.id = "test_menu_id"
    menu.name = "用户管理"
    menu.code = "user_manage"
    menu.path = "/user"
    menu.icon = "user"
    menu.tenant_id = "default"
    menu.parent_id = None
    menu.level = 1
    menu.sort_order = 0
    menu.status = "active"
    menu.is_visible_menu = Mock(return_value=True)
    return menu


@pytest.fixture
def menu_service(mock_db):
    """创建MenuService实例"""
    return MenuService(mock_db)


class TestMenuService:
    """MenuService测试类"""
    
    def test_init(self, mock_db):
        """测试MenuService初始化"""
        service = MenuService(mock_db)
        assert service.db == mock_db
        assert service.menu_repo is not None
    
    def test_create_menu_success(self, menu_service, mock_menu):
        """测试创建菜单成功"""
        # 模拟菜单编码不存在
        menu_service.menu_repo.exists_by_code = Mock(return_value=False)
        # 模拟菜单路径不存在
        menu_service.menu_repo.exists_by_path_in_tenant = Mock(return_value=False)
        # 模拟创建菜单
        menu_service.menu_repo.create = Mock(return_value=mock_menu)
        
        # 执行创建菜单
        menu_data = {
            "name": "用户管理",
            "code": "user_manage",
            "path": "/user",
            "tenant_id": "default"
        }
        result = menu_service.create_menu(menu_data)
        
        # 验证结果
        assert result.id == "test_menu_id"
        assert result.name == "用户管理"
        menu_service.menu_repo.create.assert_called_once()
    
    def test_create_menu_code_exists(self, menu_service):
        """测试创建菜单（编码已存在）"""
        # 模拟菜单编码已存在
        menu_service.menu_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建菜单并验证异常
        menu_data = {
            "name": "用户管理",
            "code": "existing_code",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="菜单编码已存在"):
            menu_service.create_menu(menu_data)
    
    def test_create_menu_parent_not_found(self, menu_service):
        """测试创建菜单（父菜单不存在）"""
        # 模拟菜单编码不存在
        menu_service.menu_repo.exists_by_code = Mock(return_value=False)
        # 模拟父菜单不存在
        menu_service.menu_repo.get_by_id = Mock(return_value=None)
        
        # 执行创建菜单并验证异常
        menu_data = {
            "name": "用户管理",
            "code": "user_manage",
            "parent_id": "nonexistent_id",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="父菜单不存在"):
            menu_service.create_menu(menu_data)
    
    def test_create_menu_path_exists(self, menu_service):
        """测试创建菜单（路径已存在）"""
        # 模拟菜单编码不存在
        menu_service.menu_repo.exists_by_code = Mock(return_value=False)
        # 模拟菜单路径已存在
        menu_service.menu_repo.exists_by_path_in_tenant = Mock(return_value=True)
        
        # 执行创建菜单并验证异常
        menu_data = {
            "name": "用户管理",
            "code": "user_manage",
            "path": "/existing_path",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="菜单路径已存在"):
            menu_service.create_menu(menu_data)
    
    def test_get_menu_success(self, menu_service, mock_menu):
        """测试获取菜单成功"""
        # 模拟查询菜单
        menu_service.menu_repo.get_by_id = Mock(return_value=mock_menu)
        
        # 执行查询
        result = menu_service.get_menu("test_menu_id")
        
        # 验证结果
        assert result.id == "test_menu_id"
        menu_service.menu_repo.get_by_id.assert_called_once_with("test_menu_id")
    
    def test_get_menu_not_found(self, menu_service):
        """测试获取菜单失败"""
        # 模拟查询菜单返回None
        menu_service.menu_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = menu_service.get_menu("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_menu_by_code_success(self, menu_service, mock_menu):
        """测试根据编码获取菜单成功"""
        # 模拟查询菜单
        menu_service.menu_repo.get_by_code = Mock(return_value=mock_menu)
        
        # 执行查询
        result = menu_service.get_menu_by_code("user_manage")
        
        # 验证结果
        assert result.code == "user_manage"
        menu_service.menu_repo.get_by_code.assert_called_once_with("user_manage")
    
    def test_update_menu_success(self, menu_service, mock_menu):
        """测试更新菜单成功"""
        # 模拟查询菜单
        menu_service.menu_repo.get_by_id = Mock(return_value=mock_menu)
        # 模拟菜单路径不存在
        menu_service.menu_repo.exists_by_path_in_tenant = Mock(return_value=False)
        # 模拟更新菜单
        menu_service.menu_repo.update = Mock(return_value=mock_menu)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = menu_service.update_menu("test_menu_id", update_data)
        
        # 验证结果
        assert result.id == "test_menu_id"
        menu_service.menu_repo.update.assert_called_once()
    
    def test_update_menu_not_found(self, menu_service):
        """测试更新菜单失败（菜单不存在）"""
        # 模拟查询菜单返回None
        menu_service.menu_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = menu_service.update_menu("nonexistent_id", update_data)
        
        # 验证结果
        assert result is None
    
    def test_delete_menu_success(self, menu_service):
        """测试删除菜单成功"""
        # 模拟删除菜单
        menu_service.menu_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = menu_service.delete_menu("test_menu_id")
        
        # 验证结果
        assert result is True
        menu_service.menu_repo.delete.assert_called_once_with("test_menu_id")
    
    def test_list_menus_success(self, menu_service, mock_menu):
        """测试获取菜单列表成功"""
        # 模拟查询菜单列表
        menu_service.menu_repo.get_by_tenant_id = Mock(return_value=[mock_menu])
        
        # 执行查询
        result = menu_service.list_menus(tenant_id="default")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_menu_id"
    
    def test_get_menu_tree_success(self, menu_service, mock_menu):
        """测试获取菜单树成功"""
        # 模拟查询菜单树
        menu_service.menu_repo.get_tree = Mock(return_value=[mock_menu])
        
        # 执行查询
        result = menu_service.get_menu_tree(tenant_id="default")
        
        # 验证结果
        assert len(result) == 1
    
    def test_get_visible_menus_success(self, menu_service, mock_menu):
        """测试获取可见菜单成功"""
        # 模拟查询可见菜单
        menu_service.menu_repo.get_visible_menus = Mock(return_value=[mock_menu])
        
        # 执行查询
        result = menu_service.get_visible_menus(tenant_id="default")
        
        # 验证结果
        assert len(result) == 1
    
    def test_count_menus_success(self, menu_service):
        """测试统计菜单数量成功"""
        # 模拟统计
        menu_service.menu_repo.count_by_tenant = Mock(return_value=10)
        
        # 执行统计
        result = menu_service.count_menus(tenant_id="default")
        
        # 验证结果
        assert result == 10
    
    def test_search_menus_success(self, menu_service, mock_menu):
        """测试搜索菜单成功"""
        # 模拟查询
        mock_query = Mock()
        mock_query.filter = Mock(return_value=mock_query)
        mock_query.count = Mock(return_value=1)
        mock_query.offset = Mock(return_value=mock_query)
        mock_query.limit = Mock(return_value=[mock_menu])
        menu_service.db.query = Mock(return_value=mock_query)
        
        # 执行搜索
        result = menu_service.search_menus({"tenant_id": "default"})
        
        # 验证结果
        assert len(result[0]) == 1
        assert result[1] == 1