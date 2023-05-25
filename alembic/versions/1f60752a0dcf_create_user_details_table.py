"""create_user_details_table

Revision ID: 1f60752a0dcf
Revises: 1c573f521604
Create Date: 2023-05-24 11:35:09.042796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f60752a0dcf'
down_revision = '1c573f521604'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table(
        'user_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column('bio', sa.String()),
        sa.Column('image_url', sa.String()),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('created_on', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_on', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('user_details')
