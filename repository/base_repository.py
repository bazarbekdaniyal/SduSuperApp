"""
Base Repository for working with JSON storage

Repository pattern isolates data access logic
from application business logic.
"""
import json
import os
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository.

    SOLID principles:
    - SRP: Repository is responsible only for CRUD operations with data
    - OCP: Can add new storage type without changing code
    - LSP: All repositories implement single interface
    - ISP: Minimal interface for working with data
    - DIP: Services depend on BaseRepository abstraction
    """

    def __init__(self, data_file: str, data_dir: str = None):
        """
        Initialize repository.

        Args:
            data_file: JSON file name (e.g., 'teachers.json')
            data_dir: Data directory
        """
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

        self._data_dir = data_dir
        self._file_path = os.path.join(data_dir, data_file)

        os.makedirs(data_dir, exist_ok=True)

        if not os.path.exists(self._file_path):
            self._save_data([])

    def _load_data(self) -> List[dict]:
        """Loads data from JSON file."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[dict]) -> None:
        """Saves data to JSON file."""
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @abstractmethod
    def _to_entity(self, data: dict) -> T:
        """Converts dictionary to model object."""
        pass

    @abstractmethod
    def _to_dict(self, entity: T) -> dict:
        """Converts model object to dictionary."""
        pass

    def get_all(self) -> List[T]:
        """Returns all records."""
        data = self._load_data()
        return [self._to_entity(item) for item in data]

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Returns record by ID."""
        data = self._load_data()
        for item in data:
            if item.get('id') == entity_id:
                return self._to_entity(item)
        return None

    def create(self, entity: T) -> T:
        """Creates new record."""
        data = self._load_data()
        entity_dict = self._to_dict(entity)
        data.append(entity_dict)
        self._save_data(data)
        return entity

    def update(self, entity: T) -> Optional[T]:
        """Updates existing record."""
        data = self._load_data()
        entity_dict = self._to_dict(entity)
        entity_id = entity_dict.get('id')

        for i, item in enumerate(data):
            if item.get('id') == entity_id:
                data[i] = entity_dict
                self._save_data(data)
                return entity
        return None

    def delete(self, entity_id: str) -> bool:
        """Deletes record by ID."""
        data = self._load_data()
        initial_length = len(data)
        data = [item for item in data if item.get('id') != entity_id]

        if len(data) < initial_length:
            self._save_data(data)
            return True
        return False

    def count(self) -> int:
        """Returns number of records."""
        return len(self._load_data())

    def exists(self, entity_id: str) -> bool:
        """Checks if record exists."""
        return self.get_by_id(entity_id) is not None

