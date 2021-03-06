"""rename user permissions column

Revision ID: 812387580a0b
Revises: a97dabbd44f4
Create Date: 2016-11-09 11:40:11.657516

"""

# revision identifiers, used by Alembic.
revision = '812387580a0b'
down_revision = 'a97dabbd44f4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('TRUNCATE permission_type')
    op.add_column('users', sa.Column('permission_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key('user_permission_type_fk', 'users', 'permission_type', ['permission_type_id'], ['permission_type_id'])
    op.drop_column('users', 'permissions')
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('permissions', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint('user_permission_type_fk', 'users', type_='foreignkey')
    op.drop_column('users', 'permission_type_id')
    op.execute('TRUNCATE permission_type')
    ### end Alembic commands ###
