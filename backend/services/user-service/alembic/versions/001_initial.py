# -*- coding: utf-8 -*-
"""鍒涘缓鐢ㄦ埛鏈嶅姟鐩稿叧琛?
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
    # 鍒涘缓绉熸埛琛?    op.create_table(
        'tenants',
        sa.Column('id', sa.String(50), primary_key=True, comment='绉熸埛ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='绉熸埛鍚嶇О'),
        sa.Column('code', sa.String(50), nullable=False, unique=True, comment='绉熸埛缂栫爜'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('description', sa.Text, comment='鎻忚堪'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Index('idx_status', 'status'),
        comment='绉熸埛琛?
    )

    # 鍒涘缓閮ㄩ棬琛?    op.create_table(
        'departments',
        sa.Column('id', sa.String(50), primary_key=True, comment='閮ㄩ棬ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, comment='绉熸埛ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='閮ㄩ棬鍚嶇О'),
        sa.Column('code', sa.String(100), nullable=False, comment='閮ㄩ棬缂栫爜'),
        sa.Column('parent_id', sa.String(50), comment='鐖堕儴闂↖D'),
        sa.Column('level', sa.Integer, nullable=False, default=1, comment='灞傜骇'),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0, comment='鎺掑簭'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['departments.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('tenant_id', 'code', name='uk_tenant_code'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_parent_id', 'parent_id'),
        sa.Index('idx_level', 'level'),
        comment='閮ㄩ棬琛?
    )

    # 鍒涘缓鐢ㄦ埛琛?    op.create_table(
        'users',
        sa.Column('id', sa.String(50), primary_key=True, comment='鐢ㄦ埛ID'),
        sa.Column('tenant_id', sa.String(64), nullable=False, index=True, comment='绉熸埛ID'),
        sa.Column('department_id', sa.String(50), comment='閮ㄩ棬ID'),
        sa.Column('username', sa.String(50), nullable=False, unique=True, index=True, comment='鐢ㄦ埛鍚?),
        sa.Column('email', sa.String(100), nullable=False, index=True, comment='閭'),
        sa.Column('phone', sa.String(20), comment='鎵嬫満鍙?),
        sa.Column('password_hash', sa.String(255), nullable=False, comment='瀵嗙爜鍝堝笇'),
        sa.Column('real_name', sa.String(50), comment='鐪熷疄濮撳悕'),
        sa.Column('avatar', sa.String(255), comment='澶村儚URL'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('last_login_at', sa.DateTime, comment='鏈€鍚庣櫥褰曟椂闂?),
        sa.Column('last_login_ip', sa.String(50), comment='鏈€鍚庣櫥褰旾P'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Column('deleted_at', sa.DateTime, comment='鍒犻櫎鏃堕棿'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_department_id', 'department_id'),
        sa.Index('idx_status', 'status'),
        comment='鐢ㄦ埛琛?
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('departments')
    op.drop_table('tenants')
