"""
JWT工具模块

功能说明：
1. JWT Token生成
2. JWT Token验证
3. JWT Token刷新
4. JWT Token解码

使用示例：
    from common.security.jwt import create_access_token, verify_token
    
    # 生成Token
    token = create_access_token(user_id="123", username="test")
    
    # 验证Token
    payload = verify_token(token)
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import JWTError, jwt
from loguru import logger
from common.config import settings


def create_access_token(
    data: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
    expires_minutes: Optional[int] = None
) -> str:
    """
    创建访问Token
    
    Args:
        data: 包含用户信息的字典（推荐方式）
            - 示例：{"user_id": "123", "username": "test"}
        user_id: 用户ID（可选，如果提供了data则忽略）
        username: 用户名（可选，如果提供了data则忽略）
        additional_claims: 额外的声明（可选）
        expires_delta: 过期时间增量（可选）
        expires_minutes: 过期时间（分钟）（可选，与expires_delta二选一）
    
    Returns:
        str: JWT Token
    
    使用示例：
        # 方式1：使用data字典（推荐）
        token = create_access_token(
            data={"user_id": "123", "username": "test"},
            expires_minutes=30
        )
        
        # 方式2：直接传递参数
        token = create_access_token(
            user_id="123",
            username="test",
            expires_delta=timedelta(minutes=30)
        )
    """
    # 如果提供了data字典，从中提取user_id和username
    if data:
        user_id = data.get("user_id")
        username = data.get("username")
    
    if not user_id:
        raise ValueError("必须提供user_id参数或data字典中包含user_id")
    
    # 计算过期时间
    if expires_delta:
        expire = datetime.now() + expires_delta
    elif expires_minutes:
        expire = datetime.now() + timedelta(minutes=expires_minutes)
    else:
        expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": user_id,
        "username": username,
        "exp": expire,
        "iat": datetime.now(),
        "type": "access"
    }
    
    # 如果提供了data字典，将其他字段也添加到token中
    if data:
        for key, value in data.items():
            if key not in ["user_id", "username"]:
                to_encode[key] = value
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    logger.debug(f"创建访问Token: user_id={user_id}, username={username}")
    return encoded_jwt


def create_refresh_token(
    data: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
    expires_days: Optional[int] = None
) -> str:
    """
    创建刷新Token
    
    Args:
        data: 包含用户信息的字典（可选）
            - 示例：{"user_id": "123"}
        user_id: 用户ID（可选，如果提供了data则忽略）
        expires_delta: 过期时间增量（可选）
        expires_days: 过期时间（天）（可选，与expires_delta二选一）
    
    Returns:
        str: JWT Token
    
    使用示例：
        # 方式1：使用data字典（推荐）
        token = create_refresh_token(
            data={"user_id": "123"},
            expires_days=7
        )
        
        # 方式2：直接传递参数
        token = create_refresh_token(
            user_id="123",
            expires_delta=timedelta(days=7)
        )
    """
    # 如果提供了data字典，从中提取user_id
    if data:
        user_id = data.get("user_id")
    
    if not user_id:
        raise ValueError("必须提供user_id参数或data字典中包含user_id")
    
    # 计算过期时间
    if expires_delta:
        expire = datetime.now() + expires_delta
    elif expires_days:
        expire = datetime.now() + timedelta(days=expires_days)
    else:
        expire = datetime.now() + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)
    
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(),
        "type": "refresh"
    }
    
    # 如果提供了data字典，将其他字段也添加到token中
    if data:
        for key, value in data.items():
            if key != "user_id":
                to_encode[key] = value
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    logger.debug(f"创建刷新Token: user_id={user_id}")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证Token
    
    Args:
        token: JWT Token
    
    Returns:
        Optional[Dict[str, Any]]: Token载荷（验证成功）或 None（验证失败）
    
    使用示例：
        payload = verify_token(token)
        if payload:
            print(f"用户ID: {payload['sub']}")
        else:
            print("Token无效")
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        logger.debug(f"Token验证成功: user_id={payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.warning(f"Token验证失败: {e}")
        return None


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码Token（不验证过期时间）
    
    Args:
        token: JWT Token
    
    Returns:
        Optional[Dict[str, Any]]: Token载荷（解码成功）或 None（解码失败）
    
    使用示例：
        payload = decode_token(token)
        if payload:
            print(f"Token类型: {payload.get('type')}")
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False}
        )
        return payload
    except JWTError as e:
        logger.warning(f"Token解码失败: {e}")
        return None