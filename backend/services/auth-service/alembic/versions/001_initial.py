# -*- coding: utf-8 -*-
"""鍒涘缓璁よ瘉鏈嶅姟鐩稿叧琛?
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
    # 鍒涘缓鐢ㄦ埛琛?    op.create_table(
        'users',
        sa.Column('id', sa.String(50), primary_key=True, comment='鐢ㄦ埛ID'),
        sa.Column('tenant_id', sa.String(64), nullable=False, index=True, comment='绉熸埛ID'),
        sa.Column('username', sa.String(50), nullable=False, unique=True, index=True, comment='鐢ㄦ埛鍚?),
        sa.Column('email', sa.String(100), nullable=False, index=True, comment='閭'),
        sa.Column('password_hash', sa.String(255), nullable=False, comment='瀵嗙爜鍝堝笇'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('last_login_at', sa.DateTime, comment='鏈€鍚庣櫥褰曟椂闂?),
        sa.Column('last_login_ip', sa.String(50), comment='鏈€鍚庣櫥褰旾P'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Column('deleted_at', sa.DateTime, comment='鍒犻櫎鏃堕棿'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_status', 'status'),
        comment='鐢ㄦ埛琛?
    )

    # 鍒涘缓Token琛?    op.create_table(
        'tokens',
        sa.Column('id', sa.String(50), primary_key=True, comment='Token ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='鐢ㄦ埛ID'),
        sa.Column('token_type', sa.String(20), nullable=False, comment='Token绫诲瀷'),
        sa.Column('access_token', sa.Text, nullable=False, comment='璁块棶Token'),
        sa.Column('refresh_token', sa.Text, nullable=False, comment='鍒锋柊Token'),
        sa.Column('expires_at', sa.DateTime, nullable=False, comment='杩囨湡鏃堕棿'),
        sa.Column('is_revoked', sa.Boolean, nullable=False, default=False, comment='鏄惁宸插悐閿€'),
        sa.Column('revoked_at', sa.DateTime, comment='鍚婇攢鏃堕棿'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_token_type', 'token_type'),
        sa.Index('idx_expires_at', 'expires_at'),
        comment='Token琛?
    )


def downgrade():
    op.drop_table('tokens')
    op.drop_table('users')
