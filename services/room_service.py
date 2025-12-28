"""
Room/Cabinet Service
Adapted for working with real SDU data
"""
from typing import List, Optional, Tuple
from datetime import datetime
from models.room import Cabinet, CabinetLesson, TIME_SLOTS, DAYS_OF_WEEK
from repository.room_repository import CabinetRepository


class CabinetService:
    """Service for working with cabinets and finding available ones."""

    def __init__(self, cabinet_repository: CabinetRepository = None):
        self._repo = cabinet_repository or CabinetRepository()

    def get_all_cabinets(self) -> List[Cabinet]:
        """Returns all cabinets."""
        return self._repo.get_all()

    def get_cabinet_by_id(self, cabinet_id: int) -> Optional[Cabinet]:
        """Returns cabinet by ID."""
        return self._repo.get_by_id(cabinet_id)

    def get_cabinet_by_name(self, name: str) -> Optional[Cabinet]:
        """Returns cabinet by name."""
        return self._repo.find_by_name(name)

    def get_cabinets_by_building(self, building: str) -> List[Cabinet]:
        """Returns cabinets in a building."""
        return self._repo.find_by_building(building)

    def get_buildings(self) -> List[str]:
        """Returns list of buildings."""
        return self._repo.get_buildings()

    def get_cabinet_schedule(self, cabinet_id: int) -> List[CabinetLesson]:
        """Returns cabinet schedule."""
        return self._repo.get_cabinet_schedule(cabinet_id)

    def search_cabinets(self, query: str) -> List[Cabinet]:
        """Searches cabinets."""
        return self._repo.search(query)

    def get_time_slots(self) -> List[str]:
        """Returns time slots."""
        return [slot[0] for slot in TIME_SLOTS]

    def get_days(self) -> dict:
        """Returns days of week."""
        return DAYS_OF_WEEK

    def _find_time_slot(self, time: str) -> Optional[Tuple[str, str]]:
        """Finds time slot for the specified time."""
        for start, end in TIME_SLOTS:
            if start <= time < end or time == start:
                return (start, end)
        # If time is after all slots, return None
        if time > TIME_SLOTS[-1][1]:
            return None
        # If time is before all slots, return first
        return TIME_SLOTS[0]

    def get_free_cabinets(self, week_id: int, time: str,
                          building: str = None) -> List[Cabinet]:
        """
        Finds available cabinets at the specified time.

        Args:
            week_id: Day of week (1-6, where 1 = Monday)
            time: Time (format HH:MM)
            building: Building filter (optional)

        Returns:
            List of available cabinets
        """
        # Find time slot
        slot = self._find_time_slot(time)
        if slot is None:
            return []

        start_time = slot[0]

        # Get all cabinets
        all_cabinets = self._repo.get_all()

        # Filter by building
        if building:
            all_cabinets = [c for c in all_cabinets
                          if building.lower() in c.parent_building_en.lower()]

        # Get occupied cabinets
        occupied = self._repo.get_occupied_cabinets(week_id, start_time)

        # Return available ones
        free_cabinets = [c for c in all_cabinets if str(c.id) not in occupied]

        return sorted(free_cabinets, key=lambda c: (c.parent_building_en, c.name))

    def get_current_free_cabinets(self, building: str = None) -> List[Cabinet]:
        """Finds cabinets available now."""
        now = datetime.now()
        week_id = now.weekday() + 1  # 1-6 (Monday-Saturday), 7 = weekend

        if week_id == 7:  # Weekend
            return []

        current_time = now.strftime('%H:%M')
        return self.get_free_cabinets(week_id, current_time, building)

    def get_next_slot_free_cabinets(self, building: str = None) -> Tuple[int, str, List[Cabinet]]:
        """
        Finds cabinets available for the next lesson.

        Returns:
            Tuple[week_id, time, List[Cabinet]]
        """
        now = datetime.now()
        week_id = now.weekday() + 1
        current_time = now.strftime('%H:%M')

        # If weekend, return Monday
        if week_id == 7:
            week_id = 1
            next_time = TIME_SLOTS[0][0]
        else:
            # Find next slot
            next_time = None
            for start, end in TIME_SLOTS:
                if current_time < start:
                    next_time = start
                    break

            if next_time is None:
                # Move to next day
                week_id = week_id + 1 if week_id < 6 else 1
                next_time = TIME_SLOTS[0][0]

        cabinets = self.get_free_cabinets(week_id, next_time, building)
        return week_id, next_time, cabinets

    def is_cabinet_free(self, cabinet_id: int, week_id: int, time: str) -> bool:
        """Checks if cabinet is available."""
        slot = self._find_time_slot(time)
        if slot is None:
            return True

        occupied = self._repo.get_occupied_cabinets(week_id, slot[0])
        return str(cabinet_id) not in occupied


# Alias for backward compatibility
RoomService = CabinetService
