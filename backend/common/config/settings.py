"""
应用配置模块

功能说明：
1. 使用 Pydantic 管理配置
2. 支持环境变量覆盖
3. 支持多环境配置（开发、测试、生产）
4. 提供配置验证

使用示例：
    from common.config.settings import settings
    
    # 访问配置
    print(settings.APP_NAME)
    print(settings.DB_HOST)
    
    # 访问数据库配置
    print(settings.DATABASE_URL)
    
    # 访问Redis配置
    print(settings.REDIS_HOST)
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """
    应用配置类
    
    功能：
    - 从环境变量读取配置
    - 提供配置验证
    - 支持默认值
    
    使用方法：
        settings = Settings()
        print(settings.APP_NAME)
    """
    
    # ========== 应用配置 ==========
    APP_NAME: str = Field(default="企业级AI综合管理平台", description="应用名称")
    APP_ENV: str = Field(default="development", description="运行环境")
    APP_DEBUG: bool = Field(default=True, description="调试模式")
    APP_PORT: int = Field(default=8000, description="应用端口")
    APP_HOST: str = Field(default="0.0.0.0", description="应用主机")
    
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
    
    # ========== Oracle数据源配置 ==========
    ORACLE_HOST: Optional[str] = Field(default="", description="Oracle主机")
    ORACLE_PORT: int = Field(default=1521, description="Oracle端口")
    ORACLE_SERVICE_NAME: Optional[str] = Field(default="", description="Oracle服务名")
    ORACLE_USER: Optional[str] = Field(default="", description="Oracle用户名")
    ORACLE_PASSWORD: Optional[str] = Field(default="", description="Oracle密码")
    
    # ========== PostgreSQL数据源配置 ==========
    POSTGRESQL_HOST: Optional[str] = Field(default="", description="PostgreSQL主机")
    POSTGRESQL_PORT: int = Field(default=5432, description="PostgreSQL端口")
    POSTGRESQL_DATABASE: Optional[str] = Field(default="", description="PostgreSQL数据库名")
    POSTGRESQL_USER: Optional[str] = Field(default="", description="PostgreSQL用户名")
    POSTGRESQL_PASSWORD: Optional[str] = Field(default="", description="PostgreSQL密码")
    
    # ========== Redis配置 ==========
    CACHE_ENABLED: bool = Field(default=True, description="是否启用缓存")
    CACHE_TYPE: str = Field(default="local", description="缓存类型")
    REDIS_HOST: str = Field(default="127.0.0.1", description="Redis主机")
    REDIS_PORT: int = Field(default=6379, description="Redis端口")
    REDIS_PASSWORD: Optional[str] = Field(default="", description="Redis密码")
    REDIS_DB: int = Field(default=0, description="Redis数据库编号")
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Redis最大连接数")
    
    # ========== Nacos配置 ==========
    USE_NACOS: bool = Field(default=False, description="是否使用Nacos")
    NACOS_HOST: str = Field(default="127.0.0.1", description="Nacos主机")
    NACOS_PORT: int = Field(default=8848, description="Nacos端口")
    NACOS_NAMESPACE: str = Field(default="mcp-platform", description="Nacos命名空间")
    NACOS_USERNAME: str = Field(default="nacos", description="Nacos用户名")
    NACOS_PASSWORD: str = Field(default="nacos", description="Nacos密码")
    
    # ========== RabbitMQ配置 ==========
    USE_RABBITMQ: bool = Field(default=False, description="是否使用RabbitMQ")
    RABBITMQ_HOST: str = Field(default="localhost", description="RabbitMQ主机")
    RABBITMQ_PORT: int = Field(default=5672, description="RabbitMQ端口")
    RABBITMQ_USERNAME: str = Field(default="admin", description="RabbitMQ用户名")
    RABBITMQ_PASSWORD: str = Field(default="admin123", description="RabbitMQ密码")
    RABBITMQ_VHOST: str = Field(default="/", description="RabbitMQ虚拟主机")
    
    # ========== JWT配置 ==========
    JWT_SECRET: str = Field(default="your-secret-key-change-in-production", description="JWT密钥")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT算法")
    JWT_EXPIRE_MINUTES: int = Field(default=1440, description="JWT过期时间（分钟）")
    JWT_REFRESH_EXPIRE_DAYS: int = Field(default=7, description="JWT刷新过期时间（天）")
    
    # ========== API Key配置 ==========
    API_KEY_SECRET: str = Field(default="your-api-key-secret", description="API Key密钥")
    
    # ========== 日志配置 ==========
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    LOG_FILE_PATH: str = Field(default="logs/app.log", description="日志文件路径")
    LOG_ROTATION: str = Field(default="100 MB", description="日志轮转大小")
    LOG_RETENTION: str = Field(default="30 days", description="日志保留时间")
    
    # ========== 文件上传配置 ==========
    UPLOAD_PATH: str = Field(default="uploads", description="上传文件路径")
    MAX_UPLOAD_SIZE: int = Field(default=10485760, description="最大上传大小（字节）")
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "application/pdf"],
        description="允许的文件类型"
    )
    
    # ========== 监控配置 ==========
    USE_MONITORING: bool = Field(default=False, description="是否启用监控")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus端口")
    USE_JAEGER: bool = Field(default=False, description="是否使用Jaeger")
    JAEGER_HOST: str = Field(default="localhost", description="Jaeger主机")
    JAEGER_PORT: int = Field(default=6831, description="Jaeger端口")
    
    # ========== 限流熔断配置 ==========
    USE_SENTINEL: bool = Field(default=False, description="是否使用Sentinel")
    SENTINEL_HOST: str = Field(default="localhost", description="Sentinel主机")
    SENTINEL_PORT: int = Field(default=8719, description="Sentinel端口")
    
    # ========== API网关配置 ==========
    USE_APISIX: bool = Field(default=False, description="是否使用APISIX")
    APISIX_HOST: str = Field(default="localhost", description="APISIX主机")
    APISIX_PORT: int = Field(default=9080, description="APISIX端口")
    APISIX_ADMIN_KEY: str = Field(default="", description="APISIX管理密钥")
    
    # ========== CORS配置 ==========
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="允许的CORS来源"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="允许携带凭证")
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["*"],
        description="允许的HTTP方法"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"],
        description="允许的HTTP头"
    )
    
    # ========== 分页配置 ==========
    DEFAULT_PAGE_SIZE: int = Field(default=10, description="默认页大小")
    MAX_PAGE_SIZE: int = Field(default=100, description="最大页大小")
    PAGE_SIZE_OPTIONS: List[int] = Field(
        default=[10, 20, 50, 100],
        description="页大小选项"
    )
    
    class Config:
        """Pydantic配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("APP_ENV")
    def validate_app_env(cls, v):
        """验证运行环境"""
        if v not in ["development", "testing", "production"]:
            raise ValueError(f"无效的运行环境: {v}")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """验证日志级别"""
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"无效的日志级别: {v}")
        return v
    
    @property
    def DATABASE_URL(self) -> str:
        """
        构建数据库连接URL
        
        Returns:
            str: 数据库连接URL
        
        使用示例：
            print(settings.DATABASE_URL)
            # mysql+pymysql://root:12345678@localhost:3306/mcp_platform
        """
        if self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"
        elif self.DB_TYPE == "postgresql":
            return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == "oracle":
            return f"oracle+oracledb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"不支持的数据库类型: {self.DB_TYPE}")
    
    @property
    def IS_DEVELOPMENT(self) -> bool:
        """是否为开发环境"""
        return self.APP_ENV == "development"
    
    @property
    def IS_PRODUCTION(self) -> bool:
        """是否为生产环境"""
        return self.APP_ENV == "production"
    
    @property
    def IS_TESTING(self) -> bool:
        """是否为测试环境"""
        return self.APP_ENV == "testing"
    
    def __repr__(self) -> str:
        return f"<Settings(app_name='{self.APP_NAME}', env='{self.APP_ENV}')>"


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置实例（单例模式）
    
    Returns:
        Settings: 配置实例
    
    使用示例：
        settings = get_settings()
        print(settings.APP_NAME)
    """
    return Settings()


# 全局配置实例
settings = get_settings()