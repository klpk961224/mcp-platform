# -*- coding: utf-8 -*-
"""
TenantService单元测试

测试内容：
1. 创建租户
2. 获取租户
3. 更新租户
4. 删除租户
5. 获取租户列表
6. 检查资源配额
7. 获取套餐信息
8. 更新租户套餐
9. 检查租户过期
10. 续费租户
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.tenant_service import TenantService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_tenant():
    """模拟租户对象"""
    tenant = Mock()
    tenant.id = "test_tenant_id"
    tenant.name = "测试租户"
    tenant.code = "test_tenant"
    tenant.status = "active"
    tenant.description = "测试租户描述"
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
        "name": "测试租户",
        "code": "test_tenant"
    })
    return tenant


@pytest.fixture
def tenant_service(mock_db):
    """创建TenantService实例"""
    return TenantService(mock_db)


class TestTenantService:
    """TenantService测试类"""
    
    def test_init(self, mock_db):
        """测试TenantService初始化"""
        service = TenantService(mock_db)
        assert service.db == mock_db
        assert service.tenant_repo is not None
    
    def test_create_tenant_success(self, tenant_service, mock_tenant):
        """测试创建租户成功"""
        # 模拟租户编码不存在
        tenant_service.tenant_repo.exists_by_code = Mock(return_value=False)
        # 模拟租户名称不存在
        tenant_service.tenant_repo.exists_by_name = Mock(return_value=False)
        # 模拟创建租户
        tenant_service.tenant_repo.create = Mock(return_value=mock_tenant)
        
        # 执行创建租户
        tenant_data = {
            "name": "测试租户",
            "code": "test_tenant"
        }
        result = tenant_service.create_tenant(tenant_data)
        
        # 验证结果
        assert result.id == "test_tenant_id"
        assert result.name == "测试租户"
        tenant_service.tenant_repo.create.assert_called_once()
    
    def test_create_tenant_name_empty(self, tenant_service):
        """测试创建租户（名称为空）"""
        # 执行创建租户并验证异常
        tenant_data = {
            "name": "",
            "code": "test_tenant"
        }
        with pytest.raises(ValueError, match="租户名称不能为空"):
            tenant_service.create_tenant(tenant_data)
    
    def test_create_tenant_code_empty(self, tenant_service):
        """测试创建租户（编码为空）"""
        # 执行创建租户并验证异常
        tenant_data = {
            "name": "测试租户",
            "code": ""
        }
        with pytest.raises(ValueError, match="租户编码不能为空"):
            tenant_service.create_tenant(tenant_data)
    
    def test_create_tenant_code_exists(self, tenant_service):
        """测试创建租户（编码已存在）"""
        # 模拟租户编码已存在
        tenant_service.tenant_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建租户并验证异常
        tenant_data = {
            "name": "测试租户",
            "code": "existing_code"
        }
        with pytest.raises(ValueError, match="租户编码已存在"):
            tenant_service.create_tenant(tenant_data)
    
    def test_create_tenant_name_exists(self, tenant_service):
        """测试创建租户（名称已存在）"""
        # 模拟租户编码不存在
        tenant_service.tenant_repo.exists_by_code = Mock(return_value=False)
        # 模拟租户名称已存在
        tenant_service.tenant_repo.exists_by_name = Mock(return_value=True)
        
        # 执行创建租户并验证异常
        tenant_data = {
            "name": "existing_name",
            "code": "test_tenant"
        }
        with pytest.raises(ValueError, match="租户名称已存在"):
            tenant_service.create_tenant(tenant_data)
    
    def test_get_tenant_success(self, tenant_service, mock_tenant):
        """测试获取租户成功"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 执行查询
        result = tenant_service.get_tenant("test_tenant_id")
        
        # 验证结果
        assert result.id == "test_tenant_id"
        tenant_service.tenant_repo.get_by_id.assert_called_once_with("test_tenant_id")
    
    def test_get_tenant_not_found(self, tenant_service):
        """测试获取租户失败"""
        # 模拟查询租户返回None
        tenant_service.tenant_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = tenant_service.get_tenant("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_update_tenant_success(self, tenant_service, mock_tenant):
        """测试更新租户成功"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 模拟租户名称不存在
        tenant_service.tenant_repo.exists_by_name = Mock(return_value=False)
        # 模拟更新租户
        tenant_service.tenant_repo.update = Mock(return_value=mock_tenant)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = tenant_service.update_tenant("test_tenant_id", update_data)
        
        # 验证结果
        assert result.id == "test_tenant_id"
        tenant_service.tenant_repo.update.assert_called_once()
    
    def test_update_tenant_not_found(self, tenant_service):
        """测试更新租户失败（租户不存在）"""
        # 模拟查询租户返回None
        tenant_service.tenant_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新并验证异常
        update_data = {"description": "更新后的描述"}
        with pytest.raises(ValueError, match="租户不存在"):
            tenant_service.update_tenant("nonexistent_id", update_data)
    
    def test_delete_tenant_success(self, tenant_service, mock_tenant):
        """测试删除租户成功"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 模拟删除租户
        tenant_service.tenant_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = tenant_service.delete_tenant("test_tenant_id")
        
        # 验证结果
        assert result is True
        tenant_service.tenant_repo.delete.assert_called_once_with("test_tenant_id")
    
    def test_delete_tenant_has_users(self, tenant_service, mock_tenant):
        """测试删除租户失败（有用户）"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 设置有用户
        mock_tenant.users = [Mock()]
        
        # 执行删除并验证异常
        with pytest.raises(ValueError, match="该租户下存在用户"):
            tenant_service.delete_tenant("test_tenant_id")
    
    def test_delete_tenant_has_departments(self, tenant_service, mock_tenant):
        """测试删除租户失败（有部门）"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 设置有部门
        mock_tenant.departments = [Mock()]
        
        # 执行删除并验证异常
        with pytest.raises(ValueError, match="该租户下存在部门"):
            tenant_service.delete_tenant("test_tenant_id")
    
    def test_list_tenants_success(self, tenant_service, mock_tenant):
        """测试获取租户列表成功"""
        # 模拟查询租户列表
        tenant_service.tenant_repo.get_all = Mock(return_value=[mock_tenant])
        tenant_service.tenant_repo.count_all = Mock(return_value=1)
        
        # 执行查询
        result = tenant_service.list_tenants()
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_check_quota_users(self, tenant_service, mock_tenant):
        """测试检查用户配额"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 执行检查
        result = tenant_service.check_quota("test_tenant_id", "users")
        
        # 验证结果
        assert result["used"] == 10
        assert result["max"] == 50
        assert result["available"] == 40
    
    def test_check_quota_departments(self, tenant_service, mock_tenant):
        """测试检查部门配额"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 执行检查
        result = tenant_service.check_quota("test_tenant_id", "departments")
        
        # 验证结果
        assert result["used"] == 5
        assert result["max"] == 20
        assert result["available"] == 15
    
    def test_get_package_info_success(self, tenant_service):
        """测试获取套餐信息成功"""
        # 执行获取
        result = tenant_service.get_package_info("basic")
        
        # 验证结果
        assert result is not None
        assert result["name"] == "基础版"
    
    def test_get_package_info_not_found(self, tenant_service):
        """测试获取套餐信息失败"""
        # 执行获取
        result = tenant_service.get_package_info("nonexistent")
        
        # 验证结果
        assert result is None
    
    def test_get_all_packages(self, tenant_service):
        """测试获取所有套餐信息"""
        # 执行获取
        result = tenant_service.get_all_packages()
        
        # 验证结果
        assert "free" in result
        assert "basic" in result
        assert "professional" in result
        assert "enterprise" in result
    
    def test_update_package_success(self, tenant_service, mock_tenant):
        """测试更新租户套餐成功"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 模拟更新租户
        tenant_service.tenant_repo.update = Mock(return_value=mock_tenant)
        
        # 执行更新
        result = tenant_service.update_package("test_tenant_id", "professional")
        
        # 验证结果
        assert result.id == "test_tenant_id"
    
    def test_update_package_not_found(self, tenant_service):
        """测试更新租户套餐失败（套餐不存在）"""
        # 执行更新并验证异常
        with pytest.raises(ValueError, match="套餐不存在"):
            tenant_service.update_package("test_tenant_id", "nonexistent")
    
    def test_check_expiration_true(self, tenant_service, mock_tenant):
        """测试检查租户过期（已过期）"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 设置已过期
        mock_tenant.is_expired = Mock(return_value=True)
        
        # 执行检查
        result = tenant_service.check_expiration("test_tenant_id")
        
        # 验证结果
        assert result is True
    
    def test_check_expiration_false(self, tenant_service, mock_tenant):
        """测试检查租户过期（未过期）"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        
        # 执行检查
        result = tenant_service.check_expiration("test_tenant_id")
        
        # 验证结果
        assert result is False
    
    def test_renew_tenant_success(self, tenant_service, mock_tenant):
        """测试续费租户成功"""
        # 模拟查询租户
        tenant_service.tenant_repo.get_by_id = Mock(return_value=mock_tenant)
        # 模拟更新租户
        tenant_service.tenant_repo.update = Mock(return_value=mock_tenant)
        
        # 执行续费
        result = tenant_service.renew_tenant("test_tenant_id", days=365)
        
        # 验证结果
        assert result.id == "test_tenant_id"
        assert result.status == "active"
    
    def test_renew_tenant_not_found(self, tenant_service):
        """测试续费租户失败（租户不存在）"""
        # 模拟查询租户返回None
        tenant_service.tenant_repo.get_by_id = Mock(return_value=None)
        
        # 执行续费并验证异常
        with pytest.raises(ValueError, match="租户不存在"):
            tenant_service.renew_tenant("nonexistent_id", days=365)