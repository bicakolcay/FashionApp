from __future__ import annotations

from flask import Flask, jsonify, request

from .cart import Cart
from .data import PRODUCTS, find_product


def create_app() -> Flask:
    app = Flask(__name__)
    cart = Cart()

    @app.get("/health")
    def health() -> tuple[dict, int]:
        """Simple health check endpoint."""
        return {"status": "ok"}, 200

    @app.get("/products")
    def list_products():
        """Return the full catalog of fashion products."""
        return jsonify(PRODUCTS)

    @app.get("/products/<int:product_id>")
    def get_product(product_id: int):
        product = find_product(product_id)
        if product is None:
            return {"error": "Product not found"}, 404
        return jsonify(product)

    @app.post("/cart")
    def add_to_cart():
        payload = request.get_json(silent=True) or {}
        product_id = payload.get("product_id")
        quantity = payload.get("quantity", 1)

        if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity < 1:
            return {"error": "Invalid payload"}, 400

        product = find_product(product_id)
        if product is None:
            return {"error": "Product not found"}, 404

        # Copy relevant fields so the in-memory cart is decoupled from catalog
        cart_item = cart.add(
            product_id=product["id"],
            name=product["name"],
            price=float(product["price"]),
            quantity=quantity,
        )
        return jsonify(cart_item.to_dict()), 201

    @app.get("/cart")
    def view_cart():
        subtotal = cart.subtotal()
        return jsonify({
            "items": cart.serialize_items(),
            "subtotal": round(subtotal, 2),
        })

    @app.delete("/cart")
    def clear_cart():
        cart.clear()
        return {"status": "cart cleared"}, 200

    return app


__all__ = ["create_app"]
