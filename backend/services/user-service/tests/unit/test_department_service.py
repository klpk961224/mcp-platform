# -*- coding: utf-8 -*-
"""
DepartmentService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓閮ㄩ棬
2. 鑾峰彇閮ㄩ棬
3. 鏇存柊閮ㄩ棬
4. 鍒犻櫎閮ㄩ棬
5. 鑾峰彇閮ㄩ棬鍒楄〃
6. 鑾峰彇閮ㄩ棬鏍?"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.department_service import DepartmentService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_department():
    """妯℃嫙閮ㄩ棬瀵硅薄"""
    dept = Mock()
    dept.id = "test_dept_id"
    dept.name = "鎶€鏈儴"
    dept.code = "tech"
    dept.tenant_id = "default"
    dept.parent_id = None
    dept.level = 1
    dept.sort_order = 0
    dept.description = "鎶€鏈儴闂?
    dept.leader_id = None
    dept.phone = None
    dept.email = None
    dept.children = []
    dept.users = []
    dept.to_dict = Mock(return_value={
        "id": "test_dept_id",
        "name": "鎶€鏈儴",
        "code": "tech"
    })
    dept.to_tree_dict = Mock(return_value={
        "id": "test_dept_id",
        "name": "鎶€鏈儴",
        "children": []
    })
    return dept


@pytest.fixture
def department_service(mock_db):
    """鍒涘缓DepartmentService瀹炰緥"""
    return DepartmentService(mock_db)


class TestDepartmentService:
    """DepartmentService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯DepartmentService鍒濆鍖?""
        service = DepartmentService(mock_db)
        assert service.db == mock_db
        assert service.dept_repo is not None
    
    def test_create_department_success(self, department_service, mock_department):
        """娴嬭瘯鍒涘缓閮ㄩ棬鎴愬姛"""
        # 妯℃嫙閮ㄩ棬缂栫爜涓嶅瓨鍦?        department_service.dept_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙閮ㄩ棬鍚嶇О涓嶅瓨鍦?        department_service.dept_repo.exists_by_name_in_tenant = Mock(return_value=False)
        # 妯℃嫙鍒涘缓閮ㄩ棬
        department_service.dept_repo.create = Mock(return_value=mock_department)
        
        # 鎵ц鍒涘缓閮ㄩ棬
        dept_data = {
            "name": "鎶€鏈儴",
            "tenant_id": "default"
        }
        result = department_service.create_department(dept_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dept_id"
        assert result.name == "鎶€鏈儴"
        department_service.dept_repo.create.assert_called_once()
    
    def test_create_department_name_empty(self, department_service):
        """娴嬭瘯鍒涘缓閮ㄩ棬锛堝悕绉颁负绌猴級"""
        # 鎵ц鍒涘缓閮ㄩ棬骞堕獙璇佸紓甯?        dept_data = {
            "name": "",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="閮ㄩ棬鍚嶇О涓嶈兘涓虹┖"):
            department_service.create_department(dept_data)
    
    def test_create_department_code_exists(self, department_service):
        """娴嬭瘯鍒涘缓閮ㄩ棬锛堢紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙閮ㄩ棬缂栫爜宸插瓨鍦?        department_service.dept_repo.exists_by_code = Mock(return_value=True)
        
        # 鎵ц鍒涘缓閮ㄩ棬骞堕獙璇佸紓甯?        dept_data = {
            "name": "鎶€鏈儴",
            "code": "existing_code",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="閮ㄩ棬缂栫爜宸插瓨鍦?):
            department_service.create_department(dept_data)
    
    def test_create_department_name_exists(self, department_service):
        """娴嬭瘯鍒涘缓閮ㄩ棬锛堝悕绉板凡瀛樺湪锛?""
        # 妯℃嫙閮ㄩ棬缂栫爜涓嶅瓨鍦?        department_service.dept_repo.exists_by_code = Mock(return_value=False)
        # 妯℃嫙閮ㄩ棬鍚嶇О宸插瓨鍦?        department_service.dept_repo.exists_by_name_in_tenant = Mock(return_value=True)
        
        # 鎵ц鍒涘缓閮ㄩ棬骞堕獙璇佸紓甯?        dept_data = {
            "name": "existing_name",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="閮ㄩ棬鍚嶇О宸插瓨鍦?):
            department_service.create_department(dept_data)
    
    def test_get_department_success(self, department_service, mock_department):
        """娴嬭瘯鑾峰彇閮ㄩ棬鎴愬姛"""
        # 妯℃嫙鏌ヨ閮ㄩ棬
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        
        # 鎵ц鏌ヨ
        result = department_service.get_department("test_dept_id")
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dept_id"
        department_service.dept_repo.get_by_id.assert_called_once_with("test_dept_id")
    
    def test_get_department_not_found(self, department_service):
        """娴嬭瘯鑾峰彇閮ㄩ棬澶辫触"""
        # 妯℃嫙鏌ヨ閮ㄩ棬杩斿洖None
        department_service.dept_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = department_service.get_department("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_update_department_success(self, department_service, mock_department):
        """娴嬭瘯鏇存柊閮ㄩ棬鎴愬姛"""
        # 妯℃嫙鏌ヨ閮ㄩ棬
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 妯℃嫙閮ㄩ棬鍚嶇О涓嶅瓨鍦?        department_service.dept_repo.exists_by_name_in_tenant = Mock(return_value=False)
        # 妯℃嫙鏇存柊閮ㄩ棬
        department_service.dept_repo.update = Mock(return_value=mock_department)
        
        # 鎵ц鏇存柊
        update_data = {"description": "鏇存柊鍚庣殑鎻忚堪"}
        result = department_service.update_department("test_dept_id", update_data)
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_dept_id"
        department_service.dept_repo.update.assert_called_once()
    
    def test_update_department_not_found(self, department_service):
        """娴嬭瘯鏇存柊閮ㄩ棬澶辫触锛堥儴闂ㄤ笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ閮ㄩ棬杩斿洖None
        department_service.dept_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏇存柊骞堕獙璇佸紓甯?        update_data = {"description": "鏇存柊鍚庣殑鎻忚堪"}
        with pytest.raises(ValueError, match="閮ㄩ棬涓嶅瓨鍦?):
            department_service.update_department("nonexistent_id", update_data)
    
    def test_delete_department_success(self, department_service, mock_department):
        """娴嬭瘯鍒犻櫎閮ㄩ棬鎴愬姛"""
        # 妯℃嫙鏌ヨ閮ㄩ棬
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 妯℃嫙鍒犻櫎閮ㄩ棬
        department_service.dept_repo.delete = Mock(return_value=True)
        
        # 鎵ц鍒犻櫎
        result = department_service.delete_department("test_dept_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        department_service.dept_repo.delete.assert_called_once_with("test_dept_id")
    
    def test_delete_department_has_children(self, department_service, mock_department):
        """娴嬭瘯鍒犻櫎閮ㄩ棬澶辫触锛堟湁瀛愰儴闂級"""
        # 妯℃嫙鏌ヨ閮ㄩ棬
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 璁剧疆鏈夊瓙閮ㄩ棬
        mock_department.children = [Mock()]
        
        # 鎵ц鍒犻櫎骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="璇ラ儴闂ㄤ笅瀛樺湪瀛愰儴闂?):
            department_service.delete_department("test_dept_id")
    
    def test_delete_department_has_users(self, department_service, mock_department):
        """娴嬭瘯鍒犻櫎閮ㄩ棬澶辫触锛堟湁鐢ㄦ埛锛?""
        # 妯℃嫙鏌ヨ閮ㄩ棬
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 璁剧疆鏈夌敤鎴?        mock_department.users = [Mock()]
        
        # 鎵ц鍒犻櫎骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="璇ラ儴闂ㄤ笅瀛樺湪鐢ㄦ埛"):
            department_service.delete_department("test_dept_id")
    
    def test_list_departments_success(self, department_service, mock_department):
        """娴嬭瘯鑾峰彇閮ㄩ棬鍒楄〃鎴愬姛"""
        # 妯℃嫙鏌ヨ閮ㄩ棬鍒楄〃
        department_service.dept_repo.get_by_tenant_id = Mock(return_value=[mock_department])
        department_service.dept_repo.count_by_tenant = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = department_service.list_departments(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_get_department_tree_success(self, department_service, mock_department):
        """娴嬭瘯鑾峰彇閮ㄩ棬鏍戞垚鍔?""
        # 妯℃嫙鏌ヨ閮ㄩ棬鏍?        department_service.dept_repo.get_tree = Mock(return_value=[mock_department])
        
        # 鎵ц鏌ヨ
        result = department_service.get_department_tree(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0]["id"] == "test_dept_id"
