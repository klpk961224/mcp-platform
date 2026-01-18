# -*- coding: utf-8 -*-
"""
WorkflowService单元测试

测试内容：
1. 启动工作流
2. 获取工作流
3. 获取用户工作流
4. 终止工作流
5. 获取统计信息
6. 统计工作流数量
"""

import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.workflow_service import WorkflowService


@pytest.fixture
def mock_db():
    """模拟数据库会话"""
    return Mock(spec=Session)


@pytest.fixture
def mock_template():
    """模拟工作流模板对象"""
    template = Mock()
    template.id = "test_template_id"
    template.name = "测试工作流"
    template.definition = '{"nodes": [{"id": "node1", "name": "审批节点", "type": "approval", "assignee_id": "user_001", "assignee_name": "User_001"}]}'
    template.status = "active"
    template.is_available = Mock(return_value=True)
    template.increment_usage = Mock()
    return template


@pytest.fixture
def mock_workflow():
    """模拟工作流对象"""
    workflow = Mock()
    workflow.id = "test_workflow_id"
    workflow.tenant_id = "default"
    workflow.name = "测试工作流"
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
    """创建WorkflowService实例"""
    return WorkflowService(mock_db)


class TestWorkflowService:
    """WorkflowService测试类"""
    
    def test_init(self, mock_db):
        """测试WorkflowService初始化"""
        service = WorkflowService(mock_db)
        assert service.db == mock_db
        assert service.workflow_repo is not None
        assert service.task_repo is not None
        assert service.template_repo is not None
    
    def test_start_workflow_success(self, workflow_service, mock_template, mock_workflow):
        """测试启动工作流成功"""
        # 模拟获取模板
        workflow_service.template_repo.get_by_id = Mock(return_value=mock_template)
        # 模拟更新模板
        workflow_service.template_repo.update = Mock()
        # 模拟创建工作流
        workflow_service.workflow_repo.create = Mock(return_value=mock_workflow)
        # 模拟创建任务
        workflow_service.task_repo.create = Mock()
        
        # 执行启动工作流
        result = workflow_service.start_workflow(
            template_id="test_template_id",
            initiator_id="user_001",
            initiator_name="User_001",
            tenant_id="default"
        )
        
        # 验证结果
        assert result.id == "test_workflow_id"
        assert result.status == "running"
        workflow_service.workflow_repo.create.assert_called_once()
        workflow_service.task_repo.create.assert_called_once()
    
    def test_start_workflow_template_not_found(self, workflow_service):
        """测试启动工作流失败（模板不存在）"""
        # 模拟获取模板返回None
        workflow_service.template_repo.get_by_id = Mock(return_value=None)
        
        # 执行启动工作流并验证异常
        with pytest.raises(ValueError, match="工作流模板不存在"):
            workflow_service.start_workflow(
                template_id="nonexistent_id",
                initiator_id="user_001",
                initiator_name="User_001",
                tenant_id="default"
            )
    
    def test_start_workflow_template_not_available(self, workflow_service, mock_template):
        """测试启动工作流失败（模板不可用）"""
        # 模拟获取模板
        workflow_service.template_repo.get_by_id = Mock(return_value=mock_template)
        # 模拟模板不可用
        mock_template.is_available = Mock(return_value=False)
        
        # 执行启动工作流并验证异常
        with pytest.raises(ValueError, match="工作流模板不可用"):
            workflow_service.start_workflow(
                template_id="test_template_id",
                initiator_id="user_001",
                initiator_name="User_001",
                tenant_id="default"
            )
    
    def test_get_workflow_success(self, workflow_service, mock_workflow):
        """测试获取工作流成功"""
        # 模拟查询工作流
        workflow_service.workflow_repo.get_by_id = Mock(return_value=mock_workflow)
        
        # 执行查询
        result = workflow_service.get_workflow("test_workflow_id")
        
        # 验证结果
        assert result is not None
        assert result.id == "test_workflow_id"
        workflow_service.workflow_repo.get_by_id.assert_called_once_with("test_workflow_id")
    
    def test_get_workflow_not_found(self, workflow_service):
        """测试获取工作流失败"""
        # 模拟查询工作流返回None
        workflow_service.workflow_repo.get_by_id = Mock(return_value=None)
        
        # 执行查询
        result = workflow_service.get_workflow("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_user_workflows_success(self, workflow_service, mock_workflow):
        """测试获取用户工作流成功"""
        # 模拟查询工作流列表
        workflow_service.workflow_repo.get_user_workflows = Mock(return_value=[mock_workflow])
        
        # 执行查询
        result = workflow_service.get_user_workflows("user_001")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].initiator_id == "user_001"
        workflow_service.workflow_repo.get_user_workflows.assert_called_once()
    
    def test_terminate_workflow_success(self, workflow_service, mock_workflow):
        """测试终止工作流成功"""
        # 模拟查询工作流
        workflow_service.workflow_repo.get_by_id = Mock(return_value=mock_workflow)
        # 模拟更新工作流
        workflow_service.workflow_repo.update = Mock(return_value=mock_workflow)
        
        # 执行终止
        result = workflow_service.terminate_workflow("test_workflow_id")
        
        # 验证结果
        assert result is not None
        assert result.id == "test_workflow_id"
        mock_workflow.terminate.assert_called_once()
        workflow_service.workflow_repo.update.assert_called_once()
    
    def test_terminate_workflow_not_found(self, workflow_service):
        """测试终止工作流失败（工作流不存在）"""
        # 模拟查询工作流返回None
        workflow_service.workflow_repo.get_by_id = Mock(return_value=None)
        
        # 执行终止
        result = workflow_service.terminate_workflow("nonexistent_id")
        
        # 验证结果
        assert result is None
    
    def test_get_workflow_statistics_success(self, workflow_service):
        """测试获取工作流统计信息成功"""
        # 模拟统计
        workflow_service.workflow_repo.count_by_tenant = Mock(side_effect=[10, 2, 6, 2])
        
        # 执行获取统计
        result = workflow_service.get_workflow_statistics("default")
        
        # 验证结果
        assert result["total"] == 10
        assert result["running"] == 2
        assert result["completed"] == 6
        assert result["terminated"] == 2
        assert result["completion_rate"] == 60.0
    
    def test_count_workflows_success(self, workflow_service):
        """测试统计工作流数量成功"""
        # 模拟统计
        workflow_service.workflow_repo.count_by_tenant = Mock(return_value=10)
        
        # 执行统计
        result = workflow_service.count_workflows(tenant_id="default")
        
        # 验证结果
        assert result == 10
        workflow_service.workflow_repo.count_by_tenant.assert_called_once_with("default")
    
    def test_count_workflows_all_success(self, workflow_service):
        """测试统计所有工作流数量成功"""
        # 模拟统计
        workflow_service.workflow_repo.count_all = Mock(return_value=100)
        
        # 执行统计
        result = workflow_service.count_workflows()
        
        # 验证结果
        assert result == 100
        workflow_service.workflow_repo.count_all.assert_called_once()