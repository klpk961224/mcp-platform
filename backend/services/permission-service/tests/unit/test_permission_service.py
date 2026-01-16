# -*- coding: utf-8 -*-
"""
PermissionService单元测试

测试内容：
1. 创建权限
2. 获取权限
3. 更新权限
4. 删除权限
5. 获取权限列表
6. 统计权限数量
7. 检查用户权限
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.permission_service import PermissionService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_permission():
    """模拟权限对象"""
    permission = Mock()
    permission.id = "test_permission_id"
    permission.name = "用户管理"
    permission.code = "user:manage"
    permission.type = "operation"
    permission.resource = "user"
    permission.description = "用户管理权限"
    permission.status = "active"
    return permission


@pytest.fixture
def permission_service(mock_db):
    """创建PermissionService实例"""
    return PermissionService(mock_db)


class TestPermissionService:
    """PermissionService测试类"""
    
    def test_init(self, mock_db):
        """测试PermissionService初始化"""
        service = PermissionService(mock_db)
        assert service.db == mock_db
        assert service.perm_repo is not None
    
    def test_create_permission_success(self, permission_service, mock_permission):
        """测试创建权限成功"""
        # 模拟权限编码不存在
        permission_service.perm_repo.exists_by_code = Mock(return_value=False)
        # 模拟创建权限
        permission_service.perm_repo.create = Mock(return_value=mock_permission)
        
        # 执行创建权限
        permission_data = {
            "name": "用户管理",
            "code": "user:manage",
            "type": "operation",
            "resource": "user"
        }
        result = permission_service.create_permission(permission_data)
        
        # 验证结果
        assert result.id == "test_permission_id"
        assert result.name == "用户管理"
        permission_service.perm_repo.create.assert_called_once()
    
    def test_create_permission_code_exists(self, permission_service):
        """测试创建权限（编码已存在）"""
        # 模拟权限编码已存在
        permission_service.perm_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建权限并验证异常
        permission_data = {
            "name": "用户管理",
            "code": "existing_code"
        }
        with pytest.raises(ValueError, match="权限编码已存在"):
            permission_service.create_permission(permission_data)
    
    def test_get_permission_success(self, permission_service, mock_permission):
        """测试获取权限成功"""
        # 模拟查询权限
        permission_service.perm_repo.get_by_id = Mock(return_value=mock_permission)
        
        # 执行查询
        result = permission_service.get_permission("test_permission_id")
        
        # 验证结果
        assert result.id == "test_permission_id"
        permission_service.perm_repo.get_by_id.assert_called_once_with("test_permission_id")
    
    def test_get_permission_not_found(self, permission_service):
        """测试获取权限失败"""
        # 模拟查询权限返回None
        permission_service.perm_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = permission_service.get_permission("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_permission_by_code_success(self, permission_service, mock_permission):
        """测试根据编码获取权限成功"""
        # 模拟查询权限
        permission_service.perm_repo.get_by_code = Mock(return_value=mock_permission)
        
        # 执行查询
        result = permission_service.get_permission_by_code("user:manage")
        
        # 验证结果
        assert result.code == "user:manage"
        permission_service.perm_repo.get_by_code.assert_called_once_with("user:manage")
    
    def test_update_permission_success(self, permission_service, mock_permission):
        """测试更新权限成功"""
        # 模拟查询权限
        permission_service.perm_repo.get_by_id = Mock(return_value=mock_permission)
        # 模拟更新权限
        permission_service.perm_repo.update = Mock(return_value=mock_permission)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = permission_service.update_permission("test_permission_id", update_data)
        
        # 验证结果
        assert result.id == "test_permission_id"
        permission_service.perm_repo.update.assert_called_once()
    
    def test_update_permission_not_found(self, permission_service):
        """测试更新权限失败（权限不存在）"""
        # 模拟查询权限返回None
        permission_service.perm_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = permission_service.update_permission("nonexistent_id", update_data)
        
        # 验证结果
        assert result is None
    
    def test_delete_permission_success(self, permission_service):
        """测试删除权限成功"""
        # 模拟删除权限
        permission_service.perm_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = permission_service.delete_permission("test_permission_id")
        
        # 验证结果
        assert result is True
        permission_service.perm_repo.delete.assert_called_once_with("test_permission_id")
    
    def test_list_permissions_success(self, permission_service, mock_permission):
        """测试获取权限列表成功"""
        # 模拟查询权限列表
        permission_service.perm_repo.get_all = Mock(return_value=[mock_permission])
        
        # 执行查询
        result = permission_service.list_permissions()
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_permission_id"
    
    def test_count_permissions_success(self, permission_service):
        """测试统计权限数量成功"""
        # 模拟统计
        permission_service.perm_repo.count_all = Mock(return_value=50)
        
        # 执行统计
        result = permission_service.count_permissions()
        
        # 验证结果
        assert result == 50
    
    def test_check_user_permission_has_permission(self, permission_service, mock_permission):
        """测试检查用户权限（有权限）"""
        # 模拟查询角色
        mock_role = Mock()
        mock_role.has_permission = Mock(return_value=True)
        permission_service.db.query.return_value.join.return_value.filter.return_value.all = Mock(return_value=[mock_role])
        
        # 执行检查
        result = permission_service.check_user_permission("user_001", "user:manage")
        
        # 验证结果
        assert result is True
    
    def test_check_user_permission_no_permission(self, permission_service, mock_permission):
        """测试检查用户权限（无权限）"""
        # 模拟查询角色返回空列表
        permission_service.db.query.return_value.join.return_value.filter.return_value.all = Mock(return_value=[])
        
        # 执行检查
        result = permission_service.check_user_permission("user_001", "user:manage")
        
        # 验证结果
        assert result is False