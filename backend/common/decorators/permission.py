"""权限装饰器"""
from functools import wraps
from typing import List, Callable
from fastapi import HTTPException, status, Request
from loguru import logger


def require_permissions(permissions: List[str]):
    """权限验证装饰器
    
    Args:
        permissions: 需要的权限列表
    
    使用示例：
        @router.get("/admin/users")
        @require_permissions(["user:read", "user:list"])
        async def list_users(request: Request):
            return {"users": []}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # 获取用户权限（从request.state）
            user_permissions = getattr(request.state, 'permissions', [])
            
            # 检查权限
            for perm in permissions:
                if perm not in user_permissions:
                    logger.warning(f"权限不足: 需要 {perm}, 用户权限: {user_permissions}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"权限不足: {perm}"
                    )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_roles(roles: List[str]):
    """角色验证装饰器
    
    Args:
        roles: 需要的角色列表
    
    使用示例：
        @router.get("/admin/settings")
        @require_roles(["admin", "super_admin"])
        async def get_settings(request: Request):
            return {"settings": {}}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # 获取用户角色（从request.state）
            user_roles = getattr(request.state, 'roles', [])
            
            # 检查角色
            if not any(role in user_roles for role in roles):
                logger.warning(f"角色不足: 需要 {roles}, 用户角色: {user_roles}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"角色不足: {roles}"
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator