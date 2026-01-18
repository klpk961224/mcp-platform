"""
密码加密模块

功能说明：
1. 密码哈希
2. 密码验证
3. 密码强度检查

使用示例：
    from common.security.password import hash_password, verify_password
    
    # 哈希密码
    hashed = hash_password("password123")
    
    # 验证密码
    is_valid = verify_password("password123", hashed)
"""

from passlib.context import CryptContext
from typing import Optional
from loguru import logger


# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    哈希密码
    
    Args:
        password: 明文密码
    
    Returns:
        str: 哈希后的密码
    
    使用示例：
        hashed = hash_password("password123")
        print(hashed)
    """
    hashed = pwd_context.hash(password)
    logger.debug("密码哈希成功")
    return hashed


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
    
    Returns:
        bool: 是否匹配
    
    使用示例：
        is_valid = verify_password("password123", hashed)
        if is_valid:
            print("密码正确")
    """
    is_valid = pwd_context.verify(plain_password, hashed_password)
    if is_valid:
        logger.debug("密码验证成功")
    else:
        logger.warning("密码验证失败")
    return is_valid


def check_password_strength(password: str) -> tuple[bool, str]:
    """
    检查密码强度
    
    Args:
        password: 密码
    
    Returns:
        tuple[bool, str]: (是否通过, 提示信息)
    
    使用示例：
        is_valid, message = check_password_strength("password123")
        if not is_valid:
            print(message)
    """
    if len(password) < 8:
        return False, "密码长度至少8位"
    
    if not any(c.isupper() for c in password):
        return False, "密码必须包含大写字母"
    
    if not any(c.islower() for c in password):
        return False, "密码必须包含小写字母"
    
    if not any(c.isdigit() for c in password):
        return False, "密码必须包含数字"
    
    return True, "密码强度符合要求"