"""
News Factory (Factory Method Pattern)
"""
import uuid
from datetime import datetime
from factory.base_factory import BaseFactory
from models.news import News


class NewsFactory(BaseFactory):
    """
    Factory for creating News objects.

    Allows creating news of different categories
    with appropriate presets.
    """

    def create(self, data: dict) -> News:
        """
        Creates news from data dictionary.

        Args:
            data: Dictionary with news data

        Returns:
            News object
        """
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        if 'created_at' not in data or not data['created_at']:
            data['created_at'] = datetime.now().isoformat()

        return News.from_dict(data)

    def create_default(self) -> News:
        """
        Creates news with default values.
        """
        return News(
            id=str(uuid.uuid4()),
            title="New Article",
            content="",
            category="Announcement",
            author="Admin",
            created_at=datetime.now().isoformat(),
            is_published=False,
            views_count=0
        )

    def create_event(self, title: str, content: str, author: str, image: str = None) -> News:
        """
        Creates event news.
        """
        return News(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            category="Event",
            author=author,
            created_at=datetime.now().isoformat(),
            image=image,
            is_published=True,
            views_count=0
        )

    def create_announcement(self, title: str, content: str, author: str) -> News:
        """
        Creates announcement.
        """
        return News(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            category="Announcement",
            author=author,
            created_at=datetime.now().isoformat(),
            is_published=True,
            views_count=0
        )

    def create_academic_news(self, title: str, content: str, author: str) -> News:
        """
        Creates academic news.
        """
        return News(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            category="Academic",
            author=author,
            created_at=datetime.now().isoformat(),
            is_published=True,
            views_count=0
        )

