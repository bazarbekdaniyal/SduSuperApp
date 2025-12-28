"""
Teacher Model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Teacher:
    """SDU Teacher Model"""
    id: str
    full_name_en: str  # Name in English
    full_name_kz: Optional[str] = None  # Name in Kazakh
    level: Optional[str] = None  # Degree (PhD, Candidate of Science, etc.)
    rating: float = 0.0
    reviews_count: int = 0

    @property
    def name(self) -> str:
        """Main display name"""
        return self.full_name_en

    @property
    def name_kz(self) -> str:
        """Name in Kazakh"""
        return self.full_name_kz or self.full_name_en

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'full_name_en': self.full_name_en,
            'full_name_kz': self.full_name_kz,
            'level': self.level,
            'rating': self.rating,
            'reviews_count': self.reviews_count
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Teacher':
        """Create from dictionary"""
        return cls(
            id=str(data.get('id', '')),
            full_name_en=data.get('full_name_en', ''),
            full_name_kz=data.get('full_name_kz'),
            level=data.get('level'),
            rating=data.get('rating', 0.0),
            reviews_count=data.get('reviews_count', 0)
        )
