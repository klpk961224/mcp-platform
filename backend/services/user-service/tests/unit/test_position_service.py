# -*- coding: utf-8 -*-
"""
PositionService单元测试

测试内容：
1. 创建岗位
2. 获取岗位
3. 更新岗位
4. 删除岗位
5. 获取岗位列表
6. 统计岗位数量
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.position_service import PositionService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_position():
    """模拟岗位对象"""
    position = Mock()
    position.id = "test_position_id"
    position.name = "开发工程师"
    position.code = "developer"
    position.level = 1
    position.description = "开发工程师岗位"
    position.tenant_id = "default"
    position.status = "active"
    return position


@pytest.fixture
def position_service(mock_db):
    """创建PositionService实例"""
    return PositionService(mock_db)


class TestPositionService:
    """PositionService测试类"""
    
    def test_init(self, mock_db):
        """测试PositionService初始化"""
        service = PositionService(mock_db)
        assert service.db == mock_db
        assert service.position_repo is not None
    
    def test_create_position_success(self, position_service, mock_position):
        """测试创建岗位成功"""
        # 模拟岗位编码不存在
        position_service.position_repo.exists_by_code = Mock(return_value=False)
        # 模拟创建岗位
        position_service.position_repo.create = Mock(return_value=mock_position)
        
        # 执行创建岗位
        position_data = {
            "name": "开发工程师",
            "code": "developer",
            "tenant_id": "default"
        }
        result = position_service.create_position(position_data)
        
        # 验证结果
        assert result.id == "test_position_id"
        assert result.name == "开发工程师"
        position_service.position_repo.create.assert_called_once()
    
    def test_create_position_code_exists(self, position_service):
        """测试创建岗位（编码已存在）"""
        # 模拟岗位编码已存在
        position_service.position_repo.exists_by_code = Mock(return_value=True)
        
        # 执行创建岗位并验证异常
        position_data = {
            "name": "开发工程师",
            "code": "existing_code",
            "tenant_id": "default"
        }
        with pytest.raises(ValueError, match="岗位编码已存在"):
            position_service.create_position(position_data)
    
    def test_get_position_success(self, position_service, mock_position):
        """测试获取岗位成功"""
        # 模拟查询岗位
        position_service.position_repo.get_by_id = Mock(return_value=mock_position)
        
        # 执行查询
        result = position_service.get_position("test_position_id")
        
        # 验证结果
        assert result.id == "test_position_id"
        position_service.position_repo.get_by_id.assert_called_once_with("test_position_id")
    
    def test_get_position_not_found(self, position_service):
        """测试获取岗位失败"""
        # 模拟查询岗位返回None
        position_service.position_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = position_service.get_position("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_position_by_code_success(self, position_service, mock_position):
        """测试根据编码获取岗位成功"""
        # 模拟查询岗位
        position_service.position_repo.get_by_code = Mock(return_value=mock_position)
        
        # 执行查询
        result = position_service.get_position_by_code("developer")
        
        # 验证结果
        assert result.code == "developer"
        position_service.position_repo.get_by_code.assert_called_once_with("developer")
    
    def test_update_position_success(self, position_service, mock_position):
        """测试更新岗位成功"""
        # 模拟查询岗位
        position_service.position_repo.get_by_id = Mock(return_value=mock_position)
        # 模拟更新岗位
        position_service.position_repo.update = Mock(return_value=mock_position)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = position_service.update_position("test_position_id", update_data)
        
        # 验证结果
        assert result.id == "test_position_id"
        position_service.position_repo.update.assert_called_once()
    
    def test_update_position_not_found(self, position_service):
        """测试更新岗位失败（岗位不存在）"""
        # 模拟查询岗位返回None
        position_service.position_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = position_service.update_position("nonexistent_id", update_data)
        
        # 验证结果
        assert result is None
    
    def test_delete_position_success(self, position_service):
        """测试删除岗位成功"""
        # 模拟删除岗位
        position_service.position_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = position_service.delete_position("test_position_id")
        
        # 验证结果
        assert result is True
        position_service.position_repo.delete.assert_called_once_with("test_position_id")
    
    def test_list_positions_success(self, position_service, mock_position):
        """测试获取岗位列表成功"""
        # 模拟查询岗位列表
        position_service.position_repo.get_by_tenant_id = Mock(return_value=[mock_position])
        
        # 执行查询
        result = position_service.list_positions(tenant_id="default")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_position_id"
    
    def test_count_positions_success(self, position_service):
        """测试统计岗位数量成功"""
        # 模拟统计
        position_service.position_repo.count_by_tenant = Mock(return_value=10)
        
        # 执行统计
        result = position_service.count_positions(tenant_id="default")
        
        # 验证结果
        assert result == 10
    
    def test_count_positions_all(self, position_service):
        """测试统计所有岗位数量成功"""
        # 模拟统计
        position_service.position_repo.count_all = Mock(return_value=50)
        
        # 执行统计
        result = position_service.count_positions()
        
        # 验证结果
        assert result == 50