# -*- coding: utf-8 -*-
"""
DepartmentService单元测试

测试内容：
1. 创建部门
2. 获取部门
3. 更新部门
4. 删除部门
5. 获取部门列表
6. 获取部门树
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.department_service import DepartmentService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_department():
    """模拟部门对象"""
    dept = Mock()
    dept.id = "test_dept_id"
    dept.name = "技术部"
    dept.code = "tech"
    dept.tenant_id = "default"
    dept.parent_id = None
    dept.level = 1
    dept.sort_order = 0
    dept.description = "技术部门"
    dept.leader_id = None
    dept.phone = None
    dept.email = None
    dept.children = []
    dept.users = []
    dept.to_dict = Mock(return_value={
        "id": "test_dept_id",
        "name": "技术部",
        "code": "tech"
    })
    dept.to_tree_dict = Mock(return_value={
        "id": "test_dept_id",
        "name": "技术部",
        "children": []
    })
    return dept


@pytest.fixture
def department_service(mock_db):
    """创建DepartmentService实例"""
    return DepartmentService(mock_db)


class TestDepartmentService:
    """DepartmentService测试类"""
    
    def test_init(self, mock_db):
        """测试DepartmentService初始化"""
        service = DepartmentService(mock_db)
        assert service.db == mock_db
        assert service.dept_repo is not None
    
    def test_create_department_success(self, department_service, mock_department):
        """测试创建部门成功"""
        # 模拟部门编码不存在
        department_service.dept_repo.exists_by_code = Mock(return_value=False)
        # 模拟部门名称不存在
        department_service.dept_repo.exists_by_name_in_tenant = Mock(return_value=False)
        # 模拟创建部门
        department_service.dept_repo.create = Mock(return_value=mock_department)
        
        # 执行创建部门
        dept_data = {
            "name": "技术部",
            "tenant_id": "default"
        }
        result = department_service.create_department(dept_data)
        
        # 验证结果
        assert result.id == "test_dept_id"
        assert result.name == "技术部"
        department_service.dept_repo.create.assert_called_once()
    
    def test_create_department_name_empty(self, department_service):
        """测试创建部门（名称为空）"""
        # 执行创建部门并验证异常
        dept_data = {
            "name": "",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="部门名称不能为空"):
            department_service.create_department(dept_data)
    
    def test_create_department_code_exists(self, department_service):
        """测试创建部门（编码已存在）"""
        # 模拟部门编码已存在
        department_service.dept_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建部门并验证异常
        dept_data = {
            "name": "技术部",
            "code": "existing_code",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="部门编码已存在"):
            department_service.create_department(dept_data)
    
    def test_create_department_name_exists(self, department_service):
        """测试创建部门（名称已存在）"""
        # 模拟部门编码不存在
        department_service.dept_repo.exists_by_code = Mock(return_value=False)
        # 模拟部门名称已存在
        department_service.dept_repo.exists_by_name_in_tenant = Mock(return_value=True)
        
        # 执行创建部门并验证异常
        dept_data = {
            "name": "existing_name",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="部门名称已存在"):
            department_service.create_department(dept_data)
    
    def test_get_department_success(self, department_service, mock_department):
        """测试获取部门成功"""
        # 模拟查询部门
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        
        # 执行查询
        result = department_service.get_department("test_dept_id")
        
        # 验证结果
        assert result.id == "test_dept_id"
        department_service.dept_repo.get_by_id.assert_called_once_with("test_dept_id")
    
    def test_get_department_not_found(self, department_service):
        """测试获取部门失败"""
        # 模拟查询部门返回None
        department_service.dept_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = department_service.get_department("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_update_department_success(self, department_service, mock_department):
        """测试更新部门成功"""
        # 模拟查询部门
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 模拟部门名称不存在
        department_service.dept_repo.exists_by_name_in_tenant = Mock(return_value=False)
        # 模拟更新部门
        department_service.dept_repo.update = Mock(return_value=mock_department)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = department_service.update_department("test_dept_id", update_data)
        
        # 验证结果
        assert result.id == "test_dept_id"
        department_service.dept_repo.update.assert_called_once()
    
    def test_update_department_not_found(self, department_service):
        """测试更新部门失败（部门不存在）"""
        # 模拟查询部门返回None
        department_service.dept_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新并验证异常
        update_data = {"description": "更新后的描述"}
        with pytest.raises(ValueError, match="部门不存在"):
            department_service.update_department("nonexistent_id", update_data)
    
    def test_delete_department_success(self, department_service, mock_department):
        """测试删除部门成功"""
        # 模拟查询部门
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 模拟删除部门
        department_service.dept_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = department_service.delete_department("test_dept_id")
        
        # 验证结果
        assert result is True
        department_service.dept_repo.delete.assert_called_once_with("test_dept_id")
    
    def test_delete_department_has_children(self, department_service, mock_department):
        """测试删除部门失败（有子部门）"""
        # 模拟查询部门
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 设置有子部门
        mock_department.children = [Mock()]
        
        # 执行删除并验证异常
        with pytest.raises(ValueError, match="该部门下存在子部门"):
            department_service.delete_department("test_dept_id")
    
    def test_delete_department_has_users(self, department_service, mock_department):
        """测试删除部门失败（有用户）"""
        # 模拟查询部门
        department_service.dept_repo.get_by_id = Mock(return_value=mock_department)
        # 设置有用户
        mock_department.users = [Mock()]
        
        # 执行删除并验证异常
        with pytest.raises(ValueError, match="该部门下存在用户"):
            department_service.delete_department("test_dept_id")
    
    def test_list_departments_success(self, department_service, mock_department):
        """测试获取部门列表成功"""
        # 模拟查询部门列表
        department_service.dept_repo.get_by_tenant_id = Mock(return_value=[mock_department])
        department_service.dept_repo.count_by_tenant = Mock(return_value=1)
        
        # 执行查询
        result = department_service.list_departments(tenant_id="default")
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_get_department_tree_success(self, department_service, mock_department):
        """测试获取部门树成功"""
        # 模拟查询部门树
        department_service.dept_repo.get_tree = Mock(return_value=[mock_department])
        
        # 执行查询
        result = department_service.get_department_tree(tenant_id="default")
        
        # 验证结果
        assert len(result) == 1
        assert result[0]["id"] == "test_dept_id"