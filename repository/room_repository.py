"""
Room Repository
Adapted for working with real SDU data
"""
import json
import os
from typing import List, Optional, Dict
from models.room import Cabinet, CabinetLesson


class CabinetRepository:
    """Repository for working with SDU rooms."""

    def __init__(self, data_dir: str = None):
        self._data_dir = data_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self._cabinets_file = os.path.join(self._data_dir, 'cabinets.json')
        self._schedules_file = os.path.join(self._data_dir, 'cabinet_schedules.json')
        self._cabinets_cache = None
        self._schedules_cache = None

    def _load_cabinets(self) -> List[dict]:
        """Loads rooms from JSON."""
        if self._cabinets_cache is not None:
            return self._cabinets_cache

        try:
            with open(self._cabinets_file, 'r', encoding='utf-8') as f:
                self._cabinets_cache = json.load(f)
                return self._cabinets_cache
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _load_schedules(self) -> Dict[str, List[dict]]:
        """Loads room schedules from JSON."""
        if self._schedules_cache is not None:
            return self._schedules_cache

        try:
            with open(self._schedules_file, 'r', encoding='utf-8') as f:
                self._schedules_cache = json.load(f)
                return self._schedules_cache
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def get_all(self) -> List[Cabinet]:
        """Returns all rooms."""
        data = self._load_cabinets()
        return [Cabinet.from_dict(item) for item in data]

    def get_by_id(self, cabinet_id: int) -> Optional[Cabinet]:
        """Finds room by ID."""
        cabinets = self.get_all()
        for cabinet in cabinets:
            if cabinet.id == cabinet_id:
                return cabinet
        return None

    def find_by_name(self, name: str) -> Optional[Cabinet]:
        """Finds room by name."""
        cabinets = self.get_all()
        for cabinet in cabinets:
            if cabinet.name.lower() == name.lower():
                return cabinet
        return None

    def find_by_building(self, building: str) -> List[Cabinet]:
        """Finds rooms by building."""
        cabinets = self.get_all()
        return [c for c in cabinets if building.lower() in c.parent_building_en.lower()]

    def get_buildings(self) -> List[str]:
        """Returns list of unique buildings."""
        cabinets = self.get_all()
        buildings = set(c.parent_building_en for c in cabinets if c.parent_building_en)
        return sorted(list(buildings))

    def get_cabinet_schedule(self, cabinet_id: int) -> List[CabinetLesson]:
        """Returns room schedule."""
        schedules = self._load_schedules()
        lessons_data = schedules.get(str(cabinet_id), [])
        return [CabinetLesson.from_dict(item) for item in lessons_data]

    def get_occupied_cabinets(self, week_id: int, time: str) -> set:
        """
        Returns IDs of rooms occupied at the specified time.

        Args:
            week_id: Day of week (1-6)
            time: Lesson start time (format HH:MM)

        Returns:
            set: Set of occupied room IDs
        """
        schedules = self._load_schedules()
        occupied = set()

        for cabinet_id, lessons in schedules.items():
            for lesson in lessons:
                if lesson.get('week_id') == week_id and lesson.get('start_time') == time:
                    occupied.add(cabinet_id)
                    break

        return occupied

    def search(self, query: str) -> List[Cabinet]:
        """Search rooms by name or building."""
        query = query.lower().strip()
        cabinets = self.get_all()
        results = []

        for cabinet in cabinets:
            if (query in cabinet.name.lower() or
                query in cabinet.parent_building_en.lower()):
                results.append(cabinet)

        return results


# Alias for backward compatibility
RoomRepository = CabinetRepository
