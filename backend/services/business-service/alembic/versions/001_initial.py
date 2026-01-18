# -*- coding: utf-8 -*-
"""鍒涘缓涓氬姟鏈嶅姟鐩稿叧琛?
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
    # 鍒涘缓宸ヤ綔娴佹ā鏉胯〃
    op.create_table(
        'workflow_templates',
        sa.Column('id', sa.String(50), primary_key=True, comment='妯℃澘ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='妯℃澘鍚嶇О'),
        sa.Column('code', sa.String(100), nullable=False, unique=True, comment='妯℃澘缂栫爜'),
        sa.Column('category', sa.String(50), nullable=False, comment='妯℃澘鍒嗙被'),
        sa.Column('description', sa.Text, comment='鎻忚堪'),
        sa.Column('definition', sa.Text, nullable=False, comment='娴佺▼瀹氫箟'),
        sa.Column('version', sa.String(20), nullable=False, default='1.0', comment='鐗堟湰'),
        sa.Column('status', sa.String(20), nullable=False, default='active', comment='鐘舵€?),
        sa.Column('created_by', sa.String(50), comment='鍒涘缓浜篒D'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Index('idx_category', 'category'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_code', 'code'),
        comment='宸ヤ綔娴佹ā鏉胯〃'
    )

    # 鍒涘缓宸ヤ綔娴佸疄渚嬭〃
    op.create_table(
        'workflows',
        sa.Column('id', sa.String(50), primary_key=True, comment='宸ヤ綔娴両D'),
        sa.Column('template_id', sa.String(50), nullable=False, comment='妯℃澘ID'),
        sa.Column('name', sa.String(100), nullable=False, comment='宸ヤ綔娴佸悕绉?),
        sa.Column('status', sa.String(20), nullable=False, default='running', comment='鐘舵€?),
        sa.Column('current_node', sa.String(50), comment='褰撳墠鑺傜偣'),
        sa.Column('initiator_id', sa.String(50), nullable=False, comment='鍙戣捣浜篒D'),
        sa.Column('initiator_name', sa.String(50), nullable=False, comment='鍙戣捣浜哄悕绉?),
        sa.Column('form_data', sa.Text, comment='琛ㄥ崟鏁版嵁'),
        sa.Column('variables', sa.Text, comment='娴佺▼鍙橀噺'),
        sa.Column('started_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='寮€濮嬫椂闂?),
        sa.Column('finished_at', sa.DateTime, comment='缁撴潫鏃堕棿'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.ForeignKeyConstraint(['template_id'], ['workflow_templates.id'], ondelete='CASCADE'),
        sa.Index('idx_template_id', 'template_id'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_initiator_id', 'initiator_id'),
        sa.Index('idx_started_at', 'started_at'),
        comment='宸ヤ綔娴佸疄渚嬭〃'
    )

    # 鍒涘缓宸ヤ綔娴佷换鍔¤〃
    op.create_table(
        'workflow_tasks',
        sa.Column('id', sa.String(50), primary_key=True, comment='浠诲姟ID'),
        sa.Column('workflow_id', sa.String(50), nullable=False, comment='宸ヤ綔娴両D'),
        sa.Column('node_id', sa.String(50), nullable=False, comment='鑺傜偣ID'),
        sa.Column('node_name', sa.String(100), nullable=False, comment='鑺傜偣鍚嶇О'),
        sa.Column('node_type', sa.String(20), nullable=False, comment='鑺傜偣绫诲瀷'),
        sa.Column('assignee_id', sa.String(50), comment='瀹℃壒浜篒D'),
        sa.Column('assignee_name', sa.String(50), comment='瀹℃壒浜哄悕绉?),
        sa.Column('status', sa.String(20), nullable=False, default='pending', comment='鐘舵€?),
        sa.Column('comment', sa.Text, comment='瀹℃壒鎰忚'),
        sa.Column('action', sa.String(20), comment='鎿嶄綔'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Column('completed_at', sa.DateTime, comment='瀹屾垚鏃堕棿'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.Index('idx_workflow_id', 'workflow_id'),
        sa.Index('idx_assignee_id', 'assignee_id'),
        sa.Index('idx_status', 'status'),
        sa.Index('idx_created_at', 'created_at'),
        comment='宸ヤ綔娴佷换鍔¤〃'
    )

    # 鍒涘缓宸ヤ綔娴佽妭鐐硅〃
    op.create_table(
        'workflow_nodes',
        sa.Column('id', sa.String(50), primary_key=True, comment='鑺傜偣ID'),
        sa.Column('workflow_id', sa.String(50), nullable=False, comment='宸ヤ綔娴両D'),
        sa.Column('node_id', sa.String(50), nullable=False, comment='鑺傜偣ID'),
        sa.Column('node_name', sa.String(100), nullable=False, comment='鑺傜偣鍚嶇О'),
        sa.Column('node_type', sa.String(20), nullable=False, comment='鑺傜偣绫诲瀷'),
        sa.Column('position_x', sa.Integer, comment='X鍧愭爣'),
        sa.Column('position_y', sa.Integer, comment='Y鍧愭爣'),
        sa.Column('config', sa.Text, comment='鑺傜偣閰嶇疆'),
        sa.Column('status', sa.String(20), nullable=False, default='pending', comment='鐘舵€?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鏇存柊鏃堕棿'),
        sa.Column('completed_at', sa.DateTime, comment='瀹屾垚鏃堕棿'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.Index('idx_workflow_id', 'workflow_id'),
        sa.Index('idx_node_id', 'node_id'),
        sa.Index('idx_status', 'status'),
        comment='宸ヤ綔娴佽妭鐐硅〃'
    )

    # 鍒涘缓宸ヤ綔娴佽繛绾胯〃
    op.create_table(
        'workflow_edges',
        sa.Column('id', sa.String(50), primary_key=True, comment='杩炵嚎ID'),
        sa.Column('workflow_id', sa.String(50), nullable=False, comment='宸ヤ綔娴両D'),
        sa.Column('source_node_id', sa.String(50), nullable=False, comment='婧愯妭鐐笽D'),
        sa.Column('target_node_id', sa.String(50), nullable=False, comment='鐩爣鑺傜偣ID'),
        sa.Column('condition', sa.Text, comment='鏉′欢琛ㄨ揪寮?),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now(), comment='鍒涘缓鏃堕棿'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.Index('idx_workflow_id', 'workflow_id'),
        sa.Index('idx_source_node_id', 'source_node_id'),
        sa.Index('idx_target_node_id', 'target_node_id'),
        comment='宸ヤ綔娴佽繛绾胯〃'
    )


def downgrade():
    op.drop_table('workflow_edges')
    op.drop_table('workflow_nodes')
    op.drop_table('workflow_tasks')
    op.drop_table('workflows')
    op.drop_table('workflow_templates')
