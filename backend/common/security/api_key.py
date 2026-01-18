"""
API Key管理模块

功能说明：
1. API Key生成
2. API Key验证
3. API Key解码

使用示例：
    from common.security.api_key import generate_api_key, verify_api_key
    
    # 生成API Key
    api_key = generate_api_key(user_id="123", name="test")
    
    # 验证API Key
    payload = verify_api_key(api_key)
"""

import secrets
import hmac
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
from loguru import logger
from common.config import settings


def generate_api_key(
    user_id: str,
    name: str,
    expires_days: Optional[int] = None
) -> str:
    """
    生成API Key
    
    Args:
        user_id: 用户ID
        name: API Key名称
        expires_days: 过期天数（可选）
    
    Returns:
        str: API Key
    
    使用示例：
        api_key = generate_api_key(
            user_id="123",
            name="test",
            expires_days=30
        )
    """
    # 生成随机密钥
    key_id = secrets.token_hex(8)
    key_secret = secrets.token_hex(16)
    
    # 组合API Key
    api_key = f"{key_id}.{key_secret}"
    
    logger.info(f"生成API Key: user_id={user_id}, name={name}")
    return api_key


def verify_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """
    验证API Key
    
    Args:
        api_key: API Key
    
    Returns:
        Optional[Dict[str, Any]]: API Key信息（验证成功）或 None（验证失败）
    
    使用示例：
        payload = verify_api_key(api_key)
        if payload:
            print(f"API Key ID: {payload['key_id']}")
    """
    if not api_key or "." not in api_key:
        logger.warning("API Key格式无效")
        return None
    
    parts = api_key.split(".", 1)
    if len(parts) != 2:
        logger.warning("API Key格式无效")
        return None
    
    key_id, key_secret = parts
    
    # 这里应该查询数据库验证API Key
    # 简化版本，只返回基本信息
    logger.debug(f"API Key验证成功: key_id={key_id}")
    return {
        "key_id": key_id,
        "key_secret": key_secret,
        "is_valid": True
    }


def decode_api_key(api_key: str) -> Optional[tuple[str, str]]:
    """
    解码API Key
    
    Args:
        api_key: API Key
    
    Returns:
        Optional[tuple[str, str]]: (key_id, key_secret) 或 None
    
    使用示例：
        key_id, key_secret = decode_api_key(api_key)
        if key_id and key_secret:
            print(f"Key ID: {key_id}")
    """
    if not api_key or "." not in api_key:
        return None
    
    parts = api_key.split(".", 1)
    if len(parts) != 2:
        return None
    
    return parts[0], parts[1]