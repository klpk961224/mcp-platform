# -*- coding: utf-8 -*-
"""
RegionService单元测试

测试内容：
1. 创建地区
2. 获取地区
3. 更新地区
4. 删除地区
5. 获取地区列表
6. 获取子地区
7. 获取地区树
8. 搜索地区
9. 获取统计信息
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.region_service import RegionService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_region():
    """模拟地区对象"""
    region = Mock()
    region.id = "test_region_id"
    region.name = "北京市"
    region.code = "110000"
    region.level = "province"
    region.parent_id = None
    region.sort_order = 0
    region.status = "active"
    region.created_at = datetime(2026, 1, 15)
    region.updated_at = datetime(2026, 1, 15)
    return region


@pytest.fixture
def region_service(mock_db):
    """创建RegionService实例"""
    return RegionService(mock_db)


class TestRegionService:
    """RegionService测试类"""
    
    def test_init(self, mock_db):
        """测试RegionService初始化"""
        service = RegionService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_region_by_id_success(self, region_service, mock_region):
        """测试根据ID获取地区成功"""
        # 模拟查询地区
        region_service.repository.get_by_id = Mock(return_value=mock_region)
        
        # 执行查询
        result = region_service.get_region_by_id("test_region_id")
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_region_id"
        assert result["name"] == "北京市"
    
    def test_get_region_by_id_not_found(self, region_service):
        """测试根据ID获取地区失败"""
        # 模拟查询地区返回None
        region_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = region_service.get_region_by_id("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_region_by_code_success(self, region_service, mock_region):
        """测试根据地区编码获取成功"""
        # 模拟查询地区
        region_service.repository.get_by_code = Mock(return_value=mock_region)
        
        # 执行查询
        result = region_service.get_region_by_code("110000")
        
        # 验证结果
        assert result is not None
        assert result["code"] == "110000"
    
    def test_get_all_regions_success(self, region_service, mock_region):
        """测试获取所有地区成功"""
        # 模拟查询地区列表
        region_service.repository.get_all = Mock(return_value=[mock_region])
        region_service.repository.count = Mock(return_value=1)
        
        # 执行查询
        result = region_service.get_all_regions()
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["name"] == "北京市"
    
    def test_get_regions_by_level_success(self, region_service, mock_region):
        """测试按级别获取地区成功"""
        # 模拟查询地区列表
        region_service.repository.get_by_level = Mock(return_value=[mock_region])
        region_service.repository.count_by_level = Mock(return_value=1)
        
        # 执行查询
        result = region_service.get_regions_by_level("province")
        
        # 验证结果
        assert result["total"] == 1
        assert result["items"][0]["level"] == "province"
    
    def test_get_regions_by_parent_success(self, region_service, mock_region):
        """测试按父级ID获取子地区成功"""
        # 模拟查询地区列表
        region_service.repository.get_by_parent_id = Mock(return_value=[mock_region])
        region_service.repository.count_by_parent = Mock(return_value=1)
        
        # 执行查询
        result = region_service.get_regions_by_parent("parent_id")
        
        # 验证结果
        assert result["total"] == 1
    
    def test_get_children_success(self, region_service, mock_region):
        """测试获取子地区成功"""
        # 模拟查询子地区
        region_service.repository.get_children = Mock(return_value=[mock_region])
        region_service.repository.count_by_parent = Mock(return_value=1)
        
        # 执行查询
        result = region_service.get_children("test_region_id")
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_get_all_children_success(self, region_service, mock_region):
        """测试获取所有子地区（递归）成功"""
        # 模拟查询所有子地区
        region_service.repository.get_all_children = Mock(return_value=[mock_region])
        
        # 执行查询
        result = region_service.get_all_children("test_region_id")
        
        # 验证结果
        assert len(result) == 1
        assert result[0]["id"] == "test_region_id"
    
    def test_get_region_tree_success(self, region_service, mock_region):
        """测试获取地区树成功"""
        # 模拟获取地区树
        mock_tree = [{"id": "1", "name": "北京市", "children": [{"id": "2", "name": "朝阳区"}]}]
        region_service.repository.get_tree = Mock(return_value=mock_tree)
        
        # 执行查询
        result = region_service.get_region_tree()
        
        # 验证结果
        assert len(result) == 1
        assert result[0]["name"] == "北京市"
    
    def test_search_regions_success(self, region_service, mock_region):
        """测试搜索地区成功"""
        # 模拟搜索地区
        region_service.repository.search = Mock(return_value=([mock_region], 1))
        
        # 执行搜索
        result = region_service.search_regions({"name": "北京"})
        
        # 验证结果
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_region_success(self, region_service, mock_region):
        """测试创建地区成功"""
        # 模拟地区编码不存在
        region_service.repository.get_by_code = Mock(return_value=None)
        # 模拟创建地区
        region_service.repository.create = Mock(return_value=mock_region)
        
        # 执行创建地区
        result = region_service.create_region(
            name="北京市",
            code="110000",
            level="province"
        )
        
        # 验证结果
        assert result["name"] == "北京市"
        assert result["code"] == "110000"
        assert result["level"] == "province"
        region_service.repository.create.assert_called_once()
    
    def test_create_region_code_exists(self, region_service, mock_region):
        """测试创建地区（地区编码已存在）"""
        # 模拟地区编码已存在
        region_service.repository.get_by_code = Mock(return_value=mock_region)
        
        # 执行创建地区并验证异常
        with pytest.raises(ValueError, match="地区编码 110000 已存在"):
            region_service.create_region(
                name="北京市",
                code="110000",
                level="province"
            )
    
    def test_create_region_parent_not_found(self, region_service):
        """测试创建地区（父级地区不存在）"""
        # 模拟地区编码不存在
        region_service.repository.get_by_code = Mock(return_value=None)
        # 模拟父级地区不存在
        region_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行创建地区并验证异常
        with pytest.raises(ValueError, match="父级地区 nonexistent_id 不存在"):
            region_service.create_region(
                name="朝阳区",
                code="110100",
                level="city",
                parent_id="nonexistent_id"
            )
    
    def test_update_region_success(self, region_service, mock_region):
        """测试更新地区成功"""
        # 模拟查询地区
        region_service.repository.get_by_id = Mock(return_value=mock_region)
        # 模拟更新地区
        region_service.repository.update = Mock(return_value=mock_region)
        
        # 执行更新
        result = region_service.update_region(
            "test_region_id",
            name="更新后的名称"
        )
        
        # 验证结果
        assert result is not None
        assert result["id"] == "test_region_id"
        region_service.repository.update.assert_called_once()
    
    def test_update_region_not_found(self, region_service):
        """测试更新地区失败（地区不存在）"""
        # 模拟查询地区返回None
        region_service.repository.get_by_id = Mock(return_value=None)
        
        # 执行更新
        result = region_service.update_region(
            "nonexistent_id",
            name="更新后的名称"
        )
        
        # 验证结果
        assert result is None
    
    def test_delete_region_success(self, region_service):
        """测试删除地区成功"""
        # 模拟删除地区
        region_service.repository.delete = Mock(return_value=True)
        
        # 执行删除
        result = region_service.delete_region("test_region_id")
        
        # 验证结果
        assert result is True
        region_service.repository.delete.assert_called_once_with("test_region_id")
    
    def test_get_statistics_success(self, region_service):
        """测试获取统计信息成功"""
        # 模拟统计
        region_service.repository.count = Mock(return_value=10)
        region_service.repository.count_by_level = Mock(return_value=5)
        region_service.repository.search = Mock(return_value=([], 5))
        region_service.repository.count_by_parent = Mock(return_value=3)
        
        # 执行获取统计
        result = region_service.get_statistics()
        
        # 验证结果
        assert result["total"] == 10
        assert "by_level" in result
        assert "by_status" in result
        assert result["top_level_count"] == 3