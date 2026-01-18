"""
璁よ瘉API璺敱

鍔熻兘璇存槑锛?1. 鐢ㄦ埛鐧诲綍
2. 鐢ㄦ埛娉ㄥ唽
3. 鐢ㄦ埛鐧诲嚭
4. Token鍒锋柊

浣跨敤绀轰緥锛?    # 鐧诲綍
    POST /api/v1/auth/login
    {
        "username": "admin",
        "password": "123456"
    }
    
    # 娉ㄥ唽
    POST /api/v1/auth/register
    {
        "username": "newuser",
        "password": "123456",
        "email": "newuser@example.com"
    }
    
    # 鍒锋柊Token
    POST /api/v1/auth/refresh
    {
        "refresh_token": "xxx"
    }
    
    # 鐧诲嚭
    POST /api/v1/auth/logout
    {
        "refresh_token": "xxx"
    }
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from common.security import verify_token
from common.responses import success, error

from app.core.config import settings
from app.core.deps import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["璁よ瘉"])


@router.post("/login", response_model=LoginResponse, summary="鐢ㄦ埛鐧诲綍")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    鐢ㄦ埛鐧诲綍
    
    鍔熻兘璇存槑锛?    1. 楠岃瘉鐢ㄦ埛鍚嶅拰瀵嗙爜
    2. 鐢熸垚璁块棶Token鍜屽埛鏂癟oken
    3. 杩斿洖鐢ㄦ埛淇℃伅鍜孴oken
    
    Args:
        request: 鐧诲綍璇锋眰
        db: 鏁版嵁搴撲細璇?    
    Returns:
        LoginResponse: 鐧诲綍鍝嶅簲
    
    浣跨敤绀轰緥锛?        POST /api/v1/auth/login
        {
            "username": "admin",
            "password": "123456",
            "tenant_code": "default"
        }
    """
    logger.info(f"鐢ㄦ埛鐧诲綍璇锋眰: username={request.username}")
    
    try:
        # 浣跨敤AuthService杩涜鐧诲綍楠岃瘉
        auth_service = AuthService(db)
        result = auth_service.login(
            username=request.username,
            password=request.password,
            tenant_id=getattr(request, 'tenant_code', None)
        )
        
        logger.info(f"鐢ㄦ埛鐧诲綍鎴愬姛: username={request.username}, user_id={result['user_info']['id']}")
        
        return LoginResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
            user_info=result["user_info"]
        )
    except ValueError as e:
        logger.warning(f"鐢ㄦ埛鐧诲綍澶辫触: username={request.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"鐢ㄦ埛鐧诲綍寮傚父: username={request.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="鐧诲綍澶辫触锛岃绋嶅悗閲嶈瘯"
        )


@router.post("/register", response_model=RegisterResponse, summary="鐢ㄦ埛娉ㄥ唽")
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    鐢ㄦ埛娉ㄥ唽
    
    鍔熻兘璇存槑锛?    1. 楠岃瘉鐢ㄦ埛鍚嶅拰閭鏄惁宸插瓨鍦?    2. 鍒涘缓鏂扮敤鎴?    3. 杩斿洖鐢ㄦ埛淇℃伅
    
    Args:
        request: 娉ㄥ唽璇锋眰
        db: 鏁版嵁搴撲細璇?    
    Returns:
        RegisterResponse: 娉ㄥ唽鍝嶅簲
    
    浣跨敤绀轰緥锛?        POST /api/v1/auth/register
        {
            "username": "newuser",
            "password": "123456",
            "email": "newuser@example.com",
            "phone": "132800138000",
            "tenant_code": "default"
        }
    """
    logger.info(f"鐢ㄦ埛娉ㄥ唽璇锋眰: username={request.username}, email={request.email}")
    
    try:
        # 浣跨敤AuthService杩涜娉ㄥ唽
        auth_service = AuthService(db)
        result = auth_service.register(
            username=request.username,
            password=request.password,
            email=request.email,
            phone=request.phone,
            tenant_id=getattr(request, 'tenant_code', None)
        )
        
        logger.info(f"鐢ㄦ埛娉ㄥ唽鎴愬姛: username={request.username}, user_id={result['user_id']}")
        
        return RegisterResponse(
            message=result["message"],
            user_id=result["user_id"],
            username=result["username"],
            email=result["email"]
        )
    except ValueError as e:
        logger.warning(f"鐢ㄦ埛娉ㄥ唽澶辫触: username={request.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"鐢ㄦ埛娉ㄥ唽寮傚父: username={request.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="娉ㄥ唽澶辫触锛岃绋嶅悗閲嶈瘯"
        )


@router.post("/refresh", response_model=RefreshTokenResponse, summary="鍒锋柊Token")
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    鍒锋柊Token
    
    鍔熻兘璇存槑锛?    1. 楠岃瘉鍒锋柊Token
    2. 鐢熸垚鏂扮殑璁块棶Token
    3. 杩斿洖鏂扮殑璁块棶Token
    
    Args:
        request: 鍒锋柊Token璇锋眰
        db: 鏁版嵁搴撲細璇?    
    Returns:
        RefreshTokenResponse: 鍒锋柊Token鍝嶅簲
    
    浣跨敤绀轰緥锛?        POST /api/v1/auth/refresh
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    logger.info("鍒锋柊Token璇锋眰")
    
    try:
        # 浣跨敤AuthService鍒锋柊Token
        auth_service = AuthService(db)
        result = auth_service.refresh_token(request.refresh_token)
        
        logger.info(f"鍒锋柊Token鎴愬姛: user_id={result.get('user_id', 'unknown')}")
        
        return RefreshTokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"]
        )
    except ValueError as e:
        logger.warning(f"鍒锋柊Token澶辫触: error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"鍒锋柊Token寮傚父: error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="鍒锋柊Token澶辫触锛岃绋嶅悗閲嶈瘯"
        )


@router.post("/logout", response_model=LogoutResponse, summary="鐢ㄦ埛鐧诲嚭")
async def logout(
    request: Optional[RefreshTokenRequest] = None,
    db: Session = Depends(get_db)
):
    """
    鐢ㄦ埛鐧诲嚭
    
    鍔熻兘璇存槑锛?    1. 楠岃瘉Token锛堝彲閫夛級
    2. 鍚婇攢鎵€鏈塗oken
    3. 杩斿洖鐧诲嚭鎴愬姛娑堟伅
    
    Args:
        request: 鍖呭惈Token鐨勮姹傦紙鍙€夛級
        db: 鏁版嵁搴撲細璇?    
    Returns:
        LogoutResponse: 鐧诲嚭鍝嶅簲
    
    浣跨敤绀轰緥锛?        POST /api/v1/auth/logout
        {
            "refresh_token": "xxx"
        }
        
        鎴?        
        POST /api/v1/auth/logout
    """
    logger.info("鐢ㄦ埛鐧诲嚭璇锋眰")
    
    try:
        # 濡傛灉鎻愪緵浜唕efresh_token锛屽垯楠岃瘉骞剁櫥鍑?        if request and request.refresh_token:
            # 楠岃瘉Token骞惰幏鍙栫敤鎴稩D
            payload = verify_token(request.refresh_token)
            if payload:
                user_id = payload.get("user_id")
                
                # 浣跨敤AuthService杩涜鐧诲嚭
                auth_service = AuthService(db)
                auth_service.logout(user_id)
                
                logger.info(f"鐢ㄦ埛鐧诲嚭鎴愬姛: user_id={user_id}")
            else:
                logger.warning("Token鏃犳晥锛屼絾浠嶇劧杩斿洖鐧诲嚭鎴愬姛")
        else:
            logger.info("鏈彁渚汿oken锛岀洿鎺ヨ繑鍥炵櫥鍑烘垚鍔?)
        
        return LogoutResponse(message="鐧诲嚭鎴愬姛")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"鐢ㄦ埛鐧诲嚭寮傚父: error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="鐧诲嚭澶辫触锛岃绋嶅悗閲嶈瘯"
        )
