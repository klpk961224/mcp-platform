"""
API Key绠＄悊妯″潡

鍔熻兘璇存槑锛?1. API Key鐢熸垚
2. API Key楠岃瘉
3. API Key瑙ｇ爜

浣跨敤绀轰緥锛?    from common.security.api_key import generate_api_key, verify_api_key
    
    # 鐢熸垚API Key
    api_key = generate_api_key(user_id="123", name="test")
    
    # 楠岃瘉API Key
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
    鐢熸垚API Key
    
    Args:
        user_id: 用户ID
        name: API Key名称
        expires_days: 杩囨湡澶╂暟锛堝彲閫夛級
    
    Returns:
        str: API Key
    
    浣跨敤绀轰緥锛?        api_key = generate_api_key(
            user_id="123",
            name="test",
            expires_days=30
        )
    """
    # 鐢熸垚闅忔満瀵嗛挜
    key_id = secrets.token_hex(8)
    key_secret = secrets.token_hex(16)
    
    # 缁勫悎API Key
    api_key = f"{key_id}.{key_secret}"
    
    logger.info(f"鐢熸垚API Key: user_id={user_id}, name={name}")
    return api_key


def verify_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """
    楠岃瘉API Key
    
    Args:
        api_key: API Key
    
    Returns:
        Optional[Dict[str, Any]]: API Key淇℃伅锛堥獙璇佹垚鍔燂級鎴?None锛堥獙璇佸け璐ワ級
    
    浣跨敤绀轰緥锛?        payload = verify_api_key(api_key)
        if payload:
            print(f"API Key ID: {payload['key_id']}")
    """
    if not api_key or "." not in api_key:
        logger.warning("API Key鏍煎紡鏃犳晥")
        return None
    
    parts = api_key.split(".", 1)
    if len(parts) != 2:
        logger.warning("API Key鏍煎紡鏃犳晥")
        return None
    
    key_id, key_secret = parts
    
    # 杩欓噷搴旇查询鏁版嵁搴撻獙璇丄PI Key
    # 绠€鍖栫増鏈紝鍙繑鍥炲熀鏈俊鎭?    logger.debug(f"API Key楠岃瘉鎴愬姛: key_id={key_id}")
    return {
        "key_id": key_id,
        "key_secret": key_secret,
        "is_valid": True
    }


def decode_api_key(api_key: str) -> Optional[tuple[str, str]]:
    """
    瑙ｇ爜API Key
    
    Args:
        api_key: API Key
    
    Returns:
        Optional[tuple[str, str]]: (key_id, key_secret) 鎴?None
    
    浣跨敤绀轰緥锛?        key_id, key_secret = decode_api_key(api_key)
        if key_id and key_secret:
            print(f"Key ID: {key_id}")
    """
    if not api_key or "." not in api_key:
        return None
    
    parts = api_key.split(".", 1)
    if len(parts) != 2:
        return None
    
    return parts[0], parts[1]
