# -*- coding: utf-8 -*-
"""
鏉冮檺缂撳瓨鏈嶅姟

鍔熻兘璇存槑锛?1. 鐢ㄦ埛鏉冮檺缂撳瓨
2. 瑙掕壊鏉冮檺缂撳瓨
3. 鑿滃崟鏉冮檺缂撳瓨

浣跨敤绀轰緥锛?    from app.services.permission_cache_service import PermissionCacheService
    
    permission_cache_service = PermissionCacheService()
    # 缂撳瓨鐢ㄦ埛鏉冮檺
    permission_cache_service.cache_user_permissions("user_001", permissions)
"""

from typing import Optional, List, Dict, Any
from loguru import logger
import json

from common.cache.redis import redis_cache


class PermissionCacheService:
    """
    鏉冮檺缂撳瓨鏈嶅姟
    
    鍔熻兘锛?    - 鐢ㄦ埛鏉冮檺缂撳瓨
    - 瑙掕壊鏉冮檺缂撳瓨
    - 鑿滃崟鏉冮檺缂撳瓨
    
    浣跨敤鏂规硶锛?        permission_cache_service = PermissionCacheService()
        permission_cache_service.cache_user_permissions("user_001", permissions)
    """
    
    # 缂撳瓨閿墠缂€
    CACHE_PREFIX_USER = "user:permissions:"
    CACHE_PREFIX_ROLE = "role:permissions:"
    CACHE_PREFIX_MENU = "user:menus:"
    
    # 缂撳瓨杩囨湡鏃堕棿锛堢锛?    CACHE_TTL = 3600  # 1灏忔椂
    
    def __init__(self):
        """鍒濆鍖栨潈闄愮紦瀛樻湇鍔?""
        self.redis = redis_cache
    
    def cache_user_permissions(self, user_id: str, permissions: List[str]) -> bool:
        """
        缂撳瓨鐢ㄦ埛鏉冮檺
        
        Args:
            user_id: 用户ID
            permissions: 鏉冮檺鍒楄〃
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            key = f"{self.CACHE_PREFIX_USER}{user_id}"
            value = json.dumps(permissions)
            self.redis.set(key, value, self.CACHE_TTL)
            logger.info(f"缂撳瓨鐢ㄦ埛鏉冮檺: user_id={user_id}, permissions_count={len(permissions)}")
            return True
        except Exception as e:
            logger.error(f"缂撳瓨鐢ㄦ埛鏉冮檺澶辫触: user_id={user_id}, error={str(e)}")
            return False
    
    def get_user_permissions(self, user_id: str) -> Optional[List[str]]:
        """
        鑾峰彇鐢ㄦ埛鏉冮檺缂撳瓨
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[List[str]]: 鏉冮檺鍒楄〃锛屼笉瀛樺湪杩斿洖None
        """
        try:
            key = f"{self.CACHE_PREFIX_USER}{user_id}"
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"鑾峰彇鐢ㄦ埛鏉冮檺缂撳瓨澶辫触: user_id={user_id}, error={str(e)}")
            return None
    
    def invalidate_user_permissions(self, user_id: str) -> bool:
        """
        浣跨敤鎴锋潈闄愮紦瀛樺け鏁?        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            key = f"{self.CACHE_PREFIX_USER}{user_id}"
            self.redis.delete(key)
            logger.info(f"浣跨敤鎴锋潈闄愮紦瀛樺け鏁? user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"浣跨敤鎴锋潈闄愮紦瀛樺け鏁堝け璐? user_id={user_id}, error={str(e)}")
            return False
    
    def cache_role_permissions(self, role_id: str, permissions: List[str]) -> bool:
        """
        缂撳瓨瑙掕壊鏉冮檺
        
        Args:
            role_id: 角色ID
            permissions: 鏉冮檺鍒楄〃
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            key = f"{self.CACHE_PREFIX_ROLE}{role_id}"
            value = json.dumps(permissions)
            self.redis.set(key, value, self.CACHE_TTL)
            logger.info(f"缂撳瓨瑙掕壊鏉冮檺: role_id={role_id}, permissions_count={len(permissions)}")
            return True
        except Exception as e:
            logger.error(f"缂撳瓨瑙掕壊鏉冮檺澶辫触: role_id={role_id}, error={str(e)}")
            return False
    
    def get_role_permissions(self, role_id: str) -> Optional[List[str]]:
        """
        鑾峰彇瑙掕壊鏉冮檺缂撳瓨
        
        Args:
            role_id: 角色ID
        
        Returns:
            Optional[List[str]]: 鏉冮檺鍒楄〃锛屼笉瀛樺湪杩斿洖None
        """
        try:
            key = f"{self.CACHE_PREFIX_ROLE}{role_id}"
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"鑾峰彇瑙掕壊鏉冮檺缂撳瓨澶辫触: role_id={role_id}, error={str(e)}")
            return None
    
    def invalidate_role_permissions(self, role_id: str) -> bool:
        """
        浣胯鑹叉潈闄愮紦瀛樺け鏁?        
        Args:
            role_id: 角色ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            key = f"{self.CACHE_PREFIX_ROLE}{role_id}"
            self.redis.delete(key)
            logger.info(f"浣胯鑹叉潈闄愮紦瀛樺け鏁? role_id={role_id}")
            return True
        except Exception as e:
            logger.error(f"浣胯鑹叉潈闄愮紦瀛樺け鏁堝け璐? role_id={role_id}, error={str(e)}")
            return False
    
    def cache_user_menus(self, user_id: str, menus: List[Dict[str, Any]]) -> bool:
        """
        缂撳瓨鐢ㄦ埛鑿滃崟
        
        Args:
            user_id: 用户ID
            menus: 鑿滃崟鍒楄〃
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            key = f"{self.CACHE_PREFIX_MENU}{user_id}"
            value = json.dumps(menus)
            self.redis.set(key, value, self.CACHE_TTL)
            logger.info(f"缂撳瓨鐢ㄦ埛鑿滃崟: user_id={user_id}, menus_count={len(menus)}")
            return True
        except Exception as e:
            logger.error(f"缂撳瓨鐢ㄦ埛鑿滃崟澶辫触: user_id={user_id}, error={str(e)}")
            return False
    
    def get_user_menus(self, user_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        鑾峰彇鐢ㄦ埛鑿滃崟缂撳瓨
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[List[Dict[str, Any]]]: 鑿滃崟鍒楄〃锛屼笉瀛樺湪杩斿洖None
        """
        try:
            key = f"{self.CACHE_PREFIX_MENU}{user_id}"
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"鑾峰彇鐢ㄦ埛鑿滃崟缂撳瓨澶辫触: user_id={user_id}, error={str(e)}")
            return None
    
    def invalidate_user_menus(self, user_id: str) -> bool:
        """
        浣跨敤鎴疯彍鍗曠紦瀛樺け鏁?        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            key = f"{self.CACHE_PREFIX_MENU}{user_id}"
            self.redis.delete(key)
            logger.info(f"浣跨敤鎴疯彍鍗曠紦瀛樺け鏁? user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"浣跨敤鎴疯彍鍗曠紦瀛樺け鏁堝け璐? user_id={user_id}, error={str(e)}")
            return False
    
    def invalidate_all_user_cache(self, user_id: str) -> bool:
        """
        浣跨敤鎴锋墍鏈夌紦瀛樺け鏁?        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 鏄惁鎴愬姛
        """
        try:
            # 浣跨敤鎴锋潈闄愮紦瀛樺け鏁?            self.invalidate_user_permissions(user_id)
            # 浣跨敤鎴疯彍鍗曠紦瀛樺け鏁?            self.invalidate_user_menus(user_id)
            logger.info(f"浣跨敤鎴锋墍鏈夌紦瀛樺け鏁? user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"浣跨敤鎴锋墍鏈夌紦瀛樺け鏁堝け璐? user_id={user_id}, error={str(e)}")
            return False
