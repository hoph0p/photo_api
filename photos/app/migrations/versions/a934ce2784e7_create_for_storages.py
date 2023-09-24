"""create for storages

Revision ID: a934ce2784e7
Revises: 
Create Date: 2023-08-13 20:48:50.385307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a934ce2784e7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('processed_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_storage_id'), 'storage', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_storage_id'), table_name='storage')
    op.drop_table('storage')
    # ### end Alembic commands ###