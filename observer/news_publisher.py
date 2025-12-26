"""
NewsPublisher - Concrete Subject for publishing news
"""
from typing import Any
from observer.subject import Subject
from models.news import News


class NewsPublisher(Subject):
    """
    News Publisher.

    Notifies subscribers about new news, updates and deletions.
    Implements Singleton pattern for global access.
    """

    _instance = None

    # Event types
    EVENT_NEWS_CREATED = 'news_created'
    EVENT_NEWS_UPDATED = 'news_updated'
    EVENT_NEWS_DELETED = 'news_deleted'

    def __new__(cls):
        """Singleton - single publisher instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Publisher initialization."""
        if self._initialized:
            return
        super().__init__()
        self._initialized = True
        print("[NewsPublisher] Initialized")

    def publish_news(self, news: News) -> None:
        """
        Publishes new news and notifies subscribers.

        Args:
            news: News object
        """
        print(f"[NewsPublisher] Publishing news: {news.title}")
        self.notify(self.EVENT_NEWS_CREATED, news)

    def update_news(self, news: News) -> None:
        """
        Updates news and notifies subscribers.

        Args:
            news: Updated news object
        """
        print(f"[NewsPublisher] Updating news: {news.title}")
        self.notify(self.EVENT_NEWS_UPDATED, news)

    def delete_news(self, news_id: str, title: str) -> None:
        """
        Deletes news and notifies subscribers.

        Args:
            news_id: ID of news to delete
            title: Title for notification
        """
        print(f"[NewsPublisher] Deleting news: {title}")
        self.notify(self.EVENT_NEWS_DELETED, {'id': news_id, 'title': title})

    def subscribe_to_all(self, observer) -> None:
        """
        Subscribes observer to all events.

        Args:
            observer: Observer object
        """
        self.attach(self.EVENT_NEWS_CREATED, observer)
        self.attach(self.EVENT_NEWS_UPDATED, observer)
        self.attach(self.EVENT_NEWS_DELETED, observer)

    def unsubscribe_from_all(self, observer) -> None:
        """
        Unsubscribes observer from all events.

        Args:
            observer: Observer object
        """
        self.detach(self.EVENT_NEWS_CREATED, observer)
        self.detach(self.EVENT_NEWS_UPDATED, observer)
        self.detach(self.EVENT_NEWS_DELETED, observer)

    def remove_observer_by_id(self, subscriber_id: str) -> None:
        """
        Removes observer by subscriber_id from all events.

        Args:
            subscriber_id: Subscriber ID
        """
        # Create temp observer for search and removal
        from observer.email_subscriber import EmailSubscriber
        temp_observer = EmailSubscriber(subscriber_id, '', '', 'ru')
        
        # Remove from all events
        for event_type in [self.EVENT_NEWS_CREATED, self.EVENT_NEWS_UPDATED, self.EVENT_NEWS_DELETED]:
            if event_type in self._observers:
                self._observers[event_type] = [
                    obs for obs in self._observers[event_type]
                    if obs.subscriber_id != subscriber_id
                ]
        print(f"[NewsPublisher] Observer {subscriber_id} removed")

