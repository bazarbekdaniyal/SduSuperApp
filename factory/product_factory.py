"""
Product Factory (Factory Method Pattern)
"""
import uuid
from factory.base_factory import BaseFactory
from models.product import Product


class ProductFactory(BaseFactory):
    """
    Factory for creating Product objects.

    Allows creating products of different categories
    with appropriate presets.
    """

    def create(self, data: dict) -> Product:
        """
        Creates product from data dictionary.
        """
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        return Product.from_dict(data)

    def create_default(self) -> Product:
        """
        Creates product with default values.
        """
        return Product(
            id=str(uuid.uuid4()),
            name="New Product",
            description="",
            price=0.0,
            category="Other",
            stock=0,
            is_available=False
        )

    def create_clothing(self, name: str, description: str, price: float, stock: int, image: str = None) -> Product:
        """
        Creates clothing product.
        """
        return Product(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            price=price,
            category="Clothing",
            image=image,
            stock=stock,
            is_available=stock > 0
        )

    def create_accessory(self, name: str, description: str, price: float, stock: int, image: str = None) -> Product:
        """
        Creates accessory.
        """
        return Product(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            price=price,
            category="Accessories",
            image=image,
            stock=stock,
            is_available=stock > 0
        )

    def create_stationery(self, name: str, description: str, price: float, stock: int) -> Product:
        """
        Creates stationery product.
        """
        return Product(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            price=price,
            category="Stationery",
            stock=stock,
            is_available=stock > 0
        )

