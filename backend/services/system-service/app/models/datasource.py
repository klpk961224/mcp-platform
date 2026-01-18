# -*- coding: utf-8 -*-
"""
鏁版嵁婧愭ā鍨?
鍔熻兘璇存槑锛?1. 鏁版嵁婧愰厤缃?2. 鏁版嵁婧愯繛鎺ョ鐞?3. 鏁版嵁婧愬仴搴锋鏌?
浣跨敤绀轰緥锛?    from app.models.datasource import DataSource
    
    datasource = DataSource(
        name="涓绘暟鎹簱",
        type="mysql",
        host="localhost",
        port=3306,
        database="mcp_platform"
    )
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from datetime import datetime

from common.database.base import BaseModel


class DataSource(BaseModel):
    """
    鏁版嵁婧愭ā鍨?    
    鍔熻兘锛?    - 鏁版嵁婧愰厤缃?    - 鏁版嵁婧愯繛鎺ョ鐞?    - 鏁版嵁婧愬仴搴锋鏌?    
    灞炴€ц鏄庯細
    - id: 鏁版嵁婧怚D锛堜富閿級
    - tenant_id: 租户ID
    - name: 鏁版嵁婧愬悕绉?    - type: 鏁版嵁婧愮被鍨嬶紙mysql/postgresql/oracle锛?    - host: 涓绘満地址
    - port: 绔彛
    - database: 鏁版嵁搴撳悕绉?    - username: 用户名?    - password: 密码（加密）
    - charset: 瀛楃闆?    - pool_size: 杩炴帴姹犲ぇ灏?    - max_overflow: 鏈€澶ф孩鍑鸿繛鎺ユ暟
    - status: 状态侊紙active/inactive锛?    - is_default: 鏄惁默认鏁版嵁婧?    - health_check_interval: 鍋ュ悍妫€鏌ラ棿闅旓紙绉掞級
    - last_health_check_at: 鏈€鍚庡仴搴锋鏌ユ椂闂?    - is_healthy: 鏄惁鍋ュ悍
    - created_at: 创建时间
    - updated_at: 更新鏃堕棿
    """
    
    __tablename__ = "datasources"
    
    # 鍩烘湰淇℃伅
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="鏁版嵁婧愬悕绉?)
    type = Column(String(20), nullable=False, comment="鏁版嵁婧愮被鍨?)
    host = Column(String(255), nullable=False, comment="涓绘満地址")
    port = Column(Integer, nullable=False, comment="绔彛")
    database = Column(String(100), nullable=False, comment="鏁版嵁搴撳悕绉?)
    
    # 杩炴帴閰嶇疆
    username = Column(String(100), nullable=False, comment="用户名?)
    password = Column(String(255), nullable=False, comment="密码（加密）")
    charset = Column(String(20), nullable=False, default="utf8mb4", comment="瀛楃闆?)
    
    # 杩炴帴姹犻厤缃?    pool_size = Column(Integer, nullable=False, default=10, comment="杩炴帴姹犲ぇ灏?)
    max_overflow = Column(Integer, nullable=False, default=20, comment="鏈€澶ф孩鍑鸿繛鎺ユ暟")
    
    # 状态佷俊鎭?    status = Column(String(20), nullable=False, default="active", comment="状态?)
    is_default = Column(Boolean, nullable=False, default=False, comment="鏄惁默认鏁版嵁婧?)
    
    # 鍋ュ悍妫€鏌ラ厤缃?    health_check_interval = Column(Integer, nullable=False, default=60, comment="鍋ュ悍妫€鏌ラ棿闅旓紙绉掞級")
    last_health_check_at = Column(DateTime, nullable=True, comment="鏈€鍚庡仴搴锋鏌ユ椂闂?)
    is_healthy = Column(Boolean, nullable=True, comment="鏄惁鍋ュ悍")
    
    # 鎵╁睍閰嶇疆
    config = Column(Text, nullable=True, comment="鎵╁睍閰嶇疆锛圝SON锛?)
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name={self.name}, type={self.type})>"
    
    def to_dict(self):
        """杞崲涓哄瓧鍏?""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "type": self.type,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "username": self.username,
            "charset": self.charset,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "status": self.status,
            "is_default": self.is_default,
            "health_check_interval": self.health_check_interval,
            "last_health_check_at": self.last_health_check_at.isoformat() if self.last_health_check_at else None,
            "is_healthy": self.is_healthy,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_health_status(self, is_healthy: bool):
        """更新鍋ュ悍状态?""
        self.is_healthy = is_healthy
        self.last_health_check_at = datetime.now()
    
    def is_available(self) -> bool:
        """妫€鏌ユ暟鎹簮鏄惁鍙敤"""
        return self.status == "active" and self.is_healthy
    
    def get_connection_string(self) -> str:
        """鑾峰彇杩炴帴瀛楃涓?""
        if self.type == "mysql":
            return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        elif self.type == "postgresql":
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.type == "oracle":
            return f"oracle+cx_oracle://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError(f"涓嶆敮鎸佺殑鏁版嵁婧愮被鍨? {self.type}")
