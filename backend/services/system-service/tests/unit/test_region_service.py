# -*- coding: utf-8 -*-
"""
RegionService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍒涘缓鍦板尯
2. 鑾峰彇鍦板尯
3. 鏇存柊鍦板尯
4. 鍒犻櫎鍦板尯
5. 鑾峰彇鍦板尯鍒楄〃
6. 鑾峰彇瀛愬湴鍖?7. 鑾峰彇鍦板尯鏍?8. 鎼滅储鍦板尯
9. 鑾峰彇缁熻淇℃伅
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.region_service import RegionService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_region():
    """妯℃嫙鍦板尯瀵硅薄"""
    region = Mock()
    region.id = "test_region_id"
    region.name = "鍖椾含甯?
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
    """鍒涘缓RegionService瀹炰緥"""
    return RegionService(mock_db)


class TestRegionService:
    """RegionService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯RegionService鍒濆鍖?""
        service = RegionService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_region_by_id_success(self, region_service, mock_region):
        """娴嬭瘯鏍规嵁ID鑾峰彇鍦板尯鎴愬姛"""
        # 妯℃嫙鏌ヨ鍦板尯
        region_service.repository.get_by_id = Mock(return_value=mock_region)
        
        # 鎵ц鏌ヨ
        result = region_service.get_region_by_id("test_region_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_region_id"
        assert result["name"] == "鍖椾含甯?
    
    def test_get_region_by_id_not_found(self, region_service):
        """娴嬭瘯鏍规嵁ID鑾峰彇鍦板尯澶辫触"""
        # 妯℃嫙鏌ヨ鍦板尯杩斿洖None
        region_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = region_service.get_region_by_id("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_region_by_code_success(self, region_service, mock_region):
        """娴嬭瘯鏍规嵁鍦板尯缂栫爜鑾峰彇鎴愬姛"""
        # 妯℃嫙鏌ヨ鍦板尯
        region_service.repository.get_by_code = Mock(return_value=mock_region)
        
        # 鎵ц鏌ヨ
        result = region_service.get_region_by_code("110000")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["code"] == "110000"
    
    def test_get_all_regions_success(self, region_service, mock_region):
        """娴嬭瘯鑾峰彇鎵€鏈夊湴鍖烘垚鍔?""
        # 妯℃嫙鏌ヨ鍦板尯鍒楄〃
        region_service.repository.get_all = Mock(return_value=[mock_region])
        region_service.repository.count = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = region_service.get_all_regions()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["name"] == "鍖椾含甯?
    
    def test_get_regions_by_level_success(self, region_service, mock_region):
        """娴嬭瘯鎸夌骇鍒幏鍙栧湴鍖烘垚鍔?""
        # 妯℃嫙鏌ヨ鍦板尯鍒楄〃
        region_service.repository.get_by_level = Mock(return_value=[mock_region])
        region_service.repository.count_by_level = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = region_service.get_regions_by_level("province")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["level"] == "province"
    
    def test_get_regions_by_parent_success(self, region_service, mock_region):
        """娴嬭瘯鎸夌埗绾D鑾峰彇瀛愬湴鍖烘垚鍔?""
        # 妯℃嫙鏌ヨ鍦板尯鍒楄〃
        region_service.repository.get_by_parent_id = Mock(return_value=[mock_region])
        region_service.repository.count_by_parent = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = region_service.get_regions_by_parent("parent_id")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
    
    def test_get_children_success(self, region_service, mock_region):
        """娴嬭瘯鑾峰彇瀛愬湴鍖烘垚鍔?""
        # 妯℃嫙鏌ヨ瀛愬湴鍖?        region_service.repository.get_children = Mock(return_value=[mock_region])
        region_service.repository.count_by_parent = Mock(return_value=1)
        
        # 鎵ц鏌ヨ
        result = region_service.get_children("test_region_id")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_get_all_children_success(self, region_service, mock_region):
        """娴嬭瘯鑾峰彇鎵€鏈夊瓙鍦板尯锛堥€掑綊锛夋垚鍔?""
        # 妯℃嫙鏌ヨ鎵€鏈夊瓙鍦板尯
        region_service.repository.get_all_children = Mock(return_value=[mock_region])
        
        # 鎵ц鏌ヨ
        result = region_service.get_all_children("test_region_id")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0]["id"] == "test_region_id"
    
    def test_get_region_tree_success(self, region_service, mock_region):
        """娴嬭瘯鑾峰彇鍦板尯鏍戞垚鍔?""
        # 妯℃嫙鑾峰彇鍦板尯鏍?        mock_tree = [{"id": "1", "name": "鍖椾含甯?, "children": [{"id": "2", "name": "鏈濋槼鍖?}]}]
        region_service.repository.get_tree = Mock(return_value=mock_tree)
        
        # 鎵ц鏌ヨ
        result = region_service.get_region_tree()
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0]["name"] == "鍖椾含甯?
    
    def test_search_regions_success(self, region_service, mock_region):
        """娴嬭瘯鎼滅储鍦板尯鎴愬姛"""
        # 妯℃嫙鎼滅储鍦板尯
        region_service.repository.search = Mock(return_value=([mock_region], 1))
        
        # 鎵ц鎼滅储
        result = region_service.search_regions({"name": "鍖椾含"})
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_region_success(self, region_service, mock_region):
        """娴嬭瘯鍒涘缓鍦板尯鎴愬姛"""
        # 妯℃嫙鍦板尯缂栫爜涓嶅瓨鍦?        region_service.repository.get_by_code = Mock(return_value=None)
        # 妯℃嫙鍒涘缓鍦板尯
        region_service.repository.create = Mock(return_value=mock_region)
        
        # 鎵ц鍒涘缓鍦板尯
        result = region_service.create_region(
            name="鍖椾含甯?,
            code="110000",
            level="province"
        )
        
        # 楠岃瘉缁撴灉
        assert result["name"] == "鍖椾含甯?
        assert result["code"] == "110000"
        assert result["level"] == "province"
        region_service.repository.create.assert_called_once()
    
    def test_create_region_code_exists(self, region_service, mock_region):
        """娴嬭瘯鍒涘缓鍦板尯锛堝湴鍖虹紪鐮佸凡瀛樺湪锛?""
        # 妯℃嫙鍦板尯缂栫爜宸插瓨鍦?        region_service.repository.get_by_code = Mock(return_value=mock_region)
        
        # 鎵ц鍒涘缓鍦板尯骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="鍦板尯缂栫爜 110000 宸插瓨鍦?):
            region_service.create_region(
                name="鍖椾含甯?,
                code="110000",
                level="province"
            )
    
    def test_create_region_parent_not_found(self, region_service):
        """娴嬭瘯鍒涘缓鍦板尯锛堢埗绾у湴鍖轰笉瀛樺湪锛?""
        # 妯℃嫙鍦板尯缂栫爜涓嶅瓨鍦?        region_service.repository.get_by_code = Mock(return_value=None)
        # 妯℃嫙鐖剁骇鍦板尯涓嶅瓨鍦?        region_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鍒涘缓鍦板尯骞堕獙璇佸紓甯?        with pytest.raises(ValueError, match="鐖剁骇鍦板尯 nonexistent_id 涓嶅瓨鍦?):
            region_service.create_region(
                name="鏈濋槼鍖?,
                code="110100",
                level="city",
                parent_id="nonexistent_id"
            )
    
    def test_update_region_success(self, region_service, mock_region):
        """娴嬭瘯鏇存柊鍦板尯鎴愬姛"""
        # 妯℃嫙鏌ヨ鍦板尯
        region_service.repository.get_by_id = Mock(return_value=mock_region)
        # 妯℃嫙鏇存柊鍦板尯
        region_service.repository.update = Mock(return_value=mock_region)
        
        # 鎵ц鏇存柊
        result = region_service.update_region(
            "test_region_id",
            name="鏇存柊鍚庣殑鍚嶇О"
        )
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_region_id"
        region_service.repository.update.assert_called_once()
    
    def test_update_region_not_found(self, region_service):
        """娴嬭瘯鏇存柊鍦板尯澶辫触锛堝湴鍖轰笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ鍦板尯杩斿洖None
        region_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏇存柊
        result = region_service.update_region(
            "nonexistent_id",
            name="鏇存柊鍚庣殑鍚嶇О"
        )
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_region_success(self, region_service):
        """娴嬭瘯鍒犻櫎鍦板尯鎴愬姛"""
        # 妯℃嫙鍒犻櫎鍦板尯
        region_service.repository.delete = Mock(return_value=True)
        
        # 鎵ц鍒犻櫎
        result = region_service.delete_region("test_region_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        region_service.repository.delete.assert_called_once_with("test_region_id")
    
    def test_get_statistics_success(self, region_service):
        """娴嬭瘯鑾峰彇缁熻淇℃伅鎴愬姛"""
        # 妯℃嫙缁熻
        region_service.repository.count = Mock(return_value=10)
        region_service.repository.count_by_level = Mock(return_value=5)
        region_service.repository.search = Mock(return_value=([], 5))
        region_service.repository.count_by_parent = Mock(return_value=3)
        
        # 鎵ц鑾峰彇缁熻
        result = region_service.get_statistics()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 10
        assert "by_level" in result
        assert "by_status" in result
        assert result["top_level_count"] == 3
