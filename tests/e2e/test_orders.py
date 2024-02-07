def test_get_order(client, order):
    response = client.get(f"/orders/{order.id}")
    assert response.json()["id"] == order.id
