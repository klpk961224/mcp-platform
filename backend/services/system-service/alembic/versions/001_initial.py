# -*- coding: utf-8 -*-
"""鍒涘缓绯荤粺鏈嶅姟鐩稿叧琛?
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
    # 鍒涘缓MCP宸ュ叿琛?    op.create_table(
        'mcp_tools',
        sa.Column('id', sa.String(50), primary_key=True, comment='MCP宸ュ叿ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='宸ュ叿鍚嶇О'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='宸ュ叿缂栫爜'),
        sa.Column('description', sa.Text, comment='鎻忚堪'),
        sa.Column('api_endpoint', sa.String(255), nullable=False, comment='API绔偣'),
        sa.Column('method', sa.String(10), nullable=False, comment='HTTP鏂规硶'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('call_count', sa.Integer, nullable=False, default=0, comment='璋冪敤娆℃暟'),
        sa.Column('success_count', sa.Integer, nullable=False, default=0, comment='鎴愬姛娆℃暟'),
        sa.Column('fail_count', sa.Integer, nullable=False, default=0, comment='澶辫触娆℃暟'),
        sa.Column('last_call_at', sa.DateTime, comment='鏈€鍚庤皟鐢ㄦ椂闂?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_code', 'code'),
        comment='MCP宸ュ叿琛?
    )

    # 鍒涘缓鏁版嵁婧愯〃
    op.create_table(
        'datasources',
        sa.Column('id', sa.String(50), primary_key=True, comment='鏁版嵁婧怚D'),
        sa.Column('name', sa.String(100), nullable=False, comment='鏁版嵁婧愬悕绉?),
        sa.Column('type', sa.String(20), nullable=False, comment='鏁版嵁婧愮被鍨?),
        sa.Column('host', sa.String(100), nullable=False, comment='涓绘満鍦板潃'),
        sa.Column('port', sa.Integer, nullable=False, comment='绔彛'),
        sa.Column('database', sa.String(100), nullable=False, comment='鏁版嵁搴撳悕'),
        sa.Column('username', sa.String(100), nullable=False, comment='鐢ㄦ埛鍚?),
        sa.Column('password', sa.String(255), nullable=False, comment='瀵嗙爜'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Index('idx_type', 'type'),
        sa.Index('idx_status', 'status'),
        comment='鏁版嵁婧愯〃'
    )

    # 鍒涘缓瀛楀吀琛?    op.create_table(
        'dicts',
        sa.Column('id', sa.String(50), primary_key=True, comment='瀛楀吀ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='瀛楀吀鍚嶇О'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='瀛楀吀缂栫爜'),
        sa.Column('description', sa.Text, comment='鎻忚堪'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_code', 'code'),
        comment='瀛楀吀琛?
    )

    # 鍒涘缓瀛楀吀椤硅〃
    op.create_table(
        'dict_items',
        sa.Column('id', sa.String(50), primary_key=True, comment='瀛楀吀椤笽D'),
        sa.Column('dict_id', sa.String(50), nullable=False, comment='瀛楀吀ID'),
        sa.Column('label', sa.String(100), nullable=False, comment='鏍囩'),
        sa.Column('value', sa.String(100), nullable=False, comment='鍊?),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0, comment='鎺掑簭'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.ForeignKeyConstraint(['dict_id'], ['dicts.id'], ondelete='CASCADE'),
        sa.Index('idx_dict_id', 'dict_id'),
        sa.Index('idx_status', 'status'),
        comment='瀛楀吀椤硅〃'
    )


def downgrade():
    op.drop_table('dict_items')
    op.drop_table('dicts')
    op.drop_table('datasources')
    op.drop_table('mcp_tools')
