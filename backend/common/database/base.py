from sqlalchemy import Column, Integer, DateTime, Boolean, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from datetime import datetime
from typing import Optional
import uuid

# 创建DeclarativeBase对象（SQLAlchemy 2.0+）
class Base(DeclarativeBase):
    """SQLAlchemy 2.0+ 基类"""
    pass

class BaseModel(Base):
    """数据库模型基类"""
    
    __abstract__ = True
    __table_args__ = {'extend_existing': True}
    
    @declared_attr.directive
    def __tablename__(cls):
        """表名（默认使用类名的小写）"""
        return cls.__name__.lower()
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), comment='主键ID')
    
    def to_dict(self):
        """将模型转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    def __repr__(self):
        """模型字符串表示"""
        return f"<{self.__class__.__name__}(id={self.id})>"

class TimestampMixin:
    """时间戳混入类"""
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')

class SoftDeleteMixin:
    """软删除混入类"""
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment='是否删除')
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='删除时间')
    
    def soft_delete(self):
        """软删除"""
        self.is_deleted = True
        self.deleted_at = datetime.now()
    
    def restore(self):
        """恢复"""
        self.is_deleted = False
        self.deleted_at = None

class AuditMixin:
    """审计混入类"""
    
    created_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, comment='创建人ID')
    updated_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, comment='更新人ID')
    deleted_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, comment='删除人ID')

class FullModelMixin(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """完整模型混入类"""
    pass
