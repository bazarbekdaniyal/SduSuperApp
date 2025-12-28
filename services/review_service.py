"""
Review Service
"""
from typing import List, Optional, Tuple
from models.review import Review
from repository.review_repository import ReviewRepository
from factory.review_factory import ReviewFactory


class ReviewService:
    """Service for working with teacher reviews."""

    def __init__(self, repository: ReviewRepository = None):
        self._repository = repository or ReviewRepository()
        self._factory = ReviewFactory()

    def get_teacher_reviews(self, teacher_id: str) -> List[Review]:
        """Returns approved reviews for a teacher."""
        return self._repository.find_by_teacher(teacher_id, approved_only=True)

    def get_pending_reviews(self) -> List[Review]:
        """Returns reviews pending moderation."""
        return self._repository.get_pending_reviews()

    def get_teacher_rating(self, teacher_id: str) -> Tuple[float, int]:
        """
        Returns teacher's rating.

        Returns:
            (average_rating, review_count)
        """
        return self._repository.get_average_rating(teacher_id)

    def get_rating_distribution(self, teacher_id: str) -> dict:
        """Returns rating distribution."""
        return self._repository.get_rating_distribution(teacher_id)

    def create_review(self, teacher_id: str, author_name: str, rating: int,
                      comment: str, is_anonymous: bool = False) -> Review:
        """
        Creates a new review (requires moderation).

        Args:
            teacher_id: Teacher ID
            author_name: Author name
            rating: Rating (1-5)
            comment: Review text
            is_anonymous: Anonymous review

        Returns:
            Created review
        """
        review = self._factory.create_review(
            teacher_id=teacher_id,
            author_name=author_name,
            rating=rating,
            comment=comment,
            is_anonymous=is_anonymous
        )
        return self._repository.create(review)

    def approve_review(self, review_id: str) -> Optional[Review]:
        """Approves a review."""
        return self._repository.approve_review(review_id)

    def reject_review(self, review_id: str) -> bool:
        """Rejects (deletes) a review."""
        return self._repository.reject_review(review_id)

    def delete_review(self, review_id: str) -> bool:
        """Deletes a review."""
        return self._repository.delete(review_id)

    def get_reviews_count(self) -> dict:
        """
        Returns review statistics.

        Returns:
            {'pending': n, 'approved': m, 'total': k}
        """
        pending = len(self._repository.get_pending_reviews())
        approved = len(self._repository.get_approved_reviews())
        return {
            'pending': pending,
            'approved': approved,
            'total': pending + approved
        }
