"""create_access_token_table

Revision ID: 4922f2981e57
Revises: 1f60752a0dcf
Create Date: 2023-05-24 11:43:02.980077

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4922f2981e57'
down_revision = '1f60752a0dcf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'access_tokens',
        sa.Column('id', sa.Integer(), nullable=False, index=True),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('expiration_time', sa.DateTime()),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='True'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
 op.drop_table('access_tokens')
