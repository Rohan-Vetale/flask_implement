"""third rev

Revision ID: d7f5cbef0877
Revises: f829d140672c
Create Date: 2024-04-30 16:00:17.239499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7f5cbef0877'
down_revision: Union[str, None] = 'f829d140672c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"User_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('twitter_id', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('oauth_token', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('oauth_token_secret', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='User_pkey'),
    sa.UniqueConstraint('email', name='User_email_key'),
    sa.UniqueConstraint('twitter_id', name='User_twitter_id_key'),
    sa.UniqueConstraint('username', name='User_username_key')
    )
    # ### end Alembic commands ###
