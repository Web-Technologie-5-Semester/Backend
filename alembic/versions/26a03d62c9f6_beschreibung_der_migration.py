"""Beschreibung der Migration

Revision ID: 26a03d62c9f6
Revises: 
Create Date: 2024-11-08 10:55:52.782426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26a03d62c9f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publisher')
    op.drop_table('genre')
    op.drop_table('author')
    op.drop_table('book')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.create_table('author',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('birthday', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='author_pkey')
    )
    op.create_table('genre',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='genre_pkey')
    )
    op.create_table('publisher',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('publisher', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='publisher_pkey')
    )
    # ### end Alembic commands ###
