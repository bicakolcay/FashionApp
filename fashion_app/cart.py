"""In-memory cart domain model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class CartItem:
    product_id: int
    name: str
    price: float
    quantity: int = 1

    def to_dict(self) -> dict[str, object]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }


@dataclass
class Cart:
    _items: Dict[int, CartItem] = field(default_factory=dict)

    def add(self, *, product_id: int, name: str, price: float, quantity: int) -> CartItem:
        item = self._items.get(product_id)
        if item is None:
            item = CartItem(product_id=product_id, name=name, price=price, quantity=quantity)
            self._items[product_id] = item
        else:
            item.quantity += quantity
        return item

    def clear(self) -> None:
        self._items.clear()

    def subtotal(self) -> float:
        return sum(item.price * item.quantity for item in self._items.values())

    def serialize_items(self) -> List[dict[str, object]]:
        return [item.to_dict() for item in self._items.values()]

    def __iter__(self) -> Iterable[CartItem]:
        return iter(self._items.values())
