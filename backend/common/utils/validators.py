"""楠岃瘉鍣?""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """楠岃瘉閭鏍煎紡"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """楠岃瘉鎵嬫満鍙锋牸寮忥紙涓浗澶ч檰锛?""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_username(username: str) -> bool:
    """楠岃瘉鐢ㄦ埛鍚嶆牸寮?""
    pattern = r'^[a-zA-Z0-9_]{4,20}$'
    return re.match(pattern, username) is not None


def validate_password(password: str) -> bool:
    """楠岃瘉瀵嗙爜鏍煎紡"""
    return len(password) >= 6


def validate_url(url: str) -> bool:
    """楠岃瘉URL鏍煎紡"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None
