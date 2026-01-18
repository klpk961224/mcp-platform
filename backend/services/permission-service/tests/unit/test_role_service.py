# -*- coding: utf-8 -*-
"""
RoleService单元测试

测试内容：
1. 创建角色
2. 获取角色
3. 更新角色
4. 删除角色
5. 搜索角色
6. 角色权限管理
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

# 导入所有模型以初始化SQLAlchemy mapper
from common.database.models.user import Role
from common.database.models.permission import Permission, Menu

# 手动配置SQLAlchemy mapper
from sqlalchemy.orm import configure_mappers
configure_mappers()

from app.services.role_service import RoleService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_role():
    """模拟角色对象"""
    role = Mock(spec=Role)
    role.id = "test_role_id"
    role.name = "测试角色"
    role.code = "test_role"
    role.description = "测试角色描述"
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
    """创建RoleService实例"""
    return RoleService(mock_db)


class TestRoleService:
    """RoleService测试类"""
    
    def test_init(self, mock_db):
        """测试RoleService初始化"""
        service = RoleService(mock_db)
        assert service.db == mock_db
        assert service.role_repo is not None
        assert service.perm_repo is not None
        assert service.menu_repo is not None
    
    def test_create_role_success(self, role_service, mock_role):
        """测试创建角色成功"""
        # 模拟角色代码不存在
        role_service.role_repo.exists_by_code = Mock(return_value=False)
        # 模拟角色名称在同一租户中不存在
        role_service.role_repo.exists_by_name_in_tenant = Mock(return_value=False)
        # 模拟创建角色
        role_service.role_repo.create = Mock(return_value=mock_role)
        
        # 执行创建角色
        role_data = {
            "name": "测试角色",
            "code": "test_role",
            "tenant_id": "default",
            "description": "测试角色描述"
        }
        result = role_service.create_role(role_data)
        
        # 验证结果
        assert result.id == "test_role_id"
        assert result.name == "测试角色"
        role_service.role_repo.create.assert_called_once()
    
    def test_create_role_code_exists(self, role_service):
        """测试创建角色时代码已存在"""
        # 模拟角色代码已存在
        role_service.role_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建角色并验证异常
        role_data = {
            "name": "测试角色",
            "code": "existing_role",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="角色编码已存在"):
            role_service.create_role(role_data)
    
    def test_get_by_id_success(self, role_service, mock_role):
        """测试获取角色成功"""
        # 模拟查询角色
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        
        # 执行查询
        result = role_service.get_role("test_role_id")
        
        # 验证结果
        assert result.id == "test_role_id"
        role_service.role_repo.get_by_id.assert_called_once_with("test_role_id")
    
    def test_get_by_id_not_found(self, role_service):
        """测试获取角色失败"""
        # 模拟查询角色返回None
        role_service.role_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = role_service.get_role("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_update_role_success(self, role_service, mock_role):
        """测试更新角色成功"""
        # 模拟查询角色
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 模拟更新角色
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = role_service.update_role("test_role_id", update_data)
        
        # 验证结果
        assert result.id == "test_role_id"
        role_service.role_repo.update.assert_called_once()
    
    def test_delete_role_success(self, role_service):
        """测试删除角色成功"""
        # 模拟删除角色
        role_service.role_repo.delete = Mock()
        
        # 执行删除
        role_service.delete_role("test_role_id")
        
        # 验证结果
        role_service.role_repo.delete.assert_called_once_with("test_role_id")
    
    def test_search_roles_success(self, role_service, mock_role):
        """测试搜索角色成功"""
        # 模拟搜索角色
        role_service.role_repo.search = Mock(return_value=[mock_role])
        
        # 执行搜索
        result = role_service.list_roles(
            tenant_id="default",
            keyword="测试"
        )
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_role_id"
    
    def test_assign_permission_to_role_success(self, role_service, mock_role):
        """测试分配权限给角色成功"""
        # 模拟角色存在
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 模拟权限存在
        role_service.perm_repo.get_by_id = Mock(return_value=Mock())
        # 模拟更新角色
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 执行分配权限
        result = role_service.assign_permissions("test_role_id", ["test_permission_id"])
        
        # 验证结果
        assert result.id == "test_role_id"
    
    def test_revoke_permission_from_role_success(self, role_service, mock_role):
        """测试撤销角色权限成功"""
        # 模拟角色存在
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 模拟更新角色
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 执行撤销权限（使用assign_permissions，传入空列表）
        result = role_service.assign_permissions("test_role_id", [])
        
        # 验证结果
        assert result.id == "test_role_id"
    
    def test_get_role_permissions_success(self, role_service, mock_role):
        """测试获取角色权限成功"""
        # 模拟获取权限
        mock_permission = Mock()
        mock_permission.id = "test_permission_id"
        mock_permission.name = "测试权限"
        mock_permission.code = "test:permission"
        mock_role.permissions = [mock_permission]
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        
        # 执行获取权限
        result = role_service.get_role_permissions("test_role_id")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_permission_id"
    
    def test_assign_menu_to_role_success(self, role_service, mock_role):
        """测试分配菜单给角色成功"""
        # 模拟角色存在
        role_service.role_repo.get_by_id = Mock(return_value=mock_role)
        # 模拟菜单存在
        role_service.menu_repo.get_by_id = Mock(return_value=Mock())
        # 模拟更新角色
        role_service.role_repo.update = Mock(return_value=mock_role)
        
        # 执行分配菜单
        result = role_service.assign_menus("test_role_id", ["test_menu_id"])
        
        # 验证结果
        assert result.id == "test_role_id"
    
    def test_get_role_statistics(self, role_service):
        """测试获取角色统计"""
        # 模拟获取统计
        role_service.role_repo.count_all = Mock(return_value=10)
        
        # 执行获取统计
        result = role_service.count_roles()
        
        # 验证结果
        assert result == 10