"""
鏉冮檺鐩稿叧妯″瀷

鍖呭惈锛?
- Permission: 鏉冮檺琛?
- Menu: 鑿滃崟琛?
- RolePermission: 瑙掕壊鏉冮檺鍏宠仈琛?
- RoleMenu: 瑙掕壊鑿滃崟鍏宠仈琛?
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel, TimestampMixin


# 瑙掕壊鏉冮檺鍏宠仈琛?
role_permissions = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True, comment='鍏宠仈ID'),
    Column('role_id', String(50), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='瑙掕壊ID'),
    Column('permission_id', String(50), ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False, comment='鏉冮檺ID'),
    Column('created_at', DateTime, nullable=False, default=datetime.now, comment='鍒涘缓鏃堕棿'),
    keep_existing=True
)


# 瑙掕壊鑿滃崟鍏宠仈琛?
role_menus = Table(
    'role_menus',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True, comment='鍏宠仈ID'),
    Column('role_id', String(50), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='瑙掕壊ID'),
    Column('menu_id', String(50), ForeignKey('menus.id', ondelete='CASCADE'), nullable=False, comment='鑿滃崟ID'),
    Column('created_at', DateTime, nullable=False, default=datetime.now, comment='鍒涘缓鏃堕棿'),
    keep_existing=True
)


class Permission(BaseModel, TimestampMixin):
    """鏉冮檺琛?""
    
    __tablename__ = 'permissions'
    
    name = Column(String(100), nullable=False, comment='鏉冮檺鍚嶇О')
    code = Column(String(100), nullable=False, unique=True, comment='鏉冮檺缂栫爜')
    type = Column(String(20), nullable=False, comment='绫诲瀷')
    description = Column(Text, comment='鎻忚堪')
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name}, code={self.code})>"


class Menu(BaseModel, TimestampMixin):
    """鑿滃崟琛?""
    
    __tablename__ = 'menus'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='绉熸埛ID')
    name = Column(String(100), nullable=False, comment='鑿滃崟鍚嶇О')
    path = Column(String(255), comment='鑿滃崟璺緞')
    icon = Column(String(100), comment='鑿滃崟鍥炬爣')
    parent_id = Column(String(50), ForeignKey('menus.id', ondelete='CASCADE'), comment='鐖惰彍鍗旾D')
    sort_order = Column(Integer, nullable=False, default=0, comment='鎺掑簭')
    is_visible = Column(Boolean, nullable=False, default=True, comment='鏄惁鍙')
    status = Column(String(20), nullable=False, default='active', comment='鐘舵€?)
    
    # 鍏崇郴
    tenant = relationship('Tenant', back_populates='menus')
    parent = relationship('Menu', remote_side='Menu.id', backref='children')
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name={self.name}, path={self.path})>"
