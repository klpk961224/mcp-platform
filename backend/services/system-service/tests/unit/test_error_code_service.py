# -*- coding: utf-8 -*-
"""
ErrorCodeService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 创建閿欒鐮?2. 鑾峰彇閿欒鐮?3. 更新閿欒鐮?4. 删除閿欒鐮?5. 鑾峰彇閿欒鐮佸垪琛?6. 鎸夋ā鍧楄幏鍙栭敊璇爜
7. 鎸夌骇鍒幏鍙栭敊璇爜
8. 鎼滅储閿欒鐮?9. 鑾峰彇缁熻淇℃伅
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.error_code_service import ErrorCodeService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_error_code():
    """妯℃嫙閿欒鐮佸璞?""
    error_code = Mock()
    error_code.id = "test_error_code_id"
    error_code.code = "ERR001"
    error_code.message = "绯荤粺閿欒"
    error_code.level = "error"
    error_code.module = "system"
    error_code.description = "绯荤粺鍐呴儴閿欒"
    error_code.status = "active"
    error_code.created_at = datetime(2026, 1, 15)
    error_code.updated_at = datetime(2026, 1, 15)
    return error_code


@pytest.fixture
def error_code_service(mock_db):
    """创建ErrorCodeService瀹炰緥"""
    return ErrorCodeService(mock_db)


class TestErrorCodeService:
    """ErrorCodeService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯ErrorCodeService鍒濆鍖?""
        service = ErrorCodeService(mock_db)
        assert service.db == mock_db
        assert service.repository is not None
    
    def test_get_error_code_by_id_success(self, error_code_service, mock_error_code):
        """娴嬭瘯根据ID鑾峰彇閿欒鐮佹垚鍔?""
        # 妯℃嫙查询閿欒鐮?        error_code_service.repository.get_by_id = Mock(return_value=mock_error_code)
        
        # 鎵ц查询
        result = error_code_service.get_error_code_by_id("test_error_code_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_error_code_id"
        assert result["code"] == "ERR001"
    
    def test_get_error_code_by_id_not_found(self, error_code_service):
        """娴嬭瘯根据ID鑾峰彇閿欒鐮佸け璐?""
        # 妯℃嫙查询閿欒鐮佽繑鍥濶one
        error_code_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц查询
        result = error_code_service.get_error_code_by_id("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_error_code_by_code_success(self, error_code_service, mock_error_code):
        """娴嬭瘯根据閿欒鐮佽幏鍙栨垚鍔?""
        # 妯℃嫙查询閿欒鐮?        error_code_service.repository.get_by_code = Mock(return_value=mock_error_code)
        
        # 鎵ц查询
        result = error_code_service.get_error_code_by_code("ERR001")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["code"] == "ERR001"
    
    def test_get_all_error_codes_success(self, error_code_service, mock_error_code):
        """娴嬭瘯鑾峰彇鎵€鏈夐敊璇爜鎴愬姛"""
        # 妯℃嫙查询閿欒鐮佸垪琛?        error_code_service.repository.get_all = Mock(return_value=[mock_error_code])
        error_code_service.repository.count = Mock(return_value=1)
        
        # 鎵ц查询
        result = error_code_service.get_all_error_codes()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["code"] == "ERR001"
    
    def test_get_error_codes_by_module_success(self, error_code_service, mock_error_code):
        """娴嬭瘯鎸夋ā鍧楄幏鍙栭敊璇爜鎴愬姛"""
        # 妯℃嫙查询閿欒鐮佸垪琛?        error_code_service.repository.get_by_module = Mock(return_value=[mock_error_code])
        error_code_service.repository.count_by_module = Mock(return_value=1)
        
        # 鎵ц查询
        result = error_code_service.get_error_codes_by_module("system")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["module"] == "system"
    
    def test_get_error_codes_by_level_success(self, error_code_service, mock_error_code):
        """娴嬭瘯鎸夌骇鍒幏鍙栭敊璇爜鎴愬姛"""
        # 妯℃嫙查询閿欒鐮佸垪琛?        error_code_service.repository.get_by_level = Mock(return_value=[mock_error_code])
        error_code_service.repository.count_by_level = Mock(return_value=1)
        
        # 鎵ц查询
        result = error_code_service.get_error_codes_by_level("error")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert result["items"][0]["level"] == "error"
    
    def test_search_error_codes_success(self, error_code_service, mock_error_code):
        """娴嬭瘯鎼滅储閿欒鐮佹垚鍔?""
        # 妯℃嫙鎼滅储閿欒鐮?        error_code_service.repository.search = Mock(return_value=([mock_error_code], 1))
        
        # 鎵ц鎼滅储
        result = error_code_service.search_error_codes({"module": "system"})
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 1
        assert len(result["items"]) == 1
    
    def test_create_error_code_success(self, error_code_service, mock_error_code):
        """娴嬭瘯创建閿欒鐮佹垚鍔?""
        # 妯℃嫙閿欒鐮佷笉瀛樺湪
        error_code_service.repository.get_by_code = Mock(return_value=None)
        # 妯℃嫙创建閿欒鐮?        error_code_service.repository.create = Mock(return_value=mock_error_code)
        
        # 鎵ц创建閿欒鐮?        result = error_code_service.create_error_code(
            code="ERR001",
            message="绯荤粺閿欒",
            module="system",
            level="error"
        )
        
        # 楠岃瘉缁撴灉
        assert result["code"] == "ERR001"
        assert result["message"] == "绯荤粺閿欒"
        assert result["level"] == "error"
        assert result["module"] == "system"
        error_code_service.repository.create.assert_called_once()
    
    def test_create_error_code_code_exists(self, error_code_service, mock_error_code):
        """娴嬭瘯创建閿欒鐮侊紙閿欒鐮佸凡瀛樺湪锛?""
        # 妯℃嫙閿欒鐮佸凡瀛樺湪
        error_code_service.repository.get_by_code = Mock(return_value=mock_error_code)
        
        # 鎵ц创建閿欒鐮佸苟楠岃瘉寮傚父
        with pytest.raises(ValueError, match="閿欒鐮?ERR001 宸插瓨鍦?):
            error_code_service.create_error_code(
                code="ERR001",
                message="绯荤粺閿欒",
                module="system"
            )
    
    def test_update_error_code_success(self, error_code_service, mock_error_code):
        """娴嬭瘯更新閿欒鐮佹垚鍔?""
        # 妯℃嫙查询閿欒鐮?        error_code_service.repository.get_by_id = Mock(return_value=mock_error_code)
        # 妯℃嫙更新閿欒鐮?        error_code_service.repository.update = Mock(return_value=mock_error_code)
        
        # 鎵ц更新
        result = error_code_service.update_error_code(
            "test_error_code_id",
            message="更新鍚庣殑閿欒淇℃伅"
        )
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result["id"] == "test_error_code_id"
        error_code_service.repository.update.assert_called_once()
    
    def test_update_error_code_not_found(self, error_code_service):
        """娴嬭瘯更新閿欒鐮佸け璐ワ紙閿欒鐮佷笉瀛樺湪锛?""
        # 妯℃嫙查询閿欒鐮佽繑鍥濶one
        error_code_service.repository.get_by_id = Mock(return_value=None)
        
        # 鎵ц更新
        result = error_code_service.update_error_code(
            "nonexistent_id",
            message="更新鍚庣殑閿欒淇℃伅"
        )
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_delete_error_code_success(self, error_code_service):
        """娴嬭瘯删除閿欒鐮佹垚鍔?""
        # 妯℃嫙删除閿欒鐮?        error_code_service.repository.delete = Mock(return_value=True)
        
        # 鎵ц删除
        result = error_code_service.delete_error_code("test_error_code_id")
        
        # 楠岃瘉缁撴灉
        assert result is True
        error_code_service.repository.delete.assert_called_once_with("test_error_code_id")
    
    def test_get_statistics_success(self, error_code_service):
        """娴嬭瘯鑾峰彇缁熻淇℃伅鎴愬姛"""
        # 妯℃嫙缁熻
        error_code_service.repository.count = Mock(return_value=10)
        error_code_service.repository.count_by_level = Mock(return_value=5)
        error_code_service.repository.search = Mock(return_value=([], 5))
        
        # 鎵ц鑾峰彇缁熻
        result = error_code_service.get_statistics()
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 10
        assert "by_level" in result
        assert "by_status" in result
