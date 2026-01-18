"""鏈湴缂撳瓨妯″潡"""
from typing import Optional, Dict
from datetime import datetime, timedelta
from loguru import logger


class LocalCache:
    """鏈湴缂撳瓨绫?""
    
    def __init__(self):
        self.cache: Dict[str, tuple[str, datetime]] = {}
        logger.info("鏈湴缂撳瓨鍒濆鍖栧畬鎴?)
    
    def get(self, key: str) -> Optional[str]:
        """鑾峰彇缂撳瓨"""
        if key not in self.cache:
            return None
        
        value, expire_time = self.cache[key]
        if datetime.now() > expire_time:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: str, ttl: int = 3600):
        """璁剧疆缂撳瓨"""
        expire_time = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expire_time)
    
    def delete(self, key: str):
        """删除缂撳瓨"""
        if key in self.cache:
            del self.cache[key]
    
    def exists(self, key: str) -> bool:
        """妫€鏌ョ紦瀛樻槸鍚﹀瓨鍦?""
        return self.get(key) is not None


local_cache = LocalCache()
