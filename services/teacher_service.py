"""
Teacher Service
"""
from typing import List, Optional
from models.teacher import Teacher
from repository.teacher_repository import TeacherRepository
from factory.teacher_factory import TeacherFactory


class TeacherService:
    """
    Service for working with teachers.

    SOLID:
    - SRP: Only business logic for working with teachers
    - DIP: Depends on abstractions (repository)
    """

    def __init__(self, repository: TeacherRepository = None):
        self._repository = repository or TeacherRepository()
        self._factory = TeacherFactory()

    def get_all_teachers(self) -> List[Teacher]:
        """Returns all teachers."""
        return self._repository.get_all()

    def get_teacher_by_id(self, teacher_id: str) -> Optional[Teacher]:
        """Returns teacher by ID."""
        return self._repository.get_by_id(teacher_id)

    def search_teachers(self, query: str) -> List[Teacher]:
        """Searches teachers by name."""
        return self._repository.find_by_name(query)

    def get_teachers_by_level(self, level: str) -> List[Teacher]:
        """Returns teachers by degree level."""
        return self._repository.find_by_level(level)

    def get_top_rated_teachers(self, limit: int = 10) -> List[Teacher]:
        """Returns top rated teachers."""
        return self._repository.get_top_rated(limit)

    def get_levels(self) -> List[str]:
        """Returns list of teacher degree levels."""
        return self._repository.get_levels()

    def create_teacher(self, data: dict) -> Teacher:
        """Creates a new teacher."""
        teacher = self._factory.create(data)
        return self._repository.create(teacher)

    def update_teacher(self, teacher_id: str, data: dict) -> Optional[Teacher]:
        """Updates teacher data."""
        teacher = self._repository.get_by_id(teacher_id)
        if not teacher:
            return None

        # Update fields
        for key, value in data.items():
            if hasattr(teacher, key):
                setattr(teacher, key, value)

        return self._repository.update(teacher)

    def update_teacher_rating(self, teacher_id: str, rating: float, reviews_count: int) -> Optional[Teacher]:
        """Updates teacher rating."""
        return self._repository.update_rating(teacher_id, rating, reviews_count)

    def delete_teacher(self, teacher_id: str) -> bool:
        """Deletes a teacher."""
        return self._repository.delete(teacher_id)

    def get_teacher_count(self) -> int:
        """Returns number of teachers."""
        return self._repository.count()
