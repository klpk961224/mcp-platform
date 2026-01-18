"""验证器"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """验证手机号格式（中国大陆）"""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_username(username: str) -> bool:
    """验证用户名格式"""
    pattern = r'^[a-zA-Z0-9_]{4,20}$'
    return re.match(pattern, username) is not None


def validate_password(password: str) -> bool:
    """验证密码格式"""
    return len(password) >= 6


def validate_url(url: str) -> bool:
    """验证URL格式"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None