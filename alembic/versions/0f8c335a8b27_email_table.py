"""email table

Revision ID: 0f8c335a8b27
Revises: 
Create Date: 2023-05-24 11:10:37.988011

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0f8c335a8b27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index('ix_verify_tokens_id', table_name='verify_tokens')
    op.drop_table('verify_tokens')
    op.drop_index('ix_access_tokens_id', table_name='access_tokens')
    op.drop_table('access_tokens')
    op.drop_table('user_detials')
    op.drop_index('ix_emails_id', table_name='emails')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_emails_id', 'emails', ['id'], unique=False)
    op.create_table('user_detials',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bio', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_detials_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='user_detials_pkey')
    )
    op.create_table('access_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('expiration_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='access_tokens_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='access_tokens_pkey')
    )
    op.create_index('ix_access_tokens_id', 'access_tokens', ['id'], unique=False)
    op.create_table('verify_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['email_id'], ['emails.id'], name='verify_tokens_email_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='verify_tokens_pkey')
    )
    op.create_index('ix_verify_tokens_id', 'verify_tokens', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('date_of_birth', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['email_id'], ['emails.id'], name='users_email_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email_id', name='users_email_id_key')
    )
    # ### end Alembic commands ###
