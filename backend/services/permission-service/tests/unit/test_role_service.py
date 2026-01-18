# -*- coding: utf-8 -*-
"""
RoleService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建瑙掕壊
2. 鑾峰彇瑙掕壊
3. 更新瑙掕壊
4. 删除瑙掕壊
5. 鎼滅储瑙掕壊
6. 瑙掕壊鏉冮檺绠＄悊
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

# 瀵煎叆鎵€鏈夋ā鍨嬩互鍒濆鍖朣QLAlchemy mapper
from common.database.models.user import Role
from common.database.models.permission import Permission, Menu

# 鎵嬪姩閰嶇疆SQLAlchemy mapper
from sqlalchemy.orm import configure_mappers
configure_mappers()

from app.services.role_service import RoleService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_role():
    """妯℃嫙瑙掕壊瀵硅薄"""
    role = Mock(spec=Role)
    role.id = "test_role_id"
    role.name = "娴嬭瘯瑙掕壊"
    role.code = "test_role"
    role.description = "娴嬭瘯角色描述"
    role.tenant_id = "default"
    role.is_system = False
    role.status = "active"
    role.created_at = Mock()
    role.updated_at = Mock()
    role.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
    role.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
    return role


@pytest.fixture
def role_service(mock_db):
    """创建RoleService瀹炰緥"""
    return RoleService(mock_db)


class TestRoleService:
    """RoleService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯RoleService鍒濆鍖?""
        service = RoleService(mock_db)
        assert service.db == mock_db
        assert service.role_repo is not None
        assert service.perm_repo is not None
        assert service.menu_repo is not None
    
    def test_create_role_success(self, role_service, mock_role):
        """娴嬭瘯创建瑙掕壊鎴愬姛"""
        # 妯℃嫙瑙掕壊浠ｇ爜涓嶅瓨鍦?        role_service.role_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙角色名称鍦ㄥ悓涓€绉熸埛涓笉瀛樺湪
        role_service.role_repo.exists_by_name_in_tenant = Mock(return_value=False)
        # 妯℃嫙创建瑙掕壊
        role_service.role_repo.create = Mock(return_value=mock_role)
        
        # 鎵ц创建瑙掕壊
        role_data = {
            "name": "娴嬭瘯瑙掕壊",
            "code": "test_role",
            "tenant_id": "default",
            "description": "娴嬭瘯角色描述"
        }
        result = role_service.create_role(role_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_role_id"
        assert result.name == "娴嬭瘯瑙掕壊"
        role_service.role_repo.create.assert_called_once()
    
    def test_create_role_code_exists(self, role_service):
        """娴嬭瘯创建瑙掕壊鏃朵唬鐮佸凡瀛樺湪"""
        # 妯℃嫙瑙掕壊浠ｇ爜宸插瓨鍦?        role_service.role_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц创建瑙掕壊骞堕獙璇佸紓甯?        role_data = {
            "name": "娴嬭瘯瑙掕壊",
            "code": "existing_role",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="角色编码宸插瓨鍦?):
            role_service.create_role(role_data)
    
    def test_get_by_id_success(self, role_service, mock_role):
        """娴嬭瘯鑾峰彇瑙掕壊鎴愬姛"""
        # 妯℃嫙查询瑙掕壊
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        
        # 鎵ц查询
        result = role_service.get_role("test_role_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_role_id"
        role_service.role_repo.get_by_id.assert_called_once_with("test_role_id")
    
    def test_get_by_id_not_found(self, role_service):
        """娴嬭瘯鑾峰彇瑙掕壊澶辫触"""
        # 妯℃嫙查询瑙掕壊杩斿洖None
        role_service.role_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = role_service.get_role("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_update_role_success(self, role_service, mock_role):
        """娴嬭瘯更新瑙掕壊鎴愬姛"""
        # 妯℃嫙查询瑙掕壊
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 妯℃嫙更新瑙掕壊
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 鎵ц更新
        update_data = {"description": "更新鍚庣殑描述"}
        result = role_service.update_role("test_role_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_role_id"
        role_service.role_repo.update.assert_called_once()
    
    def test_delete_role_success(self, role_service):
        """娴嬭瘯删除瑙掕壊鎴愬姛"""
        # 妯℃嫙删除瑙掕壊
        role_service.role_repo.delete = Mock()
        
        # 鎵ц删除
        role_service.delete_role("test_role_id")
        
        # 楠岃瘉缁撴灉
        role_service.role_repo.delete.assert_called_once_with("test_role_id")
    
    def test_search_roles_success(self, role_service, mock_role):
        """娴嬭瘯鎼滅储瑙掕壊鎴愬姛"""
        # 妯℃嫙鎼滅储瑙掕壊
        role_service.role_repo.search = Mock(return_value=[mock_role])
        
        # 鎵ц鎼滅储
        result = role_service.list_roles(
            tenant_id="default",
            keyword="娴嬭瘯"
        )
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_role_id"
    
    def test_assign_permission_to_role_success(self, role_service, mock_role):
        """娴嬭瘯鍒嗛厤鏉冮檺缁欒鑹叉垚鍔?""
        # 妯℃嫙瑙掕壊瀛樺湪
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 妯℃嫙鏉冮檺瀛樺湪
        role_service.perm_repo.get_by_id = Mock(return_value=Mock())
        # 妯℃嫙更新瑙掕壊
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 鎵ц鍒嗛厤鏉冮檺
        result = role_service.assign_permissions("test_role_id", ["test_permission_id"])
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_role_id"
    
    def test_revoke_permission_from_role_success(self, role_service, mock_role):
        """娴嬭瘯鎾ら攢瑙掕壊鏉冮檺鎴愬姛"""
        # 妯℃嫙瑙掕壊瀛樺湪
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 妯℃嫙更新瑙掕壊
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 鎵ц鎾ら攢鏉冮檺锛堜娇鐢╝ssign_permissions锛屼紶鍏ョ┖鍒楄〃锛?        result = role_service.assign_permissions("test_role_id", [])
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_role_id"
    
    def test_get_role_permissions_success(self, role_service, mock_role):
        """娴嬭瘯鑾峰彇瑙掕壊鏉冮檺鎴愬姛"""
        # 妯℃嫙鑾峰彇鏉冮檺
        mock_permission = Mock()
        mock_permission.id = "test_permission_id"
        mock_permission.name = "娴嬭瘯鏉冮檺"
        mock_permission.code = "test:permission"
        mock_role.permissions = [mock_permission]
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        
        # 鎵ц鑾峰彇鏉冮檺
        result = role_service.get_role_permissions("test_role_id")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].id == "test_permission_id"
    
    def test_assign_menu_to_role_success(self, role_service, mock_role):
        """娴嬭瘯鍒嗛厤鑿滃崟缁欒鑹叉垚鍔?""
        # 妯℃嫙瑙掕壊瀛樺湪
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 妯℃嫙鑿滃崟瀛樺湪
        role_service.menu_repo.get_by_id = Mock(return_value=Mock())
        # 妯℃嫙更新瑙掕壊
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 鎵ц鍒嗛厤鑿滃崟
        result = role_service.assign_menus("test_role_id", ["test_menu_id"])
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_role_id"
    
    def test_get_role_statistics(self, role_service):
        """娴嬭瘯鑾峰彇瑙掕壊缁熻"""
        # 妯℃嫙鑾峰彇缁熻
        role_service.role_repo.count_all = Mock(return_value=10)
        
        # 鎵ц鑾峰彇缁熻
        result = role_service.count_roles()
        
        # 楠岃瘉缁撴灉
        assert result == 10
