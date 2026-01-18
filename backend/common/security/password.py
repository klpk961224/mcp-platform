"""
瀵嗙爜鍔犲瘑妯″潡

鍔熻兘璇存槑锛?1. 瀵嗙爜鍝堝笇
2. 瀵嗙爜楠岃瘉
3. 瀵嗙爜寮哄害妫€鏌?
浣跨敤绀轰緥锛?    from common.security.password import hash_password, verify_password
    
    # 鍝堝笇瀵嗙爜
    hashed = hash_password("password123")
    
    # 楠岃瘉瀵嗙爜
    is_valid = verify_password("password123", hashed)
"""

from passlib.context import CryptContext
from typing import Optional
from loguru import logger


# 瀵嗙爜鍔犲瘑涓婁笅鏂?pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    鍝堝笇瀵嗙爜
    
    Args:
        password: 鏄庢枃瀵嗙爜
    
    Returns:
        str: 鍝堝笇鍚庣殑瀵嗙爜
    
    浣跨敤绀轰緥锛?        hashed = hash_password("password123")
        print(hashed)
    """
    hashed = pwd_context.hash(password)
    logger.debug("瀵嗙爜鍝堝笇鎴愬姛")
    return hashed


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    楠岃瘉瀵嗙爜
    
    Args:
        plain_password: 鏄庢枃瀵嗙爜
        hashed_password: 鍝堝笇鍚庣殑瀵嗙爜
    
    Returns:
        bool: 鏄惁鍖归厤
    
    浣跨敤绀轰緥锛?        is_valid = verify_password("password123", hashed)
        if is_valid:
            print("瀵嗙爜姝ｇ‘")
    """
    is_valid = pwd_context.verify(plain_password, hashed_password)
    if is_valid:
        logger.debug("瀵嗙爜楠岃瘉鎴愬姛")
    else:
        logger.warning("瀵嗙爜楠岃瘉澶辫触")
    return is_valid


def check_password_strength(password: str) -> tuple[bool, str]:
    """
    妫€鏌ュ瘑鐮佸己搴?    
    Args:
        password: 瀵嗙爜
    
    Returns:
        tuple[bool, str]: (鏄惁閫氳繃, 鎻愮ず淇℃伅)
    
    浣跨敤绀轰緥锛?        is_valid, message = check_password_strength("password123")
        if not is_valid:
            print(message)
    """
    if len(password) < 8:
        return False, "瀵嗙爜长度鑷冲皯8浣?
    
    if not any(c.isupper() for c in password):
        return False, "瀵嗙爜蹇呴』鍖呭惈澶у啓瀛楁瘝"
    
    if not any(c.islower() for c in password):
        return False, "瀵嗙爜蹇呴』鍖呭惈灏忓啓瀛楁瘝"
    
    if not any(c.isdigit() for c in password):
        return False, "瀵嗙爜蹇呴』鍖呭惈鏁板瓧"
    
    return True, "瀵嗙爜寮哄害绗﹀悎瑕佹眰"
