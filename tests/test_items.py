def test_get_items_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []

def test_create_item(client):
    response = client.post("/items", json={"name":"pen", "price":5.0})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["name"] == "pen"
    assert data["price"] == 5.0
    assert "id" in data


def test_get_item_not_found(client):
    response = client.get("/items/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
    
def test_create_item_invalid_category(client):
    response = client.post("/items", json={"name":"pencil", "price":3.0, "category_id":999})
    
    assert response.status_code == 400

 