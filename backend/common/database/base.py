from sqlalchemy import Column, Integer, DateTime, Boolean, String
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from datetime import datetime
import uuid

# 创建declarative_base对象
Base = declarative_base()

class BaseModel(Base):
    """数据库模型基类"""
    
    __abstract__ = True
    
    @declared_attr
    def id(cls):
        """主键（UUID）"""
        return Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), comment='主键ID')
    
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
        return f""<{self.__class__.__name__}(id={self.id})>""

class TimestampMixin:
    """时间戳混入类"""
    
    @declared_attr
    def created_at(cls):
        """创建时间"""
        return Column(DateTime, default=datetime.now, nullable=False, comment='创建时间')
    
    @declared_attr
    def updated_at(cls):
        """更新时间"""
        return Column(
            DateTime,
            default=datetime.now,
            onupdate=datetime.now,
            nullable=False,
            comment='更新时间'
        )

class SoftDeleteMixin:
    """软删除混入类"""
    
    @declared_attr
    def is_deleted(cls):
        """是否删除"""
        return Column(Boolean, default=False, nullable=False, comment='是否删除')
    
    @declared_attr
    def deleted_at(cls):
        """删除时间"""
        return Column(DateTime, nullable=True, comment='删除时间')
    
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
    
    @declared_attr
    def created_by(cls):
        """创建人ID"""
        return Column(String(36), nullable=True, comment='创建人ID')
    
    @declared_attr
    def updated_by(cls):
        """更新人ID"""
        return Column(String(36), nullable=True, comment='更新人ID')
    
    @declared_attr
    def deleted_by(cls):
        """删除人ID"""
        return Column(String(36), nullable=True, comment='删除人ID')

class FullModelMixin(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """完整模型混入类"""
    pass
