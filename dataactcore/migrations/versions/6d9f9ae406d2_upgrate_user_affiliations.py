"""Upgrade user-affiliations table to include frec_id

Revision ID: 6d9f9ae406d2
Revises: 20ee975316b9
Create Date: 2017-06-12 20:02:42.007400

"""

# revision identifiers, used by Alembic.
revision = '6d9f9ae406d2'
down_revision = '20ee975316b9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_data_broker():
    op.add_column('user_affiliation', sa.Column('frec_id', sa.Integer(), nullable=False))
    op.create_foreign_key('user_affiliation_frec_fk', 'user_affiliation', 'frec', ['frec_id'], ['frec_id'], ondelete='CASCADE')
    ### end Alembic commands ###


def downgrade_data_broker():
    op.drop_constraint('user_affiliation_frec_fk', 'user_affiliation', type_='foreignkey')
    op.drop_column('user_affiliation', 'frec_id')
    ### end Alembic commands ###

