"""
Schedule Service
"""
from typing import List, Optional, Dict
from models.schedule import Schedule
from repository.schedule_repository import ScheduleRepository


class ScheduleService:
    """Service for working with schedules."""

    DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    DAYS_MAPPING = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

    TIME_SLOTS = [
        ('08:30', '09:20'),
        ('09:30', '10:20'),
        ('10:30', '11:20'),
        ('11:30', '12:20'),
        ('12:30', '13:20'),
        ('13:30', '14:20'),
        ('14:30', '15:20'),
        ('15:30', '16:20'),
        ('16:30', '17:20'),
        ('17:30', '18:20'),
        ('18:30', '19:20'),
        ('19:30', '20:20'),
    ]

    def __init__(self, repository: ScheduleRepository = None):
        self._repository = repository or ScheduleRepository()

    def get_teacher_schedule(self, teacher_id: str) -> Dict[str, List[Schedule]]:
        """
        Returns teacher's schedule grouped by days.

        Returns:
            Dictionary {day: [Schedule]}
        """
        schedules = self._repository.find_by_teacher(teacher_id)
        result = {day: [] for day in self.DAYS_OF_WEEK}

        for schedule in schedules:
            day_name = self.DAYS_MAPPING.get(schedule.week_id)
            if day_name and day_name in result:
                result[day_name].append(schedule)

        # Sort by time
        for day in result:
            result[day].sort(key=lambda s: s.start_time)

        return result

    def get_room_schedule(self, room: str) -> Dict[str, List[Schedule]]:
        """Returns schedule for a room."""
        schedules = self._repository.find_by_room(room)
        result = {day: [] for day in self.DAYS_OF_WEEK}

        for schedule in schedules:
            day_name = self.DAYS_MAPPING.get(schedule.week_id)
            if day_name and day_name in result:
                result[day_name].append(schedule)

        for day in result:
            result[day].sort(key=lambda s: s.start_time)

        return result

    def get_schedule_by_day(self, day_of_week: str) -> List[Schedule]:
        """Returns all lessons on a specific day."""
        # Convert day name to week_id
        day_to_id = {v: k for k, v in self.DAYS_MAPPING.items()}
        week_id = day_to_id.get(day_of_week, 0)
        if week_id:
            return self._repository.find_by_day(week_id)
        return []

    def get_current_lessons(self, week_id: int, time: str) -> List[Schedule]:
        """Returns current lessons."""
        return self._repository.find_by_day_and_time(week_id, time)

    def get_all_rooms(self) -> List[str]:
        """Returns all unique rooms."""
        return self._repository.get_all_rooms()

    def get_all_buildings(self) -> List[str]:
        """Returns all unique buildings."""
        return self._repository.get_all_buildings()

    def get_occupied_rooms(self, week_id: int, time: str) -> List[str]:
        """Returns occupied rooms at the specified time."""
        return self._repository.get_occupied_rooms(week_id, time)
