"""create_users_table

Revision ID: 1c573f521604
Revises: 53418deec21a
Create Date: 2023-05-24 11:29:24.296887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c573f521604'
down_revision = '53418deec21a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email_id', sa.Integer(), sa.ForeignKey("emails.id", ondelete="CASCADE"), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('created_on', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_on', sa.DateTime()),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='True'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_id')
    )



def downgrade() -> None:
    op.drop_table('users')