from abc import ABC, abstractmethod
from typing import Literal

from rest_framework.request import Request


class CartServiceInterface(ABC):
    @abstractmethod
    def add_to_cart(self, request: Request, product_slug: str) -> Literal[201, 204]:
        raise NotImplementedError

    @abstractmethod
    def get_cart(self, request: Request) -> dict:
        raise NotImplementedError
