# -*- coding: utf-8 -*-
"""
WorkflowService鍗曞厓娴嬭瘯

娴嬭瘯鍐呭锛?1. 鍚姩宸ヤ綔娴?2. 鑾峰彇宸ヤ綔娴?3. 鑾峰彇鐢ㄦ埛宸ヤ綔娴?4. 缁堟宸ヤ綔娴?5. 鑾峰彇缁熻淇℃伅
6. 缁熻宸ヤ綔娴佹暟閲?"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.workflow_service import WorkflowService


@pytest.fixture
def mock_db():
    """妯℃嫙鏁版嵁搴撲細璇?""
    return Mock(spec=Session)


@pytest.fixture
def mock_template():
    """妯℃嫙宸ヤ綔娴佹ā鏉垮璞?""
    template = Mock()
    template.id = "test_template_id"
    template.name = "娴嬭瘯宸ヤ綔娴?
    template.definition = '{"nodes": [{"id": "node1", "name": "瀹℃壒鑺傜偣", "type": "approval", "assignee_id": "user_001", "assignee_name": "User_001"}]}'
    template.status = "active"
    template.is_available = Mock(return_value=True)
    template.increment_usage = Mock()
    return template


@pytest.fixture
def mock_workflow():
    """妯℃嫙宸ヤ綔娴佸璞?""
    workflow = Mock()
    workflow.id = "test_workflow_id"
    workflow.tenant_id = "default"
    workflow.name = "娴嬭瘯宸ヤ綔娴?
    workflow.template_id = "test_template_id"
    workflow.initiator_id = "user_001"
    workflow.initiator_name = "User_001"
    workflow.business_data = None
    workflow.variables = None
    workflow.status = "running"
    workflow.terminate = Mock()
    workflow.created_at = datetime(2026, 1, 15)
    workflow.updated_at = datetime(2026, 1, 15)
    return workflow


@pytest.fixture
def workflow_service(mock_db):
    """鍒涘缓WorkflowService瀹炰緥"""
    return WorkflowService(mock_db)


class TestWorkflowService:
    """WorkflowService娴嬭瘯绫?""
    
    def test_init(self, mock_db):
        """娴嬭瘯WorkflowService鍒濆鍖?""
        service = WorkflowService(mock_db)
        assert service.db == mock_db
        assert service.workflow_repo is not None
        assert service.task_repo is not None
        assert service.template_repo is not None
    
    def test_start_workflow_success(self, workflow_service, mock_template, mock_workflow):
        """娴嬭瘯鍚姩宸ヤ綔娴佹垚鍔?""
        # 妯℃嫙鑾峰彇妯℃澘
        workflow_service.template_repo.get_by_id = Mock(return_value=mock_template)
        # 妯℃嫙鏇存柊妯℃澘
        workflow_service.template_repo.update = Mock()
        # 妯℃嫙鍒涘缓宸ヤ綔娴?        workflow_service.workflow_repo.create = Mock(return_value=mock_workflow)
        # 妯℃嫙鍒涘缓浠诲姟
        workflow_service.task_repo.create = Mock()
        
        # 鎵ц鍚姩宸ヤ綔娴?        result = workflow_service.start_workflow(
            template_id="test_template_id",
            initiator_id="user_001",
            initiator_name="User_001",
            tenant_id="default"
        )
        
        # 楠岃瘉缁撴灉
        assert result.id == "test_workflow_id"
        assert result.status == "running"
        workflow_service.workflow_repo.create.assert_called_once()
        workflow_service.task_repo.create.assert_called_once()
    
    def test_start_workflow_template_not_found(self, workflow_service):
        """娴嬭瘯鍚姩宸ヤ綔娴佸け璐ワ紙妯℃澘涓嶅瓨鍦級"""
        # 妯℃嫙鑾峰彇妯℃澘杩斿洖None
        workflow_service.template_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鍚姩宸ヤ綔娴佸苟楠岃瘉寮傚父
        with pytest.raises(ValueError, match="宸ヤ綔娴佹ā鏉夸笉瀛樺湪"):
            workflow_service.start_workflow(
                template_id="nonexistent_id",
                initiator_id="user_001",
                initiator_name="User_001",
                tenant_id="default"
            )
    
    def test_start_workflow_template_not_available(self, workflow_service, mock_template):
        """娴嬭瘯鍚姩宸ヤ綔娴佸け璐ワ紙妯℃澘涓嶅彲鐢級"""
        # 妯℃嫙鑾峰彇妯℃澘
        workflow_service.template_repo.get_by_id = Mock(return_value=mock_template)
        # 妯℃嫙妯℃澘涓嶅彲鐢?        mock_template.is_available = Mock(return_value=False)
        
        # 鎵ц鍚姩宸ヤ綔娴佸苟楠岃瘉寮傚父
        with pytest.raises(ValueError, match="宸ヤ綔娴佹ā鏉夸笉鍙敤"):
            workflow_service.start_workflow(
                template_id="test_template_id",
                initiator_id="user_001",
                initiator_name="User_001",
                tenant_id="default"
            )
    
    def test_get_workflow_success(self, workflow_service, mock_workflow):
        """娴嬭瘯鑾峰彇宸ヤ綔娴佹垚鍔?""
        # 妯℃嫙鏌ヨ宸ヤ綔娴?        workflow_service.workflow_repo.get_by_id = Mock(return_value=mock_workflow)
        
        # 鎵ц鏌ヨ
        result = workflow_service.get_workflow("test_workflow_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result.id == "test_workflow_id"
        workflow_service.workflow_repo.get_by_id.assert_called_once_with("test_workflow_id")
    
    def test_get_workflow_not_found(self, workflow_service):
        """娴嬭瘯鑾峰彇宸ヤ綔娴佸け璐?""
        # 妯℃嫙鏌ヨ宸ヤ綔娴佽繑鍥濶one
        workflow_service.workflow_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц鏌ヨ
        result = workflow_service.get_workflow("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_user_workflows_success(self, workflow_service, mock_workflow):
        """娴嬭瘯鑾峰彇鐢ㄦ埛宸ヤ綔娴佹垚鍔?""
        # 妯℃嫙鏌ヨ宸ヤ綔娴佸垪琛?        workflow_service.workflow_repo.get_user_workflows = Mock(return_value=[mock_workflow])
        
        # 鎵ц鏌ヨ
        result = workflow_service.get_user_workflows("user_001")
        
        # 楠岃瘉缁撴灉
        assert len(result) == 1
        assert result[0].initiator_id == "user_001"
        workflow_service.workflow_repo.get_user_workflows.assert_called_once()
    
    def test_terminate_workflow_success(self, workflow_service, mock_workflow):
        """娴嬭瘯缁堟宸ヤ綔娴佹垚鍔?""
        # 妯℃嫙鏌ヨ宸ヤ綔娴?        workflow_service.workflow_repo.get_by_id = Mock(return_value=mock_workflow)
        # 妯℃嫙鏇存柊宸ヤ綔娴?        workflow_service.workflow_repo.update = Mock(return_value=mock_workflow)
        
        # 鎵ц缁堟
        result = workflow_service.terminate_workflow("test_workflow_id")
        
        # 楠岃瘉缁撴灉
        assert result is not None
        assert result.id == "test_workflow_id"
        mock_workflow.terminate.assert_called_once()
        workflow_service.workflow_repo.update.assert_called_once()
    
    def test_terminate_workflow_not_found(self, workflow_service):
        """娴嬭瘯缁堟宸ヤ綔娴佸け璐ワ紙宸ヤ綔娴佷笉瀛樺湪锛?""
        # 妯℃嫙鏌ヨ宸ヤ綔娴佽繑鍥濶one
        workflow_service.workflow_repo.get_by_id = Mock(return_value=None)
        
        # 鎵ц缁堟
        result = workflow_service.terminate_workflow("nonexistent_id")
        
        # 楠岃瘉缁撴灉
        assert result is None
    
    def test_get_workflow_statistics_success(self, workflow_service):
        """娴嬭瘯鑾峰彇宸ヤ綔娴佺粺璁′俊鎭垚鍔?""
        # 妯℃嫙缁熻
        workflow_service.workflow_repo.count_by_tenant = Mock(side_effect=[10, 2, 6, 2])
        
        # 鎵ц鑾峰彇缁熻
        result = workflow_service.get_workflow_statistics("default")
        
        # 楠岃瘉缁撴灉
        assert result["total"] == 10
        assert result["running"] == 2
        assert result["completed"] == 6
        assert result["terminated"] == 2
        assert result["completion_rate"] == 60.0
    
    def test_count_workflows_success(self, workflow_service):
        """娴嬭瘯缁熻宸ヤ綔娴佹暟閲忔垚鍔?""
        # 妯℃嫙缁熻
        workflow_service.workflow_repo.count_by_tenant = Mock(return_value=10)
        
        # 鎵ц缁熻
        result = workflow_service.count_workflows(tenant_id="default")
        
        # 楠岃瘉缁撴灉
        assert result == 10
        workflow_service.workflow_repo.count_by_tenant.assert_called_once_with("default")
    
    def test_count_workflows_all_success(self, workflow_service):
        """娴嬭瘯缁熻鎵€鏈夊伐浣滄祦鏁伴噺鎴愬姛"""
        # 妯℃嫙缁熻
        workflow_service.workflow_repo.count_all = Mock(return_value=100)
        
        # 鎵ц缁熻
        result = workflow_service.count_workflows()
        
        # 楠岃瘉缁撴灉
        assert result == 100
        workflow_service.workflow_repo.count_all.assert_called_once()
