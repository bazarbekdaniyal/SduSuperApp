"""
Schedule Model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Schedule:
    """Lesson Schedule Model"""
    id: str
    code: str  # Subject code (CSS 222)
    section: str  # Section
    type: str  # Lesson type (T - theory, P - practice, L - lab)
    name_en: str  # Subject name in English
    name_kz: Optional[str] = None  # Name in Kazakh
    start_time: str = ""  # "15:30"
    end_time: str = ""  # "16:20"
    week_id: int = 1  # Day of week (1-6, Monday-Saturday)
    teacher_id: Optional[str] = None  # Teacher ID
    teacher_name: Optional[str] = None  # Teacher name
    cabinet_name: Optional[str] = None  # Room name
    cabinet_building: Optional[str] = None  # Building

    @property
    def subject(self) -> str:
        """Subject name"""
        return self.name_en

    @property
    def room(self) -> str:
        """Room"""
        return self.cabinet_name or ""

    @property
    def day_of_week(self) -> str:
        """Returns day of week name"""
        days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
        return days.get(self.week_id, 'Unknown')

    @property
    def lesson_type(self) -> str:
        """Returns full lesson type name"""
        types = {'T': 'Lecture', 'P': 'Practice', 'L': 'Lab'}
        return types.get(self.type, self.type)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
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
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'cabinet_name': self.cabinet_name,
            'cabinet_building': self.cabinet_building
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Schedule':
        """Create from dictionary"""
        # Extract teacher info
        teacher = data.get('teacher', {})
        teacher_id = str(teacher.get('id', '')) if teacher else None
        teacher_name = teacher.get('full_name_en', '') if teacher else None

        # Extract room info
        cabinet = data.get('cabinet', {})
        cabinet_name = cabinet.get('name', '') if cabinet else None
        cabinet_building = cabinet.get('parent_building_en', '') if cabinet else None

        return cls(
            id=str(data.get('id', '')),
            code=data.get('code', ''),
            section=data.get('section', ''),
            type=data.get('type', ''),
            name_en=data.get('name_en', ''),
            name_kz=data.get('name_kz'),
            start_time=data.get('start_time', ''),
            end_time=data.get('end_time', ''),
            week_id=data.get('week_id', 1),
            teacher_id=teacher_id,
            teacher_name=teacher_name,
            cabinet_name=cabinet_name,
            cabinet_building=cabinet_building
        )
