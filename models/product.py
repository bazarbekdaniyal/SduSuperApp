"""
Product Model
"""
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Product:
    """Shop Product Model"""
    id: str
    name: str 
    description: str
    price: float
    category: str  # Clothing, Accessories, Stationery, Books
    image: Optional[str] = None
    stock: int = 0
    is_available: bool = True
    translations: Optional[Dict] = None  # Multilingual data: {lang: {name, description, category}}

    def get_name(self, lang: str = 'ru') -> str:
        """Gets name in specified language"""
        if self.translations and lang in self.translations:
            return self.translations[lang].get('name', self.name)
        return self.name

    def get_description(self, lang: str = 'ru') -> str:
        """Gets description in specified language"""
        if self.translations and lang in self.translations:
            return self.translations[lang].get('description', self.description)
        return self.description

    def get_category(self, lang: str = 'ru') -> str:
        """Gets category in specified language"""
        if self.translations and lang in self.translations:
            return self.translations[lang].get('category', self.category)
        return self.category

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image': self.image,
            'stock': self.stock,
            'is_available': self.is_available
        }
        if self.translations:
            result['translations'] = self.translations
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            price=data.get('price', 0.0),
            category=data.get('category', ''),
            image=data.get('image'),
            stock=data.get('stock', 0),
            is_available=data.get('is_available', True),
            translations=data.get('translations')
        )

