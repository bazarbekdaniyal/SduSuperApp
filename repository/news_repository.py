"""
News Repository
"""
from typing import List, Optional
from repository.base_repository import BaseRepository
from models.news import News


class NewsRepository(BaseRepository[News]):
    """Repository for working with news."""

    def __init__(self, data_dir: str = None):
        super().__init__('news.json', data_dir)

    def _to_entity(self, data: dict) -> News:
        return News.from_dict(data)

    def _to_dict(self, entity: News) -> dict:
        return entity.to_dict()

    def get_published(self, limit: int = None) -> List[News]:
        """Returns published news."""
        all_news = self.get_all()
        published = [n for n in all_news if n.is_published]
        published = sorted(published, key=lambda n: n.created_at, reverse=True)
        if limit:
            return published[:limit]
        return published

    def get_drafts(self) -> List[News]:
        """Returns drafts."""
        all_news = self.get_all()
        return [n for n in all_news if not n.is_published]

    def find_by_category(self, category: str) -> List[News]:
        """Finds news by category."""
        all_news = self.get_all()
        result = [
            n for n in all_news
            if n.category.lower() == category.lower() and n.is_published
        ]
        return sorted(result, key=lambda n: n.created_at, reverse=True)

    def search(self, query: str) -> List[News]:
        """Searches news by title or content."""
        all_news = self.get_all()
        query_lower = query.lower()
        result = [
            n for n in all_news
            if (query_lower in n.title.lower() or query_lower in n.content.lower())
            and n.is_published
        ]
        return sorted(result, key=lambda n: n.created_at, reverse=True)

    def increment_views(self, news_id: str) -> Optional[News]:
        """Increments view counter."""
        news = self.get_by_id(news_id)
        if news:
            news.views_count += 1
            return self.update(news)
        return None

    def get_popular(self, limit: int = 5) -> List[News]:
        """Returns popular news."""
        published = self.get_published()
        return sorted(published, key=lambda n: n.views_count, reverse=True)[:limit]

    def get_categories(self) -> List[str]:
        """Returns list of categories."""
        all_news = self.get_all()
        categories = set(n.category for n in all_news)
        return sorted(list(categories))

    def publish(self, news_id: str) -> Optional[News]:
        """Publishes news."""
        news = self.get_by_id(news_id)
        if news:
            news.is_published = True
            return self.update(news)
        return None

    def unpublish(self, news_id: str) -> Optional[News]:
        """Unpublishes news."""
        news = self.get_by_id(news_id)
        if news:
            news.is_published = False
            return self.update(news)
        return None

