"""
用户关系模型

包括：
- User: 用户表
- Department: 部门表
- Role: 角色表
- UserRole: 用户角色关联表
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import BaseModel, TimestampMixin, FullModelMixin


# 用户角色关联表
user_roles = Table(
    'user_roles',
    BaseModel.metadata,
    Column('id', String(50), primary_key=True, comment='关联ID'),
    Column('user_id', String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='用户ID'),
    Column('role_id', String(50), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='角色ID'),
    Column('created_at', DateTime, nullable=False, default=datetime.now, comment='创建时间'),
    keep_existing=True
)


class User(BaseModel, FullModelMixin):
    """用户表"""
    
    __tablename__ = 'users'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='租户ID')
    username = Column(String(50), nullable=False, comment='用户名')
    password = Column(String(255), nullable=False, comment='密码（加密）')
    email = Column(String(100), comment='邮箱')
    phone = Column(String(20), comment='手机号')
    dept_id = Column(String(50), ForeignKey('departments.id', ondelete='SET NULL'), comment='部门ID')
    position_id = Column(String(50), comment='岗位ID')
    status = Column(String(20), nullable=False, default='active', comment='状态')
    last_login_at = Column(DateTime, comment='最后登录时间')
    last_login_ip = Column(String(50), comment='最后登录IP')
    
    # 关系
    tenant = relationship('Tenant', back_populates='users')
    department = relationship('Department', back_populates='users')
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Department(BaseModel, FullModelMixin):
    """部门表"""
    
    __tablename__ = 'departments'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='租户ID')
    name = Column(String(100), nullable=False, comment='部门名称')
    code = Column(String(50), comment='部门编码')
    parent_id = Column(String(50), ForeignKey('departments.id', ondelete='SET NULL'), comment='上级部门ID')
    leader_id = Column(String(50), ForeignKey('users.id', ondelete='SET NULL'), comment='部门负责人ID')
    sort_order = Column(Integer, default=0, comment='排序')
    status = Column(String(20), nullable=False, default='active', comment='状态')
    
    # 关系
    tenant = relationship('Tenant', back_populates='departments')
    parent = relationship('Department', remote_side='Department.id', backref='children')
    leader = relationship('User', foreign_keys=[leader_id])
    users = relationship('User', back_populates='department')
    
    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name})>"


class Role(BaseModel, FullModelMixin):
    """角色表"""
    
    __tablename__ = 'roles'
    
    tenant_id = Column(String(50), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, comment='租户ID')
    name = Column(String(50), nullable=False, comment='角色名称')
    code = Column(String(50), comment='角色编码')
    description = Column(Text, comment='角色描述')
    status = Column(String(20), nullable=False, default='active', comment='状态')
    
    # 关系
    tenant = relationship('Tenant', back_populates='roles')
    users = relationship('User', secondary=user_roles, back_populates='roles')
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"