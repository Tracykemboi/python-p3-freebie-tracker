"""create_freebies_table

Revision ID: <some_generated_id>
Revises: 5f72c58bf48c
Create Date: <current_date_and_time>

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '<some_generated_id>'
down_revision = '5f72c58bf48c'
branch_labels = None
depends_on = None


def upgrade():
    # Create freebies table
    op.create_table('freebies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_name', sa.String(), nullable=True),
        sa.Column('value', sa.Integer(), nullable=True),
        sa.Column('dev_id', sa.Integer(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create company_dev association table
    op.create_table('company_dev',
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('dev_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], )
    )


def downgrade():
    # Drop tables
    op.drop_table('company_dev')
    op.drop_table('freebies')