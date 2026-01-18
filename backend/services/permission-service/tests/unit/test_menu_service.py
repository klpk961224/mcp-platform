# -*- coding: utf-8 -*-
"""
MenuService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建鑿滃崟
2. 鑾峰彇鑿滃崟
3. 更新鑿滃崟
4. 删除鑿滃崟
5. 鑾峰彇鑿滃崟鍒楄〃
6. 鑾峰彇鑿滃崟鏍?7. 鑾峰彇鍙鑿滃崟
8. 鑾峰彇鐢ㄦ埛鑿滃崟
9. 缁熻鑿滃崟数量
10. 鎼滅储鑿滃崟
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.menu_service import MenuService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_menu():
    """妯℃嫙鑿滃崟瀵硅薄"""
    menu = Mock()
    menu.id = "test_menu_id"
    menu.name = "鐢ㄦ埛绠＄悊"
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
    """创建MenuService瀹炰緥"""
    return MenuService(mock_db)


class TestMenuService:
    """MenuService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯MenuService鍒濆鍖?""
        service = MenuService(mock_db)
        assert service.db == mock_db
        assert service.menu_repo is not None
    
    def test_create_menu_success(self, menu_service, mock_menu):
        """娴嬭瘯创建鑿滃崟鎴愬姛"""
        # 妯℃嫙鑿滃崟编码涓嶅瓨鍦?        menu_service.menu_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙鑿滃崟璺緞涓嶅瓨鍦?        menu_service.menu_repo.exists_by_path_in_tenant = Mock(return_value=False)
        # 妯℃嫙创建鑿滃崟
        menu_service.menu_repo.create = Mock(return_value=mock_menu)
        
        # 鎵ц创建鑿滃崟
        menu_data = {
            "name": "鐢ㄦ埛绠＄悊",
            "code": "user_manage",
            "path": "/user",
            "tenant_id": "default"
        }
        result = menu_service.create_menu(menu_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_menu_id"
        assert result.name == "鐢ㄦ埛绠＄悊"
        menu_service.menu_repo.create.assert_called_once()
    
    def test_create_menu_code_exists(self, menu_service):
        """娴嬭瘯创建鑿滃崟锛堢紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙鑿滃崟编码宸插瓨鍦?        menu_service.menu_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц创建鑿滃崟骞堕獙璇佸紓甯?        menu_data = {
            "name": "鐢ㄦ埛绠＄悊",
            "code": "existing_code",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="鑿滃崟编码宸插瓨鍦?):
            menu_service.create_menu(menu_data)
    
    def test_create_menu_parent_not_found(self, menu_service):
        """娴嬭瘯创建鑿滃崟锛堢埗鑿滃崟涓嶅瓨鍦級"""
        # 妯℃嫙鑿滃崟编码涓嶅瓨鍦?        menu_service.menu_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙鐖惰彍鍗曚笉瀛樺湪
        menu_service.menu_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц创建鑿滃崟骞堕獙璇佸紓甯?        menu_data = {
            "name": "鐢ㄦ埛绠＄悊",
            "code": "user_manage",
            "parent_id": "nonexistent_id",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="鐖惰彍鍗曚笉瀛樺湪"):
            menu_service.create_menu(menu_data)
    
    def test_create_menu_path_exists(self, menu_service):
        """娴嬭瘯创建鑿滃崟锛堣矾寰勫凡瀛樺湪锛?""
        # 妯℃嫙鑿滃崟编码涓嶅瓨鍦?        menu_service.menu_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙鑿滃崟璺緞宸插瓨鍦?        menu_service.menu_repo.exists_by_path_in_tenant = Mock(return_value=True)
        
        # 鎵ц创建鑿滃崟骞堕獙璇佸紓甯?        menu_data = {
            "name": "鐢ㄦ埛绠＄悊",
            "code": "user_manage",
            "path": "/existing_path",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="鑿滃崟璺緞宸插瓨鍦?):
            menu_service.create_menu(menu_data)
    
    def test_get_menu_success(self, menu_service, mock_menu):
        """娴嬭瘯鑾峰彇鑿滃崟鎴愬姛"""
        # 妯℃嫙查询鑿滃崟
        menu_service.menu_repo.get_by_id = Mock(return_value=mock_menu)
        
        # 鎵ц查询
        result = menu_service.get_menu("test_menu_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_menu_id"
        menu_service.menu_repo.get_by_id.assert_called_once_with("test_menu_id")
    
    def test_get_menu_not_found(self, menu_service):
        """娴嬭瘯鑾峰彇鑿滃崟澶辫触"""
        # 妯℃嫙查询鑿滃崟杩斿洖None
        menu_service.menu_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = menu_service.get_menu("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_menu_by_code_success(self, menu_service, mock_menu):
        """娴嬭瘯根据编码鑾峰彇鑿滃崟鎴愬姛"""
        # 妯℃嫙查询鑿滃崟
        menu_service.menu_repo.get_by_code = Mock(return_value=mock_menu)
        
        # 鎵ц查询
        result = menu_service.get_menu_by_code("user_manage")
        
        # 楠岃瘉缁撴灉
        assert result.code == "user_manage"
        menu_service.menu_repo.get_by_code.assert_called_once_with("user_manage")
    
    def test_update_menu_success(self, menu_service, mock_menu):
        """娴嬭瘯更新鑿滃崟鎴愬姛"""
        # 妯℃嫙查询鑿滃崟
        menu_service.menu_repo.get_by_id = Mock(return_value=mock_menu)
        # 妯℃嫙鑿滃崟璺緞涓嶅瓨鍦?        menu_service.menu_repo.exists_by_path_in_tenant = Mock(return_value=False)
        # 妯℃嫙更新鑿滃崟
        menu_service.menu_repo.update = Mock(return_value=mock_menu)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = menu_service.update_menu("test_menu_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_menu_id"
        menu_service.menu_repo.update.assert_called_once()
    
    def test_update_menu_not_found(self, menu_service):
        """娴嬭瘯更新鑿滃崟澶辫触锛堣彍鍗曚笉瀛樺湪锛?""
        # 妯℃嫙查询鑿滃崟杩斿洖None
        menu_service.menu_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = menu_service.update_menu("nonexistent_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_menu_success(self, menu_service):
        """娴嬭瘯删除鑿滃崟鎴愬姛"""
        # 妯℃嫙删除鑿滃崟
        menu_service.menu_repo.delete = Mock(return_value=True)
        
        # 鎵ц删除
        result = menu_service.delete_menu("test_menu_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        menu_service.menu_repo.delete.assert_called_once_with("test_menu_id")
    
    def test_list_menus_success(self, menu_service, mock_menu):
        """娴嬭瘯鑾峰彇鑿滃崟鍒楄〃鎴愬姛"""
        # 妯℃嫙查询鑿滃崟鍒楄〃
        menu_service.menu_repo.get_by_tenant_id = Mock(return_value=[mock_menu])
        
        # 鎵ц查询
        result = menu_service.list_menus(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_menu_id"
    
    def test_get_menu_tree_success(self, menu_service, mock_menu):
        """娴嬭瘯鑾峰彇鑿滃崟鏍戞垚鍔?""
        # 妯℃嫙查询鑿滃崟鏍?        menu_service.menu_repo.get_tree = Mock(return_value=[mock_menu])
        
        # 鎵ц查询
        result = menu_service.get_menu_tree(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
    
    def test_get_visible_menus_success(self, menu_service, mock_menu):
        """娴嬭瘯鑾峰彇鍙鑿滃崟鎴愬姛"""
        # 妯℃嫙查询鍙鑿滃崟
        menu_service.menu_repo.get_visible_menus = Mock(return_value=[mock_menu])
        
        # 鎵ц查询
        result = menu_service.get_visible_menus(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
    
    def test_count_menus_success(self, menu_service):
        """娴嬭瘯缁熻鑿滃崟数量鎴愬姛"""
        # 妯℃嫙缁熻
        menu_service.menu_repo.count_by_tenant = Mock(return_value=10)
        
        # 鎵ц缁熻
        result = menu_service.count_menus(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert result == 10
    
    def test_search_menus_success(self, menu_service, mock_menu):
        """娴嬭瘯鎼滅储鑿滃崟鎴愬姛"""
        # 妯℃嫙查询
        mock_query = Mock()
        mock_query.filter = Mock(return_value=mock_query)
        mock_query.count = Mock(return_value=1)
        mock_query.offset = Mock(return_value=mock_query)
        mock_query.limit = Mock(return_value=[mock_menu])
        menu_service.db.query = Mock(return_value=mock_query)
        
        # 鎵ц鎼滅储
        result = menu_service.search_menus({"tenant_id": "default"})
        
        # 楠岃瘉缁撴灉
        assert len(result[0]) == 1
        assert result[1] == 1
