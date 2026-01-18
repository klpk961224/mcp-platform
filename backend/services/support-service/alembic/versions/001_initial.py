# -*- coding: utf-8 -*-
"""创建鏀拺鏈嶅姟鐩稿叧琛?
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
    # 创建鐧诲綍鏃ュ織琛?    op.create_table(
        'login_logs',
        sa.Column('id', sa.String(50), primary_key=True, comment='鏃ュ織ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('username', sa.String(50), nullable=False, comment='用户名?),
        sa.Column('ip', sa.String(50), comment='IP地址'),
        sa.Column('user_agent', sa.String(255), comment='鐢ㄦ埛浠ｇ悊'),
        sa.Column('login_time', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鐧诲綍鏃堕棿'),
        sa.Column('status', sa.String(20), nullable=False, comment='状态?),
        sa.Column('message', sa.String(255), comment='娑堟伅'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_login_time', 'login_time'),
        sa.Index('idx_status', 'status'),
        comment='鐧诲綍鏃ュ織琛?
    )

    # 创建鎿嶄綔鏃ュ織琛?    op.create_table(
        'operation_logs',
        sa.Column('id', sa.String(50), primary_key=True, comment='鏃ュ織ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('username', sa.String(50), nullable=False, comment='用户名?),
        sa.Column('module', sa.String(50), nullable=False, comment='妯″潡'),
        sa.Column('action', sa.String(50), nullable=False, comment='鎿嶄綔'),
        sa.Column('method', sa.String(10), nullable=False, comment='HTTP鏂规硶'),
        sa.Column('path', sa.String(255), nullable=False, comment='璇锋眰璺緞'),
        sa.Column('params', sa.Text, comment='璇锋眰鍙傛暟'),
        sa.Column('ip', sa.String(50), comment='IP地址'),
        sa.Column('user_agent', sa.String(255), comment='鐢ㄦ埛浠ｇ悊'),
        sa.Column('execute_time', sa.Integer, comment='鎵ц鏃堕棿(ms)'),
        sa.Column('status', sa.String(20), nullable=False, comment='状态?),
        sa.Column('message', sa.String(255), comment='娑堟伅'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_module', 'module'),
        sa.Index('idx_action', 'action'),
        sa.Index('idx_created_at', 'created_at'),
        sa.Index('idx_status', 'status'),
        comment='鎿嶄綔鏃ュ織琛?
    )

    # 创建閫氱煡琛?    op.create_table(
        'notifications',
        sa.Column('id', sa.String(50), primary_key=True, comment='閫氱煡ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, index=True, comment='租户ID'),
        sa.Column('title', sa.String(200), nullable=False, comment='鏍囬'),
        sa.Column('content', sa.Text, comment='鍐呭'),
        sa.Column('type', sa.String(20), nullable=False, comment='閫氱煡类型'),
        sa.Column('priority', sa.String(20), nullable=False, default='normal', comment='浼樺厛绾?),
        sa.Column('target_type', sa.String(20), nullable=False, comment='鐩爣类型'),
        sa.Column('target_id', sa.String(50), comment='鐩爣ID'),
        sa.Column('sender_id', sa.String(50), comment='鍙戦€佽€匢D'),
        sa.Column('sender_name', sa.String(50), comment='鍙戦€佽€呭悕绉?),
        sa.Column('status', sa.String(20), nullable=False, default='unread', comment='状态?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新鏃堕棿'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_type', 'type'),
        sa.Index('idx_target_type', 'target_type'),
        sa.Index('idx_status', 'status'),
        comment='閫氱煡琛?
    )

    # 创建閫氱煡宸茶琛?    op.create_table(
        'notification_reads',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('notification_id', sa.String(50), nullable=False, comment='閫氱煡ID'),
        sa.Column('user_id', sa.String(50), nullable=False, comment='用户ID'),
        sa.Column('read_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='宸茶鏃堕棿'),
        sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('notification_id', 'user_id', name='uk_notification_user'),
        sa.Index('idx_notification_id', 'notification_id'),
        sa.Index('idx_user_id', 'user_id'),
        comment='閫氱煡宸茶琛?
    )

    # 创建寰呭姙浠诲姟琛?    op.create_table(
        'todo_tasks',
        sa.Column('id', sa.String(50), primary_key=True, comment='浠诲姟ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('title', sa.String(200), nullable=False, comment='浠诲姟鏍囬'),
        sa.Column('description', sa.Text, comment='浠诲姟描述'),
        sa.Column('type', sa.String(20), nullable=False, default='personal', comment='浠诲姟类型'),
        sa.Column('priority', sa.String(20), nullable=False, default='medium', comment='浼樺厛绾?),
        sa.Column('status', sa.String(20), nullable=False, default='pending', comment='状态?),
        sa.Column('due_date', sa.DateTime, comment='鎴鏃ユ湡'),
        sa.Column('completed_at', sa.DateTime, comment='瀹屾垚鏃堕棿'),
        sa.Column('tags', sa.String(255), comment='鏍囩'),
        sa.Column('attachment', sa.String(255), comment='闄勪欢'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新鏃堕棿'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_type', 'type'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_priority', 'priority'),
        sa.Index('idx_due_date', 'due_date'),
        comment='寰呭姙浠诲姟琛?
    )

    # 创建姣忔棩璁″垝琛?    op.create_table(
        'daily_plans',
        sa.Column('id', sa.String(50), primary_key=True, comment='璁″垝ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('plan_date', sa.Date, nullable=False, comment='璁″垝鏃ユ湡'),
        sa.Column('task_ids', sa.Text, comment='浠诲姟ID鍒楄〃'),
        sa.Column('completed_count', sa.Integer, nullable=False, default=0, comment='瀹屾垚数量'),
        sa.Column('total_count', sa.Integer, nullable=False, default=0, comment='鎬绘暟閲?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新鏃堕棿'),
        sa.UniqueConstraint('user_id', 'plan_date', name='uk_user_date'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_plan_date', 'plan_date'),
        comment='姣忔棩璁″垝琛?
    )


def downgrade():
    op.drop_table('daily_plans')
    op.drop_table('todo_tasks')
    op.drop_table('notification_reads')
    op.drop_table('notifications')
    op.drop_table('operation_logs')
    op.drop_table('login_logs')
