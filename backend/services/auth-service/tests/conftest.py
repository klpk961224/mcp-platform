# -*- coding: utf-8 -*-
"""
Pytest配置文件

测试配置：
1. 测试发现路径
2. 测试标记
3. 测试夹具
4. 测试覆盖率配置
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line(
        "markers", "unit: 单元测试标记"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试标记"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试标记"
    )


@pytest.fixture(scope="session")
def test_config():
    """测试配置"""
    return {
        "test_database_url": "sqlite:///:memory:",
        "test_redis_url": "redis://localhost:6379/1",
        "test_timeout": 30
    }


@pytest.fixture(scope="function")
def clean_db():
    """清理数据库"""
    # 在每个测试函数执行前清理数据库
    yield
    # 在每个测试函数执行后清理数据库
    pass