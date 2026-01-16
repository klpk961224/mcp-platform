# -*- coding: utf-8 -*-
"""创建系统服务相关表

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
    # 创建MCP工具表
    op.create_table(
        'mcp_tools',
        sa.Column('id', sa.String(50), primary_key=True, comment='MCP工具ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='工具名称'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='工具编码'),
        sa.Column('description', sa.Text, comment='描述'),
        sa.Column('api_endpoint', sa.String(255), nullable=False, comment='API端点'),
        sa.Column('method', sa.String(10), nullable=False, comment='HTTP方法'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('call_count', sa.Integer, nullable=False, default=0, comment='调用次数'),
        sa.Column('success_count', sa.Integer, nullable=False, default=0, comment='成功次数'),
        sa.Column('fail_count', sa.Integer, nullable=False, default=0, comment='失败次数'),
        sa.Column('last_call_at', sa.DateTime, comment='最后调用时间'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_code', 'code'),
        comment='MCP工具表'
    )

    # 创建数据源表
    op.create_table(
        'datasources',
        sa.Column('id', sa.String(50), primary_key=True, comment='数据源ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='数据源名称'),
        sa.Column('type', sa.String(20), nullable=False, comment='数据源类型'),
        sa.Column('host', sa.String(100), nullable=False, comment='主机地址'),
        sa.Column('port', sa.Integer, nullable=False, comment='端口'),
        sa.Column('database', sa.String(100), nullable=False, comment='数据库名'),
        sa.Column('username', sa.String(100), nullable=False, comment='用户名'),
        sa.Column('password', sa.String(255), nullable=False, comment='密码'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_type', 'type'),
        sa.Index('idx_status', 'status'),
        comment='数据源表'
    )

    # 创建字典表
    op.create_table(
        'dicts',
        sa.Column('id', sa.String(50), primary_key=True, comment='字典ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='字典名称'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='字典编码'),
        sa.Column('description', sa.Text, comment='描述'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_code', 'code'),
        comment='字典表'
    )

    # 创建字典项表
    op.create_table(
        'dict_items',
        sa.Column('id', sa.String(50), primary_key=True, comment='字典项ID'),
        sa.Column('dict_id', sa.String(50), nullable=False, comment='字典ID'),
        sa.Column('label', sa.String(100), nullable=False, comment='标签'),
        sa.Column('value', sa.String(100), nullable=False, comment='值'),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0, comment='排序'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.ForeignKeyConstraint(['dict_id'], ['dicts.id'], ondelete='CASCADE'),
        sa.Index('idx_dict_id', 'dict_id'),
        sa.Index('idx_status', 'status'),
        comment='字典项表'
    )


def downgrade():
    op.drop_table('dict_items')
    op.drop_table('dicts')
    op.drop_table('datasources')
    op.drop_table('mcp_tools')