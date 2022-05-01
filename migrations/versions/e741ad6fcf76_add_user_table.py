"""Add user table

Revision ID: e741ad6fcf76
Revises: 
Create Date: 2022-02-25 10:21:03.313611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e741ad6fcf76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.String(100),
                              nullable=False, primary_key=True),
                    sa.Column('username', sa.String(255),
                              unique=True, nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('user')
    pass
