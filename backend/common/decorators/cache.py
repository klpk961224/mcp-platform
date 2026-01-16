"""缓存装饰器"""
from functools import wraps
from typing import Optional, Callable
from loguru import logger
from common.cache import local_cache


def cache_result(ttl: int = 3600, key_prefix: Optional[str] = None):
    """缓存结果装饰器
    
    Args:
        ttl: 缓存时间（秒）
        key_prefix: 缓存键前缀
    
    使用示例：
        @cache_result(ttl=600, key_prefix="user:")
        async def get_user(user_id: str):
            return {"id": user_id, "name": "test"}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix or func.__name__}:{args}:{kwargs}"
            
            # 尝试从缓存获取
            cached = local_cache.get(cache_key)
            if cached:
                logger.debug(f"缓存命中: {cache_key}")
                return cached
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 缓存结果
            local_cache.set(cache_key, str(result), ttl)
            logger.debug(f"缓存设置: {cache_key}")
            
            return result
        return wrapper
    return decorator