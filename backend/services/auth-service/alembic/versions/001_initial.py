# -*- coding: utf-8 -*-
"""创建认证服务相关表

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
    # 创建用户表
    op.create_table(
        'users',
        sa.Column('id', sa.String(50), primary_key=True, comment='用户ID'),
        sa.Column('tenant_id', sa.String(64), nullable=False, index=True, comment='租户ID'),
        sa.Column('username', sa.String(50), nullable=False, unique=True, index=True, comment='用户名'),
        sa.Column('email', sa.String(100), nullable=False, index=True, comment='邮箱'),
        sa.Column('password_hash', sa.String(255), nullable=False, comment='密码哈希'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('last_login_at', sa.DateTime, comment='最后登录时间'),
        sa.Column('last_login_ip', sa.String(50), comment='最后登录IP'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Column('deleted_at', sa.DateTime, comment='删除时间'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_status', 'status'),
        comment='用户表'
    )

    # 创建Token表
    op.create_table(
        'tokens',
        sa.Column('id', sa.String(50), primary_key=True, comment='Token ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('token_type', sa.String(20), nullable=False, comment='Token类型'),
        sa.Column('access_token', sa.Text, nullable=False, comment='访问Token'),
        sa.Column('refresh_token', sa.Text, nullable=False, comment='刷新Token'),
        sa.Column('expires_at', sa.DateTime, nullable=False, comment='过期时间'),
        sa.Column('is_revoked', sa.Boolean, nullable=False, default=False, comment='是否已吊销'),
        sa.Column('revoked_at', sa.DateTime, comment='吊销时间'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_token_type', 'token_type'),
        sa.Index('idx_expires_at', 'expires_at'),
        comment='Token表'
    )


def downgrade():
    op.drop_table('tokens')
    op.drop_table('users')