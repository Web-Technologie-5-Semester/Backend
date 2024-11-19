"""genre, publisher, author name column

Revision ID: d1f583c999df
Revises: 3b6962ad5e71
Create Date: 2024-11-13 13:26:19.743531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1f583c999df'
down_revision: Union[str, None] = '3b6962ad5e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publisher')
    op.drop_table('role')
    op.drop_table('book')
    op.drop_table('genre')
    op.drop_table('author')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('forename', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('residence', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('postal_code', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('street', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('id_role', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_role'], ['role.id'], name='user_id_role_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_table('author',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('author_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('birthday', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='author_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('genre',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('genre_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='genre_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('book',
    sa.Column('isbn', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('release', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('age_recommendation', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('publisher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('stock', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='book_author_id_fkey'),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], name='book_genre_id_fkey'),
    sa.ForeignKeyConstraint(['publisher_id'], ['publisher.id'], name='book_publisher_id_fkey'),
    sa.PrimaryKeyConstraint('isbn', name='book_pkey')
    )
    op.create_table('role',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='role_pkey')
    )
    op.create_table('publisher',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('publisher', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='publisher_pkey')
    )
    # ### end Alembic commands ###