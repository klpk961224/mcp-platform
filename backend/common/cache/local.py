"""本地缓存模块"""
from typing import Optional, Dict
from datetime import datetime, timedelta
from loguru import logger


class LocalCache:
    """本地缓存类"""
    
    def __init__(self):
        self.cache: Dict[str, tuple[str, datetime]] = {}
        logger.info("本地缓存初始化完成")
    
    def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        if key not in self.cache:
            return None
        
        value, expire_time = self.cache[key]
        if datetime.now() > expire_time:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: str, ttl: int = 3600):
        """设置缓存"""
        expire_time = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expire_time)
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self.cache:
            del self.cache[key]
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return self.get(key) is not None


local_cache = LocalCache()