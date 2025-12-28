"""
Teacher Repository
"""
import json
import os
from typing import List, Optional
from repository.base_repository import BaseRepository
from models.teacher import Teacher


class TeacherRepository(BaseRepository[Teacher]):
    """Repository for working with teachers."""

    def __init__(self, data_dir: str = None):
        super().__init__('teachers.json', data_dir)
        self._ratings = self._load_ratings()

    def _load_ratings(self) -> dict:
        """Loads ratings from ratings.json"""
        ratings_file = os.path.join(self._data_dir, 'ratings.json')
        try:
            with open(ratings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_ratings(self) -> None:
        """Saves ratings to ratings.json"""
        ratings_file = os.path.join(self._data_dir, 'ratings.json')
        with open(ratings_file, 'w', encoding='utf-8') as f:
            json.dump(self._ratings, f, ensure_ascii=False, indent=2)

    def _to_entity(self, data: dict) -> Teacher:
        """Converts dictionary to Teacher with rating."""
        teacher = Teacher.from_dict(data)
        teacher_id = str(teacher.id)
        if teacher_id in self._ratings:
            rating_data = self._ratings[teacher_id]
            teacher.rating = rating_data.get('rating', 0.0)
            teacher.reviews_count = rating_data.get('reviews_count', 0)
        return teacher

    def _to_dict(self, entity: Teacher) -> dict:
        """Converts Teacher to dictionary."""
        return entity.to_dict()

    def get_by_id(self, entity_id: str) -> Optional[Teacher]:
        """Returns record by ID (supports int and str)."""
        data = self._load_data()
        for item in data:
            if str(item.get('id')) == str(entity_id):
                return self._to_entity(item)
        return None

    def find_by_name(self, name: str) -> List[Teacher]:
        """Searches teachers by name (English or Kazakh)."""
        all_teachers = self.get_all()
        name_lower = name.lower()
        return [
            t for t in all_teachers
            if name_lower in t.full_name_en.lower() or
               (t.full_name_kz and name_lower in t.full_name_kz.lower())
        ]

    def find_by_level(self, level: str) -> List[Teacher]:
        """Finds teachers by degree (PhD, etc.)."""
        all_teachers = self.get_all()
        level_lower = level.lower()
        return [
            t for t in all_teachers
            if t.level and level_lower in t.level.lower()
        ]

    def get_top_rated(self, limit: int = 10) -> List[Teacher]:
        """Returns top teachers by rating."""
        all_teachers = self.get_all()
        rated_teachers = [t for t in all_teachers if t.rating > 0]
        sorted_teachers = sorted(rated_teachers, key=lambda t: t.rating, reverse=True)
        return sorted_teachers[:limit]

    def update_rating(self, teacher_id: str, new_rating: float, reviews_count: int) -> Optional[Teacher]:
        """Updates teacher rating in ratings.json"""
        teacher_id = str(teacher_id)
        self._ratings[teacher_id] = {
            'rating': round(new_rating, 2),
            'reviews_count': reviews_count
        }
        self._save_ratings()
        return self.get_by_id(teacher_id)

    def get_levels(self) -> List[str]:
        """Returns list of all degrees."""
        all_teachers = self.get_all()
        levels = set(t.level.strip() for t in all_teachers if t.level)
        return sorted(list(levels))

