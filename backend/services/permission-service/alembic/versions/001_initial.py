# -*- coding: utf-8 -*-
"""鍒涘缓鏉冮檺鏈嶅姟鐩稿叧琛?
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
    # 鍒涘缓瑙掕壊琛?    op.create_table(
        'roles',
        sa.Column('id', sa.String(50), primary_key=True, comment='瑙掕壊ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, index=True, comment='绉熸埛ID'),
        sa.Column('name', sa.String(50), nullable=False, comment='瑙掕壊鍚嶇О'),
        sa.Column('code', sa.String(50), nullable=False, comment='瑙掕壊缂栫爜'),
        sa.Column('description', sa.Text, comment='鎻忚堪'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.UniqueConstraint('tenant_id', 'code', name='uk_tenant_code'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_status', 'status'),
        comment='瑙掕壊琛?
    )

    # 鍒涘缓鏉冮檺琛?    op.create_table(
        'permissions',
        sa.Column('id', sa.String(50), primary_key=True, comment='鏉冮檺ID'),
        sa.Column('name', sa.String(50), nullable=False, comment='鏉冮檺鍚嶇О'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='鏉冮檺缂栫爜'),
        sa.Column('resource', sa.String(100), nullable=False, comment='璧勬簮'),
        sa.Column('action', sa.String(50), nullable=False, comment='鎿嶄綔'),
        sa.Column('description', sa.Text, comment='鎻忚堪'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Index('idx_resource', 'resource'),
        sa.Index('idx_action', 'action'),
        comment='鏉冮檺琛?
    )

    # 鍒涘缓瑙掕壊鏉冮檺鍏宠仈琛?    op.create_table(
        'role_permissions',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('role_id', sa.String(50), nullable=False, comment='瑙掕壊ID'),
        sa.Column('permission_id', sa.String(50), nullable=False, comment='鏉冮檺ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('role_id', 'permission_id', name='uk_role_permission'),
        sa.Index('idx_role_id', 'role_id'),
        sa.Index('idx_permission_id', 'permission_id'),
        comment='瑙掕壊鏉冮檺鍏宠仈琛?
    )

    # 鍒涘缓鑿滃崟琛?    op.create_table(
        'menus',
        sa.Column('id', sa.String(50), primary_key=True, comment='鑿滃崟ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, index=True, comment='绉熸埛ID'),
        sa.Column('parent_id', sa.String(50), comment='鐖惰彍鍗旾D'),
        sa.Column('name', sa.String(50), nullable=False, comment='鑿滃崟鍚嶇О'),
        sa.Column('type', sa.String(20), nullable=False, comment='鑿滃崟绫诲瀷'),
        sa.Column('path', sa.String(200), comment='璺敱璺緞'),
        sa.Column('component', sa.String(200), comment='缁勪欢璺緞'),
        sa.Column('icon', sa.String(50), comment='鍥炬爣'),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0, comment='鎺掑簭'),
        sa.Column('visible', sa.Boolean, nullable=False, default=True, comment='鏄惁鍙'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.ForeignKeyConstraint(['parent_id'], ['menus.id'], ondelete='SET NULL'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_parent_id', 'parent_id'),
        sa.Index('idx_type', 'type'),
        comment='鑿滃崟琛?
    )

    # 鍒涘缓瑙掕壊鑿滃崟鍏宠仈琛?    op.create_table(
        'role_menus',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('role_id', sa.String(50), nullable=False, comment='瑙掕壊ID'),
        sa.Column('menu_id', sa.String(50), nullable=False, comment='鑿滃崟ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('role_id', 'menu_id', name='uk_role_menu'),
        sa.Index('idx_role_id', 'role_id'),
        sa.Index('idx_menu_id', 'menu_id'),
        comment='瑙掕壊鑿滃崟鍏宠仈琛?
    )

    # 鍒涘缓鐢ㄦ埛瑙掕壊鍏宠仈琛?    op.create_table(
        'user_roles',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('user_id', sa.String(50), nullable=False, comment='鐢ㄦ埛ID'),
        sa.Column('role_id', sa.String(50), nullable=False, comment='瑙掕壊ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'role_id', name='uk_user_role'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_role_id', 'role_id'),
        comment='鐢ㄦ埛瑙掕壊鍏宠仈琛?
    )


def downgrade():
    op.drop_table('user_roles')
    op.drop_table('role_menus')
    op.drop_table('menus')
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')
