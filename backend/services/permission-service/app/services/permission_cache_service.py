# -*- coding: utf-8 -*-
"""
权限缓存服务

功能说明：
1. 用户权限缓存
2. 角色权限缓存
3. 菜单权限缓存

使用示例：
    from app.services.permission_cache_service import PermissionCacheService
    
    permission_cache_service = PermissionCacheService()
    # 缓存用户权限
    permission_cache_service.cache_user_permissions("user_001", permissions)
"""

from typing import Optional, List, Dict, Any
from loguru import logger
import json

from common.cache.redis import redis_cache


class PermissionCacheService:
    """
    权限缓存服务
    
    功能：
    - 用户权限缓存
    - 角色权限缓存
    - 菜单权限缓存
    
    使用方法：
        permission_cache_service = PermissionCacheService()
        permission_cache_service.cache_user_permissions("user_001", permissions)
    """
    
    # 缓存键前缀
    CACHE_PREFIX_USER = "user:permissions:"
    CACHE_PREFIX_ROLE = "role:permissions:"
    CACHE_PREFIX_MENU = "user:menus:"
    
    # 缓存过期时间（秒）
    CACHE_TTL = 3600  # 1小时
    
    def __init__(self):
        """初始化权限缓存服务"""
        self.redis = redis_cache
    
    def cache_user_permissions(self, user_id: str, permissions: List[str]) -> bool:
        """
        缓存用户权限
        
        Args:
            user_id: 用户ID
            permissions: 权限列表
        
        Returns:
            bool: 是否成功
        """
        try:
            key = f"{self.CACHE_PREFIX_USER}{user_id}"
            value = json.dumps(permissions)
            self.redis.set(key, value, self.CACHE_TTL)
            logger.info(f"缓存用户权限: user_id={user_id}, permissions_count={len(permissions)}")
            return True
        except Exception as e:
            logger.error(f"缓存用户权限失败: user_id={user_id}, error={str(e)}")
            return False
    
    def get_user_permissions(self, user_id: str) -> Optional[List[str]]:
        """
        获取用户权限缓存
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[List[str]]: 权限列表，不存在返回None
        """
        try:
            key = f"{self.CACHE_PREFIX_USER}{user_id}"
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"获取用户权限缓存失败: user_id={user_id}, error={str(e)}")
            return None
    
    def invalidate_user_permissions(self, user_id: str) -> bool:
        """
        使用户权限缓存失效
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否成功
        """
        try:
            key = f"{self.CACHE_PREFIX_USER}{user_id}"
            self.redis.delete(key)
            logger.info(f"使用户权限缓存失效: user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"使用户权限缓存失效失败: user_id={user_id}, error={str(e)}")
            return False
    
    def cache_role_permissions(self, role_id: str, permissions: List[str]) -> bool:
        """
        缓存角色权限
        
        Args:
            role_id: 角色ID
            permissions: 权限列表
        
        Returns:
            bool: 是否成功
        """
        try:
            key = f"{self.CACHE_PREFIX_ROLE}{role_id}"
            value = json.dumps(permissions)
            self.redis.set(key, value, self.CACHE_TTL)
            logger.info(f"缓存角色权限: role_id={role_id}, permissions_count={len(permissions)}")
            return True
        except Exception as e:
            logger.error(f"缓存角色权限失败: role_id={role_id}, error={str(e)}")
            return False
    
    def get_role_permissions(self, role_id: str) -> Optional[List[str]]:
        """
        获取角色权限缓存
        
        Args:
            role_id: 角色ID
        
        Returns:
            Optional[List[str]]: 权限列表，不存在返回None
        """
        try:
            key = f"{self.CACHE_PREFIX_ROLE}{role_id}"
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"获取角色权限缓存失败: role_id={role_id}, error={str(e)}")
            return None
    
    def invalidate_role_permissions(self, role_id: str) -> bool:
        """
        使角色权限缓存失效
        
        Args:
            role_id: 角色ID
        
        Returns:
            bool: 是否成功
        """
        try:
            key = f"{self.CACHE_PREFIX_ROLE}{role_id}"
            self.redis.delete(key)
            logger.info(f"使角色权限缓存失效: role_id={role_id}")
            return True
        except Exception as e:
            logger.error(f"使角色权限缓存失效失败: role_id={role_id}, error={str(e)}")
            return False
    
    def cache_user_menus(self, user_id: str, menus: List[Dict[str, Any]]) -> bool:
        """
        缓存用户菜单
        
        Args:
            user_id: 用户ID
            menus: 菜单列表
        
        Returns:
            bool: 是否成功
        """
        try:
            key = f"{self.CACHE_PREFIX_MENU}{user_id}"
            value = json.dumps(menus)
            self.redis.set(key, value, self.CACHE_TTL)
            logger.info(f"缓存用户菜单: user_id={user_id}, menus_count={len(menus)}")
            return True
        except Exception as e:
            logger.error(f"缓存用户菜单失败: user_id={user_id}, error={str(e)}")
            return False
    
    def get_user_menus(self, user_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        获取用户菜单缓存
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[List[Dict[str, Any]]]: 菜单列表，不存在返回None
        """
        try:
            key = f"{self.CACHE_PREFIX_MENU}{user_id}"
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"获取用户菜单缓存失败: user_id={user_id}, error={str(e)}")
            return None
    
    def invalidate_user_menus(self, user_id: str) -> bool:
        """
        使用户菜单缓存失效
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否成功
        """
        try:
            key = f"{self.CACHE_PREFIX_MENU}{user_id}"
            self.redis.delete(key)
            logger.info(f"使用户菜单缓存失效: user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"使用户菜单缓存失效失败: user_id={user_id}, error={str(e)}")
            return False
    
    def invalidate_all_user_cache(self, user_id: str) -> bool:
        """
        使用户所有缓存失效
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否成功
        """
        try:
            # 使用户权限缓存失效
            self.invalidate_user_permissions(user_id)
            # 使用户菜单缓存失效
            self.invalidate_user_menus(user_id)
            logger.info(f"使用户所有缓存失效: user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"使用户所有缓存失效失败: user_id={user_id}, error={str(e)}")
            return False