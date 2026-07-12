"""subjects теперь unique

Revision ID: 3b7f22e3e685
Revises: ab9f62bf0d4c
Create Date: 2026-07-12 13:30:48.908250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7f22e3e685'
down_revision = 'ab9f62bf0d4c'
branch_labels = None
depends_on = None

def upgrade():

    with op.batch_alter_table("subject") as batch_op:

        batch_op.create_unique_constraint(
            "uq_subject_name",
            ["name"]
        )


def downgrade():

    with op.batch_alter_table("subject") as batch_op:

        batch_op.drop_constraint(
            "uq_subject_name",
            type_="unique"
        )