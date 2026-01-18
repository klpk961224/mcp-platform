"""
绯荤粺鍩熸湇鍔￠厤缃ā鍧?
鍔熻兘璇存槑锛?1. 浠庣幆澧冨彉閲忓姞杞介厤缃?2. 鎻愪緵閰嶇疆璁块棶鎺ュ彛

浣跨敤绀轰緥锛?    from app.core.config import settings
    
    print(settings.APP_NAME)
    print(settings.DATABASE_URL)
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """閰嶇疆绫?""
    
    # 搴旂敤閰嶇疆
    APP_NAME: str = "绯荤粺鍩熸湇鍔?
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 228004
    
    # 鏁版嵁搴撻厤缃?    DATABASE_URL: str
    
    # Redis閰嶇疆
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # JWT閰嶇疆
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # API Key閰嶇疆
    API_KEY_SECRET: str
    
    # 鏃ュ織閰嶇疆
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = "logs/system-service.log"
    
    class Config:
        env_file = ".env.development"
        case_sensitive = True


settings = Settings()
