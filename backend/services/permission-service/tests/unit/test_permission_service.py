# -*- coding: utf-8 -*-
"""
PermissionService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建鏉冮檺
2. 鑾峰彇鏉冮檺
3. 更新鏉冮檺
4. 删除鏉冮檺
5. 鑾峰彇鏉冮檺鍒楄〃
6. 缁熻鏉冮檺数量
7. 妫€鏌ョ敤鎴锋潈闄?"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.permission_service import PermissionService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_permission():
    """妯℃嫙鏉冮檺瀵硅薄"""
    permission = Mock()
    permission.id = "test_permission_id"
    permission.name = "鐢ㄦ埛绠＄悊"
    permission.code = "user:manage"
    permission.type = "operation"
    permission.resource = "user"
    permission.description = "鐢ㄦ埛绠＄悊鏉冮檺"
    permission.status = "active"
    return permission


@pytest.fixture
def permission_service(mock_db):
    """创建PermissionService瀹炰緥"""
    return PermissionService(mock_db)


class TestPermissionService:
    """PermissionService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯PermissionService鍒濆鍖?""
        service = PermissionService(mock_db)
        assert service.db == mock_db
        assert service.perm_repo is not None
    
    def test_create_permission_success(self, permission_service, mock_permission):
        """娴嬭瘯创建鏉冮檺鎴愬姛"""
        # 妯℃嫙鏉冮檺编码涓嶅瓨鍦?        permission_service.perm_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙创建鏉冮檺
        permission_service.perm_repo.create = Mock(return_value=mock_permission)
        
        # 鎵ц创建鏉冮檺
        permission_data = {
            "name": "鐢ㄦ埛绠＄悊",
            "code": "user:manage",
            "type": "operation",
            "resource": "user"
        }
        result = permission_service.create_permission(permission_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_permission_id"
        assert result.name == "鐢ㄦ埛绠＄悊"
        permission_service.perm_repo.create.assert_called_once()
    
    def test_create_permission_code_exists(self, permission_service):
        """娴嬭瘯创建鏉冮檺锛堢紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙鏉冮檺编码宸插瓨鍦?        permission_service.perm_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц创建鏉冮檺骞堕獙璇佸紓甯?        permission_data = {
            "name": "鐢ㄦ埛绠＄悊",
            "code": "existing_code"
        }
        with pytest.raises(ValueError, match="鏉冮檺编码宸插瓨鍦?):
            permission_service.create_permission(permission_data)
    
    def test_get_permission_success(self, permission_service, mock_permission):
        """娴嬭瘯鑾峰彇鏉冮檺鎴愬姛"""
        # 妯℃嫙查询鏉冮檺
        permission_service.perm_repo.get_by_id = Mock(return_value=mock_permission)
        
        # 鎵ц查询
        result = permission_service.get_permission("test_permission_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_permission_id"
        permission_service.perm_repo.get_by_id.assert_called_once_with("test_permission_id")
    
    def test_get_permission_not_found(self, permission_service):
        """娴嬭瘯鑾峰彇鏉冮檺澶辫触"""
        # 妯℃嫙查询鏉冮檺杩斿洖None
        permission_service.perm_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = permission_service.get_permission("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_permission_by_code_success(self, permission_service, mock_permission):
        """娴嬭瘯根据编码鑾峰彇鏉冮檺鎴愬姛"""
        # 妯℃嫙查询鏉冮檺
        permission_service.perm_repo.get_by_code = Mock(return_value=mock_permission)
        
        # 鎵ц查询
        result = permission_service.get_permission_by_code("user:manage")
        
        # 楠岃瘉缁撴灉
        assert result.code == "user:manage"
        permission_service.perm_repo.get_by_code.assert_called_once_with("user:manage")
    
    def test_update_permission_success(self, permission_service, mock_permission):
        """娴嬭瘯更新鏉冮檺鎴愬姛"""
        # 妯℃嫙查询鏉冮檺
        permission_service.perm_repo.get_by_id = Mock(return_value=mock_permission)
        # 妯℃嫙更新鏉冮檺
        permission_service.perm_repo.update = Mock(return_value=mock_permission)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = permission_service.update_permission("test_permission_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_permission_id"
        permission_service.perm_repo.update.assert_called_once()
    
    def test_update_permission_not_found(self, permission_service):
        """娴嬭瘯更新鏉冮檺澶辫触锛堟潈闄愪笉瀛樺湪锛?""
        # 妯℃嫙查询鏉冮檺杩斿洖None
        permission_service.perm_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = permission_service.update_permission("nonexistent_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_permission_success(self, permission_service):
        """娴嬭瘯删除鏉冮檺鎴愬姛"""
        # 妯℃嫙删除鏉冮檺
        permission_service.perm_repo.delete = Mock(return_value=True)
        
        # 鎵ц删除
        result = permission_service.delete_permission("test_permission_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        permission_service.perm_repo.delete.assert_called_once_with("test_permission_id")
    
    def test_list_permissions_success(self, permission_service, mock_permission):
        """娴嬭瘯鑾峰彇鏉冮檺鍒楄〃鎴愬姛"""
        # 妯℃嫙查询鏉冮檺鍒楄〃
        permission_service.perm_repo.get_all = Mock(return_value=[mock_permission])
        
        # 鎵ц查询
        result = permission_service.list_permissions()
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_permission_id"
    
    def test_count_permissions_success(self, permission_service):
        """娴嬭瘯缁熻鏉冮檺数量鎴愬姛"""
        # 妯℃嫙缁熻
        permission_service.perm_repo.count_all = Mock(return_value=50)
        
        # 鎵ц缁熻
        result = permission_service.count_permissions()
        
        # 楠岃瘉缁撴灉
        assert result == 50
    
    def test_check_user_permission_has_permission(self, permission_service, mock_permission):
        """娴嬭瘯妫€鏌ョ敤鎴锋潈闄愶紙鏈夋潈闄愶級"""
        # 妯℃嫙查询瑙掕壊
        mock_role = Mock()
        mock_role.has_permission = Mock(return_value=True)
        permission_service.db.query.return_value.join.return_value.filter.return_value.all = Mock(return_value=[mock_role])
        
        # 鎵ц妫€鏌?        result = permission_service.check_user_permission("user_001", "user:manage")
        
        # 楠岃瘉缁撴灉
        assert result is True
    
    def test_check_user_permission_no_permission(self, permission_service, mock_permission):
        """娴嬭瘯妫€鏌ョ敤鎴锋潈闄愶紙鏃犳潈闄愶級"""
        # 妯℃嫙查询瑙掕壊杩斿洖绌哄垪琛?        permission_service.db.query.return_value.join.return_value.filter.return_value.all = Mock(return_value=[])
        
        # 鎵ц妫€鏌?        result = permission_service.check_user_permission("user_001", "user:manage")
        
        # 楠岃瘉缁撴灉
        assert result is False
