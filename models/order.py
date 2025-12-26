"""
Order Model
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class Order:
    """Shop Order Model"""
    id: str
    customer_name: str
    customer_email: str
    items: List[Dict]  # [{'product_id': 'x', 'quantity': 1, 'price': 100}]
    total_amount: float
    status: str  # Pending, Confirmed, Delivered, Cancelled
    created_at: str
    delivery_address: str = ""
    language: str = 'ru'  # Order language (ru, en, kz)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'items': self.items,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at,
            'delivery_address': self.delivery_address,
            'language': self.language
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            customer_name=data.get('customer_name', ''),
            customer_email=data.get('customer_email', ''),
            items=data.get('items', []),
            total_amount=data.get('total_amount', 0.0),
            status=data.get('status', 'Pending'),
            created_at=data.get('created_at', datetime.now().isoformat()),
            delivery_address=data.get('delivery_address', ''),
            language=data.get('language', 'ru')
        )

