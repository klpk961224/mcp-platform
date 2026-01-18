# -*- coding: utf-8 -*-
"""
DataScopeService单元测试

测试内容：
1. 创建数据范围
2. 获取数据范围
3. 获取数据范围列表
4. 设置用户数据范围
5. 获取用户数据范围
6. 检查数据范围权限
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.data_scope_service import DataScopeService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_data_scope():
    """模拟数据范围对象"""
    data_scope = Mock()
    data_scope.id = "test_data_scope_id"
    data_scope.name = "本部门数据"
    data_scope.code = "department"
    data_scope.type = "custom"
    data_scope.description = "本部门数据范围"
    data_scope.status = "active"
    return data_scope


@pytest.fixture
def mock_user_data_scope():
    """模拟用户数据范围对象"""
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
    """创建DataScopeService实例"""
    return DataScopeService(mock_db)


class TestDataScopeService:
    """DataScopeService测试类"""
    
    def test_init(self, mock_db):
        """测试DataScopeService初始化"""
        service = DataScopeService(mock_db)
        assert service.db == mock_db
        assert service.data_scope_repo is not None
        assert service.user_data_scope_repo is not None
    
    def test_create_data_scope_success(self, data_scope_service, mock_data_scope):
        """测试创建数据范围成功"""
        # 模拟数据范围编码不存在
        data_scope_service.data_scope_repo.exists_by_code = Mock(return_value=False)
        # 模拟创建数据范围
        data_scope_service.data_scope_repo.create = Mock(return_value=mock_data_scope)
        
        # 执行创建数据范围
        data_scope_data = {
            "name": "本部门数据",
            "code": "department",
            "type": "custom"
        }
        result = data_scope_service.create_data_scope(data_scope_data)
        
        # 验证结果
        assert result.id == "test_data_scope_id"
        assert result.name == "本部门数据"
        data_scope_service.data_scope_repo.create.assert_called_once()
    
    def test_create_data_scope_code_exists(self, data_scope_service):
        """测试创建数据范围（编码已存在）"""
        # 模拟数据范围编码已存在
        data_scope_service.data_scope_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建数据范围并验证异常
        data_scope_data = {
            "name": "本部门数据",
            "code": "existing_code"
        }
        with pytest.raises(ValueError, match="数据范围编码已存在"):
            data_scope_service.create_data_scope(data_scope_data)
    
    def test_get_data_scope_success(self, data_scope_service, mock_data_scope):
        """测试获取数据范围成功"""
        # 模拟查询数据范围
        data_scope_service.data_scope_repo.get_by_id = Mock(return_value=mock_data_scope)
        
        # 执行查询
        result = data_scope_service.get_data_scope("test_data_scope_id")
        
        # 验证结果
        assert result.id == "test_data_scope_id"
        data_scope_service.data_scope_repo.get_by_id.assert_called_once_with("test_data_scope_id")
    
    def test_get_data_scope_not_found(self, data_scope_service):
        """测试获取数据范围失败"""
        # 模拟查询数据范围返回None
        data_scope_service.data_scope_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = data_scope_service.get_data_scope("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_data_scope_by_code_success(self, data_scope_service, mock_data_scope):
        """测试根据编码获取数据范围成功"""
        # 模拟查询数据范围
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=mock_data_scope)
        
        # 执行查询
        result = data_scope_service.get_data_scope_by_code("department")
        
        # 验证结果
        assert result.code == "department"
        data_scope_service.data_scope_repo.get_by_code.assert_called_once_with("department")
    
    def test_list_data_scopes_success(self, data_scope_service, mock_data_scope):
        """测试获取数据范围列表成功"""
        # 模拟查询数据范围列表
        data_scope_service.data_scope_repo.get_all = Mock(return_value=[mock_data_scope])
        
        # 执行查询
        result = data_scope_service.list_data_scopes()
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_data_scope_id"
    
    def test_set_user_data_scope_create(self, data_scope_service, mock_data_scope, mock_user_data_scope):
        """测试设置用户数据范围（创建）"""
        # 模拟查询数据范围
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=mock_data_scope)
        # 模拟查询用户数据范围返回None
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=None)
        # 模拟创建用户数据范围
        data_scope_service.user_data_scope_repo.create = Mock(return_value=mock_user_data_scope)
        
        # 执行设置
        result = data_scope_service.set_user_data_scope("user_001", "user", "department")
        
        # 验证结果
        assert result.id == "test_user_data_scope_id"
        data_scope_service.user_data_scope_repo.create.assert_called_once()
    
    def test_set_user_data_scope_update(self, data_scope_service, mock_data_scope, mock_user_data_scope):
        """测试设置用户数据范围（更新）"""
        # 模拟查询数据范围
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=mock_data_scope)
        # 模拟查询用户数据范围
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=mock_user_data_scope)
        # 模拟更新用户数据范围
        data_scope_service.user_data_scope_repo.update = Mock(return_value=mock_user_data_scope)
        
        # 执行设置
        result = data_scope_service.set_user_data_scope("user_001", "user", "department")
        
        # 验证结果
        assert result.id == "test_user_data_scope_id"
        data_scope_service.user_data_scope_repo.update.assert_called_once()
    
    def test_set_user_data_scope_not_found(self, data_scope_service):
        """测试设置用户数据范围（数据范围不存在）"""
        # 模拟查询数据范围返回None
        data_scope_service.data_scope_repo.get_by_code = Mock(return_value=None)
        
        # 执行设置并验证异常
        with pytest.raises(ValueError, match="数据范围不存在"):
            data_scope_service.set_user_data_scope("user_001", "user", "nonexistent")
    
    def test_get_user_data_scope_success(self, data_scope_service, mock_user_data_scope):
        """测试获取用户数据范围成功"""
        # 模拟查询用户数据范围
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=mock_user_data_scope)
        
        # 执行查询
        result = data_scope_service.get_user_data_scope("user_001", "user")
        
        # 验证结果
        assert result.id == "test_user_data_scope_id"
        data_scope_service.user_data_scope_repo.get_by_user_module.assert_called_once()
    
    def test_check_data_scope_all(self, data_scope_service, mock_user_data_scope):
        """测试检查数据范围权限（全部数据）"""
        # 模拟查询用户数据范围
        mock_user_data_scope.data_scope.code = "all"
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=mock_user_data_scope)
        
        # 执行检查
        result = data_scope_service.check_data_scope("user_001", "user", "target_001")
        
        # 验证结果
        assert result is True
    
    def test_check_data_scope_self_true(self, data_scope_service, mock_user_data_scope):
        """测试检查数据范围权限（仅本人数据，有权限）"""
        # 模拟查询用户数据范围返回None（默认为self）
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=None)
        
        # 执行检查（目标是本人）
        result = data_scope_service.check_data_scope("user_001", "user", "user_001")
        
        # 验证结果
        assert result is True
    
    def test_check_data_scope_self_false(self, data_scope_service, mock_user_data_scope):
        """测试检查数据范围权限（仅本人数据，无权限）"""
        # 模拟查询用户数据范围返回None（默认为self）
        data_scope_service.user_data_scope_repo.get_by_user_module = Mock(return_value=None)
        
        # 执行检查（目标不是本人）
        result = data_scope_service.check_data_scope("user_001", "user", "user_002")
        
        # 验证结果
        assert result is False