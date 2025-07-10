"""Add chunk_count to file_metadata and manage other table changes

Revision ID: 1d3aa5e9d35b
Revises: b00573ede956
Create Date: 2025-07-05 19:23:56.338079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# pgvector is not automatically imported, so we may need to add it
# if we were creating a vector column.
# from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '1d3aa5e9d35b'
down_revision: Union[str, Sequence[str], None] = 'b00573ede956'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # This migration handles several detected changes:
    # 1. Creates the 'model_versions' table.
    # 2. Adds the 'chunk_count' column to 'file_metadata'.
    # 3. (Manually handled) Drops several now-unused tables.

    # 1. Create the 'model_versions' table
    op.create_table('model_versions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('model_name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('loaded_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('model_name')
    )
    
    # 2. Add the 'chunk_count' column
    op.add_column('file_metadata', 
        sa.Column('chunk_count', sa.Integer(), nullable=False, server_default=sa.text('0'))
    )

    # 3. The following tables were dropped manually using psql to handle dependencies.
    # We leave these commented out to record what happened, but prevent errors.
    # Correct drop order would be: langchain_pg_embedding, then langchain_pg_collection.
    # op.drop_table('langchain_pg_embedding')
    # op.drop_table('langchain_pg_collection')
    # op.drop_table('document_chunks')


def downgrade() -> None:
    """Downgrade schema."""
    # This should only reverse the changes made in the upgrade() function.
    
    # Drop the 'chunk_count' column
    op.drop_column('file_metadata', 'chunk_count')
    
    # Drop the 'model_versions' table
    op.drop_table('model_versions')
    
    # We don't need to re-create the dropped tables in a downgrade.
    # If we truly needed to revert to that state, we would downgrade
    # to the revision before this one.