"""upgrade table restaurants

Revision ID: 743ee2d4cff2
Revises: 5300a4d52af7
Create Date: 2025-06-30 16:17:56.569115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743ee2d4cff2'
down_revision: Union[str, None] = '5300a4d52af7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Restaurants', sa.Column('detailed_description', sa.Text(), nullable=True))
    op.alter_column('Restaurants', 'name',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=150),
               existing_nullable=False)
    op.alter_column('Restaurants', 'description',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('Restaurants', 'menu',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
    op.add_column('users', sa.Column('comments', sa.JSON(), nullable=True))
    op.drop_column('users', 'comment')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'comments')
    op.alter_column('Restaurants', 'menu',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    op.alter_column('Restaurants', 'description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)
    op.alter_column('Restaurants', 'name',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    op.drop_column('Restaurants', 'detailed_description')
    # ### end Alembic commands ###
