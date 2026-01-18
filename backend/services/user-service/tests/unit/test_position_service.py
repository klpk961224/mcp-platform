# -*- coding: utf-8 -*-
"""
PositionService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建宀椾綅
2. 鑾峰彇宀椾綅
3. 更新宀椾綅
4. 删除宀椾綅
5. 鑾峰彇宀椾綅鍒楄〃
6. 缁熻宀椾綅数量
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.position_service import PositionService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_position():
    """妯℃嫙宀椾綅瀵硅薄"""
    position = Mock()
    position.id = "test_position_id"
    position.name = "寮€鍙戝伐绋嬪笀"
    position.code = "developer"
    position.level = 1
    position.description = "寮€鍙戝伐绋嬪笀宀椾綅"
    position.tenant_id = "default"
    position.status = "active"
    return position


@pytest.fixture
def position_service(mock_db):
    """创建PositionService瀹炰緥"""
    return PositionService(mock_db)


class TestPositionService:
    """PositionService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯PositionService鍒濆鍖?""
        service = PositionService(mock_db)
        assert service.db == mock_db
        assert service.position_repo is not None
    
    def test_create_position_success(self, position_service, mock_position):
        """娴嬭瘯创建宀椾綅鎴愬姛"""
        # 妯℃嫙宀椾綅编码涓嶅瓨鍦?        position_service.position_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙创建宀椾綅
        position_service.position_repo.create = Mock(return_value=mock_position)
        
        # 鎵ц创建宀椾綅
        position_data = {
            "name": "寮€鍙戝伐绋嬪笀",
            "code": "developer",
            "tenant_id": "default"
        }
        result = position_service.create_position(position_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_position_id"
        assert result.name == "寮€鍙戝伐绋嬪笀"
        position_service.position_repo.create.assert_called_once()
    
    def test_create_position_code_exists(self, position_service):
        """娴嬭瘯创建宀椾綅锛堢紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙宀椾綅编码宸插瓨鍦?        position_service.position_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц创建宀椾綅骞堕獙璇佸紓甯?        position_data = {
            "name": "寮€鍙戝伐绋嬪笀",
            "code": "existing_code",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="宀椾綅编码宸插瓨鍦?):
            position_service.create_position(position_data)
    
    def test_get_position_success(self, position_service, mock_position):
        """娴嬭瘯鑾峰彇宀椾綅鎴愬姛"""
        # 妯℃嫙查询宀椾綅
        position_service.position_repo.get_by_id = Mock(return_value=mock_position)
        
        # 鎵ц查询
        result = position_service.get_position("test_position_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_position_id"
        position_service.position_repo.get_by_id.assert_called_once_with("test_position_id")
    
    def test_get_position_not_found(self, position_service):
        """娴嬭瘯鑾峰彇宀椾綅澶辫触"""
        # 妯℃嫙查询宀椾綅杩斿洖None
        position_service.position_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = position_service.get_position("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_position_by_code_success(self, position_service, mock_position):
        """娴嬭瘯根据编码鑾峰彇宀椾綅鎴愬姛"""
        # 妯℃嫙查询宀椾綅
        position_service.position_repo.get_by_code = Mock(return_value=mock_position)
        
        # 鎵ц查询
        result = position_service.get_position_by_code("developer")
        
        # 楠岃瘉缁撴灉
        assert result.code == "developer"
        position_service.position_repo.get_by_code.assert_called_once_with("developer")
    
    def test_update_position_success(self, position_service, mock_position):
        """娴嬭瘯更新宀椾綅鎴愬姛"""
        # 妯℃嫙查询宀椾綅
        position_service.position_repo.get_by_id = Mock(return_value=mock_position)
        # 妯℃嫙更新宀椾綅
        position_service.position_repo.update = Mock(return_value=mock_position)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = position_service.update_position("test_position_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_position_id"
        position_service.position_repo.update.assert_called_once()
    
    def test_update_position_not_found(self, position_service):
        """娴嬭瘯更新宀椾綅澶辫触锛堝矖浣嶄笉瀛樺湪锛?""
        # 妯℃嫙查询宀椾綅杩斿洖None
        position_service.position_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = position_service.update_position("nonexistent_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_position_success(self, position_service):
        """娴嬭瘯删除宀椾綅鎴愬姛"""
        # 妯℃嫙删除宀椾綅
        position_service.position_repo.delete = Mock(return_value=True)
        
        # 鎵ц删除
        result = position_service.delete_position("test_position_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        position_service.position_repo.delete.assert_called_once_with("test_position_id")
    
    def test_list_positions_success(self, position_service, mock_position):
        """娴嬭瘯鑾峰彇宀椾綅鍒楄〃鎴愬姛"""
        # 妯℃嫙查询宀椾綅鍒楄〃
        position_service.position_repo.get_by_tenant_id = Mock(return_value=[mock_position])
        
        # 鎵ц查询
        result = position_service.list_positions(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_position_id"
    
    def test_count_positions_success(self, position_service):
        """娴嬭瘯缁熻宀椾綅数量鎴愬姛"""
        # 妯℃嫙缁熻
        position_service.position_repo.count_by_tenant = Mock(return_value=10)
        
        # 鎵ц缁熻
        result = position_service.count_positions(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert result == 10
    
    def test_count_positions_all(self, position_service):
        """娴嬭瘯缁熻鎵€鏈夊矖浣嶆暟閲忔垚鍔?""
        # 妯℃嫙缁熻
        position_service.position_repo.count_all = Mock(return_value=50)
        
        # 鎵ц缁熻
        result = position_service.count_positions()
        
        # 楠岃瘉缁撴灉
        assert result == 50
