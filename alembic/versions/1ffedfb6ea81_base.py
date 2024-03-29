"""empty message

Revision ID: 1ffedfb6ea81_base
Revises: 
Create Date: 2022-04-17 17:52:24.159371

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1ffedfb6ea81_base"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("auth0_id", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("auth0_id"),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("teaser", sa.String(length=500), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("author", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("modified_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author"], ["authors.id"], name="fk_articles_authors_id_author"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "articles_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tag", sa.Integer(), nullable=True),
        sa.Column("article", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["article"],
            ["articles.id"],
            name="fk_articles_tags_articles_article_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tag"],
            ["tags.id"],
            name="fk_articles_tags_tags_tag_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("articles_tags")
    op.drop_table("articles")
    op.drop_table("tags")
    op.drop_table("authors")
