"""璁よ瘉涓棿浠?""
from fastapi import Request, HTTPException, status
from loguru import logger
from common.security import verify_token


async def auth_middleware(request: Request, call_next):
    """璁よ瘉涓棿浠?""
    # 璺宠繃涓嶉渶瑕佽璇佺殑璺緞
    if request.url.path in ["/api/v1/auth/login", "/health"]:
        return await call_next(request)
    
    # 鑾峰彇Token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="鏈彁渚涜璇乀oken"
        )
    
    token = auth_header.split(" ")[1]
    
    # 楠岃瘉Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token鏃犳晥鎴栧凡杩囨湡"
        )
    
    # 灏嗙敤鎴蜂俊鎭坊鍔犲埌璇锋眰状态?    request.state.user_id = payload.get("user_id")
    request.state.username = payload.get("username")
    
    logger.debug(f"鐢ㄦ埛璁よ瘉鎴愬姛: {request.state.username}")
    return await call_next(request)
