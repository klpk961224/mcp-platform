"""Redis缂撳瓨妯″潡"""
from typing import Optional, Any
import redis
from loguru import logger
from common.config import settings


class RedisCache:
    """Redis缂撳瓨绫?""
    
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD or None,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        logger.info("Redis缂撳瓨鍒濆鍖栧畬鎴?)
    
    def get(self, key: str) -> Optional[str]:
        """鑾峰彇缂撳瓨"""
        return self.client.get(key)
    
    def set(self, key: str, value: str, ttl: int = 3600):
        """璁剧疆缂撳瓨"""
        self.client.setex(key, ttl, value)
    
    def delete(self, key: str):
        """删除缂撳瓨"""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """妫€鏌ョ紦瀛樻槸鍚﹀瓨鍦?""
        return self.client.exists(key) > 0


redis_cache = RedisCache()
