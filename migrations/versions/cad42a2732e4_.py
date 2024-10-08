"""empty message

Revision ID: cad42a2732e4
Revises: e39c7fb85f18
Create Date: 2024-05-16 17:17:02.396189

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cad42a2732e4'
down_revision = 'e39c7fb85f18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('orders_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='orders_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='orders_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('order_items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='order_items_order_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='order_items_product_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='order_items_pkey')
    )
    # ### end Alembic commands ###
