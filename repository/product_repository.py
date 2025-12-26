"""
Product Repository
"""
from typing import List, Optional
from repository.base_repository import BaseRepository
from models.product import Product


class ProductRepository(BaseRepository[Product]):
    """Repository for working with products."""

    def __init__(self, data_dir: str = None):
        super().__init__('products.json', data_dir)

    def _to_entity(self, data: dict) -> Product:
        return Product.from_dict(data)

    def _to_dict(self, entity: Product) -> dict:
        return entity.to_dict()

    def get_available(self) -> List[Product]:
        """Returns available products."""
        all_products = self.get_all()
        return [p for p in all_products if p.is_available and p.stock > 0]

    def find_by_category(self, category: str) -> List[Product]:
        """Finds products by category."""
        all_products = self.get_all()
        return [
            p for p in all_products
            if p.category.lower() == category.lower() and p.is_available
        ]

    def search(self, query: str) -> List[Product]:
        """Searches products by name or description."""
        all_products = self.get_all()
        query_lower = query.lower()
        return [
            p for p in all_products
            if (query_lower in p.name.lower() or query_lower in p.description.lower())
            and p.is_available
        ]

    def find_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Finds products in price range."""
        all_products = self.get_all()
        return [
            p for p in all_products
            if min_price <= p.price <= max_price and p.is_available
        ]

    def decrease_stock(self, product_id: str, quantity: int = 1) -> Optional[Product]:
        """Decreases product stock."""
        product = self.get_by_id(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            if product.stock == 0:
                product.is_available = False
            return self.update(product)
        return None

    def increase_stock(self, product_id: str, quantity: int) -> Optional[Product]:
        """Increases product stock."""
        product = self.get_by_id(product_id)
        if product:
            product.stock += quantity
            product.is_available = True
            return self.update(product)
        return None

    def get_categories(self) -> List[str]:
        """Returns list of product categories."""
        all_products = self.get_all()
        categories = set(p.category for p in all_products)
        return sorted(list(categories))

    def get_out_of_stock(self) -> List[Product]:
        """Returns out of stock products."""
        all_products = self.get_all()
        return [p for p in all_products if p.stock == 0]

