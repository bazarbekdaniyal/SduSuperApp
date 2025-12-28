"""
Order Repository
"""
from typing import List, Optional
from repository.base_repository import BaseRepository
from models.order import Order


class OrderRepository(BaseRepository[Order]):
    """Repository for working with orders."""

    def __init__(self, data_dir: str = None):
        super().__init__('orders.json', data_dir)

    def _to_entity(self, data: dict) -> Order:
        return Order.from_dict(data)

    def _to_dict(self, entity: Order) -> dict:
        return entity.to_dict()

    def find_by_email(self, email: str) -> List[Order]:
        """Finds orders by customer email."""
        all_orders = self.get_all()
        return [o for o in all_orders if o.customer_email.lower() == email.lower()]

    def find_by_status(self, status: str) -> List[Order]:
        """Finds orders by status."""
        all_orders = self.get_all()
        filtered = [o for o in all_orders if o.status.lower() == status.lower()]
        return sorted(filtered, key=lambda o: o.created_at, reverse=True)

    def get_pending(self) -> List[Order]:
        """Returns pending orders."""
        return self.find_by_status('Pending')

    def get_confirmed(self) -> List[Order]:
        """Returns confirmed orders."""
        return self.find_by_status('Confirmed')

    def update_status(self, order_id: str, status: str) -> Optional[Order]:
        """Updates order status."""
        order = self.get_by_id(order_id)
        if order:
            order.status = status
            return self.update(order)
        return None

    def confirm(self, order_id: str) -> Optional[Order]:
        """Confirms order."""
        return self.update_status(order_id, 'Confirmed')

    def cancel(self, order_id: str) -> Optional[Order]:
        """Cancels order."""
        return self.update_status(order_id, 'Cancelled')

    def deliver(self, order_id: str) -> Optional[Order]:
        """Marks order as delivered."""
        return self.update_status(order_id, 'Delivered')

    def get_recent(self, limit: int = 10) -> List[Order]:
        """Returns recent orders."""
        all_orders = self.get_all()
        sorted_orders = sorted(all_orders, key=lambda o: o.created_at, reverse=True)
        return sorted_orders[:limit]
"""
Repository module for working with data
"""
from repository.base_repository import BaseRepository
from repository.teacher_repository import TeacherRepository
from repository.schedule_repository import ScheduleRepository
from repository.review_repository import ReviewRepository
from repository.room_repository import RoomRepository
from repository.news_repository import NewsRepository
from repository.product_repository import ProductRepository
from repository.subscriber_repository import SubscriberRepository
from repository.order_repository import OrderRepository

__all__ = [
    'BaseRepository',
    'TeacherRepository',
    'ScheduleRepository',
    'ReviewRepository',
    'RoomRepository',
    'NewsRepository',
    'ProductRepository',
    'SubscriberRepository',
    'OrderRepository'
]

