"""
系统域服务配置模块

功能说明：
1. 从环境变量加载配置
2. 提供配置访问接口

使用示例：
    from app.core.config import settings
    
    print(settings.APP_NAME)
    print(settings.DATABASE_URL)
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """配置类"""
    
    # 应用配置
    APP_NAME: str = "系统域服务"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 228004
    
    # 数据库配置
    DATABASE_URL: str
    
    # Redis配置
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # JWT配置
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # API Key配置
    API_KEY_SECRET: str
    
    # 日志配置
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = "logs/system-service.log"
    
    class Config:
        env_file = ".env.development"
        case_sensitive = True


settings = Settings()