"""鏃ユ湡鏃堕棿宸ュ叿"""
from datetime import datetime, timedelta
from typing import Optional


def now() -> datetime:
    """鑾峰彇褰撳墠鏃堕棿"""
    return datetime.now()


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """鏍煎紡鍖栨棩鏈熸椂闂?""
    return dt.strftime(fmt)


def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """瑙ｆ瀽鏃ユ湡鏃堕棿瀛楃涓?""
    try:
        return datetime.strptime(dt_str, fmt)
    except ValueError:
        return None


def add_days(dt: datetime, days: int) -> datetime:
    """娣诲姞澶╂暟"""
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    """娣诲姞灏忔椂"""
    return dt + timedelta(hours=hours)
