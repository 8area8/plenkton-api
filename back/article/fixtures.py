"""Article fixtures."""

from back.db.models import Article, Author


class ArticlesFixture:
    """Create fake articles."""

    articles = [
        dict(name="Super Python part one", teaser="So fun", body="long body"),
        dict(name="Incredible JS", teaser="Okay", body="long body"),
        dict(name="Django or not Django", teaser="New one", body="long body"),
        dict(name="SQL and more", teaser="Why not", body="long body"),
        dict(name="Why learn Python 4", teaser="Wow !", body="long body"),
    ]

    async def add(self):
        """Create the articles."""
        admins = await Author.get_admins()
        for article in self.articles:
            artocle_obj = await Article.objects.get_or_none(name=article["name"])
            if not artocle_obj:
                await Article.objects.create(**article, author=admins[0])

    async def remove(self):
        """Delete the articles."""
        for name in [article["name"] for article in self.articles]:
            article = await Article.objects.get_or_none(name=name)
            if article:
                await article.delete()
