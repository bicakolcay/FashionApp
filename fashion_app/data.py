from __future__ import annotations

from typing import Final

PRODUCTS: Final[list[dict[str, object]]] = [
    {"id": 1, "name": "Classic Denim Jacket", "price": 89.99, "sizes": ["S", "M", "L", "XL"]},
    {"id": 2, "name": "Floral Summer Dress", "price": 59.5, "sizes": ["XS", "S", "M"]},
    {"id": 3, "name": "Minimalist White Sneakers", "price": 110.0, "sizes": ["38", "39", "40", "41", "42"]},
    {"id": 4, "name": "Wool Blend Coat", "price": 199.99, "sizes": ["M", "L"]},
]


def find_product(product_id: int) -> dict[str, object] | None:
    return next((product for product in PRODUCTS if product["id"] == product_id), None)
