"""鏉冮檺瑁呴グ鍣?""
from functools import wraps
from typing import List, Callable
from fastapi import HTTPException, status, Request
from loguru import logger


def require_permissions(permissions: List[str]):
    """鏉冮檺楠岃瘉瑁呴グ鍣?    
    Args:
        permissions: 闇€瑕佺殑鏉冮檺鍒楄〃
    
    浣跨敤绀轰緥锛?        @router.get("/admin/users")
        @require_permissions(["user:read", "user:list"])
        async def list_users(request: Request):
            return {"users": []}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # 鑾峰彇鐢ㄦ埛鏉冮檺锛堜粠request.state锛?            user_permissions = getattr(request.state, 'permissions', [])
            
            # 妫€鏌ユ潈闄?            for perm in permissions:
                if perm not in user_permissions:
                    logger.warning(f"鏉冮檺涓嶈冻: 闇€瑕?{perm}, 鐢ㄦ埛鏉冮檺: {user_permissions}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"鏉冮檺涓嶈冻: {perm}"
                    )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_roles(roles: List[str]):
    """瑙掕壊楠岃瘉瑁呴グ鍣?    
    Args:
        roles: 闇€瑕佺殑瑙掕壊鍒楄〃
    
    浣跨敤绀轰緥锛?        @router.get("/admin/settings")
        @require_roles(["admin", "super_admin"])
        async def get_settings(request: Request):
            return {"settings": {}}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # 鑾峰彇鐢ㄦ埛瑙掕壊锛堜粠request.state锛?            user_roles = getattr(request.state, 'roles', [])
            
            # 妫€鏌ヨ鑹?            if not any(role in user_roles for role in roles):
                logger.warning(f"瑙掕壊涓嶈冻: 闇€瑕?{roles}, 鐢ㄦ埛瑙掕壊: {user_roles}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"瑙掕壊涓嶈冻: {roles}"
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
