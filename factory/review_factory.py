"""
Review Factory (Factory Method Pattern)
"""
import uuid
from datetime import datetime
from factory.base_factory import BaseFactory
from models.review import Review


class ReviewFactory(BaseFactory):
    """
    Factory for creating Review objects.
    """

    def create(self, data: dict) -> Review:
        """
        Creates review from data dictionary.
        """
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        if 'created_at' not in data or not data['created_at']:
            data['created_at'] = datetime.now().isoformat()

        return Review.from_dict(data)

    def create_default(self) -> Review:
        """
        Creates review with default values.
        """
        return Review(
            id=str(uuid.uuid4()),
            teacher_id="",
            author_name="Anonymous",
            rating=3,
            comment="",
            created_at=datetime.now().isoformat(),
            is_approved=False,
            is_anonymous=True
        )

    def create_review(self, teacher_id: str, author_name: str, rating: int,
                      comment: str, is_anonymous: bool = False) -> Review:
        """
        Creates new teacher review.

        Args:
            teacher_id: Teacher ID
            author_name: Author name
            rating: Rating (1-5)
            comment: Review text
            is_anonymous: Anonymous review

        Returns:
            Review object (not approved)
        """
        # Rating validation
        rating = max(1, min(5, rating))

        display_name = "Anonymous" if is_anonymous else author_name

        return Review(
            id=str(uuid.uuid4()),
            teacher_id=teacher_id,
            author_name=display_name,
            rating=rating,
            comment=comment,
            created_at=datetime.now().isoformat(),
            is_approved=False,  # Requires moderation
            is_anonymous=is_anonymous
        )
"""
Factory Module (Factory Method Pattern)
"""
from factory.base_factory import BaseFactory
from factory.teacher_factory import TeacherFactory
from factory.news_factory import NewsFactory
from factory.product_factory import ProductFactory
from factory.review_factory import ReviewFactory

__all__ = [
    'BaseFactory',
    'TeacherFactory',
    'NewsFactory',
    'ProductFactory',
    'ReviewFactory'
]

