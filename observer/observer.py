"""
Observer Interface (Behavioral Pattern)

Observer pattern defines a one-to-many dependency between objects,
so that when one object changes state, all its dependents
are notified and updated automatically.
"""
from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """
    Abstract observer.

    Defines interface for objects that should be
    notified about changes in Subject.

    SOLID principles:
    - SRP: Observer is responsible only for receiving notifications
    - ISP: Minimal interface with one method
    - DIP: Depends on abstraction
    """

    @abstractmethod
    def update(self, event_type: str, data: Any) -> None:
        """
        Called by Subject when event occurs.

        Args:
            event_type: Event type (e.g., 'news_created', 'news_updated')
            data: Event data (e.g., News object)
        """
        pass

    @property
    @abstractmethod
    def subscriber_id(self) -> str:
        """
        Unique subscriber identifier.
        """
        pass

