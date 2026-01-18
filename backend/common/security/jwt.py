"""
JWT宸ュ叿妯″潡

鍔熻兘璇存槑锛?1. JWT Token鐢熸垚
2. JWT Token楠岃瘉
3. JWT Token鍒锋柊
4. JWT Token瑙ｇ爜

浣跨敤绀轰緥锛?    from common.security.jwt import create_access_token, verify_token
    
    # 鐢熸垚Token
    token = create_access_token(user_id="123", username="test")
    
    # 楠岃瘉Token
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
    创建璁块棶Token
    
    Args:
        data: 鍖呭惈鐢ㄦ埛淇℃伅鐨勫瓧鍏革紙鎺ㄨ崘鏂瑰紡锛?            - 绀轰緥锛歿"user_id": "123", "username": "test"}
        user_id: 用户ID锛堝彲閫夛紝濡傛灉鎻愪緵浜哾ata鍒欏拷鐣ワ級
        username: 用户名嶏紙鍙€夛紝濡傛灉鎻愪緵浜哾ata鍒欏拷鐣ワ級
        additional_claims: 棰濆鐨勫０鏄庯紙鍙€夛級
        expires_delta: 杩囨湡鏃堕棿澧為噺锛堝彲閫夛級
        expires_minutes: 杩囨湡鏃堕棿锛堝垎閽燂級锛堝彲閫夛紝涓巈xpires_delta浜岄€変竴锛?    
    Returns:
        str: JWT Token
    
    浣跨敤绀轰緥锛?        # 鏂瑰紡1锛氫娇鐢╠ata瀛楀吀锛堟帹鑽愶級
        token = create_access_token(
            data={"user_id": "123", "username": "test"},
            expires_minutes=30
        )
        
        # 鏂瑰紡2锛氱洿鎺ヤ紶閫掑弬鏁?        token = create_access_token(
            user_id="123",
            username="test",
            expires_delta=timedelta(minutes=30)
        )
    """
    # 濡傛灉鎻愪緵浜哾ata瀛楀吀锛屼粠涓彁鍙杣ser_id鍜寀sername
    if data:
        user_id = data.get("user_id")
        username = data.get("username")
    
    if not user_id:
        raise ValueError("蹇呴』鎻愪緵user_id鍙傛暟鎴杁ata瀛楀吀涓寘鍚玼ser_id")
    
    # 璁＄畻杩囨湡鏃堕棿
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
    
    # 濡傛灉鎻愪緵浜哾ata瀛楀吀锛屽皢鍏朵粬瀛楁涔熸坊鍔犲埌token涓?    if data:
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
    
    logger.debug(f"创建璁块棶Token: user_id={user_id}, username={username}")
    return encoded_jwt


def create_refresh_token(
    data: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
    expires_days: Optional[int] = None
) -> str:
    """
    创建鍒锋柊Token
    
    Args:
        data: 鍖呭惈鐢ㄦ埛淇℃伅鐨勫瓧鍏革紙鍙€夛級
            - 绀轰緥锛歿"user_id": "123"}
        user_id: 用户ID锛堝彲閫夛紝濡傛灉鎻愪緵浜哾ata鍒欏拷鐣ワ級
        expires_delta: 杩囨湡鏃堕棿澧為噺锛堝彲閫夛級
        expires_days: 杩囨湡鏃堕棿锛堝ぉ锛夛紙鍙€夛紝涓巈xpires_delta浜岄€変竴锛?    
    Returns:
        str: JWT Token
    
    浣跨敤绀轰緥锛?        # 鏂瑰紡1锛氫娇鐢╠ata瀛楀吀锛堟帹鑽愶級
        token = create_refresh_token(
            data={"user_id": "123"},
            expires_days=7
        )
        
        # 鏂瑰紡2锛氱洿鎺ヤ紶閫掑弬鏁?        token = create_refresh_token(
            user_id="123",
            expires_delta=timedelta(days=7)
        )
    """
    # 濡傛灉鎻愪緵浜哾ata瀛楀吀锛屼粠涓彁鍙杣ser_id
    if data:
        user_id = data.get("user_id")
    
    if not user_id:
        raise ValueError("蹇呴』鎻愪緵user_id鍙傛暟鎴杁ata瀛楀吀涓寘鍚玼ser_id")
    
    # 璁＄畻杩囨湡鏃堕棿
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
    
    # 濡傛灉鎻愪緵浜哾ata瀛楀吀锛屽皢鍏朵粬瀛楁涔熸坊鍔犲埌token涓?    if data:
        for key, value in data.items():
            if key != "user_id":
                to_encode[key] = value
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    logger.debug(f"创建鍒锋柊Token: user_id={user_id}")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    楠岃瘉Token
    
    Args:
        token: JWT Token
    
    Returns:
        Optional[Dict[str, Any]]: Token杞借嵎锛堥獙璇佹垚鍔燂級鎴?None锛堥獙璇佸け璐ワ級
    
    浣跨敤绀轰緥锛?        payload = verify_token(token)
        if payload:
            print(f"用户ID: {payload['sub']}")
        else:
            print("Token鏃犳晥")
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        logger.debug(f"Token楠岃瘉鎴愬姛: user_id={payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.warning(f"Token楠岃瘉澶辫触: {e}")
        return None


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    瑙ｇ爜Token锛堜笉楠岃瘉杩囨湡鏃堕棿锛?    
    Args:
        token: JWT Token
    
    Returns:
        Optional[Dict[str, Any]]: Token杞借嵎锛堣В鐮佹垚鍔燂級鎴?None锛堣В鐮佸け璐ワ級
    
    浣跨敤绀轰緥锛?        payload = decode_token(token)
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
        logger.warning(f"Token瑙ｇ爜澶辫触: {e}")
        return None
