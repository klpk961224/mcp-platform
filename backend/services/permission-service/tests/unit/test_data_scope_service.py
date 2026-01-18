# -*- coding: utf-8 -*-
"""
DataScopeService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建鏁版嵁鑼冨洿
2. 鑾峰彇鏁版嵁鑼冨洿
3. 鑾峰彇鏁版嵁鑼冨洿鍒楄〃
4. 璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿
5. 鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿
6. 妫€鏌ユ暟鎹寖鍥存潈闄?"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.data_scope_service import DataScopeService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_data_scope():
    """妯℃嫙鏁版嵁鑼冨洿瀵硅薄"""
    data_scope = Mock()
    data_scope.id = "test_data_scope_id"
    data_scope.name = "鏈儴闂ㄦ暟鎹?
    data_scope.code = "department"
    data_scope.type = "custom"
    data_scope.description = "鏈儴闂ㄦ暟鎹寖鍥?
    data_scope.status = "active"
    return data_scope


@pytest.fixture
def mock_user_data_scope():
    """妯℃嫙鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄"""
    user_data_scope = Mock()
    user_data_scope.id = "test_user_data_scope_id"
    user_data_scope.user_id = "user_001"
    user_data_scope.module = "user"
    user_data_scope.data_scope_id = "test_data_scope_id"
    user_data_scope.data_scope = Mock()
    user_data_scope.data_scope.code = "department"
    return user_data_scope


@pytest.fixture
def data_scope_service(mock_db):
    """创建DataScopeService瀹炰緥"""
    return DataScopeService(mock_db)


class TestDataScopeService:
    """DataScopeService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯DataScopeService鍒濆鍖?""
        service = DataScopeService(mock_db)
        assert service.db == mock_db
        assert service.data_scope_repo is not None
        assert service.user_data_scope_repo is not None
    
    def test_create_data_scope_success(self, data_scope_service, mock_data_scope):
        """娴嬭瘯创建鏁版嵁鑼冨洿鎴愬姛"""
        # 妯℃嫙鏁版嵁鑼冨洿编码涓嶅瓨鍦?        data_scope_service.data_scope_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙创建鏁版嵁鑼冨洿
        data_scope_service.data_scope_repo.create = Mock(return_value=mock_data_scope)
        
        # 鎵ц创建鏁版嵁鑼冨洿
        data_scope_data = {
            "name": "鏈儴闂ㄦ暟鎹?,
            "code": "department",
            "type": "custom"
        }
        result = data_scope_service.create_data_scope(data_scope_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_data_scope_id"
        assert result.name == "鏈儴闂ㄦ暟鎹?
        data_scope_service.data_scope_repo.create.assert_called_once()
    
    def test_create_data_scope_code_exists(self, data_scope_service):
        """娴嬭瘯创建鏁版嵁鑼冨洿锛堢紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙鏁版嵁鑼冨洿编码宸插瓨鍦?        data_scope_service.data_scope_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц创建鏁版嵁鑼冨洿骞堕獙璇佸紓甯?        data_scope_data = {
            "name": "鏈儴闂ㄦ暟鎹?,
            "code": "existing_code"
        }
        with pytest.raises(ValueError, match="鏁版嵁鑼冨洿编码宸插瓨鍦?):
            data_scope_service.create_data_scope(data_scope_data)
    
    def test_get_data_scope_success(self, data_scope_service, mock_data_scope):
        """娴嬭瘯鑾峰彇鏁版嵁鑼冨洿鎴愬姛"""
        # 妯℃嫙查询鏁版嵁鑼冨洿
        data_scope_service.data_scope_repo.get_by_id = Mock(return_value=mock_data_scope)
        
        # 鎵ц查询
        result = data_scope_service.get_data_scope("test_data_scope_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_data_scope_id"
        data_scope_service.data_scope_repo.get_by_id.assert_called_once_with("test_data_scope_id")
    
    def test_get_data_scope_not_found(self, data_scope_service):
        """娴嬭瘯鑾峰彇鏁版嵁鑼冨洿澶辫触"""
        # 妯℃嫙查询鏁版嵁鑼冨洿杩斿洖None
        data_scope_service.data_scope_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = data_scope_service.get_data_scope("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_data_scope_by_code_success(self, data_scope_service, mock_data_scope):
        """娴嬭瘯根据编码鑾峰彇鏁版嵁鑼冨洿鎴愬姛"""
        # 妯℃嫙查询鏁版嵁鑼冨洿
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=mock_data_scope)
        
        # 鎵ц查询
        result = data_scope_service.get_data_scope_by_code("department")
        
        # 楠岃瘉缁撴灉
        assert result.code == "department"
        data_scope_service.data_scope_repo.get_by_code.assert_called_once_with("department")
    
    def test_list_data_scopes_success(self, data_scope_service, mock_data_scope):
        """娴嬭瘯鑾峰彇鏁版嵁鑼冨洿鍒楄〃鎴愬姛"""
        # 妯℃嫙查询鏁版嵁鑼冨洿鍒楄〃
        data_scope_service.data_scope_repo.get_all = Mock(return_value=[mock_data_scope])
        
        # 鎵ц查询
        result = data_scope_service.list_data_scopes()
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_data_scope_id"
    
    def test_set_user_data_scope_create(self, data_scope_service, mock_data_scope, mock_user_data_scope):
        """娴嬭瘯璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿锛堝垱寤猴級"""
        # 妯℃嫙查询鏁版嵁鑼冨洿
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=mock_data_scope)
        # 妯℃嫙查询鐢ㄦ埛鏁版嵁鑼冨洿杩斿洖None
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=None)
        # 妯℃嫙创建鐢ㄦ埛鏁版嵁鑼冨洿
        data_scope_service.user_data_scope_repo.create = Mock(return_value=mock_user_data_scope)
        
        # 鎵ц璁剧疆
        result = data_scope_service.set_user_data_scope("user_001", "user", "department")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_user_data_scope_id"
        data_scope_service.user_data_scope_repo.create.assert_called_once()
    
    def test_set_user_data_scope_update(self, data_scope_service, mock_data_scope, mock_user_data_scope):
        """娴嬭瘯璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿锛堟洿鏂帮級"""
        # 妯℃嫙查询鏁版嵁鑼冨洿
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=mock_data_scope)
        # 妯℃嫙查询鐢ㄦ埛鏁版嵁鑼冨洿
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=mock_user_data_scope)
        # 妯℃嫙更新鐢ㄦ埛鏁版嵁鑼冨洿
        data_scope_service.user_data_scope_repo.update = Mock(return_value=mock_user_data_scope)
        
        # 鎵ц璁剧疆
        result = data_scope_service.set_user_data_scope("user_001", "user", "department")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_user_data_scope_id"
        data_scope_service.user_data_scope_repo.update.assert_called_once()
    
    def test_set_user_data_scope_not_found(self, data_scope_service):
        """娴嬭瘯璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿锛堟暟鎹寖鍥翠笉瀛樺湪锛?""
        # 妯℃嫙查询鏁版嵁鑼冨洿杩斿洖None
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=None)
        
        # 鎵ц璁剧疆骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="鏁版嵁鑼冨洿涓嶅瓨鍦?):
            data_scope_service.set_user_data_scope("user_001", "user", "nonexistent")
    
    def test_get_user_data_scope_success(self, data_scope_service, mock_user_data_scope):
        """娴嬭瘯鑾峰彇鐢ㄦ埛鏁版嵁鑼冨洿鎴愬姛"""
        # 妯℃嫙查询鐢ㄦ埛鏁版嵁鑼冨洿
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=mock_user_data_scope)
        
        # 鎵ц查询
        result = data_scope_service.get_user_data_scope("user_001", "user")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_user_data_scope_id"
        data_scope_service.user_data_scope_repo.get_by_user_module.assert_called_once()
    
    def test_check_data_scope_all(self, data_scope_service, mock_user_data_scope):
        """娴嬭瘯妫€鏌ユ暟鎹寖鍥存潈闄愶紙鍏ㄩ儴鏁版嵁锛?""
        # 妯℃嫙查询鐢ㄦ埛鏁版嵁鑼冨洿
        mock_user_data_scope.data_scope.code = "all"
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=mock_user_data_scope)
        
        # 鎵ц妫€鏌?        result = data_scope_service.check_data_scope("user_001", "user", "target_001")
        
        # 楠岃瘉缁撴灉
        assert result is True
    
    def test_check_data_scope_self_true(self, data_scope_service, mock_user_data_scope):
        """娴嬭瘯妫€鏌ユ暟鎹寖鍥存潈闄愶紙浠呮湰浜烘暟鎹紝鏈夋潈闄愶級"""
        # 妯℃嫙查询鐢ㄦ埛鏁版嵁鑼冨洿杩斿洖None锛堥粯璁や负self锛?        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=None)
        
        # 鎵ц妫€鏌ワ紙鐩爣鏄湰浜猴級
        result = data_scope_service.check_data_scope("user_001", "user", "user_001")
        
        # 楠岃瘉缁撴灉
        assert result is True
    
    def test_check_data_scope_self_false(self, data_scope_service, mock_user_data_scope):
        """娴嬭瘯妫€鏌ユ暟鎹寖鍥存潈闄愶紙浠呮湰浜烘暟鎹紝鏃犳潈闄愶級"""
        # 妯℃嫙查询鐢ㄦ埛鏁版嵁鑼冨洿杩斿洖None锛堥粯璁や负self锛?        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=None)
        
        # 鎵ц妫€鏌ワ紙鐩爣涓嶆槸鏈汉锛?        result = data_scope_service.check_data_scope("user_001", "user", "user_002")
        
        # 楠岃瘉缁撴灉
        assert result is False
