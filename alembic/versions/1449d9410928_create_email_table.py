"""create_email_table

Revision ID: 1449d9410928
Revises: 
Create Date: 2023-05-24 11:18:31.639030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1449d9410928'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table('emails',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('emails')
