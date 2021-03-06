"""update d1 and d2 for daims v1.1

Revision ID: 2ae156c8f46d
Revises: 4b1ee78268fb
Create Date: 2017-08-28 15:16:00.926683

"""

# revision identifiers, used by Alembic.
revision = '2ae156c8f46d'
down_revision = '4b1ee78268fb'
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
    op.add_column('award_procurement', sa.Column('award_or_idv_flag', sa.Text(), nullable=True))
    op.add_column('award_procurement', sa.Column('place_of_perform_country_n', sa.Text(), nullable=True))
    op.add_column('award_procurement', sa.Column('place_of_perform_county_na', sa.Text(), nullable=True))
    op.add_column('award_procurement', sa.Column('place_of_perform_state_nam', sa.Text(), nullable=True))
    op.add_column('award_procurement', sa.Column('referenced_idv_agency_name', sa.Text(), nullable=True))
    op.add_column('award_procurement', sa.Column('referenced_idv_type', sa.Text(), nullable=True))
    op.add_column('award_procurement', sa.Column('referenced_multi_or_single', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('place_of_perform_country_n', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('place_of_perform_state_nam', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('referenced_idv_agency_name', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('referenced_multi_or_single', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('award_or_idv_flag', sa.Text(), nullable=True))
    op.add_column('award_financial_assistance', sa.Column('legal_entity_country_name', sa.Text(), nullable=True))
    op.add_column('award_financial_assistance', sa.Column('place_of_perform_country_n', sa.Text(), nullable=True))
    op.add_column('award_financial_assistance', sa.Column('place_of_perform_county_co', sa.Text(), nullable=True))
    op.add_column('detached_award_financial_assistance', sa.Column('legal_entity_country_name', sa.Text(), nullable=True))
    op.add_column('detached_award_financial_assistance', sa.Column('place_of_perform_country_n', sa.Text(), nullable=True))
    op.add_column('detached_award_financial_assistance', sa.Column('place_of_perform_county_co', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('legal_entity_country_name', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('place_of_perform_country_n', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('place_of_perform_county_co', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('published_award_financial_assistance', 'place_of_perform_county_co')
    op.drop_column('published_award_financial_assistance', 'place_of_perform_country_n')
    op.drop_column('published_award_financial_assistance', 'legal_entity_country_name')
    op.drop_column('detached_award_financial_assistance', 'place_of_perform_county_co')
    op.drop_column('detached_award_financial_assistance', 'place_of_perform_country_n')
    op.drop_column('detached_award_financial_assistance', 'legal_entity_country_name')
    op.drop_column('award_financial_assistance', 'place_of_perform_county_co')
    op.drop_column('award_financial_assistance', 'place_of_perform_country_n')
    op.drop_column('award_financial_assistance', 'legal_entity_country_name')
    op.drop_column('detached_award_procurement', 'referenced_multi_or_single')
    op.drop_column('detached_award_procurement', 'referenced_idv_agency_name')
    op.drop_column('detached_award_procurement', 'place_of_perform_state_nam')
    op.drop_column('detached_award_procurement', 'place_of_perform_country_n')
    op.drop_column('detached_award_procurement', 'award_or_idv_flag')
    op.drop_column('award_procurement', 'referenced_multi_or_single')
    op.drop_column('award_procurement', 'referenced_idv_type')
    op.drop_column('award_procurement', 'referenced_idv_agency_name')
    op.drop_column('award_procurement', 'place_of_perform_state_nam')
    op.drop_column('award_procurement', 'place_of_perform_county_na')
    op.drop_column('award_procurement', 'place_of_perform_country_n')
    op.drop_column('award_procurement', 'award_or_idv_flag')
    ### end Alembic commands ###

