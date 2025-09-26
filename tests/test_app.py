from fashion_app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_products():
    app = create_app()
    client = app.test_client()

    response = client.get("/products")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data, "Product list should not be empty"


def test_cart_flow():
    app = create_app()
    client = app.test_client()

    add_response = client.post("/cart", json={"product_id": 1, "quantity": 2})
    assert add_response.status_code == 201
    added_item = add_response.get_json()
    assert added_item["quantity"] == 2

    second_add = client.post("/cart", json={"product_id": 1, "quantity": 3})
    assert second_add.status_code == 201
    assert second_add.get_json()["quantity"] == 5

    cart_response = client.get("/cart")
    assert cart_response.status_code == 200
    cart_data = cart_response.get_json()
    assert cart_data["items"]
    assert cart_data["subtotal"] > 0
    assert cart_data["items"][0]["quantity"] == 5

    clear_response = client.delete("/cart")
    assert clear_response.status_code == 200
    assert clear_response.get_json() == {"status": "cart cleared"}
