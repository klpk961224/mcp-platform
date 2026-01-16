# -*- coding: utf-8 -*-
"""
ErrorCodeService单元测试

测试内容：
1. 创建错误码
2. 获取错误码
3. 更新错误码
4. 删除错误码
5. 获取错误码列表
6. 按模块获取错误码
7. 按级别获取错误码
8. 搜索错误码
9. 获取统计信息
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.error_code_service import ErrorCodeService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_error_code():
    """模拟错误码对象"""
    error_code = Mock()
    error_code.id = "test_error_code_id"
    error_code.code = "ERR001"
    error_code.message = "系统错误"
    error_code.level = "error"
    error_code.module = "system"
    error_code.description = "系统内部错误"
    error_code.status = "active"
    error_code.created_at = datetime(2026, 1, 15)
    error_code.updated_at = datetime(2026, 1, 15)
    return error_code


@pytest.fixture
def error_code_service(mock_db):
    """创建ErrorCodeService实例"""
    return ErrorCodeService(mock_db)


class TestErrorCodeService:
    """ErrorCodeService测试类"""
    
    def test_init(self, mock_db):
        """测试ErrorCodeService初始化"""
        service = ErrorCodeService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_error_code_by_id_success(self, error_code_service, mock_error_code):
        """测试根据ID获取错误码成功"""
        # 模拟查询错误码
        error_code_service.repository.get_by_id = Mock(return_value=mock_error_code)
        
        # 执行查询
        result = error_code_service.get_error_code_by_id("test_error_code_id")
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_error_code_id"
        assert result["code"] == "ERR001"
    
    def test_get_error_code_by_id_not_found(self, error_code_service):
        """测试根据ID获取错误码失败"""
        # 模拟查询错误码返回None
        error_code_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = error_code_service.get_error_code_by_id("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_error_code_by_code_success(self, error_code_service, mock_error_code):
        """测试根据错误码获取成功"""
        # 模拟查询错误码
        error_code_service.repository.get_by_code = Mock(return_value=mock_error_code)
        
        # 执行查询
        result = error_code_service.get_error_code_by_code("ERR001")
        
        # 验证结果
        assert result is not None
        assert result["code"] == "ERR001"
    
    def test_get_all_error_codes_success(self, error_code_service, mock_error_code):
        """测试获取所有错误码成功"""
        # 模拟查询错误码列表
        error_code_service.repository.get_all = Mock(return_value=[mock_error_code])
        error_code_service.repository.count = Mock(return_value=1)
        
        # 执行查询
        result = error_code_service.get_all_error_codes()
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["code"] == "ERR001"
    
    def test_get_error_codes_by_module_success(self, error_code_service, mock_error_code):
        """测试按模块获取错误码成功"""
        # 模拟查询错误码列表
        error_code_service.repository.get_by_module = Mock(return_value=[mock_error_code])
        error_code_service.repository.count_by_module = Mock(return_value=1)
        
        # 执行查询
        result = error_code_service.get_error_codes_by_module("system")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["module"] == "system"
    
    def test_get_error_codes_by_level_success(self, error_code_service, mock_error_code):
        """测试按级别获取错误码成功"""
        # 模拟查询错误码列表
        error_code_service.repository.get_by_level = Mock(return_value=[mock_error_code])
        error_code_service.repository.count_by_level = Mock(return_value=1)
        
        # 执行查询
        result = error_code_service.get_error_codes_by_level("error")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["level"] == "error"
    
    def test_search_error_codes_success(self, error_code_service, mock_error_code):
        """测试搜索错误码成功"""
        # 模拟搜索错误码
        error_code_service.repository.search = Mock(return_value=([mock_error_code], 1))
        
        # 执行搜索
        result = error_code_service.search_error_codes({"module": "system"})
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_error_code_success(self, error_code_service, mock_error_code):
        """测试创建错误码成功"""
        # 模拟错误码不存在
        error_code_service.repository.get_by_code = Mock(return_value=None)
        # 模拟创建错误码
        error_code_service.repository.create = Mock(return_value=mock_error_code)
        
        # 执行创建错误码
        result = error_code_service.create_error_code(
            code="ERR001",
            message="系统错误",
            module="system",
            level="error"
        )
        
        # 验证结果
        assert result["code"] == "ERR001"
        assert result["message"] == "系统错误"
        assert result["level"] == "error"
        assert result["module"] == "system"
        error_code_service.repository.create.assert_called_once()
    
    def test_create_error_code_code_exists(self, error_code_service, mock_error_code):
        """测试创建错误码（错误码已存在）"""
        # 模拟错误码已存在
        error_code_service.repository.get_by_code = Mock(return_value=mock_error_code)
        
        # 执行创建错误码并验证异常
        with pytest.raises(ValueError, match="错误码 ERR001 已存在"):
            error_code_service.create_error_code(
                code="ERR001",
                message="系统错误",
                module="system"
            )
    
    def test_update_error_code_success(self, error_code_service, mock_error_code):
        """测试更新错误码成功"""
        # 模拟查询错误码
        error_code_service.repository.get_by_id = Mock(return_value=mock_error_code)
        # 模拟更新错误码
        error_code_service.repository.update = Mock(return_value=mock_error_code)
        
        # 执行更新
        result = error_code_service.update_error_code(
            "test_error_code_id",
            message="更新后的错误信息"
        )
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_error_code_id"
        error_code_service.repository.update.assert_called_once()
    
    def test_update_error_code_not_found(self, error_code_service):
        """测试更新错误码失败（错误码不存在）"""
        # 模拟查询错误码返回None
        error_code_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行更新
        result = error_code_service.update_error_code(
            "nonexistent_id",
            message="更新后的错误信息"
        )
        
        # 验证结果
        assert result is None
    
    def test_delete_error_code_success(self, error_code_service):
        """测试删除错误码成功"""
        # 模拟删除错误码
        error_code_service.repository.delete = Mock(return_value=True)
        
        # 执行删除
        result = error_code_service.delete_error_code("test_error_code_id")
        
        # 验证结果
        assert result is True
        error_code_service.repository.delete.assert_called_once_with("test_error_code_id")
    
    def test_get_statistics_success(self, error_code_service):
        """测试获取统计信息成功"""
        # 模拟统计
        error_code_service.repository.count = Mock(return_value=10)
        error_code_service.repository.count_by_level = Mock(return_value=5)
        error_code_service.repository.search = Mock(return_value=([], 5))
        
        # 执行获取统计
        result = error_code_service.get_statistics()
        
        # 验证结果
        assert result["total"] == 10
        assert "by_level" in result
        assert "by_status" in result