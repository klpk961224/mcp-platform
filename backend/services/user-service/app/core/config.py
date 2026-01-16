"""
用户域服务配置模块
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """配置类"""
    
    APP_NAME: str = "用户域服务"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8002
    
    DATABASE_URL: str
    
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    AUTH_SERVICE_URL: str = "http://localhost:8001/api/v1"
    
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = "logs/user-service.log"
    
    class Config:
        env_file = ".env.development"
        case_sensitive = True


settings = Settings()