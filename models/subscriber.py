"""
Subscriber Model
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subscriber:
    """News Subscriber Model"""
    id: str
    email: str
    name: str
    subscribed_at: str
    is_active: bool = True
    categories: list = None  # Subscription categories
    language: str = 'ru'  # Subscriber language (ru, en, kz)

    def __post_init__(self):
        if self.categories is None:
            self.categories = ['all']

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'subscribed_at': self.subscribed_at,
            'is_active': self.is_active,
            'categories': self.categories,
            'language': self.language
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Subscriber':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            email=data.get('email', ''),
            name=data.get('name', ''),
            subscribed_at=data.get('subscribed_at', datetime.now().isoformat()),
            is_active=data.get('is_active', True),
            categories=data.get('categories', ['all']),
            language=data.get('language', 'ru')
        )

