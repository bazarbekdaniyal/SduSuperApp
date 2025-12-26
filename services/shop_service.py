"""
Shop Service
"""
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from models.product import Product
from models.order import Order
from repository.product_repository import ProductRepository
from repository.order_repository import OrderRepository
from factory.product_factory import ProductFactory
from services.email_service import get_email_service
from services.translation_service import TranslationService

class ShopService:
    """Service for working with the shop. Automatically translates products when creating."""

    def __init__(self, product_repository: ProductRepository = None,
                 order_repository: OrderRepository = None,
                 translation_service: TranslationService = None):
        self._product_repo = product_repository or ProductRepository()
        self._order_repo = order_repository or OrderRepository()
        self._factory = ProductFactory()
        self._translation_service = translation_service or TranslationService()

    # === Products ===

    def get_all_products(self) -> List[Product]:
        """Returns all available products."""
        return self._product_repo.get_available()

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Returns product by ID."""
        return self._product_repo.get_by_id(product_id)

    def get_products_by_category(self, category: str) -> List[Product]:
        """Returns products by category."""
        return self._product_repo.find_by_category(category)

    def search_products(self, query: str) -> List[Product]:
        """Searches products."""
        return self._product_repo.search(query)

    def get_categories(self) -> List[str]:
        """Returns product categories."""
        return self._product_repo.get_categories()

    def create_product(self, data: dict) -> Product:
        """Creates a new product and automatically translates to other languages."""
        # Automatically translate product to English and Kazakh
        translations = {}
        if self._translation_service.is_available():
            try:
                translations = self._translation_service.translate_product(
                    name=data.get('name', ''),
                    description=data.get('description', ''),
                    category=data.get('category', ''),
                    source_lang='ru'
                )
                import logging
                logging.getLogger(__name__).info(f"Product translated successfully. Translations: {list(translations.keys())}")
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Translation failed: {str(e)}", exc_info=True)
                print(f"⚠️  Product translation error: {str(e)}")
        else:
            import logging
            logging.getLogger(__name__).warning("Translation service is not available. Install deep-translator: pip install deep-translator")
            print("⚠️  Translation service unavailable. Install library: pip install deep-translator")
        
        # Add translations to data
        if translations:
            data['translations'] = translations
        
        product = self._factory.create(data)
        return self._product_repo.create(product)

    def update_product(self, product_id: str, data: dict) -> Optional[Product]:
        """Updates product and automatically translates changes."""
        product = self._product_repo.get_by_id(product_id)
        if not product:
            return None

        # If name, description or category are updated, translate again
        needs_translation = any(key in data for key in ['name', 'description', 'category'])

        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)

        # If translatable fields changed, update translations
        if needs_translation and self._translation_service.is_available():
            try:
                translations = self._translation_service.translate_product(
                    name=product.name,
                    description=product.description,
                    category=product.category,
                    source_lang='ru'
                )
                product.translations = translations if translations else product.translations
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Translation update failed: {str(e)}")

        return self._product_repo.update(product)

    def delete_product(self, product_id: str) -> bool:
        """Deletes a product."""
        return self._product_repo.delete(product_id)

    # === Cart and Orders ===

    def calculate_cart_total(self, cart_items: List[Dict]) -> float:
        """
        Calculates cart total.

        Args:
            cart_items: [{'product_id': 'x', 'quantity': n}]

        Returns:
            Total amount
        """
        total = 0.0
        for item in cart_items:
            product = self._product_repo.get_by_id(item['product_id'])
            if product:
                total += product.price * item.get('quantity', 1)
        return round(total, 2)

    def validate_cart(self, cart_items: List[Dict]) -> Dict:
        """
        Validates cart for product availability.

        Returns:
            {'valid': bool, 'errors': [], 'items': []}
        """
        result = {'valid': True, 'errors': [], 'items': []}

        for item in cart_items:
            product = self._product_repo.get_by_id(item['product_id'])
            quantity = item.get('quantity', 1)

            if not product:
                result['valid'] = False
                result['errors'].append(f"Product {item['product_id']} not found")
                continue

            if not product.is_available:
                result['valid'] = False
                result['errors'].append(f"Product '{product.name}' is unavailable")
                continue

            if product.stock < quantity:
                result['valid'] = False
                result['errors'].append(
                    f"Insufficient stock for '{product.name}' (available: {product.stock})"
                )
                continue

            result['items'].append({
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })

        return result

    def create_order(self, customer_name: str, customer_email: str,
                     cart_items: List[Dict], delivery_address: str = "", language: str = 'ru') -> Optional[Order]:
        """
        Creates an order.

        Args:
            customer_name: Customer name
            customer_email: Customer email
            cart_items: Cart items
            delivery_address: Delivery address
            language: Order language (ru, en, kz)

        Returns:
            Order or None if error
        """
        from utils.data_i18n import get_translated_product
        
        # Validate cart
        validation = self.validate_cart(cart_items)
        if not validation['valid']:
            return None

        # Form order items with translated names
        order_items = []
        total = 0.0

        for item in validation['items']:
            # Get product for translation
            product = self._product_repo.get_by_id(item['product_id'])
            if product:
                translated = get_translated_product(product, language)
                product_name = translated['name']
            else:
                product_name = item['name']
            
            order_items.append({
                'product_id': item['product_id'],
                'name': product_name,
                'price': item['price'],
                'quantity': item['quantity']
            })
            total += item['subtotal']

        # Create order
        order = Order(
            id=str(uuid.uuid4()),
            customer_name=customer_name,
            customer_email=customer_email,
            items=order_items,
            total_amount=round(total, 2),
            status='Pending',
            created_at=datetime.now().isoformat(),
            delivery_address=delivery_address,
            language=language
        )

        created_order = self._order_repo.create(order)

        # Decrease product stock
        for item in cart_items:
            self._product_repo.decrease_stock(item['product_id'], item.get('quantity', 1))

        # Send confirmation email
        email_service = get_email_service()
        email_service.send_order_confirmation(created_order)

        return created_order

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Returns order by ID."""
        return self._order_repo.get_by_id(order_id)

    def get_customer_orders(self, email: str) -> List[Order]:
        """Returns customer orders."""
        return self._order_repo.find_by_email(email)

    def get_pending_orders(self) -> List[Order]:
        """Returns pending orders."""
        return self._order_repo.get_pending()

    def confirm_order(self, order_id: str) -> Optional[Order]:
        """Confirms an order."""
        order = self._order_repo.confirm(order_id)
        if order:
            # Send email notification
            email_service = get_email_service()
            email_service.send_order_confirmed(order)
        return order

    def cancel_order(self, order_id: str) -> Optional[Order]:
        """Cancels an order."""
        order = self._order_repo.get_by_id(order_id)
        if order and order.status != 'Cancelled':
            # Return products to stock
            for item in order.items:
                self._product_repo.increase_stock(item['product_id'], item['quantity'])

        cancelled_order = self._order_repo.cancel(order_id)
        if cancelled_order:
            # Send email notification
            email_service = get_email_service()
            email_service.send_order_cancelled(cancelled_order)
        return cancelled_order

    def deliver_order(self, order_id: str) -> Optional[Order]:
        """Marks order as delivered."""
        return self._order_repo.deliver(order_id)

    def get_orders_stats(self) -> Dict:
        """Returns order statistics."""
        all_orders = self._order_repo.get_all()
        return {
            'total': len(all_orders),
            'pending': len([o for o in all_orders if o.status == 'Pending']),
            'confirmed': len([o for o in all_orders if o.status == 'Confirmed']),
            'delivered': len([o for o in all_orders if o.status == 'Delivered']),
            'cancelled': len([o for o in all_orders if o.status == 'Cancelled']),
            'total_revenue': sum(o.total_amount for o in all_orders if o.status != 'Cancelled')
        }

