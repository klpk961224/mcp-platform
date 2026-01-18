"""
搴旂敤閰嶇疆妯″潡

鍔熻兘璇存槑锛?
1. 浣跨敤 Pydantic 绠＄悊閰嶇疆
2. 鏀寔鐜鍙橀噺瑕嗙洊
3. 鏀寔澶氱幆澧冮厤缃紙寮€鍙戙€佹祴璇曘€佺敓浜э級
4. 鎻愪緵閰嶇疆楠岃瘉

浣跨敤绀轰緥锛?
    from common.config.settings import settings
    
    # 璁块棶閰嶇疆
    print(settings.APP_NAME)
    print(settings.DB_HOST)
    
    # 璁块棶鏁版嵁搴撻厤缃?
    print(settings.DATABASE_URL)
    
    # 璁块棶Redis閰嶇疆
    print(settings.REDIS_HOST)
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """
    搴旂敤閰嶇疆绫?
    
    鍔熻兘锛?
    - 浠庣幆澧冨彉閲忚鍙栭厤缃?
    - 鎻愪緵閰嶇疆楠岃瘉
    - 鏀寔榛樿鍊?
    
    浣跨敤鏂规硶锛?
        settings = Settings()
        print(settings.APP_NAME)
    """
    
    # ========== 搴旂敤閰嶇疆 ==========
    APP_NAME: str = Field(default="浼佷笟绾I缁煎悎绠＄悊骞冲彴", description="搴旂敤鍚嶇О")
    APP_ENV: str = Field(default="development", description="杩愯鐜")
    APP_DEBUG: bool = Field(default=True, description="璋冭瘯妯″紡")
    APP_PORT: int = Field(default=8000, description="搴旂敤绔彛")
    APP_HOST: str = Field(default="0.0.0.0", description="搴旂敤涓绘満")
    
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
    
    # ========== Oracle鏁版嵁婧愰厤缃?==========
    ORACLE_HOST: Optional[str] = Field(default="", description="Oracle涓绘満")
    ORACLE_PORT: int = Field(default=1521, description="Oracle绔彛")
    ORACLE_SERVICE_NAME: Optional[str] = Field(default="", description="Oracle鏈嶅姟鍚?)
    ORACLE_USER: Optional[str] = Field(default="", description="Oracle鐢ㄦ埛鍚?)
    ORACLE_PASSWORD: Optional[str] = Field(default="", description="Oracle瀵嗙爜")
    
    # ========== PostgreSQL鏁版嵁婧愰厤缃?==========
    POSTGRESQL_HOST: Optional[str] = Field(default="", description="PostgreSQL涓绘満")
    POSTGRESQL_PORT: int = Field(default=5432, description="PostgreSQL绔彛")
    POSTGRESQL_DATABASE: Optional[str] = Field(default="", description="PostgreSQL鏁版嵁搴撳悕")
    POSTGRESQL_USER: Optional[str] = Field(default="", description="PostgreSQL鐢ㄦ埛鍚?)
    POSTGRESQL_PASSWORD: Optional[str] = Field(default="", description="PostgreSQL瀵嗙爜")
    
    # ========== Redis閰嶇疆 ==========
    CACHE_ENABLED: bool = Field(default=True, description="鏄惁鍚敤缂撳瓨")
    CACHE_TYPE: str = Field(default="local", description="缂撳瓨绫诲瀷")
    REDIS_HOST: str = Field(default="127.0.0.1", description="Redis涓绘満")
    REDIS_PORT: int = Field(default=6379, description="Redis绔彛")
    REDIS_PASSWORD: Optional[str] = Field(default="", description="Redis瀵嗙爜")
    REDIS_DB: int = Field(default=0, description="Redis鏁版嵁搴撶紪鍙?)
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Redis鏈€澶ц繛鎺ユ暟")
    
    # ========== Nacos閰嶇疆 ==========
    USE_NACOS: bool = Field(default=False, description="鏄惁浣跨敤Nacos")
    NACOS_HOST: str = Field(default="127.0.0.1", description="Nacos涓绘満")
    NACOS_PORT: int = Field(default=8848, description="Nacos绔彛")
    NACOS_NAMESPACE: str = Field(default="mcp-platform", description="Nacos鍛藉悕绌洪棿")
    NACOS_USERNAME: str = Field(default="nacos", description="Nacos鐢ㄦ埛鍚?)
    NACOS_PASSWORD: str = Field(default="nacos", description="Nacos瀵嗙爜")
    
    # ========== RabbitMQ閰嶇疆 ==========
    USE_RABBITMQ: bool = Field(default=False, description="鏄惁浣跨敤RabbitMQ")
    RABBITMQ_HOST: str = Field(default="localhost", description="RabbitMQ涓绘満")
    RABBITMQ_PORT: int = Field(default=5672, description="RabbitMQ绔彛")
    RABBITMQ_USERNAME: str = Field(default="admin", description="RabbitMQ鐢ㄦ埛鍚?)
    RABBITMQ_PASSWORD: str = Field(default="admin123", description="RabbitMQ瀵嗙爜")
    RABBITMQ_VHOST: str = Field(default="/", description="RabbitMQ铏氭嫙涓绘満")
    
    # ========== JWT閰嶇疆 ==========
    JWT_SECRET: str = Field(default="your-secret-key-change-in-production", description="JWT瀵嗛挜")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT绠楁硶")
    JWT_EXPIRE_MINUTES: int = Field(default=1440, description="JWT杩囨湡鏃堕棿锛堝垎閽燂級")
    JWT_REFRESH_EXPIRE_DAYS: int = Field(default=7, description="JWT鍒锋柊杩囨湡鏃堕棿锛堝ぉ锛?)
    
    # ========== API Key閰嶇疆 ==========
    API_KEY_SECRET: str = Field(default="your-api-key-secret", description="API Key瀵嗛挜")
    
    # ========== 鏃ュ織閰嶇疆 ==========
    LOG_LEVEL: str = Field(default="INFO", description="鏃ュ織绾у埆")
    LOG_FILE_PATH: str = Field(default="logs/app.log", description="鏃ュ織鏂囦欢璺緞")
    LOG_ROTATION: str = Field(default="100 MB", description="鏃ュ織杞浆澶у皬")
    LOG_RETENTION: str = Field(default="30 days", description="鏃ュ織淇濈暀鏃堕棿")
    
    # ========== 鏂囦欢涓婁紶閰嶇疆 ==========
    UPLOAD_PATH: str = Field(default="uploads", description="涓婁紶鏂囦欢璺緞")
    MAX_UPLOAD_SIZE: int = Field(default=10485760, description="鏈€澶т笂浼犲ぇ灏忥紙瀛楄妭锛?)
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "application/pdf"],
        description="鍏佽鐨勬枃浠剁被鍨?
    )
    
    # ========== 鐩戞帶閰嶇疆 ==========
    USE_MONITORING: bool = Field(default=False, description="鏄惁鍚敤鐩戞帶")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus绔彛")
    USE_JAEGER: bool = Field(default=False, description="鏄惁浣跨敤Jaeger")
    JAEGER_HOST: str = Field(default="localhost", description="Jaeger涓绘満")
    JAEGER_PORT: int = Field(default=6831, description="Jaeger绔彛")
    
    # ========== 闄愭祦鐔旀柇閰嶇疆 ==========
    USE_SENTINEL: bool = Field(default=False, description="鏄惁浣跨敤Sentinel")
    SENTINEL_HOST: str = Field(default="localhost", description="Sentinel涓绘満")
    SENTINEL_PORT: int = Field(default=8719, description="Sentinel绔彛")
    
    # ========== API缃戝叧閰嶇疆 ==========
    USE_APISIX: bool = Field(default=False, description="鏄惁浣跨敤APISIX")
    APISIX_HOST: str = Field(default="localhost", description="APISIX涓绘満")
    APISIX_PORT: int = Field(default=9080, description="APISIX绔彛")
    APISIX_ADMIN_KEY: str = Field(default="", description="APISIX绠＄悊瀵嗛挜")
    
    # ========== CORS閰嶇疆 ==========
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="鍏佽鐨凜ORS鏉ユ簮"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="鍏佽鎼哄甫鍑瘉")
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["*"],
        description="鍏佽鐨凥TTP鏂规硶"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"],
        description="鍏佽鐨凥TTP澶?
    )
    
    # ========== 鍒嗛〉閰嶇疆 ==========
    DEFAULT_PAGE_SIZE: int = Field(default=10, description="榛樿椤靛ぇ灏?)
    MAX_PAGE_SIZE: int = Field(default=100, description="鏈€澶ч〉澶у皬")
    PAGE_SIZE_OPTIONS: List[int] = Field(
        default=[10, 20, 50, 100],
        description="椤靛ぇ灏忛€夐」"
    )
    
    class Config:
        """Pydantic閰嶇疆"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("APP_ENV")
    def validate_app_env(cls, v):
        """楠岃瘉杩愯鐜"""
        if v not in ["development", "testing", "production"]:
            raise ValueError(f"鏃犳晥鐨勮繍琛岀幆澧? {v}")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """楠岃瘉鏃ュ織绾у埆"""
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"鏃犳晥鐨勬棩蹇楃骇鍒? {v}")
        return v
    
    @property
    def DATABASE_URL(self) -> str:
        """
        鏋勫缓鏁版嵁搴撹繛鎺RL
        
        Returns:
            str: 鏁版嵁搴撹繛鎺RL
        
        浣跨敤绀轰緥锛?
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
            raise ValueError(f"涓嶆敮鎸佺殑鏁版嵁搴撶被鍨? {self.DB_TYPE}")
    
    @property
    def IS_DEVELOPMENT(self) -> bool:
        """鏄惁涓哄紑鍙戠幆澧?""
        return self.APP_ENV == "development"
    
    @property
    def IS_PRODUCTION(self) -> bool:
        """鏄惁涓虹敓浜х幆澧?""
        return self.APP_ENV == "production"
    
    @property
    def IS_TESTING(self) -> bool:
        """鏄惁涓烘祴璇曠幆澧?""
        return self.APP_ENV == "testing"
    
    def __repr__(self) -> str:
        return f"<Settings(app_name='{self.APP_NAME}', env='{self.APP_ENV}')>"


@lru_cache()
def get_settings() -> Settings:
    """
    鑾峰彇閰嶇疆瀹炰緥锛堝崟渚嬫ā寮忥級
    
    Returns:
        Settings: 閰嶇疆瀹炰緥
    
    浣跨敤绀轰緥锛?
        settings = get_settings()
        print(settings.APP_NAME)
    """
    return Settings()


# 鍏ㄥ眬閰嶇疆瀹炰緥
settings = get_settings()
