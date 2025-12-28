"""
Base Abstract Factory (Factory Method Pattern)

Factory Method pattern defines an interface for creating objects,
but lets subclasses decide which class to instantiate.
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseFactory(ABC):
    """
    Abstract Factory - defines interface for creating objects.

    SOLID application:
    - SRP: Factory is responsible only for object creation
    - OCP: New factories can be added without changing existing ones
    - LSP: All factories implement a single interface
    - DIP: Depends on abstraction, not concrete classes
    """

    @abstractmethod
    def create(self, data: dict) -> Any:
        """
        Factory method - creates object from data dictionary.

        Args:
            data: Dictionary with data for object creation

        Returns:
            Created object
        """
        pass

    @abstractmethod
    def create_default(self) -> Any:
        """
        Creates object with default values.

        Returns:
            Object with default values
        """
        pass

    def create_many(self, data_list: list) -> list:
        """
        Creates multiple objects from list of dictionaries.

        Args:
            data_list: List of data dictionaries

        Returns:
            List of created objects
        """
        return [self.create(data) for data in data_list]

