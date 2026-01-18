# -*- coding: utf-8 -*-
"""
Pytest閰嶇疆鏂囦欢

娴嬭瘯閰嶇疆锛?1. 娴嬭瘯鍙戠幇璺緞
2. 娴嬭瘯鏍囪
3. 娴嬭瘯澶瑰叿
4. 娴嬭瘯瑕嗙洊鐜囬厤缃?"""

import pytest
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def pytest_configure(config):
    """閰嶇疆pytest"""
    config.addinivalue_line(
        "markers", "unit: 鍗曞厓娴嬭瘯鏍囪"
    )
    config.addinivalue_line(
        "markers", "integration: 闆嗘垚娴嬭瘯鏍囪"
    )
    config.addinivalue_line(
        "markers", "slow: 鎱㈤€熸祴璇曟爣璁?
    )


@pytest.fixture(scope="session")
def test_config():
    """娴嬭瘯閰嶇疆"""
    return {
        "test_database_url": "sqlite:///:memory:",
        "test_redis_url": "redis://localhost:6379/1",
        "test_timeout": 30
    }


@pytest.fixture(scope="function")
def clean_db():
    """娓呯悊鏁版嵁搴?""
    # 鍦ㄦ瘡涓祴璇曞嚱鏁版墽琛屽墠娓呯悊鏁版嵁搴?    yield
    # 鍦ㄦ瘡涓祴璇曞嚱鏁版墽琛屽悗娓呯悊鏁版嵁搴?    pass
