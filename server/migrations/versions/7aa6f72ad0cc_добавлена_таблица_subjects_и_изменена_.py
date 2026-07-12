"""Добавлена таблица Subjects и изменена таблица User

Revision ID: 7aa6f72ad0cc
Revises: 0938e640bfb1
Create Date: 2026-07-11 16:22:16.106069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aa6f72ad0cc'
down_revision = '0938e640bfb1'
branch_labels = None
depends_on = None

def upgrade():
    # Просто создаем таблицу subjects с нуля
    op.create_table('subjects',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ), # Убедитесь, что тут user.id, а не users.id
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('subjects')

    # ### end Alembic commands ###
