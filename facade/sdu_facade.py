"""
SDU Facade - Structural Pattern Facade

Facade provides a unified interface to a set of interfaces
in a subsystem. Defines a higher-level interface that
makes the subsystem easier to use.
"""
from typing import List, Optional, Dict, Any

from services.teacher_service import TeacherService
from services.schedule_service import ScheduleService
from services.review_service import ReviewService
from services.room_service import CabinetService
from services.news_service import NewsService
from services.shop_service import ShopService


class SDUFacade:
    """
    SDU SuperApp Facade.

    Provides a single interface for all application functions.
    Hides the complexity of internal structure from client code.

    SOLID principles:
    - SRP: Facade is responsible for coordinating services
    - OCP: Can add new methods without changing existing ones
    - DIP: Depends on service abstractions

    Advantages of Facade pattern:
    1. Simplifies usage of complex system
    2. Reduces dependencies between client and subsystems
    3. Provides single entry point
    4. Makes application easy to test
    """

    _instance = None

    def __new__(cls):
        """Singleton - one facade instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize all services."""
        if self._initialized:
            return

        self._teacher_service = TeacherService()
        self._schedule_service = ScheduleService()
        self._review_service = ReviewService()
        self._cabinet_service = CabinetService()
        self._news_service = NewsService()
        self._shop_service = ShopService()

        self._initialized = True
        print("[SDUFacade] Initialized")

    # ==========================================
    # Teachers
    # ==========================================

    def get_all_teachers(self) -> List:
        """Returns all teachers."""
        return self._teacher_service.get_all_teachers()

    def get_teacher(self, teacher_id: str) -> Optional[Any]:
        """Returns teacher by ID."""
        return self._teacher_service.get_teacher_by_id(teacher_id)

    def search_teachers(self, query: str) -> List:
        """Searches teachers."""
        return self._teacher_service.search_teachers(query)

    def get_teachers_by_level(self, level: str) -> List:
        """Returns teachers by degree level."""
        return self._teacher_service.get_teachers_by_level(level)

    def get_top_teachers(self, limit: int = 10) -> List:
        """Returns top teachers."""
        return self._teacher_service.get_top_rated_teachers(limit)

    def get_levels(self) -> List[str]:
        """Returns list of teacher degree levels."""
        return self._teacher_service.get_levels()

    def get_top_teachers(self, limit: int = 10) -> List:
        """Returns top teachers."""
        return self._teacher_service.get_top_rated_teachers(limit)

    # ==========================================
    # Schedules
    # ==========================================

    def get_teacher_schedule(self, teacher_id: str) -> Dict:
        """Returns teacher schedule."""
        return self._schedule_service.get_teacher_schedule(teacher_id)



    # ==========================================
    # Reviews and Ratings
    # ==========================================

    def get_teacher_reviews(self, teacher_id: str) -> List:
        """Returns teacher reviews."""
        return self._review_service.get_teacher_reviews(teacher_id)

    def get_teacher_rating(self, teacher_id: str) -> tuple:
        """Returns teacher rating (rating, count)."""
        return self._review_service.get_teacher_rating(teacher_id)

    def add_review(self, teacher_id: str, author_name: str, rating: int,
                   comment: str, is_anonymous: bool = False) -> Any:
        """Adds teacher review."""
        review = self._review_service.create_review(
            teacher_id, author_name, rating, comment, is_anonymous
        )

        # Update teacher rating
        new_rating, count = self._review_service.get_teacher_rating(teacher_id)
        self._teacher_service.update_teacher_rating(teacher_id, new_rating, count)

        return review

    def get_pending_reviews(self) -> List:
        """Returns reviews pending moderation."""
        return self._review_service.get_pending_reviews()

    def approve_review(self, review_id: str) -> Optional[Any]:
        """Approves review and updates rating."""
        review = self._review_service.approve_review(review_id)
        if review:
            new_rating, count = self._review_service.get_teacher_rating(review.teacher_id)
            self._teacher_service.update_teacher_rating(review.teacher_id, new_rating, count)
        return review

    def reject_review(self, review_id: str) -> bool:
        """Rejects review."""
        return self._review_service.reject_review(review_id)

    def delete_review(self, review_id: str) -> bool:
        """Deletes review and updates teacher rating."""
        # First get review to find teacher_id
        reviews = self._review_service._repository.get_all()
        teacher_id = None
        for review in reviews:
            if review.id == review_id:
                teacher_id = review.teacher_id
                break

        # Delete review
        result = self._review_service.delete_review(review_id)

        # Update teacher rating
        if result and teacher_id:
            new_rating, count = self._review_service.get_teacher_rating(teacher_id)
            self._teacher_service.update_teacher_rating(teacher_id, new_rating, count)

        return result

    # ==========================================
    # Cabinets
    # ==========================================

    def get_all_cabinets(self) -> List:
        """Returns all cabinets."""
        return self._cabinet_service.get_all_cabinets()

    def get_cabinet_by_id(self, cabinet_id: int) -> Optional[Any]:
        """Returns cabinet by ID."""
        return self._cabinet_service.get_cabinet_by_id(cabinet_id)

    def get_free_cabinets(self, week_id: int, time: str, building: str = None) -> List:
        """Finds available cabinets at specified time."""
        return self._cabinet_service.get_free_cabinets(week_id, time, building)

    def get_current_free_cabinets(self, building: str = None) -> List:
        """Finds cabinets available now."""
        return self._cabinet_service.get_current_free_cabinets(building)

    def get_next_slot_free_cabinets(self, building: str = None):
        """Finds cabinets available for next lesson."""
        return self._cabinet_service.get_next_slot_free_cabinets(building)

    def get_buildings(self) -> List[str]:
        """Returns list of buildings."""
        return self._cabinet_service.get_buildings()

    def get_time_slots(self) -> List[str]:
        """Returns time slots."""
        return self._cabinet_service.get_time_slots()

    def get_days(self) -> dict:
        """Returns days of week."""
        return self._cabinet_service.get_days()

    def get_cabinet_schedule(self, cabinet_id: int) -> List:
        """Returns cabinet schedule."""
        return self._cabinet_service.get_cabinet_schedule(cabinet_id)

    def search_cabinets(self, query: str) -> List:
        """Searches cabinets."""
        return self._cabinet_service.search_cabinets(query)

    # ==========================================
    # News
    # ==========================================

    def get_news(self, limit: int = None) -> List:
        """Returns news."""
        return self._news_service.get_all_news(limit)

    def get_news_article(self, news_id: str) -> Optional[Any]:
        """Returns news by ID."""
        return self._news_service.get_news_by_id(news_id)

    def get_news_by_category(self, category: str) -> List:
        """Returns news by category."""
        return self._news_service.get_news_by_category(category)

    def search_news(self, query: str) -> List:
        """Searches news."""
        return self._news_service.search_news(query)

    def get_popular_news(self, limit: int = 5) -> List:
        """Returns popular news."""
        return self._news_service.get_popular_news(limit)

    def get_news_categories(self) -> List[str]:
        """Returns news categories."""
        return self._news_service.get_categories()

    def create_news(self, title: str, content: str, category: str, author: str) -> Any:
        """Creates news."""
        return self._news_service.create_news(title, content, category, author)

    def subscribe_to_news(self, email: str, name: str, language: str = 'ru') -> bool:
        """Subscribes to news."""
        return self._news_service.subscribe(email, name, language=language)

    def unsubscribe_from_news(self, email: str) -> bool:
        """Unsubscribes from news."""
        return self._news_service.unsubscribe(email)

    def update_subscriber_observer(self, subscriber_id: str) -> bool:
        """Updates subscriber observer after data changes."""
        return self._news_service.update_subscriber_observer(subscriber_id)

    # ==========================================
    # Shop
    # ==========================================

    def get_products(self) -> List:
        """Returns all products."""
        return self._shop_service.get_all_products()

    def get_product(self, product_id: str) -> Optional[Any]:
        """Returns product by ID."""
        return self._shop_service.get_product_by_id(product_id)

    def get_products_by_category(self, category: str) -> List:
        """Returns products by category."""
        return self._shop_service.get_products_by_category(category)

    def search_products(self, query: str) -> List:
        """Searches products."""
        return self._shop_service.search_products(query)

    def get_product_categories(self) -> List[str]:
        """Returns product categories."""
        return self._shop_service.get_categories()

    def calculate_cart(self, items: List[Dict]) -> float:
        """Calculates cart total."""
        return self._shop_service.calculate_cart_total(items)

    def create_order(self, customer_name: str, customer_email: str,
                     cart_items: List[Dict], address: str = "", language: str = 'ru') -> Optional[Any]:
        """Creates order."""
        return self._shop_service.create_order(
            customer_name, customer_email, cart_items, address, language
        )

    def get_customer_orders(self, email: str) -> List:
        """Returns customer orders."""
        return self._shop_service.get_customer_orders(email)

    def get_pending_orders(self) -> List:
        """Returns pending orders."""
        return self._shop_service.get_pending_orders()

    def confirm_order(self, order_id: str) -> Optional[Any]:
        """Confirms order."""
        return self._shop_service.confirm_order(order_id)

    def cancel_order(self, order_id: str) -> Optional[Any]:
        """Cancels order."""
        return self._shop_service.cancel_order(order_id)

    # ==========================================
    # Statistics
    # ==========================================

    def get_dashboard_stats(self) -> Dict:
        """Returns dashboard statistics."""
        return {
            'teachers_count': self._teacher_service.get_teacher_count(),
            'reviews_stats': self._review_service.get_reviews_count(),
            'subscribers_count': self._news_service.get_subscribers_count(),
            'orders_stats': self._shop_service.get_orders_stats()
        }

    # ==========================================
    # Complex Operations
    # ==========================================

    def get_teacher_full_info(self, teacher_id: str) -> Optional[Dict]:
        """
        Returns complete teacher information:
        - Teacher data
        - Schedule
        - Reviews
        - Rating
        """
        teacher = self._teacher_service.get_teacher_by_id(teacher_id)
        if not teacher:
            return None

        return {
            'teacher': teacher,
            'schedule': self._schedule_service.get_teacher_schedule(teacher_id),
            'reviews': self._review_service.get_teacher_reviews(teacher_id),
            'rating': self._review_service.get_teacher_rating(teacher_id),
            'rating_distribution': self._review_service.get_rating_distribution(teacher_id)
        }

    def get_home_page_data(self) -> Dict:
        """
        Returns data for home page:
        - Top teachers
        - Latest news
        - Popular products
        """
        return {
            'top_teachers': self._teacher_service.get_top_rated_teachers(5),
            'latest_news': self._news_service.get_all_news(5),
            'popular_news': self._news_service.get_popular_news(3),
            'products': self._shop_service.get_all_products()[:6]
        }

