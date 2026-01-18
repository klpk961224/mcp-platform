"""
鐢ㄦ埛鐩稿叧妯″瀷

鍖呭惈锛?- User: 鐢ㄦ埛琛?- Department: 閮ㄩ棬琛?- Role: 瑙掕壊琛?- UserRole: 鐢ㄦ埛瑙掕壊鍏宠仈琛?"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel, TimestampMixin, FullModelMixin


# 鐢ㄦ埛瑙掕壊鍏宠仈琛?user_roles = Table(
    'user_roles',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True, comment='鍏宠仈ID'),
    Column('user_id', String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='鐢ㄦ埛ID'),
    Column('role_id', String(50), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='瑙掕壊ID'),
    Column('created_at', DateTime, nullable=False, default=datetime.now, comment='鍒涘缓鏃堕棿'),
    keep_existing=True
)


class User(BaseModel, FullModelMixin):
    """鐢ㄦ埛琛?""
    
    __tablename__ = 'users'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='绉熸埛ID')
    username = Column(String(50), nullable=False, comment='鐢ㄦ埛鍚?)
    password = Column(String(255), nullable=False, comment='瀵嗙爜锛堝姞瀵嗭級')
    email = Column(String(100), comment='閭')
    phone = Column(String(20), comment='鎵嬫満鍙?)
    dept_id = Column(String(50), ForeignKey('departments.id', ondelete='SET NULL'), comment='閮ㄩ棬ID')
    position_id = Column(String(50), comment='宀椾綅ID')
    status = Column(String(20), nullable=False, default='active', comment='鐘舵€?)
    last_login_at = Column(DateTime, comment='鏈€鍚庣櫥褰曟椂闂?)
    last_login_ip = Column(String(50), comment='鏈€鍚庣櫥褰旾P')
    
    # 鍏崇郴
    tenant = relationship('Tenant', back_populates='users')
    department = relationship('Department', back_populates='users')
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Department(BaseModel, FullModelMixin):
    """閮ㄩ棬琛?""
    
    __tablename__ = 'departments'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='绉熸埛ID')
    name = Column(String(100), nullable=False, comment='閮ㄩ棬鍚嶇О')
    code = Column(String(100), nullable=False, comment='閮ㄩ棬缂栫爜')
    parent_id = Column(String(50), ForeignKey('departments.id', ondelete='SET NULL'), comment='鐖堕儴闂↖D')
    level = Column(Integer, nullable=False, default=1, comment='灞傜骇')
    sort_order = Column(Integer, nullable=False, default=0, comment='鎺掑簭')
    status = Column(String(20), nullable=False, default='active', comment='鐘舵€?)
    
    # 鍏崇郴
    tenant = relationship('Tenant', back_populates='departments')
    parent = relationship('Department', remote_side='Department.id', backref='children')
    users = relationship('User', back_populates='department')
    
    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name}, code={self.code})>"


class Role(BaseModel, FullModelMixin):
    """瑙掕壊琛?""
    
    __tablename__ = 'roles'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='绉熸埛ID')
    name = Column(String(100), nullable=False, comment='瑙掕壊鍚嶇О')
    code = Column(String(50), nullable=False, comment='瑙掕壊缂栫爜')
    description = Column(Text, comment='鎻忚堪')
    is_system = Column(Boolean, nullable=False, default=False, comment='鏄惁绯荤粺瑙掕壊')
    status = Column(String(20), nullable=False, default='active', comment='鐘舵€?)
    
    # 鍏崇郴
    tenant = relationship('Tenant', back_populates='roles')
    users = relationship('User', secondary=user_roles, back_populates='roles')
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, code={self.code})>"
