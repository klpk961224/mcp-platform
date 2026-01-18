# -*- coding: utf-8 -*-
"""
业务服务配置

功能说明：
1. 业务服务特定的配置
2. 覆盖通用配置
3. 提供业务服务特有的配置项

使用示例：
    from app.core.config import settings
    
    print(settings.APP_NAME)
    print(settings.APP_PORT)
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    业务服务配置类
    
    功能：
    - 业务服务特定的配置
    - 覆盖通用配置的默认值
    - 提供业务服务特有的配置项
    """
    
    # ========== 应用配置 ==========
    APP_NAME: str = Field(default="业务域服务", description="应用名称")
    APP_ENV: str = Field(default="development", description="运行环境")
    APP_DEBUG: bool = Field(default=True, description="调试模式")
    APP_PORT: int = Field(default=228006, description="应用端口")
    
    # ========== 数据库配置 ==========
    DB_TYPE: str = Field(default="mysql", description="数据库类型")
    DB_HOST: str = Field(default="localhost", description="数据库主机")
    DB_PORT: int = Field(default=3306, description="数据库端口")
    DB_NAME: str = Field(default="mcp_platform", description="数据库名称")
    DB_USER: str = Field(default="root", description="数据库用户名")
    DB_PASSWORD: str = Field(default="12345678", description="数据库密码")
    DB_CHARSET: str = Field(default="utf8mb4", description="数据库字符集")
    DB_POOL_SIZE: int = Field(default=10, description="连接池大小")
    DB_MAX_OVERFLOW: int = Field(default=20, description="最大溢出连接数")
    DB_ECHO: bool = Field(default=False, description="是否打印SQL")
    
    class Config:
        """Pydantic配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @property
    def DATABASE_URL(self) -> str:
        """
        构建数据库连接URL
        
        Returns:
            str: 数据库连接URL
        """
        if self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"
        else:
            raise ValueError(f"不支持的数据库类型: {self.DB_TYPE}")


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置实例（单例模式）
    
    Returns:
        Settings: 配置实例
    """
    return Settings()


# 全局配置实例
settings = get_settings()