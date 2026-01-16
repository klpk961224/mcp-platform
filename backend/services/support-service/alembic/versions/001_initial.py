# -*- coding: utf-8 -*-
"""创建支撑服务相关表

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
    # 创建登录日志表
    op.create_table(
        'login_logs',
        sa.Column('id', sa.String(50), primary_key=True, comment='日志ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('username', sa.String(50), nullable=False, comment='用户名'),
        sa.Column('ip', sa.String(50), comment='IP地址'),
        sa.Column('user_agent', sa.String(255), comment='用户代理'),
        sa.Column('login_time', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='登录时间'),
        sa.Column('status', sa.String(20), nullable=False, comment='状态'),
        sa.Column('message', sa.String(255), comment='消息'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_login_time', 'login_time'),
        sa.Index('idx_status', 'status'),
        comment='登录日志表'
    )

    # 创建操作日志表
    op.create_table(
        'operation_logs',
        sa.Column('id', sa.String(50), primary_key=True, comment='日志ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('username', sa.String(50), nullable=False, comment='用户名'),
        sa.Column('module', sa.String(50), nullable=False, comment='模块'),
        sa.Column('action', sa.String(50), nullable=False, comment='操作'),
        sa.Column('method', sa.String(10), nullable=False, comment='HTTP方法'),
        sa.Column('path', sa.String(255), nullable=False, comment='请求路径'),
        sa.Column('params', sa.Text, comment='请求参数'),
        sa.Column('ip', sa.String(50), comment='IP地址'),
        sa.Column('user_agent', sa.String(255), comment='用户代理'),
        sa.Column('execute_time', sa.Integer, comment='执行时间(ms)'),
        sa.Column('status', sa.String(20), nullable=False, comment='状态'),
        sa.Column('message', sa.String(255), comment='消息'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_module', 'module'),
        sa.Index('idx_action', 'action'),
        sa.Index('idx_created_at', 'created_at'),
        sa.Index('idx_status', 'status'),
        comment='操作日志表'
    )

    # 创建通知表
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(50), primary_key=True, comment='通知ID'),
        sa.Column('tenant_id', sa.String(50), nullable=False, index=True, comment='租户ID'),
        sa.Column('title', sa.String(200), nullable=False, comment='标题'),
        sa.Column('content', sa.Text, comment='内容'),
        sa.Column('type', sa.String(20), nullable=False, comment='通知类型'),
        sa.Column('priority', sa.String(20), nullable=False, default='normal', comment='优先级'),
        sa.Column('target_type', sa.String(20), nullable=False, comment='目标类型'),
        sa.Column('target_id', sa.String(50), comment='目标ID'),
        sa.Column('sender_id', sa.String(50), comment='发送者ID'),
        sa.Column('sender_name', sa.String(50), comment='发送者名称'),
        sa.Column('status', sa.String(20), nullable=False, default='unread', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_tenant_id', 'tenant_id'),
        sa.Index('idx_type', 'type'),
        sa.Index('idx_target_type', 'target_type'),
        sa.Index('idx_status', 'status'),
        comment='通知表'
    )

    # 创建通知已读表
    op.create_table(
        'notification_reads',
        sa.Column('id', sa.String(50), primary_key=True, comment='ID'),
        sa.Column('notification_id', sa.String(50), nullable=False, comment='通知ID'),
        sa.Column('user_id', sa.String(50), nullable=False, comment='用户ID'),
        sa.Column('read_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='已读时间'),
        sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('notification_id', 'user_id', name='uk_notification_user'),
        sa.Index('idx_notification_id', 'notification_id'),
        sa.Index('idx_user_id', 'user_id'),
        comment='通知已读表'
    )

    # 创建待办任务表
    op.create_table(
        'todo_tasks',
        sa.Column('id', sa.String(50), primary_key=True, comment='任务ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('title', sa.String(200), nullable=False, comment='任务标题'),
        sa.Column('description', sa.Text, comment='任务描述'),
        sa.Column('type', sa.String(20), nullable=False, default='personal', comment='任务类型'),
        sa.Column('priority', sa.String(20), nullable=False, default='medium', comment='优先级'),
        sa.Column('status', sa.String(20), nullable=False, default='pending', comment='状态'),
        sa.Column('due_date', sa.DateTime, comment='截止日期'),
        sa.Column('completed_at', sa.DateTime, comment='完成时间'),
        sa.Column('tags', sa.String(255), comment='标签'),
        sa.Column('attachment', sa.String(255), comment='附件'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_type', 'type'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_priority', 'priority'),
        sa.Index('idx_due_date', 'due_date'),
        comment='待办任务表'
    )

    # 创建每日计划表
    op.create_table(
        'daily_plans',
        sa.Column('id', sa.String(50), primary_key=True, comment='计划ID'),
        sa.Column('user_id', sa.String(50), nullable=False, index=True, comment='用户ID'),
        sa.Column('plan_date', sa.Date, nullable=False, comment='计划日期'),
        sa.Column('task_ids', sa.Text, comment='任务ID列表'),
        sa.Column('completed_count', sa.Integer, nullable=False, default=0, comment='完成数量'),
        sa.Column('total_count', sa.Integer, nullable=False, default=0, comment='总数量'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.UniqueConstraint('user_id', 'plan_date', name='uk_user_date'),
        sa.Index('idx_user_id', 'user_id'),
        sa.Index('idx_plan_date', 'plan_date'),
        comment='每日计划表'
    )


def downgrade():
    op.drop_table('daily_plans')
    op.drop_table('todo_tasks')
    op.drop_table('notification_reads')
    op.drop_table('notifications')
    op.drop_table('operation_logs')
    op.drop_table('login_logs')