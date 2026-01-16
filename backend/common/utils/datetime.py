"""日期时间工具"""
from datetime import datetime, timedelta
from typing import Optional


def now() -> datetime:
    """获取当前时间"""
    return datetime.now()


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    return dt.strftime(fmt)


def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """解析日期时间字符串"""
    try:
        return datetime.strptime(dt_str, fmt)
    except ValueError:
        return None


def add_days(dt: datetime, days: int) -> datetime:
    """添加天数"""
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    """添加小时"""
    return dt + timedelta(hours=hours)