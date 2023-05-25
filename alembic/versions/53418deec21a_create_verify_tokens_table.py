"""create_verify_tokens_table

Revision ID: 53418deec21a
Revises: 1449d9410928
Create Date: 2023-05-24 11:23:21.993454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53418deec21a'
down_revision = '1449d9410928'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'verify_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email_id', sa.Integer(), sa.ForeignKey("emails.id", ondelete="CASCADE"), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='True'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_id')
    )

def downgrade() -> None:
    op.drop_table('verify_tokens')
