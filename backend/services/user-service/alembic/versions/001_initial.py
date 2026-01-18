# -*- coding: utf-8 -*-
"""创建鐢ㄦ埛鏈嶅姟鐩稿叧琛?
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
    # 创建绉熸埛琛?    op.create_table(
        'tenants',
        sa.Column('id', sa.String(50), primary_key=True, comment='租户ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='绉熸埛名称'),
        sa.Column('code', sa.String(50), nullable=False, unique=True, comment='绉熸埛编码'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态?),
        sa.Column('description', sa.Text, comment='描述'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新鏃堕棿'),
        sa.Index('idx_status', 'status'),
        comment='绉熸埛琛?
    )

    # 创建部门表?    op.create_table(
        'departments',
        sa.Column('id', sa.String(50), primary_key=True, comment='部门ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, comment='租户ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='部门名称'),
        sa.Column('code', sa.String(100), nullable=False, comment='部门编码'),
        sa.Column('parent_id', sa.String(50), comment='鐖堕儴闂↖D'),
        sa.Column('level', sa.Integer, nullable=False, default=1, comment='灞傜骇'),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0, comment='排序'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新鏃堕棿'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['departments.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('tenant_id', 'code', name='uk_tenant_code'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_parent_id', 'parent_id'),
        sa.Index('idx_level', 'level'),
        comment='部门表?
    )

    # 创建用户表?    op.create_table(
        'users',
        sa.Column('id', sa.String(50), primary_key=True, comment='用户ID'),
        sa.Column('tenant_id', sa.String(64), nullable=False, index=True, comment='租户ID'),
        sa.Column('department_id', sa.String(50), comment='部门ID'),
        sa.Column('username', sa.String(50), nullable=False, unique=True, index=True, comment='用户名?),
        sa.Column('email', sa.String(100), nullable=False, index=True, comment='邮箱'),
        sa.Column('phone', sa.String(20), comment='手机号),
        sa.Column('password_hash', sa.String(255), nullable=False, comment='瀵嗙爜鍝堝笇'),
        sa.Column('real_name', sa.String(50), comment='鐪熷疄濮撳悕'),
        sa.Column('avatar', sa.String(255), comment='澶村儚URL'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态?),
        sa.Column('last_login_at', sa.DateTime, comment='最后登录时间),
        sa.Column('last_login_ip', sa.String(50), comment='最后登录IP'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新鏃堕棿'),
        sa.Column('deleted_at', sa.DateTime, comment='删除鏃堕棿'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_department_id', 'department_id'),
        sa.Index('idx_status', 'status'),
        comment='用户表?
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('departments')
    op.drop_table('tenants')
