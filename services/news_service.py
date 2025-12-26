"""
News Service with Observer Pattern Integration
"""
from typing import List, Optional
from models.news import News
from repository.news_repository import NewsRepository
from repository.subscriber_repository import SubscriberRepository
from factory.news_factory import NewsFactory
from observer.news_publisher import NewsPublisher
from observer.email_subscriber import EmailSubscriber
from services.translation_service import TranslationService


class NewsService:
    """
    Service for working with news.
    Integrates Observer Pattern for notifications.
    Automatically translates news when creating.
    """

    def __init__(self, news_repository: NewsRepository = None,
                 subscriber_repository: SubscriberRepository = None,
                 translation_service: TranslationService = None):
        self._news_repo = news_repository or NewsRepository()
        self._subscriber_repo = subscriber_repository or SubscriberRepository()
        self._factory = NewsFactory()
        self._publisher = NewsPublisher()
        self._translation_service = translation_service or TranslationService()

        # Initialize subscribers from database
        self._init_subscribers()

    def _init_subscribers(self):
        """Loads subscribers and registers them in publisher."""
        subscribers = self._subscriber_repo.get_active()
        for sub in subscribers:
            email_observer = EmailSubscriber(sub.id, sub.email, sub.name, sub.language)
            self._publisher.subscribe_to_all(email_observer)

    def get_all_news(self, limit: int = None) -> List[News]:
        """Returns all published news."""
        return self._news_repo.get_published(limit)

    def get_news_by_id(self, news_id: str) -> Optional[News]:
        """Returns news by ID and increments view counter."""
        news = self._news_repo.get_by_id(news_id)
        if news and news.is_published:
            self._news_repo.increment_views(news_id)
        return news

    def get_news_by_category(self, category: str) -> List[News]:
        """Returns news by category."""
        return self._news_repo.find_by_category(category)

    def search_news(self, query: str) -> List[News]:
        """Searches news."""
        return self._news_repo.search(query)

    def get_popular_news(self, limit: int = 5) -> List[News]:
        """Returns popular news."""
        return self._news_repo.get_popular(limit)

    def get_categories(self) -> List[str]:
        """Returns news categories."""
        return self._news_repo.get_categories()

    def create_news(self, title: str, content: str, category: str,
                    author: str, image: str = None, publish: bool = True) -> News:
        """
        Creates news, automatically translates to other languages and notifies subscribers.
        """
        # Automatically translate news to English and Kazakh
        translations = {}
        if self._translation_service.is_available():
            try:
                translations = self._translation_service.translate_news(
                    title=title,
                    content=content,
                    category=category,
                    author=author,
                    source_lang='ru'
                )
                import logging
                logging.getLogger(__name__).info(f"News translated successfully. Translations: {list(translations.keys())}")
            except Exception as e:
                # If translation failed, continue without translations
                import logging
                logging.getLogger(__name__).error(f"Translation failed: {str(e)}", exc_info=True)
                print(f"⚠️  News translation error: {str(e)}")
        else:
            import logging
            logging.getLogger(__name__).warning("Translation service is not available. Install deep-translator: pip install deep-translator")
            print("⚠️  Translation service unavailable. Install library: pip install deep-translator")

        data = {
            'title': title,
            'content': content,
            'category': category,
            'author': author,
            'image': image,
            'is_published': publish,
            'translations': translations if translations else None
        }
        news = self._factory.create(data)
        created_news = self._news_repo.create(news)

        # Notify subscribers if published
        if publish:
            self._publisher.publish_news(created_news)

        return created_news

    def update_news(self, news_id: str, data: dict) -> Optional[News]:
        """Updates news and automatically translates changes."""
        news = self._news_repo.get_by_id(news_id)
        if not news:
            return None

        # If title, content, category or author are updated, translate again
        needs_translation = any(key in data for key in ['title', 'content', 'category', 'author'])

        for key, value in data.items():
            if hasattr(news, key):
                setattr(news, key, value)

        # If translatable fields changed, update translations
        if needs_translation and self._translation_service.is_available():
            try:
                translations = self._translation_service.translate_news(
                    title=news.title,
                    content=news.content,
                    category=news.category,
                    author=news.author,
                    source_lang='ru'
                )
                news.translations = translations if translations else news.translations
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Translation update failed: {str(e)}")

        updated_news = self._news_repo.update(news)

        if updated_news and updated_news.is_published:
            self._publisher.update_news(updated_news)

        return updated_news

    def delete_news(self, news_id: str) -> bool:
        """Deletes news."""
        return self._news_repo.delete(news_id)

    def publish_news(self, news_id: str) -> Optional[News]:
        """Publishes news."""
        news = self._news_repo.publish(news_id)
        if news:
            self._publisher.publish_news(news)
        return news

    def unpublish_news(self, news_id: str) -> Optional[News]:
        """Unpublishes news."""
        return self._news_repo.unpublish(news_id)

    # === Subscription Management ===

    def subscribe(self, email: str, name: str, categories: List[str] = None, language: str = 'ru') -> bool:
        """Subscribes to news."""
        from models.subscriber import Subscriber
        import uuid
        from datetime import datetime

        # Check if subscriber with this email already exists
        existing_subscriber = self._subscriber_repo.find_by_email(email)
        
        if existing_subscriber:
            # If subscriber is inactive - reactivate them
            if not existing_subscriber.is_active:
                existing_subscriber.is_active = True
                existing_subscriber.name = name
                existing_subscriber.language = language
                existing_subscriber.subscribed_at = datetime.now().isoformat()
                self._subscriber_repo.update(existing_subscriber)
                
                # Register back in publisher
                email_observer = EmailSubscriber(existing_subscriber.id, email, name, language)
                self._publisher.subscribe_to_all(email_observer)
                
                # Send welcome email
                from services.email_service import get_email_service
                email_service = get_email_service()
                email_service.send_subscription_welcome(email, name, existing_subscriber.id, language=language)
                
                return True
            else:
                # Subscriber is already active
                return False

        # Create new subscriber
        subscriber = Subscriber(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            subscribed_at=datetime.now().isoformat(),
            is_active=True,
            categories=categories or ['all'],
            language=language
        )

        self._subscriber_repo.create(subscriber)

        # Register in publisher
        email_observer = EmailSubscriber(subscriber.id, email, name, language)
        self._publisher.subscribe_to_all(email_observer)

        # Send welcome email
        from services.email_service import get_email_service
        email_service = get_email_service()
        email_service.send_subscription_welcome(email, name, subscriber.id, language=language)

        return True

    def unsubscribe(self, email: str) -> bool:
        """Unsubscribes from news."""
        subscriber = self._subscriber_repo.find_by_email(email)
        if subscriber:
            self._subscriber_repo.deactivate(subscriber.id)
            return True
        return False

    def get_subscribers_count(self) -> int:
        """Returns number of active subscribers."""
        return len(self._subscriber_repo.get_active())

    def update_subscriber_observer(self, subscriber_id: str) -> bool:
        """
        Updates subscriber's observer after data changes.
        
        Args:
            subscriber_id: Subscriber ID
            
        Returns:
            True if updated successfully
        """
        subscriber = self._subscriber_repo.get_by_id(subscriber_id)
        if not subscriber:
            return False
        
        # Remove old observer
        self._publisher.remove_observer_by_id(subscriber_id)
        
        # If subscriber is active, create new observer with updated data
        if subscriber.is_active:
            email_observer = EmailSubscriber(
                subscriber.id, 
                subscriber.email, 
                subscriber.name, 
                subscriber.language
            )
            self._publisher.subscribe_to_all(email_observer)
            print(f"[NewsService] Observer for subscriber {subscriber_id} updated (language: {subscriber.language})")
        
        return True
