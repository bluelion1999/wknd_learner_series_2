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
    
def test_update_item(client):
    response = client.post("/items", json={"name":"pen", "price":5.0})
    
    assert response.status_code == 200 
    
    response_data = response.json()
    data_id = response_data["id"]
    
    update = client.put(f"/items/{data_id}", json={"name":"pencil", "price": 3.0})
    
    assert update.status_code == 200
    
    update_data = update.json()
    assert update_data["name"] == "pencil"
    assert update_data["price"] == 3.0
    
def test_update_item_not_found(client):
    response = client.put("/items/999", json={"name": "notebook", "price":15.0})
    
    assert response.status_code == 404
    
def test_delete_item(client):
    response = client.post("/items", json={"name": "chocolate bar", "price": 1.99})
    
    assert response.status_code == 200
    
    data = response.json()
    data_id = data["id"]
    
    response_delete = client.delete(f"/items/{data_id}")
    
    assert response_delete.status_code == 200
    
    response_get = client.get(f"/items/{data_id}")
    
    assert response_get.status_code == 404
    
def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    
    assert response.status_code == 404

def test_create_item_negative_price(client):
    response = client.post("/items", json={"name": "chocolate bar", "price": -1.99})
        
    assert response.status_code == 422

def test_create_item_empty_name(client):
    response = client.post("/items", json={"name": "", "price": 1.99})
        
    assert response.status_code == 422

def test_create_item_blank_name(client):
    response = client.post("/items", json={"name": " ", "price": 1.99})
        
    assert response.status_code == 422

def test_create_item_strips_name(client):
    response = client.post("/items", json={"name": " spaced ", "price": 1.99})
        
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "spaced"
    