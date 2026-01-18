"""缂撳瓨瑁呴グ鍣?""
from functools import wraps
from typing import Optional, Callable
from loguru import logger
from common.cache import local_cache


def cache_result(ttl: int = 3600, key_prefix: Optional[str] = None):
    """缂撳瓨缁撴灉瑁呴グ鍣?    
    Args:
        ttl: 缂撳瓨鏃堕棿锛堢锛?        key_prefix: 缂撳瓨閿墠缂€
    
    浣跨敤绀轰緥锛?        @cache_result(ttl=600, key_prefix="user:")
        async def get_user(user_id: str):
            return {"id": user_id, "name": "test"}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 鐢熸垚缂撳瓨閿?            cache_key = f"{key_prefix or func.__name__}:{args}:{kwargs}"
            
            # 灏濊瘯浠庣紦瀛樿幏鍙?            cached = local_cache.get(cache_key)
            if cached:
                logger.debug(f"缂撳瓨鍛戒腑: {cache_key}")
                return cached
            
            # 鎵ц鍑芥暟
            result = await func(*args, **kwargs)
            
            # 缂撳瓨缁撴灉
            local_cache.set(cache_key, str(result), ttl)
            logger.debug(f"缂撳瓨璁剧疆: {cache_key}")
            
            return result
        return wrapper
    return decorator
