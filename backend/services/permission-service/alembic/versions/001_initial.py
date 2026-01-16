# -*- coding: utf-8 -*-
"""创建权限服务相关表

Revision ID: 001
Revises:
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 创建角色表
    op.create_table(
        'roles',
        sa.Column('id', sa.String(50), primary_key=True, comment='角色ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, index=True, comment='租户ID'),
        sa.Column('name', sa.String(50), nullable=False, comment='角色名称'),
        sa.Column('code', sa.String(50), nullable=False, comment='角色编码'),
        sa.Column('description', sa.Text, comment='描述'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.UniqueConstraint('tenant_id', 'code', name='uk_tenant_code'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_status', 'status'),
        comment='角色表'
    )

    # 创建权限表
    op.create_table(
        'permissions',
        sa.Column('id', sa.String(50), primary_key=True, comment='权限ID'),
        sa.Column('name', sa.String(50), nullable=False, comment='权限名称'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='权限编码'),
        sa.Column('resource', sa.String(100), nullable=False, comment='资源'),
        sa.Column('action', sa.String(50), nullable=False, comment='操作'),
        sa.Column('description', sa.Text, comment='描述'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_resource', 'resource'),
        sa.Index('idx_action', 'action'),
        comment='权限表'
    )

    # 创建角色权限关联表
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('role_id', sa.String(50), nullable=False, comment='角色ID'),
        sa.Column('permission_id', sa.String(50), nullable=False, comment='权限ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('role_id', 'permission_id', name='uk_role_permission'),
        sa.Index('idx_role_id', 'role_id'),
        sa.Index('idx_permission_id', 'permission_id'),
        comment='角色权限关联表'
    )

    # 创建菜单表
    op.create_table(
        'menus',
        sa.Column('id', sa.String(50), primary_key=True, comment='菜单ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, index=True, comment='租户ID'),
        sa.Column('parent_id', sa.String(50), comment='父菜单ID'),
        sa.Column('name', sa.String(50), nullable=False, comment='菜单名称'),
        sa.Column('type', sa.String(20), nullable=False, comment='菜单类型'),
        sa.Column('path', sa.String(200), comment='路由路径'),
        sa.Column('component', sa.String(200), comment='组件路径'),
        sa.Column('icon', sa.String(50), comment='图标'),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0, comment='排序'),
        sa.Column('visible', sa.Boolean, nullable=False, default=True, comment='是否可见'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.ForeignKeyConstraint(['parent_id'], ['menus.id'], ondelete='SET NULL'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_parent_id', 'parent_id'),
        sa.Index('idx_type', 'type'),
        comment='菜单表'
    )

    # 创建角色菜单关联表
    op.create_table(
        'role_menus',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('role_id', sa.String(50), nullable=False, comment='角色ID'),
        sa.Column('menu_id', sa.String(50), nullable=False, comment='菜单ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('role_id', 'menu_id', name='uk_role_menu'),
        sa.Index('idx_role_id', 'role_id'),
        sa.Index('idx_menu_id', 'menu_id'),
        comment='角色菜单关联表'
    )

    # 创建用户角色关联表
    op.create_table(
        'user_roles',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('user_id', sa.String(50), nullable=False, comment='用户ID'),
        sa.Column('role_id', sa.String(50), nullable=False, comment='角色ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'role_id', name='uk_user_role'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_role_id', 'role_id'),
        comment='用户角色关联表'
    )


def downgrade():
    op.drop_table('user_roles')
    op.drop_table('role_menus')
    op.drop_table('menus')
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')