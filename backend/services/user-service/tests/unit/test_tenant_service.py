# -*- coding: utf-8 -*-
"""
TenantService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓绉熸埛
2. 鑾峰彇绉熸埛
3. 鏇存柊绉熸埛
4. 鍒犻櫎绉熸埛
5. 鑾峰彇绉熸埛鍒楄〃
6. 妫€鏌ヨ祫婧愰厤棰?7. 鑾峰彇濂楅淇℃伅
8. 鏇存柊绉熸埛濂楅
9. 妫€鏌ョ鎴疯繃鏈?10. 缁垂绉熸埛
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.tenant_service import TenantService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_tenant():
    """妯℃嫙绉熸埛瀵硅薄"""
    tenant = Mock()
    tenant.id = "test_tenant_id"
    tenant.name = "娴嬭瘯绉熸埛"
    tenant.code = "test_tenant"
    tenant.status = "active"
    tenant.description = "娴嬭瘯绉熸埛鎻忚堪"
    tenant.package_id = "basic"
    tenant.max_users = 50
    tenant.max_departments = 20
    tenant.max_storage = 10240
    tenant.expires_at = datetime(2026-12-31)
    tenant.users = []
    tenant.departments = []
    tenant.is_expired = Mock(return_value=False)
    tenant.get_user_count = Mock(return_value=10)
    tenant.get_department_count = Mock(return_value=5)
    tenant.to_dict = Mock(return_value={
        "id": "test_tenant_id",
        "name": "娴嬭瘯绉熸埛",
        "code": "test_tenant"
    })
    return tenant


@pytest.fixture
def tenant_service(mock_db):
    """鍒涘缓TenantService瀹炰緥"""
    return TenantService(mock_db)


class TestTenantService:
    """TenantService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯TenantService鍒濆鍖?""
        service = TenantService(mock_db)
        assert service.db == mock_db
        assert service.tenant_repo is not None
    
    def test_create_tenant_success(self, tenant_service, mock_tenant):
        """娴嬭瘯鍒涘缓绉熸埛鎴愬姛"""
        # 妯℃嫙绉熸埛缂栫爜涓嶅瓨鍦?        tenant_service.tenant_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙绉熸埛鍚嶇О涓嶅瓨鍦?        tenant_service.tenant_repo.exists_by_name = Mock(return_value=False)
        # 妯℃嫙鍒涘缓绉熸埛
        tenant_service.tenant_repo.create = Mock(return_value=mock_tenant)
        
        # 鎵ц鍒涘缓绉熸埛
        tenant_data = {
            "name": "娴嬭瘯绉熸埛",
            "code": "test_tenant"
        }
        result = tenant_service.create_tenant(tenant_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_tenant_id"
        assert result.name == "娴嬭瘯绉熸埛"
        tenant_service.tenant_repo.create.assert_called_once()
    
    def test_create_tenant_name_empty(self, tenant_service):
        """娴嬭瘯鍒涘缓绉熸埛锛堝悕绉颁负绌猴級"""
        # 鎵ц鍒涘缓绉熸埛骞堕獙璇佸紓甯?        tenant_data = {
            "name": "",
            "code": "test_tenant"
        }
        with pytest.raises(ValueError, match="绉熸埛鍚嶇О涓嶈兘涓虹┖"):
            tenant_service.create_tenant(tenant_data)
    
    def test_create_tenant_code_empty(self, tenant_service):
        """娴嬭瘯鍒涘缓绉熸埛锛堢紪鐮佷负绌猴級"""
        # 鎵ц鍒涘缓绉熸埛骞堕獙璇佸紓甯?        tenant_data = {
            "name": "娴嬭瘯绉熸埛",
            "code": ""
        }
        with pytest.raises(ValueError, match="绉熸埛缂栫爜涓嶈兘涓虹┖"):
            tenant_service.create_tenant(tenant_data)
    
    def test_create_tenant_code_exists(self, tenant_service):
        """娴嬭瘯鍒涘缓绉熸埛锛堢紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙绉熸埛缂栫爜宸插瓨鍦?        tenant_service.tenant_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц鍒涘缓绉熸埛骞堕獙璇佸紓甯?        tenant_data = {
            "name": "娴嬭瘯绉熸埛",
            "code": "existing_code"
        }
        with pytest.raises(ValueError, match="绉熸埛缂栫爜宸插瓨鍦?):
            tenant_service.create_tenant(tenant_data)
    
    def test_create_tenant_name_exists(self, tenant_service):
        """娴嬭瘯鍒涘缓绉熸埛锛堝悕绉板凡瀛樺湪锛?""
        # 妯℃嫙绉熸埛缂栫爜涓嶅瓨鍦?        tenant_service.tenant_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙绉熸埛鍚嶇О宸插瓨鍦?        tenant_service.tenant_repo.exists_by_name = Mock(return_value=True)
        
        # 鎵ц鍒涘缓绉熸埛骞堕獙璇佸紓甯?        tenant_data = {
            "name": "existing_name",
            "code": "test_tenant"
        }
        with pytest.raises(ValueError, match="绉熸埛鍚嶇О宸插瓨鍦?):
            tenant_service.create_tenant(tenant_data)
    
    def test_get_tenant_success(self, tenant_service, mock_tenant):
        """娴嬭瘯鑾峰彇绉熸埛鎴愬姛"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 鎵ц鏌ヨ
        result = tenant_service.get_tenant("test_tenant_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_tenant_id"
        tenant_service.tenant_repo.get_by_id.assert_called_once_with("test_tenant_id")
    
    def test_get_tenant_not_found(self, tenant_service):
        """娴嬭瘯鑾峰彇绉熸埛澶辫触"""
        # 妯℃嫙鏌ヨ绉熸埛杩斿洖None
        tenant_service.tenant_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = tenant_service.get_tenant("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_update_tenant_success(self, tenant_service, mock_tenant):
        """娴嬭瘯鏇存柊绉熸埛鎴愬姛"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 妯℃嫙绉熸埛鍚嶇О涓嶅瓨鍦?        tenant_service.tenant_repo.exists_by_name = Mock(return_value=False)
        # 妯℃嫙鏇存柊绉熸埛
        tenant_service.tenant_repo.update = Mock(return_value=mock_tenant)
        
        # 鎵ц鏇存柊
        update_data = {"description": "鏇存柊鍚庣殑鎻忚堪"}
        result = tenant_service.update_tenant("test_tenant_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_tenant_id"
        tenant_service.tenant_repo.update.assert_called_once()
    
    def test_update_tenant_not_found(self, tenant_service):
        """娴嬭瘯鏇存柊绉熸埛澶辫触锛堢鎴蜂笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ绉熸埛杩斿洖None
        tenant_service.tenant_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏇存柊骞堕獙璇佸紓甯?        update_data = {"description": "鏇存柊鍚庣殑鎻忚堪"}
        with pytest.raises(ValueError, match="绉熸埛涓嶅瓨鍦?):
            tenant_service.update_tenant("nonexistent_id", update_data)
    
    def test_delete_tenant_success(self, tenant_service, mock_tenant):
        """娴嬭瘯鍒犻櫎绉熸埛鎴愬姛"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 妯℃嫙鍒犻櫎绉熸埛
        tenant_service.tenant_repo.delete = Mock(return_value=True)
        
        # 鎵ц鍒犻櫎
        result = tenant_service.delete_tenant("test_tenant_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        tenant_service.tenant_repo.delete.assert_called_once_with("test_tenant_id")
    
    def test_delete_tenant_has_users(self, tenant_service, mock_tenant):
        """娴嬭瘯鍒犻櫎绉熸埛澶辫触锛堟湁鐢ㄦ埛锛?""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 璁剧疆鏈夌敤鎴?        mock_tenant.users = [Mock()]
        
        # 鎵ц鍒犻櫎骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="璇ョ鎴蜂笅瀛樺湪鐢ㄦ埛"):
            tenant_service.delete_tenant("test_tenant_id")
    
    def test_delete_tenant_has_departments(self, tenant_service, mock_tenant):
        """娴嬭瘯鍒犻櫎绉熸埛澶辫触锛堟湁閮ㄩ棬锛?""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 璁剧疆鏈夐儴闂?        mock_tenant.departments = [Mock()]
        
        # 鎵ц鍒犻櫎骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="璇ョ鎴蜂笅瀛樺湪閮ㄩ棬"):
            tenant_service.delete_tenant("test_tenant_id")
    
    def test_list_tenants_success(self, tenant_service, mock_tenant):
        """娴嬭瘯鑾峰彇绉熸埛鍒楄〃鎴愬姛"""
        # 妯℃嫙鏌ヨ绉熸埛鍒楄〃
        tenant_service.tenant_repo.get_all = Mock(return_value=[mock_tenant])
        tenant_service.tenant_repo.count_all = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = tenant_service.list_tenants()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_check_quota_users(self, tenant_service, mock_tenant):
        """娴嬭瘯妫€鏌ョ敤鎴烽厤棰?""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 鎵ц妫€鏌?        result = tenant_service.check_quota("test_tenant_id", "users")
        
        # 楠岃瘉缁撴灉
        assert result["used"] == 10
        assert result["max"] == 50
        assert result["available"] == 40
    
    def test_check_quota_departments(self, tenant_service, mock_tenant):
        """娴嬭瘯妫€鏌ラ儴闂ㄩ厤棰?""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 鎵ц妫€鏌?        result = tenant_service.check_quota("test_tenant_id", "departments")
        
        # 楠岃瘉缁撴灉
        assert result["used"] == 5
        assert result["max"] == 20
        assert result["available"] == 15
    
    def test_get_package_info_success(self, tenant_service):
        """娴嬭瘯鑾峰彇濂楅淇℃伅鎴愬姛"""
        # 鎵ц鑾峰彇
        result = tenant_service.get_package_info("basic")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["name"] == "鍩虹鐗?
    
    def test_get_package_info_not_found(self, tenant_service):
        """娴嬭瘯鑾峰彇濂楅淇℃伅澶辫触"""
        # 鎵ц鑾峰彇
        result = tenant_service.get_package_info("nonexistent")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_all_packages(self, tenant_service):
        """娴嬭瘯鑾峰彇鎵€鏈夊椁愪俊鎭?""
        # 鎵ц鑾峰彇
        result = tenant_service.get_all_packages()
        
        # 楠岃瘉缁撴灉
        assert "free" in result
        assert "basic" in result
        assert "professional" in result
        assert "enterprise" in result
    
    def test_update_package_success(self, tenant_service, mock_tenant):
        """娴嬭瘯鏇存柊绉熸埛濂楅鎴愬姛"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 妯℃嫙鏇存柊绉熸埛
        tenant_service.tenant_repo.update = Mock(return_value=mock_tenant)
        
        # 鎵ц鏇存柊
        result = tenant_service.update_package("test_tenant_id", "professional")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_tenant_id"
    
    def test_update_package_not_found(self, tenant_service):
        """娴嬭瘯鏇存柊绉熸埛濂楅澶辫触锛堝椁愪笉瀛樺湪锛?""
        # 鎵ц鏇存柊骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="濂楅涓嶅瓨鍦?):
            tenant_service.update_package("test_tenant_id", "nonexistent")
    
    def test_check_expiration_true(self, tenant_service, mock_tenant):
        """娴嬭瘯妫€鏌ョ鎴疯繃鏈燂紙宸茶繃鏈燂級"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 璁剧疆宸茶繃鏈?        mock_tenant.is_expired = Mock(return_value=True)
        
        # 鎵ц妫€鏌?        result = tenant_service.check_expiration("test_tenant_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
    
    def test_check_expiration_false(self, tenant_service, mock_tenant):
        """娴嬭瘯妫€鏌ョ鎴疯繃鏈燂紙鏈繃鏈燂級"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 鎵ц妫€鏌?        result = tenant_service.check_expiration("test_tenant_id")
        
        # 楠岃瘉缁撴灉
        assert result is False
    
    def test_renew_tenant_success(self, tenant_service, mock_tenant):
        """娴嬭瘯缁垂绉熸埛鎴愬姛"""
        # 妯℃嫙鏌ヨ绉熸埛
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 妯℃嫙鏇存柊绉熸埛
        tenant_service.tenant_repo.update = Mock(return_value=mock_tenant)
        
        # 鎵ц缁垂
        result = tenant_service.renew_tenant("test_tenant_id", days=365)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_tenant_id"
        assert result.status == "active"
    
    def test_renew_tenant_not_found(self, tenant_service):
        """娴嬭瘯缁垂绉熸埛澶辫触锛堢鎴蜂笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ绉熸埛杩斿洖None
        tenant_service.tenant_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц缁垂骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="绉熸埛涓嶅瓨鍦?):
            tenant_service.renew_tenant("nonexistent_id", days=365)
