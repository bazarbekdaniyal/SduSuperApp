"""
Schedule Repository

Works with format: { "teacher_id": [ {lesson}, {lesson}, ... ], ... }
"""
import json
import os
from typing import List, Optional, Dict
from models.schedule import Schedule


class ScheduleRepository:
    """Repository for working with schedules."""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self._file_path = os.path.join(data_dir, 'schedules.json')
        self._data: Dict[str, List[dict]] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Loads data from JSON file."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {}

    def get_all(self) -> List[Schedule]:
        """Returns all lessons."""
        result = []
        for teacher_id, lessons in self._data.items():
            for lesson_data in lessons:
                result.append(Schedule.from_dict(lesson_data))
        return result

    def get_by_id(self, schedule_id: str) -> Optional[Schedule]:
        """Returns lesson by ID."""
        for lessons in self._data.values():
            for lesson_data in lessons:
                if str(lesson_data.get('id')) == schedule_id:
                    return Schedule.from_dict(lesson_data)
        return None

    def find_by_teacher(self, teacher_id: str) -> List[Schedule]:
        """Finds teacher's schedule."""
        lessons = self._data.get(str(teacher_id), [])
        return [Schedule.from_dict(lesson) for lesson in lessons]

    def find_by_room(self, room: str) -> List[Schedule]:
        """Finds schedule for a room."""
        result = []
        room_lower = room.lower()
        for lessons in self._data.values():
            for lesson_data in lessons:
                cabinet = lesson_data.get('cabinet', {})
                if cabinet and cabinet.get('name', '').lower() == room_lower:
                    result.append(Schedule.from_dict(lesson_data))
        return result

    def find_by_day(self, week_id: int) -> List[Schedule]:
        """Finds schedule by day of week (1-6)."""
        result = []
        for lessons in self._data.values():
            for lesson_data in lessons:
                if lesson_data.get('week_id') == week_id:
                    result.append(Schedule.from_dict(lesson_data))
        return result

    def find_by_day_and_time(self, week_id: int, time: str) -> List[Schedule]:
        """Finds lessons by day and time."""
        result = []
        for lessons in self._data.values():
            for lesson_data in lessons:
                if lesson_data.get('week_id') == week_id:
                    start = lesson_data.get('start_time', '')
                    end = lesson_data.get('end_time', '')
                    if start <= time < end:
                        result.append(Schedule.from_dict(lesson_data))
        return result

    def get_occupied_rooms(self, week_id: int, time: str) -> List[str]:
        """Returns occupied rooms at specified time."""
        schedules = self.find_by_day_and_time(week_id, time)
        return list(set(s.room for s in schedules if s.room))

    def get_all_rooms(self) -> List[str]:
        """Returns all unique rooms."""
        rooms = set()
        for lessons in self._data.values():
            for lesson in lessons:
                cabinet = lesson.get('cabinet', {})
                if cabinet and cabinet.get('name'):
                    rooms.add(cabinet.get('name'))
        return sorted(list(rooms))

    def get_all_buildings(self) -> List[str]:
        """Returns all unique buildings."""
        buildings = set()
        for lessons in self._data.values():
            for lesson in lessons:
                cabinet = lesson.get('cabinet', {})
                if cabinet and cabinet.get('parent_building_en'):
                    buildings.add(cabinet.get('parent_building_en'))
        return sorted(list(buildings))

