"""
Review Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Review:
    """Teacher Review Model"""
    id: str
    teacher_id: str
    author_name: str
    rating: int  # 1-5
    comment: str
    created_at: str
    is_approved: bool = False
    is_anonymous: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'author_name': self.author_name,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at,
            'is_approved': self.is_approved,
            'is_anonymous': self.is_anonymous
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Review':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            teacher_id=data.get('teacher_id', ''),
            author_name=data.get('author_name', ''),
            rating=data.get('rating', 0),
            comment=data.get('comment', ''),
            created_at=data.get('created_at', datetime.now().isoformat()),
            is_approved=data.get('is_approved', False),
            is_anonymous=data.get('is_anonymous', False)
        )

