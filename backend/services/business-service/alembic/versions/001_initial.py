# -*- coding: utf-8 -*-
"""创建业务服务相关表

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
    # 创建工作流模板表
    op.create_table(
        'workflow_templates',
        sa.Column('id', sa.String(50), primary_key=True, comment='模板ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='模板名称'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='模板编码'),
        sa.Column('category', sa.String(50), nullable=False, comment='模板分类'),
        sa.Column('description', sa.Text, comment='描述'),
        sa.Column('definition', sa.Text, nullable=False, comment='流程定义'),
        sa.Column('version', sa.String(20), nullable=False, default='1.0', comment='版本'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='状态'),
        sa.Column('created_by', sa.String(50), comment='创建人ID'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Index('idx_category', 'category'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_code', 'code'),
        comment='工作流模板表'
    )

    # 创建工作流实例表
    op.create_table(
        'workflows',
        sa.Column('id', sa.String(50), primary_key=True, comment='工作流ID'),
        sa.Column('template_id', sa.String(50), nullable=False, comment='模板ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='工作流名称'),
        sa.Column('status', sa.String(20), nullable=False, default='running', comment='状态'),
        sa.Column('current_node', sa.String(50), comment='当前节点'),
        sa.Column('initiator_id', sa.String(50), nullable=False, comment='发起人ID'),
        sa.Column('initiator_name', sa.String(50), nullable=False, comment='发起人名称'),
        sa.Column('form_data', sa.Text, comment='表单数据'),
        sa.Column('variables', sa.Text, comment='流程变量'),
        sa.Column('started_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='开始时间'),
        sa.Column('finished_at', sa.DateTime, comment='结束时间'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.ForeignKeyConstraint(['template_id'], ['workflow_templates.id'], ondelete='CASCADE'),
        sa.Index('idx_template_id', 'template_id'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_initiator_id', 'initiator_id'),
        sa.Index('idx_started_at', 'started_at'),
        comment='工作流实例表'
    )

    # 创建工作流任务表
    op.create_table(
        'workflow_tasks',
        sa.Column('id', sa.String(50), primary_key=True, comment='任务ID'),
        sa.Column('workflow_id', sa.String(50), nullable=False, comment='工作流ID'),
        sa.Column('node_id', sa.String(50), nullable=False, comment='节点ID'),
        sa.Column('node_name', sa.String(100), nullable=False, comment='节点名称'),
        sa.Column('node_type', sa.String(20), nullable=False, comment='节点类型'),
        sa.Column('assignee_id', sa.String(50), comment='审批人ID'),
        sa.Column('assignee_name', sa.String(50), comment='审批人名称'),
        sa.Column('status', sa.String(20), nullable=False, default='pending', comment='状态'),
        sa.Column('comment', sa.Text, comment='审批意见'),
        sa.Column('action', sa.String(20), comment='操作'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Column('completed_at', sa.DateTime, comment='完成时间'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.Index('idx_workflow_id', 'workflow_id'),
        sa.Index('idx_assignee_id', 'assignee_id'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_created_at', 'created_at'),
        comment='工作流任务表'
    )

    # 创建工作流节点表
    op.create_table(
        'workflow_nodes',
        sa.Column('id', sa.String(50), primary_key=True, comment='节点ID'),
        sa.Column('workflow_id', sa.String(50), nullable=False, comment='工作流ID'),
        sa.Column('node_id', sa.String(50), nullable=False, comment='节点ID'),
        sa.Column('node_name', sa.String(100), nullable=False, comment='节点名称'),
        sa.Column('node_type', sa.String(20), nullable=False, comment='节点类型'),
        sa.Column('position_x', sa.Integer, comment='X坐标'),
        sa.Column('position_y', sa.Integer, comment='Y坐标'),
        sa.Column('config', sa.Text, comment='节点配置'),
        sa.Column('status', sa.String(20), nullable=False, default='pending', comment='状态'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='更新时间'),
        sa.Column('completed_at', sa.DateTime, comment='完成时间'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.Index('idx_workflow_id', 'workflow_id'),
        sa.Index('idx_node_id', 'node_id'),
        sa.Index('idx_status', 'status'),
        comment='工作流节点表'
    )

    # 创建工作流连线表
    op.create_table(
        'workflow_edges',
        sa.Column('id', sa.String(50), primary_key=True, comment='连线ID'),
        sa.Column('workflow_id', sa.String(50), nullable=False, comment='工作流ID'),
        sa.Column('source_node_id', sa.String(50), nullable=False, comment='源节点ID'),
        sa.Column('target_node_id', sa.String(50), nullable=False, comment='目标节点ID'),
        sa.Column('condition', sa.Text, comment='条件表达式'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='创建时间'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.Index('idx_workflow_id', 'workflow_id'),
        sa.Index('idx_source_node_id', 'source_node_id'),
        sa.Index('idx_target_node_id', 'target_node_id'),
        comment='工作流连线表'
    )


def downgrade():
    op.drop_table('workflow_edges')
    op.drop_table('workflow_nodes')
    op.drop_table('workflow_tasks')
    op.drop_table('workflows')
    op.drop_table('workflow_templates')