"""
Subject (Publisher) - base class for Observer Pattern
"""
from abc import ABC
from typing import List, Dict, Any
from observer.observer import Observer


class Subject(ABC):
    """
    Abstract Subject (Publisher).

    Stores list of observers and notifies them about events.

    SOLID principles:
    - SRP: Subject manages subscriptions and notifications
    - OCP: Can add new event types without changing the class
    """

    def __init__(self):
        """Initialize list of observers."""
        self._observers: Dict[str, List[Observer]] = {}

    def attach(self, event_type: str, observer: Observer) -> None:
        """
        Subscribes observer to specific event type.

        Args:
            event_type: Event type to subscribe to
            observer: Observer object
        """
        if event_type not in self._observers:
            self._observers[event_type] = []

        # Check if already subscribed
        for obs in self._observers[event_type]:
            if obs.subscriber_id == observer.subscriber_id:
                return

        self._observers[event_type].append(observer)
        print(f"[Observer] {observer.subscriber_id} subscribed to '{event_type}'")

    def detach(self, event_type: str, observer: Observer) -> None:
        """
        Unsubscribes observer from event.

        Args:
            event_type: Event type
            observer: Observer object
        """
        if event_type in self._observers:
            self._observers[event_type] = [
                obs for obs in self._observers[event_type]
                if obs.subscriber_id != observer.subscriber_id
            ]
            print(f"[Observer] {observer.subscriber_id} unsubscribed from '{event_type}'")

    def notify(self, event_type: str, data: Any) -> None:
        """
        Notifies all subscribers about event.

        Args:
            event_type: Event type
            data: Event data
        """
        if event_type not in self._observers:
            return

        print(f"[Observer] Notification about event '{event_type}' for {len(self._observers[event_type])} subscribers")

        for observer in self._observers[event_type]:
            try:
                observer.update(event_type, data)
            except Exception as e:
                print(f"[Observer] Notification error {observer.subscriber_id}: {e}")

    def get_observers_count(self, event_type: str) -> int:
        """Returns number of subscribers to event."""
        return len(self._observers.get(event_type, []))

