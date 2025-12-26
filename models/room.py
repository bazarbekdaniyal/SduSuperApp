"""
Cabinet Model (Room)
Adapted for working with real SDU data
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Cabinet:
    """SDU Cabinet Model"""
    id: int
    name: str
    parent_building_en: str

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'parent_building_en': self.parent_building_en
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Cabinet':
        """Create from dictionary"""
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            parent_building_en=data.get('parent_building_en', '')
        )


@dataclass
class CabinetLesson:
    """Cabinet Lesson Model"""
    id: int
    code: str
    section: str
    type: str
    name_en: str
    name_kz: str
    start_time: str
    end_time: str
    week_id: int
    teacher: Optional[dict] = None
    cabinet: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'code': self.code,
            'section': self.section,
            'type': self.type,
            'name_en': self.name_en,
            'name_kz': self.name_kz,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'week_id': self.week_id,
            'teacher': self.teacher,
            'cabinet': self.cabinet
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CabinetLesson':
        return cls(
            id=data.get('id', 0),
            code=data.get('code', ''),
            section=data.get('section', ''),
            type=data.get('type', ''),
            name_en=data.get('name_en', ''),
            name_kz=data.get('name_kz', ''),
            start_time=data.get('start_time', ''),
            end_time=data.get('end_time', ''),
            week_id=data.get('week_id', 0),
            teacher=data.get('teacher'),
            cabinet=data.get('cabinet')
        )


# Time slots for SDU schedule
TIME_SLOTS = [
    ("08:30", "09:20"), ("09:30", "10:20"), ("10:30", "11:20"),
    ("11:30", "12:20"), ("12:30", "13:20"), ("13:30", "14:20"),
    ("14:30", "15:20"), ("15:30", "16:20"), ("16:30", "17:20"),
    ("17:30", "18:20"), ("18:30", "19:20"), ("19:30", "20:20"),
    ("20:30", "21:20"), ("21:30", "22:20")
]

# Days of week
DAYS_OF_WEEK = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}
