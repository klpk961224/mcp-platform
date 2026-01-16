"""
认证API路由

功能说明：
1. 用户登录
2. 用户登出
3. Token刷新

使用示例：
    # 登录
    POST /api/v1/auth/login
    {
        "username": "admin",
        "password": "123456"
    }
    
    # 刷新Token
    POST /api/v1/auth/refresh
    {
        "refresh_token": "xxx"
    }
    
    # 登出
    POST /api/v1/auth/logout
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
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
    LogoutResponse
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    用户登录
    
    功能说明：
    1. 验证用户名和密码
    2. 生成访问Token和刷新Token
    3. 返回用户信息和Token
    
    Args:
        request: 登录请求
        db: 数据库会话
    
    Returns:
        LoginResponse: 登录响应
    
    使用示例：
        POST /api/v1/auth/login
        {
            "username": "admin",
            "password": "123456",
            "tenant_code": "default"
        }
    """
    logger.info(f"用户登录请求: username={request.username}")
    
    try:
        # 使用AuthService进行登录验证
        auth_service = AuthService(db)
        result = auth_service.login(
            username=request.username,
            password=request.password,
            tenant_id=getattr(request, 'tenant_code', None)
        )
        
        logger.info(f"用户登录成功: username={request.username}, user_id={result['user_info']['id']}")
        
        return LoginResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
            user_info=result["user_info"]
        )
    except ValueError as e:
        logger.warning(f"用户登录失败: username={request.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"用户登录异常: username={request.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录失败，请稍后重试"
        )


@router.post("/refresh", response_model=RefreshTokenResponse, summary="刷新Token")
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    刷新Token
    
    功能说明：
    1. 验证刷新Token
    2. 生成新的访问Token
    3. 返回新的访问Token
    
    Args:
        request: 刷新Token请求
        db: 数据库会话
    
    Returns:
        RefreshTokenResponse: 刷新Token响应
    
    使用示例：
        POST /api/v1/auth/refresh
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    logger.info("刷新Token请求")
    
    try:
        # 使用AuthService刷新Token
        auth_service = AuthService(db)
        result = auth_service.refresh_token(request.refresh_token)
        
        logger.info(f"刷新Token成功: user_id={result.get('user_id', 'unknown')}")
        
        return RefreshTokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"]
        )
    except ValueError as e:
        logger.warning(f"刷新Token失败: error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"刷新Token异常: error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新Token失败，请稍后重试"
        )


@router.post("/logout", response_model=LogoutResponse, summary="用户登出")
async def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    用户登出
    
    功能说明：
    1. 验证Token
    2. 吊销所有Token
    3. 返回登出成功消息
    
    Args:
        request: 包含Token的请求
        db: 数据库会话
    
    Returns:
        LogoutResponse: 登出响应
    
    使用示例：
        POST /api/v1/auth/logout
        {
            "refresh_token": "xxx"
        }
    """
    logger.info("用户登出请求")
    
    try:
        # 验证Token并获取用户ID
        payload = verify_token(request.refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token无效或已过期"
            )
        
        user_id = payload.get("user_id")
        
        # 使用AuthService进行登出
        auth_service = AuthService(db)
        auth_service.logout(user_id)
        
        logger.info(f"用户登出成功: user_id={user_id}")
        
        return LogoutResponse(message="登出成功")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户登出异常: error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登出失败，请稍后重试"
        )