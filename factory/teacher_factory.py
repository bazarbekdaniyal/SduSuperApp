"""
Teacher Factory (Factory Method Pattern)
"""
import uuid
from factory.base_factory import BaseFactory
from models.teacher import Teacher


class TeacherFactory(BaseFactory):
    """
    Factory for creating Teacher objects.

    Encapsulates teacher creation logic,
    allowing to change creation process without affecting client code.
    """

    def create(self, data: dict) -> Teacher:
        """
        Creates teacher from data dictionary.

        Args:
            data: Dictionary with teacher data

        Returns:
            Teacher object
        """
        # Generate ID if not specified
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        return Teacher.from_dict(data)

    def create_default(self) -> Teacher:
        """
        Creates teacher with default values.

        Returns:
            Teacher with default values
        """
        return Teacher(
            id=str(uuid.uuid4()),
            full_name_en="New Teacher",
            full_name_kz=None,
            level=None,
            rating=0.0,
            reviews_count=0
        )

    def create_with_phd(self, full_name_en: str, full_name_kz: str = None) -> Teacher:
        """
        Creates teacher with PhD degree.

        Args:
            full_name_en: Name in English
            full_name_kz: Name in Kazakh

        Returns:
            Teacher with PhD degree
        """
        return Teacher(
            id=str(uuid.uuid4()),
            full_name_en=full_name_en,
            full_name_kz=full_name_kz,
            level=" PhD",
            rating=0.0,
            reviews_count=0
        )

    def create_candidate(self, full_name_en: str, full_name_kz: str = None) -> Teacher:
        """
        Creates teacher with Candidate of Science degree.
        """
        return Teacher(
            id=str(uuid.uuid4()),
            full_name_en=full_name_en,
            full_name_kz=full_name_kz,
            level=" Candidate of Science",
            rating=0.0,
            reviews_count=0
        )

