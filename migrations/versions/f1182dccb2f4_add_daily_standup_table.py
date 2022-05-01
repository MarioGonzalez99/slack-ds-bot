"""Add daily_standup table

Revision ID: f1182dccb2f4
Revises: e741ad6fcf76
Create Date: 2022-02-25 10:29:41.891902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1182dccb2f4'
down_revision = 'e741ad6fcf76'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('daily_standup',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('date', sa.Date(), nullable=False),
                    sa.Column('yesterday_question',
                              sa.String(3000), nullable=False),
                    sa.Column('today_question',
                              sa.String(3000), nullable=False),
                    sa.Column('blockers_question',
                              sa.String(3000), nullable=False),
                    sa.Column('user_id', sa.String(100), sa.ForeignKey(
                        "user.id"), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('daily_standup')
    pass
