"""
NotificationSubscriber - Observer for internal notifications
"""
from typing import Any, List
from datetime import datetime
from observer.observer import Observer


class NotificationSubscriber(Observer):
    """
    Subscriber for internal notifications.

    Saves notifications to the system for display in UI.
    """

    def __init__(self, subscriber_id: str, user_name: str):
        """
        Subscriber initialization.

        Args:
            subscriber_id: Unique ID
            user_name: User name
        """
        self._subscriber_id = subscriber_id
        self._user_name = user_name
        self._notifications: List[dict] = []
        self._unread_count = 0

    @property
    def subscriber_id(self) -> str:
        """Subscriber unique ID."""
        return self._subscriber_id

    @property
    def user_name(self) -> str:
        """User name."""
        return self._user_name

    @property
    def unread_count(self) -> int:
        """Number of unread notifications."""
        return self._unread_count

    def update(self, event_type: str, data: Any) -> None:
        """
        Handles event notification.

        Args:
            event_type: Event type
            data: Event data
        """
        notification = {
            'id': len(self._notifications) + 1,
            'event_type': event_type,
            'message': self._create_message(event_type, data),
            'timestamp': datetime.now().isoformat(),
            'is_read': False,
            'data': self._serialize_data(data)
        }

        self._notifications.insert(0, notification)  # Newest first
        self._unread_count += 1

        print(f"[Notification] For {self._user_name}: {notification['message']}")

    def _create_message(self, event_type: str, data: Any) -> str:
        """Creates notification text."""
        if event_type == 'news_created':
            return f"New news: {data.title}"
        elif event_type == 'news_updated':
            return f"Updated news: {data.title}"
        elif event_type == 'news_deleted':
            return f"Deleted news: {data.get('title', 'Unknown')}"
        else:
            return f"Event: {event_type}"

    def _serialize_data(self, data: Any) -> dict:
        """Serializes data for storage."""
        if hasattr(data, 'to_dict'):
            return data.to_dict()
        elif isinstance(data, dict):
            return data
        else:
            return {'value': str(data)}

    def get_notifications(self, limit: int = 50) -> List[dict]:
        """Returns list of notifications."""
        return self._notifications[:limit]

    def mark_as_read(self, notification_id: int) -> bool:
        """Marks notification as read."""
        for notif in self._notifications:
            if notif['id'] == notification_id and not notif['is_read']:
                notif['is_read'] = True
                self._unread_count = max(0, self._unread_count - 1)
                return True
        return False

    def mark_all_as_read(self) -> None:
        """Marks all notifications as read."""
        for notif in self._notifications:
            notif['is_read'] = True
        self._unread_count = 0

    def clear_notifications(self) -> None:
        """Clears all notifications."""
        self._notifications.clear()
        self._unread_count = 0

