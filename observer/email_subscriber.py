"""
EmailSubscriber - concrete Observer for email notifications
"""
from typing import Any
from observer.observer import Observer


class EmailSubscriber(Observer):
    """
    Email notification subscriber.

    Receives event notifications and sends email via EmailService.
    """

    def __init__(self, subscriber_id: str, email: str, name: str, language: str = 'ru'):
        """
        Initialize email subscriber.

        Args:
            subscriber_id: Unique subscriber ID
            email: Email address
            name: Subscriber name
            language: Subscriber language (ru, en, kz)
        """
        self._subscriber_id = subscriber_id
        self._email = email
        self._name = name
        self._language = language
        self._notifications = []  # Stores notification history

    @property
    def subscriber_id(self) -> str:
        """Unique subscriber ID."""
        return self._subscriber_id

    @property
    def email(self) -> str:
        """Email address."""
        return self._email

    @property
    def name(self) -> str:
        """Subscriber name."""
        return self._name

    def update(self, event_type: str, data: Any) -> None:
        """
        Handles event notification.

        Args:
            event_type: Event type
            data: Event data
        """
        notification = self._create_notification(event_type, data)
        self._notifications.append(notification)
        self._send_email(event_type, data)

    def _create_notification(self, event_type: str, data: Any) -> dict:
        """Creates notification object."""
        if event_type == 'news_created':
            return {
                'type': event_type,
                'subject': f'🆕 New news: {data.title}',
                'body': f'Hello, {self._name}!\n\n'
                       f'New article published:\n'
                       f'"{data.title}"\n\n'
                       f'Category: {data.category}\n'
                       f'Author: {data.author}\n\n'
                       f'Read more on SDU SuperApp website.',
                'news_id': data.id
            }
        elif event_type == 'news_updated':
            return {
                'type': event_type,
                'subject': f'📝 News update: {data.title}',
                'body': f'Hello, {self._name}!\n\n'
                       f'News updated: "{data.title}"',
                'news_id': data.id
            }
        elif event_type == 'news_deleted':
            return {
                'type': event_type,
                'subject': f'🗑️ News deleted: {data.get("title", "Unknown")}',
                'body': f'Hello, {self._name}!\n\n'
                       f'News was deleted.',
                'news_id': data.get('id')
            }
        else:
            return {
                'type': event_type,
                'subject': f'Notification: {event_type}',
                'body': str(data)
            }

    def _send_email(self, event_type: str, data: Any) -> None:
        """
        Sends email via EmailService.
        """
        # Import here to avoid circular imports
        from services.email_service import get_email_service

        email_service = get_email_service()

        if event_type == 'news_created':
            email_service.send_news_notification(self._email, self._name, data, language=self._language)
        elif event_type == 'news_updated':
            email_service.send_news_update_notification(self._email, self._name, data, language=self._language)
        else:
            # For other events use general method
            notification = self._create_notification(event_type, data)
            email_service.send(self._email, notification['subject'], notification['body'])

    def get_notifications(self) -> list:
        """Returns notification history."""
        return self._notifications.copy()

    def clear_notifications(self) -> None:
        """Clears notification history."""
        self._notifications.clear()

