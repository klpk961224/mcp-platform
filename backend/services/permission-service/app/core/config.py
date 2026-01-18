"""
权限域服务￠厤缃ā鍧?"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """閰嶇疆绫?""
    
    APP_NAME: str = "权限域服务?
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 228003
    
    DATABASE_URL: str
    
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    AUTH_SERVICE_URL: str = "http://localhost:228001/api/v1"
    
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = "logs/permission-service.log"
    
    class Config:
        env_file = ".env.development"
        case_sensitive = True


settings = Settings()
