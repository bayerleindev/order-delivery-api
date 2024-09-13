"""empty message

Revision ID: 2409bdb65203
Revises: bb7006b5b6a7
Create Date: 2024-09-09 00:25:43.171996

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2409bdb65203"
down_revision = "bb7006b5b6a7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("item", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.REAL(),
            type_=sa.Float(precision=2),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("item", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.Float(precision=2),
            type_=sa.REAL(),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
