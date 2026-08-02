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
    
    
def test_list_items_respects_limit(client):
    response = client.post("/items", json={"name": "pen", "price": 5.0})
    response2 = client.post("/items", json={"name": "pencil", "price": 4.0})
    response3 = client.post("/items", json={"name": "eraser", "price": 2.0})
    
    response_get = client.get("/items?limit=2")
    
    assert len(response_get.json()) == 2
    
def test_list_items_respects_skip(client):
    response = client.post("/items", json={"name": "pen", "price": 5.0})
    response2 = client.post("/items", json={"name": "pencil", "price": 4.0})
    response3 = client.post("/items", json={"name": "eraser", "price": 2.0})
    
    response_get = client.get("/items?skip=2")

    assert len(response_get.json()) == 1
    
def test_list_items_pages_do_not_overlap(client):
    response = client.post("/items", json={"name": "pen", "price": 5.0})
    response2 = client.post("/items", json={"name": "pencil", "price": 4.0})
    response3 = client.post("/items", json={"name": "eraser", "price": 2.0})
    response4 = client.post("/items", json={"name": "whiteout", "price": 99.99})
    
    post_response = [response,response2,response3,response4]
    
    post_id = [val.json()["id"] for val in post_response]

    response_get1 = client.get("/items?skip=0&limit=2")
    response_get2 = client.get("/items?skip=2&limit=2")

    assert response_get1.status_code == 200
    assert response_get2.status_code == 200

    page1_id = [item["id"] for item in response_get1.json()]
    page2_id = [item["id"] for item in response_get2.json()]

    assert page1_id == post_id[:2]
    assert page2_id == post_id[2:]


def test_list_items_rejects_zero_limit(client):
    response = client.get("/items?limit=0")

    assert response.status_code == 422


def test_list_items_rejects_negative_skip(client):
    response = client.get("/items?skip=-1")

    assert response.status_code == 422


def test_list_items_rejects_limit_above_max(client):
    response = client.get("/items?limit=101")

    assert response.status_code == 422


def test_item_includes_category(client):
    category = client.post(
        "/categories", json={"name": "stationery", "description": "desk supplies"}
    ).json()

    client.post(
        "/items",
        json={"name": "pen", "price": 5.0, "category_id": category["id"]},
    )

    response = client.get("/items")

    assert response.status_code == 200

    item = response.json()[0]
    assert item["category_id"] == category["id"]
    assert item["category"]["id"] == category["id"]
    assert item["category"]["name"] == "stationery"
    assert item["category"]["description"] == "desk supplies"


def test_item_without_category_has_null_category(client):
    client.post("/items", json={"name": "orphan", "price": 1.0})

    response = client.get("/items")

    assert response.status_code == 200

    item = response.json()[0]
    assert item["category_id"] is None
    assert item["category"] is None


    