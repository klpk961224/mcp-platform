# -*- coding: utf-8 -*-
"""
DictService单元测试

测试内容：
1. 创建字典
2. 获取字典
3. 更新字典
4. 删除字典
5. 获取字典列表
6. 统计字典数量
7. 创建字典项
8. 获取字典项
9. 更新字典项
10. 删除字典项
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.dict_service import DictService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_dict():
    """模拟字典对象"""
    dict_obj = Mock()
    dict_obj.id = "test_dict_id"
    dict_obj.type = "user_status"
    dict_obj.name = "用户状态"
    dict_obj.description = "用户状态字典"
    dict_obj.status = "active"
    dict_obj.tenant_id = None
    return dict_obj


@pytest.fixture
def mock_dict_item():
    """模拟字典项对象"""
    dict_item = Mock()
    dict_item.id = "test_dict_item_id"
    dict_item.dict_id = "test_dict_id"
    dict_item.label = "正常"
    dict_item.value = "1"
    dict_item.sort_order = 0
    dict_item.status = "active"
    return dict_item


@pytest.fixture
def dict_service(mock_db):
    """创建DictService实例"""
    return DictService(mock_db)


class TestDictService:
    """DictService测试类"""
    
    def test_init(self, mock_db):
        """测试DictService初始化"""
        service = DictService(mock_db)
        assert service.db == mock_db
        assert service.dict_repo is not None
        assert service.dict_item_repo is not None
    
    def test_create_dict_success(self, dict_service, mock_dict):
        """测试创建字典成功"""
        # 模拟字典类型不存在
        dict_service.dict_repo.get_by_type = Mock(return_value=None)
        # 模拟创建字典
        dict_service.dict_repo.create = Mock(return_value=mock_dict)
        
        # 执行创建字典
        dict_data = {
            "type": "user_status",
            "name": "用户状态",
            "description": "用户状态字典"
        }
        result = dict_service.create_dict(dict_data)
        
        # 验证结果
        assert result.id == "test_dict_id"
        assert result.type == "user_status"
        dict_service.dict_repo.create.assert_called_once()
    
    def test_create_dict_type_exists(self, dict_service, mock_dict):
        """测试创建字典（类型已存在）"""
        # 模拟字典类型已存在
        dict_service.dict_repo.get_by_type = Mock(return_value=mock_dict)
        
        # 执行创建字典并验证异常
        dict_data = {
            "type": "existing_type",
            "name": "现有字典"
        }
        with pytest.raises(ValueError, match="字典类型已存在"):
            dict_service.create_dict(dict_data)
    
    def test_get_dict_success(self, dict_service, mock_dict):
        """测试获取字典成功"""
        # 模拟查询字典
        dict_service.dict_repo.get_by_id = Mock(return_value=mock_dict)
        
        # 执行查询
        result = dict_service.get_dict("test_dict_id")
        
        # 验证结果
        assert result.id == "test_dict_id"
        dict_service.dict_repo.get_by_id.assert_called_once_with("test_dict_id")
    
    def test_get_dict_not_found(self, dict_service):
        """测试获取字典失败"""
        # 模拟查询字典返回None
        dict_service.dict_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = dict_service.get_dict("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_dict_by_type_success(self, dict_service, mock_dict):
        """测试根据类型获取字典成功"""
        # 模拟查询字典
        dict_service.dict_repo.get_by_type = Mock(return_value=mock_dict)
        
        # 执行查询
        result = dict_service.get_dict_by_type("user_status")
        
        # 验证结果
        assert result.type == "user_status"
        dict_service.dict_repo.get_by_type.assert_called_once_with("user_status")
    
    def test_update_dict_success(self, dict_service, mock_dict):
        """测试更新字典成功"""
        # 模拟查询字典
        dict_service.dict_repo.get_by_id = Mock(return_value=mock_dict)
        # 模拟更新字典
        dict_service.dict_repo.update = Mock(return_value=mock_dict)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = dict_service.update_dict("test_dict_id", update_data)
        
        # 验证结果
        assert result.id == "test_dict_id"
        dict_service.dict_repo.update.assert_called_once()
    
    def test_update_dict_not_found(self, dict_service):
        """测试更新字典失败（字典不存在）"""
        # 模拟查询字典返回None
        dict_service.dict_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新
        update_data = {"description": "更新后的描述"}
        result = dict_service.update_dict("nonexistent_id", update_data)
        
        # 验证结果
        assert result is None
    
    def test_delete_dict_success(self, dict_service):
        """测试删除字典成功"""
        # 模拟删除字典
        dict_service.dict_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = dict_service.delete_dict("test_dict_id")
        
        # 验证结果
        assert result is True
        dict_service.dict_repo.delete.assert_called_once_with("test_dict_id")
    
    def test_list_dicts_success(self, dict_service, mock_dict):
        """测试获取字典列表成功"""
        # 模拟查询字典列表
        dict_service.dict_repo.get_all = Mock(return_value=[mock_dict])
        
        # 执行查询
        result = dict_service.list_dicts()
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_dict_id"
    
    def test_count_dicts_success(self, dict_service):
        """测试统计字典数量成功"""
        # 模拟统计
        dict_service.dict_repo.count_all = Mock(return_value=10)
        
        # 执行统计
        result = dict_service.count_dicts()
        
        # 验证结果
        assert result == 10
    
    def test_create_dict_item_success(self, dict_service, mock_dict, mock_dict_item):
        """测试创建字典项成功"""
        # 模拟字典存在
        dict_service.dict_repo.get_by_id = Mock(return_value=mock_dict)
        # 模拟创建字典项
        dict_service.dict_item_repo.create = Mock(return_value=mock_dict_item)
        
        # 执行创建字典项
        dict_item_data = {
            "label": "正常",
            "value": "1",
            "sort_order": 0
        }
        result = dict_service.create_dict_item("test_dict_id", dict_item_data)
        
        # 验证结果
        assert result.id == "test_dict_item_id"
        assert result.label == "正常"
        dict_service.dict_item_repo.create.assert_called_once()
    
    def test_create_dict_item_dict_not_found(self, dict_service):
        """测试创建字典项（字典不存在）"""
        # 模拟字典不存在
        dict_service.dict_repo.get_by_id = Mock(return_value=None)
        
        # 执行创建字典项并验证异常
        dict_item_data = {"label": "正常", "value": "1"}
        with pytest.raises(ValueError, match="字典不存在"):
            dict_service.create_dict_item("nonexistent_id", dict_item_data)
    
    def test_get_dict_item_success(self, dict_service, mock_dict_item):
        """测试获取字典项成功"""
        # 模拟查询字典项
        dict_service.dict_item_repo.get_by_id = Mock(return_value=mock_dict_item)
        
        # 执行查询
        result = dict_service.get_dict_item("test_dict_item_id")
        
        # 验证结果
        assert result.id == "test_dict_item_id"
        dict_service.dict_item_repo.get_by_id.assert_called_once_with("test_dict_item_id")
    
    def test_get_dict_items_success(self, dict_service, mock_dict_item):
        """测试获取字典项列表成功"""
        # 模拟查询字典项列表
        dict_service.dict_item_repo.get_by_dict_id = Mock(return_value=[mock_dict_item])
        
        # 执行查询
        result = dict_service.get_dict_items("test_dict_id")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].id == "test_dict_item_id"
    
    def test_get_dict_items_by_type_success(self, dict_service, mock_dict_item):
        """测试根据类型获取字典项列表成功"""
        # 模拟查询字典项列表
        dict_service.dict_item_repo.get_by_dict_type = Mock(return_value=[mock_dict_item])
        
        # 执行查询
        result = dict_service.get_dict_items_by_type("user_status")
        
        # 验证结果
        assert len(result) == 1
    
    def test_update_dict_item_success(self, dict_service, mock_dict_item):
        """测试更新字典项成功"""
        # 模拟查询字典项
        dict_service.dict_item_repo.get_by_id = Mock(return_value=mock_dict_item)
        # 模拟更新字典项
        dict_service.dict_item_repo.update = Mock(return_value=mock_dict_item)
        
        # 执行更新
        update_data = {"label": "更新后的标签"}
        result = dict_service.update_dict_item("test_dict_item_id", update_data)
        
        # 验证结果
        assert result.id == "test_dict_item_id"
        dict_service.dict_item_repo.update.assert_called_once()
    
    def test_update_dict_item_not_found(self, dict_service):
        """测试更新字典项失败（字典项不存在）"""
        # 模拟查询字典项返回None
        dict_service.dict_item_repo.get_by_id = Mock(return_value=None)
        
        # 执行更新
        update_data = {"label": "更新后的标签"}
        result = dict_service.update_dict_item("nonexistent_id", update_data)
        
        # 验证结果
        assert result is None
    
    def test_delete_dict_item_success(self, dict_service):
        """测试删除字典项成功"""
        # 模拟删除字典项
        dict_service.dict_item_repo.delete = Mock(return_value=True)
        
        # 执行删除
        result = dict_service.delete_dict_item("test_dict_item_id")
        
        # 验证结果
        assert result is True
        dict_service.dict_item_repo.delete.assert_called_once_with("test_dict_item_id")
    
    def test_count_dict_items_success(self, dict_service):
        """测试统计字典项数量成功"""
        # 模拟统计
        dict_service.dict_item_repo.count_by_dict = Mock(return_value=5)
        
        # 执行统计
        result = dict_service.count_dict_items("test_dict_id")
        
        # 验证结果
        assert result == 5