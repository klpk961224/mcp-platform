"""Redis缓存模块"""
from typing import Optional, Any
import redis
from loguru import logger
from common.config import settings


class RedisCache:
    """Redis缓存类"""
    
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD or None,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        logger.info("Redis缓存初始化完成")
    
    def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        return self.client.get(key)
    
    def set(self, key: str, value: str, ttl: int = 3600):
        """设置缓存"""
        self.client.setex(key, ttl, value)
    
    def delete(self, key: str):
        """删除缓存"""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return self.client.exists(key) > 0


redis_cache = RedisCache()