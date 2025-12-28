"""
Subscriber Repository
"""
from typing import List, Optional
from repository.base_repository import BaseRepository
from models.subscriber import Subscriber


class SubscriberRepository(BaseRepository[Subscriber]):
    """Repository for working with subscribers."""

    def __init__(self, data_dir: str = None):
        super().__init__('subscribers.json', data_dir)

    def _to_entity(self, data: dict) -> Subscriber:
        return Subscriber.from_dict(data)

    def _to_dict(self, entity: Subscriber) -> dict:
        return entity.to_dict()

    def find_by_email(self, email: str) -> Optional[Subscriber]:
        """Finds subscriber by email."""
        all_subscribers = self.get_all()
        for sub in all_subscribers:
            if sub.email.lower() == email.lower():
                return sub
        return None

    def get_active(self) -> List[Subscriber]:
        """Returns active subscribers."""
        all_subscribers = self.get_all()
        return [s for s in all_subscribers if s.is_active]

    def get_by_category(self, category: str) -> List[Subscriber]:
        """Returns subscribers to category."""
        all_subscribers = self.get_all()
        return [
            s for s in all_subscribers
            if s.is_active and ('all' in s.categories or category.lower() in [c.lower() for c in s.categories])
        ]

    def activate(self, subscriber_id: str) -> Optional[Subscriber]:
        """Activates subscriber."""
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            subscriber.is_active = True
            return self.update(subscriber)
        return None

    def deactivate(self, subscriber_id: str) -> Optional[Subscriber]:
        """Deactivates subscriber."""
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            subscriber.is_active = False
            return self.update(subscriber)
        return None

    def email_exists(self, email: str) -> bool:
        """Checks if email exists."""
        return self.find_by_email(email) is not None

    def update_categories(self, subscriber_id: str, categories: List[str]) -> Optional[Subscriber]:
        """Updates subscription categories."""
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            subscriber.categories = categories
            return self.update(subscriber)
        return None

