"""The urls and faces tables are created

Revision ID: 2ae0baefaf1b
Revises: 
Create Date: 2021-04-23 00:26:51.979450

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2ae0baefaf1b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "faces",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("url_id", sa.BigInteger(), nullable=False),
        sa.Column("ts", sa.Float(), nullable=False),
        sa.Column("face_id", sa.SmallInteger(), nullable=False),
        sa.Column("box", postgresql.ARRAY(sa.SmallInteger(), as_tuple=True), nullable=True),
        sa.Column("entity", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("encoder", sa.String(), nullable=False),
        sa.Column("encoding", postgresql.ARRAY(sa.Float()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "urls",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("urls")
    op.drop_table("faces")
    # ### end Alembic commands ###