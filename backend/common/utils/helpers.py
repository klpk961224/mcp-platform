"""杈呭姪鍑芥暟"""
import secrets
import string
from typing import Optional


def generate_random_string(length: int = 32) -> str:
    """鐢熸垚闅忔満瀛楃涓?""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_uuid() -> str:
    """鐢熸垚UUID"""
    return secrets.token_hex(16)


def mask_string(s: str, visible_chars: int = 4) -> str:
    """鑴辨晱瀛楃涓?""
    if len(s) <= visible_chars:
        return s
    return s[:visible_chars] + '*' * (len(s) - visible_chars)


def truncate_string(s: str, max_length: int = 100) -> str:
    """鎴柇瀛楃涓?""
    if len(s) <= max_length:
        return s
    return s[:max_length] + '...'
