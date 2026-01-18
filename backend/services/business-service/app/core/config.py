# -*- coding: utf-8 -*-
"""
涓氬姟鏈嶅姟閰嶇疆

鍔熻兘璇存槑锛?1. 涓氬姟鏈嶅姟鐗瑰畾鐨勯厤缃?2. 瑕嗙洊閫氱敤閰嶇疆
3. 鎻愪緵涓氬姟鏈嶅姟鐗规湁鐨勯厤缃」

浣跨敤绀轰緥锛?    from app.core.config import settings
    
    print(settings.APP_NAME)
    print(settings.APP_PORT)
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    涓氬姟鏈嶅姟閰嶇疆绫?    
    鍔熻兘锛?    - 涓氬姟鏈嶅姟鐗瑰畾鐨勯厤缃?    - 瑕嗙洊閫氱敤閰嶇疆鐨勯粯璁ゅ€?    - 鎻愪緵涓氬姟鏈嶅姟鐗规湁鐨勯厤缃」
    """
    
    # ========== 搴旂敤閰嶇疆 ==========
    APP_NAME: str = Field(default="涓氬姟鍩熸湇鍔?, description="搴旂敤鍚嶇О")
    APP_ENV: str = Field(default="development", description="杩愯鐜")
    APP_DEBUG: bool = Field(default=True, description="璋冭瘯妯″紡")
    APP_PORT: int = Field(default=228006, description="搴旂敤绔彛")
    
    # ========== 鏁版嵁搴撻厤缃?==========
    DB_TYPE: str = Field(default="mysql", description="鏁版嵁搴撶被鍨?)
    DB_HOST: str = Field(default="localhost", description="鏁版嵁搴撲富鏈?)
    DB_PORT: int = Field(default=3306, description="鏁版嵁搴撶鍙?)
    DB_NAME: str = Field(default="mcp_platform", description="鏁版嵁搴撳悕绉?)
    DB_USER: str = Field(default="root", description="鏁版嵁搴撶敤鎴峰悕")
    DB_PASSWORD: str = Field(default="12345678", description="鏁版嵁搴撳瘑鐮?)
    DB_CHARSET: str = Field(default="utf8mb4", description="鏁版嵁搴撳瓧绗﹂泦")
    DB_POOL_SIZE: int = Field(default=10, description="杩炴帴姹犲ぇ灏?)
    DB_MAX_OVERFLOW: int = Field(default=20, description="鏈€澶ф孩鍑鸿繛鎺ユ暟")
    DB_ECHO: bool = Field(default=False, description="鏄惁鎵撳嵃SQL")
    
    class Config:
        """Pydantic閰嶇疆"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @property
    def DATABASE_URL(self) -> str:
        """
        鏋勫缓鏁版嵁搴撹繛鎺RL
        
        Returns:
            str: 鏁版嵁搴撹繛鎺RL
        """
        if self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"
        else:
            raise ValueError(f"涓嶆敮鎸佺殑鏁版嵁搴撶被鍨? {self.DB_TYPE}")


@lru_cache()
def get_settings() -> Settings:
    """
    鑾峰彇閰嶇疆瀹炰緥锛堝崟渚嬫ā寮忥級
    
    Returns:
        Settings: 閰嶇疆瀹炰緥
    """
    return Settings()


# 鍏ㄥ眬閰嶇疆瀹炰緥
settings = get_settings()
