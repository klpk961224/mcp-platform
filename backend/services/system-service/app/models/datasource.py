# -*- coding: utf-8 -*-
"""
数据源模型

功能说明：
1. 数据源配置
2. 数据源连接管理
3. 数据源健康检查

使用示例：
    from app.models.datasource import DataSource
    
    datasource = DataSource(
        name="主数据库",
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
    数据源模型
    
    功能：
    - 数据源配置
    - 数据源连接管理
    - 数据源健康检查
    
    属性说明：
    - id: 数据源ID（主键）
    - tenant_id: 租户ID
    - name: 数据源名称
    - type: 数据源类型（mysql/postgresql/oracle）
    - host: 主机地址
    - port: 端口
    - database: 数据库名称
    - username: 用户名
    - password: 密码（加密）
    - charset: 字符集
    - pool_size: 连接池大小
    - max_overflow: 最大溢出连接数
    - status: 状态（active/inactive）
    - is_default: 是否默认数据源
    - health_check_interval: 健康检查间隔（秒）
    - last_health_check_at: 最后健康检查时间
    - is_healthy: 是否健康
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    __tablename__ = "datasources"
    
    # 基本信息
    tenant_id = Column(String(64), nullable=False, index=True, comment="租户ID")
    name = Column(String(100), nullable=False, comment="数据源名称")
    type = Column(String(20), nullable=False, comment="数据源类型")
    host = Column(String(255), nullable=False, comment="主机地址")
    port = Column(Integer, nullable=False, comment="端口")
    database = Column(String(100), nullable=False, comment="数据库名称")
    
    # 连接配置
    username = Column(String(100), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码（加密）")
    charset = Column(String(20), nullable=False, default="utf8mb4", comment="字符集")
    
    # 连接池配置
    pool_size = Column(Integer, nullable=False, default=10, comment="连接池大小")
    max_overflow = Column(Integer, nullable=False, default=20, comment="最大溢出连接数")
    
    # 状态信息
    status = Column(String(20), nullable=False, default="active", comment="状态")
    is_default = Column(Boolean, nullable=False, default=False, comment="是否默认数据源")
    
    # 健康检查配置
    health_check_interval = Column(Integer, nullable=False, default=60, comment="健康检查间隔（秒）")
    last_health_check_at = Column(DateTime, nullable=True, comment="最后健康检查时间")
    is_healthy = Column(Boolean, nullable=True, comment="是否健康")
    
    # 扩展配置
    config = Column(Text, nullable=True, comment="扩展配置（JSON）")
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name={self.name}, type={self.type})>"
    
    def to_dict(self):
        """转换为字典"""
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
        """更新健康状态"""
        self.is_healthy = is_healthy
        self.last_health_check_at = datetime.now()
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        return self.status == "active" and self.is_healthy
    
    def get_connection_string(self) -> str:
        """获取连接字符串"""
        if self.type == "mysql":
            return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        elif self.type == "postgresql":
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.type == "oracle":
            return f"oracle+cx_oracle://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError(f"不支持的数据源类型: {self.type}")