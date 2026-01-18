# -*- coding: utf-8 -*-
"""
鐢ㄦ埛鏈嶅姟妯″瀷

鍖呭惈锛?- User: 鐢ㄦ埛妯″瀷
- Department: 閮ㄩ棬妯″瀷锛堜粠common瀵煎叆锛?- Tenant: 绉熸埛妯″瀷锛堜粠common瀵煎叆锛?"""

from .user import User
from common.database.models import Department, Tenant

__all__ = ["User", "Department", "Tenant"]
