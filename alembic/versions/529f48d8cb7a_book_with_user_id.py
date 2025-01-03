"""book with user_id

Revision ID: 529f48d8cb7a
Revises: efac7a6763e2
Create Date: 2025-01-03 18:26:22.166129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '529f48d8cb7a'
down_revision: Union[str, None] = 'efac7a6763e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'book', 'user', ['user_id'], ['id'])
    op.alter_column('user', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_column('book', 'user_id')
    # ### end Alembic commands ###
