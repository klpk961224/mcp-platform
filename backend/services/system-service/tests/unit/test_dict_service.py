# -*- coding: utf-8 -*-
"""
DictService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建瀛楀吀
2. 鑾峰彇瀛楀吀
3. 更新瀛楀吀
4. 删除瀛楀吀
5. 鑾峰彇瀛楀吀鍒楄〃
6. 缁熻瀛楀吀数量
7. 创建瀛楀吀椤?8. 鑾峰彇瀛楀吀椤?9. 更新瀛楀吀椤?10. 删除瀛楀吀椤?"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.dict_service import DictService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_dict():
    """妯℃嫙瀛楀吀瀵硅薄"""
    dict_obj = Mock()
    dict_obj.id = "test_dict_id"
    dict_obj.type = "user_status"
    dict_obj.name = "鐢ㄦ埛状态?
    dict_obj.description = "鐢ㄦ埛状态佸瓧鍏?
    dict_obj.status = "active"
    dict_obj.tenant_id = None
    return dict_obj


@pytest.fixture
def mock_dict_item():
    """妯℃嫙瀛楀吀椤瑰璞?""
    dict_item = Mock()
    dict_item.id = "test_dict_item_id"
    dict_item.dict_id = "test_dict_id"
    dict_item.label = "姝ｅ父"
    dict_item.value = "1"
    dict_item.sort_order = 0
    dict_item.status = "active"
    return dict_item


@pytest.fixture
def dict_service(mock_db):
    """创建DictService瀹炰緥"""
    return DictService(mock_db)


class TestDictService:
    """DictService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯DictService鍒濆鍖?""
        service = DictService(mock_db)
        assert service.db == mock_db
        assert service.dict_repo is not None
        assert service.dict_item_repo is not None
    
    def test_create_dict_success(self, dict_service, mock_dict):
        """娴嬭瘯创建瀛楀吀鎴愬姛"""
        # 妯℃嫙瀛楀吀类型涓嶅瓨鍦?        dict_service.dict_repo.get_by_type = Mock(return_value=None)
        # 妯℃嫙创建瀛楀吀
        dict_service.dict_repo.create = Mock(return_value=mock_dict)
        
        # 鎵ц创建瀛楀吀
        dict_data = {
            "type": "user_status",
            "name": "鐢ㄦ埛状态?,
            "description": "鐢ㄦ埛状态佸瓧鍏?
        }
        result = dict_service.create_dict(dict_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dict_id"
        assert result.type == "user_status"
        dict_service.dict_repo.create.assert_called_once()
    
    def test_create_dict_type_exists(self, dict_service, mock_dict):
        """娴嬭瘯创建瀛楀吀锛堢被鍨嬪凡瀛樺湪锛?""
        # 妯℃嫙瀛楀吀类型宸插瓨鍦?        dict_service.dict_repo.get_by_type = Mock(return_value=mock_dict)
        
        # 鎵ц创建瀛楀吀骞堕獙璇佸紓甯?        dict_data = {
            "type": "existing_type",
            "name": "鐜版湁瀛楀吀"
        }
        with pytest.raises(ValueError, match="瀛楀吀类型宸插瓨鍦?):
            dict_service.create_dict(dict_data)
    
    def test_get_dict_success(self, dict_service, mock_dict):
        """娴嬭瘯鑾峰彇瀛楀吀鎴愬姛"""
        # 妯℃嫙查询瀛楀吀
        dict_service.dict_repo.get_by_id = Mock(return_value=mock_dict)
        
        # 鎵ц查询
        result = dict_service.get_dict("test_dict_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dict_id"
        dict_service.dict_repo.get_by_id.assert_called_once_with("test_dict_id")
    
    def test_get_dict_not_found(self, dict_service):
        """娴嬭瘯鑾峰彇瀛楀吀澶辫触"""
        # 妯℃嫙查询瀛楀吀杩斿洖None
        dict_service.dict_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = dict_service.get_dict("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_dict_by_type_success(self, dict_service, mock_dict):
        """娴嬭瘯根据类型鑾峰彇瀛楀吀鎴愬姛"""
        # 妯℃嫙查询瀛楀吀
        dict_service.dict_repo.get_by_type = Mock(return_value=mock_dict)
        
        # 鎵ц查询
        result = dict_service.get_dict_by_type("user_status")
        
        # 楠岃瘉缁撴灉
        assert result.type == "user_status"
        dict_service.dict_repo.get_by_type.assert_called_once_with("user_status")
    
    def test_update_dict_success(self, dict_service, mock_dict):
        """娴嬭瘯更新瀛楀吀鎴愬姛"""
        # 妯℃嫙查询瀛楀吀
        dict_service.dict_repo.get_by_id = Mock(return_value=mock_dict)
        # 妯℃嫙更新瀛楀吀
        dict_service.dict_repo.update = Mock(return_value=mock_dict)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = dict_service.update_dict("test_dict_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dict_id"
        dict_service.dict_repo.update.assert_called_once()
    
    def test_update_dict_not_found(self, dict_service):
        """娴嬭瘯更新瀛楀吀澶辫触锛堝瓧鍏镐笉瀛樺湪锛?""
        # 妯℃嫙查询瀛楀吀杩斿洖None
        dict_service.dict_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = dict_service.update_dict("nonexistent_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_dict_success(self, dict_service):
        """娴嬭瘯删除瀛楀吀鎴愬姛"""
        # 妯℃嫙删除瀛楀吀
        dict_service.dict_repo.delete = Mock(return_value=True)
        
        # 鎵ц删除
        result = dict_service.delete_dict("test_dict_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        dict_service.dict_repo.delete.assert_called_once_with("test_dict_id")
    
    def test_list_dicts_success(self, dict_service, mock_dict):
        """娴嬭瘯鑾峰彇瀛楀吀鍒楄〃鎴愬姛"""
        # 妯℃嫙查询瀛楀吀鍒楄〃
        dict_service.dict_repo.get_all = Mock(return_value=[mock_dict])
        
        # 鎵ц查询
        result = dict_service.list_dicts()
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_dict_id"
    
    def test_count_dicts_success(self, dict_service):
        """娴嬭瘯缁熻瀛楀吀数量鎴愬姛"""
        # 妯℃嫙缁熻
        dict_service.dict_repo.count_all = Mock(return_value=10)
        
        # 鎵ц缁熻
        result = dict_service.count_dicts()
        
        # 楠岃瘉缁撴灉
        assert result == 10
    
    def test_create_dict_item_success(self, dict_service, mock_dict, mock_dict_item):
        """娴嬭瘯创建瀛楀吀椤规垚鍔?""
        # 妯℃嫙瀛楀吀瀛樺湪
        dict_service.dict_repo.get_by_id = Mock(return_value=mock_dict)
        # 妯℃嫙创建瀛楀吀椤?        dict_service.dict_item_repo.create = Mock(return_value=mock_dict_item)
        
        # 鎵ц创建瀛楀吀椤?        dict_item_data = {
            "label": "姝ｅ父",
            "value": "1",
            "sort_order": 0
        }
        result = dict_service.create_dict_item("test_dict_id", dict_item_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dict_item_id"
        assert result.label == "姝ｅ父"
        dict_service.dict_item_repo.create.assert_called_once()
    
    def test_create_dict_item_dict_not_found(self, dict_service):
        """娴嬭瘯创建瀛楀吀椤癸紙瀛楀吀涓嶅瓨鍦級"""
        # 妯℃嫙瀛楀吀涓嶅瓨鍦?        dict_service.dict_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц创建瀛楀吀椤瑰苟楠岃瘉寮傚父
        dict_item_data = {"label": "姝ｅ父", "value": "1"}
        with pytest.raises(ValueError, match="瀛楀吀涓嶅瓨鍦?):
            dict_service.create_dict_item("nonexistent_id", dict_item_data)
    
    def test_get_dict_item_success(self, dict_service, mock_dict_item):
        """娴嬭瘯鑾峰彇瀛楀吀椤规垚鍔?""
        # 妯℃嫙查询瀛楀吀椤?        dict_service.dict_item_repo.get_by_id = Mock(return_value=mock_dict_item)
        
        # 鎵ц查询
        result = dict_service.get_dict_item("test_dict_item_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dict_item_id"
        dict_service.dict_item_repo.get_by_id.assert_called_once_with("test_dict_item_id")
    
    def test_get_dict_items_success(self, dict_service, mock_dict_item):
        """娴嬭瘯鑾峰彇瀛楀吀椤瑰垪琛ㄦ垚鍔?""
        # 妯℃嫙查询瀛楀吀椤瑰垪琛?        dict_service.dict_item_repo.get_by_dict_id = Mock(return_value=[mock_dict_item])
        
        # 鎵ц查询
        result = dict_service.get_dict_items("test_dict_id")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_dict_item_id"
    
    def test_get_dict_items_by_type_success(self, dict_service, mock_dict_item):
        """娴嬭瘯根据类型鑾峰彇瀛楀吀椤瑰垪琛ㄦ垚鍔?""
        # 妯℃嫙查询瀛楀吀椤瑰垪琛?        dict_service.dict_item_repo.get_by_dict_type = Mock(return_value=[mock_dict_item])
        
        # 鎵ц查询
        result = dict_service.get_dict_items_by_type("user_status")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
    
    def test_update_dict_item_success(self, dict_service, mock_dict_item):
        """娴嬭瘯更新瀛楀吀椤规垚鍔?""
        # 妯℃嫙查询瀛楀吀椤?        dict_service.dict_item_repo.get_by_id = Mock(return_value=mock_dict_item)
        # 妯℃嫙更新瀛楀吀椤?        dict_service.dict_item_repo.update = Mock(return_value=mock_dict_item)
        
        # 鎵ц更新
        update_data = {"label": "更新鍚庣殑鏍囩"}
        result = dict_service.update_dict_item("test_dict_item_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dict_item_id"
        dict_service.dict_item_repo.update.assert_called_once()
    
    def test_update_dict_item_not_found(self, dict_service):
        """娴嬭瘯更新瀛楀吀椤瑰け璐ワ紙瀛楀吀椤逛笉瀛樺湪锛?""
        # 妯℃嫙查询瀛楀吀椤硅繑鍥濶one
        dict_service.dict_item_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц更新
        update_data = {"label": "更新鍚庣殑鏍囩"}
        result = dict_service.update_dict_item("nonexistent_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_dict_item_success(self, dict_service):
        """娴嬭瘯删除瀛楀吀椤规垚鍔?""
        # 妯℃嫙删除瀛楀吀椤?        dict_service.dict_item_repo.delete = Mock(return_value=True)
        
        # 鎵ц删除
        result = dict_service.delete_dict_item("test_dict_item_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        dict_service.dict_item_repo.delete.assert_called_once_with("test_dict_item_id")
    
    def test_count_dict_items_success(self, dict_service):
        """娴嬭瘯缁熻瀛楀吀椤规暟閲忔垚鍔?""
        # 妯℃嫙缁熻
        dict_service.dict_item_repo.count_by_dict = Mock(return_value=5)
        
        # 鎵ц缁熻
        result = dict_service.count_dict_items("test_dict_id")
        
        # 楠岃瘉缁撴灉
        assert result == 5
