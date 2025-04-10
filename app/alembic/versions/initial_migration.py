"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tables table
    op.create_table(
        'tables',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('seats', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tables_name'), 'tables', ['name'], unique=False)
    op.create_index(op.f('ix_tables_location'), 'tables', ['location'], unique=False)

    # Create reservations table
    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_name', sa.String(length=100), nullable=False),
        sa.Column('table_id', sa.Integer(), nullable=False),
        sa.Column('reservation_time', sa.DateTime(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['table_id'], ['tables.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_customer_name'), 'reservations', ['customer_name'], unique=False)
    op.create_index(op.f('ix_reservations_reservation_time'), 'reservations', ['reservation_time'], unique=False)
    op.create_index(op.f('ix_reservations_table_id'), 'reservations', ['table_id'], unique=False)


def downgrade() -> None:
    # Drop reservations table
    op.drop_index(op.f('ix_reservations_table_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_reservation_time'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_customer_name'), table_name='reservations')
    op.drop_table('reservations')

    # Drop tables table
    op.drop_index(op.f('ix_tables_location'), table_name='tables')
    op.drop_index(op.f('ix_tables_name'), table_name='tables')
    op.drop_table('tables') 