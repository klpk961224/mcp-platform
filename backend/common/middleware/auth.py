"""认证中间件"""
from fastapi import Request, HTTPException, status
from loguru import logger
from common.security import verify_token


async def auth_middleware(request: Request, call_next):
    """认证中间件"""
    # 跳过不需要认证的路径
    if request.url.path in ["/api/v1/auth/login", "/health"]:
        return await call_next(request)
    
    # 获取Token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证Token"
        )
    
    token = auth_header.split(" ")[1]
    
    # 验证Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期"
        )
    
    # 将用户信息添加到请求状态
    request.state.user_id = payload.get("user_id")
    request.state.username = payload.get("username")
    
    logger.debug(f"用户认证成功: {request.state.username}")
    return await call_next(request)