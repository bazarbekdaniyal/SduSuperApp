"""
News Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class News:
    """University news model"""
    id: str
    title: str  # Main text in Russian
    content: str  # Main text in Russian
    category: str  # Event, Announcement, Academic, Sports
    author: str
    created_at: str
    image: Optional[str] = None
    is_published: bool = True
    views_count: int = 0
    translations: Optional[Dict] = None  # Automatic translations: {lang: {title, content, category, author}}

    def get_title(self, lang: str = 'ru') -> str:
        """Gets title in specified language"""
        if lang == 'ru':
            return self.title
        if self.translations and lang in self.translations:
            return self.translations[lang].get('title', self.title)
        return self.title

    def get_content(self, lang: str = 'ru') -> str:
        """Gets content in specified language"""
        if lang == 'ru':
            return self.content
        if self.translations and lang in self.translations:
            return self.translations[lang].get('content', self.content)
        return self.content

    def get_category(self, lang: str = 'ru') -> str:
        """Gets category in specified language"""
        if lang == 'ru':
            return self.category
        if self.translations and lang in self.translations:
            return self.translations[lang].get('category', self.category)
        return self.category

    def get_author(self, lang: str = 'ru') -> str:
        """Gets author in specified language"""
        if lang == 'ru':
            return self.author
        if self.translations and lang in self.translations:
            return self.translations[lang].get('author', self.author)
        return self.author

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        result = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author': self.author,
            'created_at': self.created_at,
            'image': self.image,
            'is_published': self.is_published,
            'views_count': self.views_count
        }
        if self.translations:
            result['translations'] = self.translations
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'News':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            content=data.get('content', ''),
            category=data.get('category', ''),
            author=data.get('author', ''),
            created_at=data.get('created_at', datetime.now().isoformat()),
            image=data.get('image'),
            is_published=data.get('is_published', True),
            views_count=data.get('views_count', 0),
            translations=data.get('translations')
        )

