"""
Review Repository
"""
from typing import List, Optional
from repository.base_repository import BaseRepository
from models.review import Review


class ReviewRepository(BaseRepository[Review]):
    """Repository for working with reviews."""

    def __init__(self, data_dir: str = None):
        super().__init__('reviews.json', data_dir)

    def _to_entity(self, data: dict) -> Review:
        return Review.from_dict(data)

    def _to_dict(self, entity: Review) -> dict:
        return entity.to_dict()

    def find_by_teacher(self, teacher_id: str, approved_only: bool = True) -> List[Review]:
        """Finds reviews for a teacher."""
        all_reviews = self.get_all()
        reviews = [r for r in all_reviews if r.teacher_id == teacher_id]
        if approved_only:
            reviews = [r for r in reviews if r.is_approved]
        return sorted(reviews, key=lambda r: r.created_at, reverse=True)

    def get_pending_reviews(self) -> List[Review]:
        """Returns unapproved reviews (for moderation)."""
        all_reviews = self.get_all()
        return [r for r in all_reviews if not r.is_approved]

    def get_approved_reviews(self) -> List[Review]:
        """Returns all approved reviews."""
        all_reviews = self.get_all()
        return [r for r in all_reviews if r.is_approved]

    def approve_review(self, review_id: str) -> Optional[Review]:
        """Approves review."""
        review = self.get_by_id(review_id)
        if review:
            review.is_approved = True
            return self.update(review)
        return None

    def reject_review(self, review_id: str) -> bool:
        """Rejects (deletes) review."""
        return self.delete(review_id)

    def get_average_rating(self, teacher_id: str) -> tuple:
        """
        Calculates average teacher rating.

        Returns:
            Tuple (average_rating, reviews_count)
        """
        reviews = self.find_by_teacher(teacher_id, approved_only=True)
        if not reviews:
            return (0.0, 0)

        total = sum(r.rating for r in reviews)
        count = len(reviews)
        return (round(total / count, 2), count)

    def get_rating_distribution(self, teacher_id: str) -> dict:
        """
        Returns rating distribution.

        Returns:
            Dictionary {1: count, 2: count, ...}
        """
        reviews = self.find_by_teacher(teacher_id, approved_only=True)
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for review in reviews:
            if 1 <= review.rating <= 5:
                distribution[review.rating] += 1
        return distribution

