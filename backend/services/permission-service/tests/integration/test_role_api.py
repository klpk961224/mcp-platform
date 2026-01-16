# -*- coding: utf-8 -*-
"""
Role API集成测试

测试内容：
1. 创建角色API
2. 获取角色列表API
3. 获取角色详情API
4. 更新角色API
5. 删除角色API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


@pytest.fixture
def client():
    """创建测试客户端"""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_role():
    """模拟角色数据"""
    return {
        "id": "test_role_id",
        "tenant_id": "default",
        "name": "测试角色",
        "code": "test_role",
        "description": "测试角色描述",
        "is_system": False,
        "status": "active",
        "created_at": "2026-01-15T00:00:00",
        "updated_at": "2026-01-15T00:00:00"
    }


class TestRoleAPI:
    """Role API测试类"""
    
    def test_create_role_success(self, client, mock_role):
        """测试创建角色成功"""
        # 模拟RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "测试角色"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "测试角色描述"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.create_role.return_value = mock_role_obj
            MockRoleService.return_value = mock_service
            
            # 发送创建角色请求
            response = client.post("/api/v1/roles", json={
                "name": "测试角色",
                "code": "test_role",
                "tenant_id": "default",
                "description": "测试角色描述"
            })
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "测试角色"
            assert data["code"] == "test_role"
    
    def test_create_role_code_exists(self, client):
        """测试创建角色失败（角色代码已存在）"""
        # 模拟RoleService抛出异常
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.create_role.side_effect = ValueError("角色代码已存在")
            MockRoleService.return_value = mock_service
            
            # 发送创建角色请求
            response = client.post("/api/v1/roles", json={
                "name": "测试角色",
                "code": "existing_role",
                "tenant_id": "default"
            })
            
            # 验证响应
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
    
    def test_get_roles_success(self, client, mock_role):
        """测试获取角色列表成功"""
        # 模拟RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "测试角色"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "测试角色描述"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.search_roles.return_value = ([mock_role_obj], 1)
            MockRoleService.return_value = mock_service
            
            # 发送获取角色列表请求
            response = client.get("/api/v1/roles?page=1&page_size=10")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert len(data["items"]) == 1
            assert data["items"][0]["name"] == "测试角色"
    
    def test_get_roles_with_filters(self, client):
        """测试获取角色列表（带筛选条件）"""
        # 模拟RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.search_roles.return_value = ([], 0)
            MockRoleService.return_value = mock_service
            
            # 发送获取角色列表请求（带筛选条件）
            response = client.get("/api/v1/roles?page=1&page_size=10&tenant_id=default&status=active&keyword=测试")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["items"]) == 0
    
    def test_get_role_success(self, client, mock_role):
        """测试获取角色详情成功"""
        # 模拟RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "测试角色"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "测试角色描述"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.get_by_id.return_value = mock_role_obj
            MockRoleService.return_value = mock_service
            
            # 发送获取角色详情请求
            response = client.get("/api/v1/roles/test_role_id")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_role_id"
            assert data["name"] == "测试角色"
    
    def test_get_role_not_found(self, client):
        """测试获取角色详情失败（角色不存在）"""
        # 模拟RoleService返回None
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockRoleService.return_value = mock_service
            
            # 发送获取角色详情请求
            response = client.get("/api/v1/roles/nonexistent_id")
            
            # 验证响应
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_update_role_success(self, client):
        """测试更新角色成功"""
        # 模拟RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_role_obj.id = "test_role_id"
            mock_role_obj.name = "更新后的角色"
            mock_role_obj.code = "test_role"
            mock_role_obj.description = "更新后的描述"
            mock_role_obj.tenant_id = "default"
            mock_role_obj.is_system = False
            mock_role_obj.status = "active"
            mock_role_obj.created_at = Mock()
            mock_role_obj.updated_at = Mock()
            mock_role_obj.created_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_role_obj.updated_at.isoformat = Mock(return_value="2026-01-15T00:00:00")
            mock_service.get_by_id.return_value = mock_role_obj
            mock_service.update_role.return_value = mock_role_obj
            MockRoleService.return_value = mock_service
            
            # 发送更新角色请求
            response = client.put("/api/v1/roles/test_role_id", json={
                "name": "更新后的角色",
                "description": "更新后的描述"
            })
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "更新后的角色"
    
    def test_update_role_not_found(self, client):
        """测试更新角色失败（角色不存在）"""
        # 模拟RoleService返回None
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockRoleService.return_value = mock_service
            
            # 发送更新角色请求
            response = client.put("/api/v1/roles/nonexistent_id", json={
                "name": "更新后的角色"
            })
            
            # 验证响应
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_delete_role_success(self, client):
        """测试删除角色成功"""
        # 模拟RoleService
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_role_obj = Mock()
            mock_service.get_by_id.return_value = mock_role_obj
            mock_service.delete_role = Mock()
            MockRoleService.return_value = mock_service
            
            # 发送删除角色请求
            response = client.delete("/api/v1/roles/test_role_id")
            
            # 验证响应
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "删除成功"
    
    def test_delete_role_not_found(self, client):
        """测试删除角色失败（角色不存在）"""
        # 模拟RoleService返回None
        with patch('app.api.v1.roles.RoleService') as MockRoleService:
            mock_service = Mock()
            mock_service.get_by_id.return_value = None
            MockRoleService.return_value = mock_service
            
            # 发送删除角色请求
            response = client.delete("/api/v1/roles/nonexistent_id")
            
            # 验证响应
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
    
    def test_create_role_missing_name(self, client):
        """测试创建角色失败（缺少角色名称）"""
        # 发送创建角色请求（缺少角色名称）
        response = client.post("/api/v1/roles", json={
            "code": "test_role",
            "tenant_id": "default"
        })
        
        # 验证响应
        assert response.status_code == 422  # Validation Error
    
    def test_create_role_missing_code(self, client):
        """测试创建角色失败（缺少角色代码）"""
        # 发送创建角色请求（缺少角色代码）
        response = client.post("/api/v1/roles", json={
            "name": "测试角色",
            "tenant_id": "default"
        })
        
        # 验证响应
        assert response.status_code == 422  # Validation Error