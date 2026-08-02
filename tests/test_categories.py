def test_create_category(client):
    response = client.post("/categories", json={"name":"Stationery", "description":"Desk paper products"})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data
    assert data["name"] == "Stationery"
    assert data["description"] == "Desk paper products"
    
def test_create_duplicate_categories(client):
    response1 = client.post("/categories", json={"name":"gadgets", "description":"desk electronics"})
    response2 = client.post("/categories", json={"name":"gadgets", "description":"desk electronics"})
    
    assert response1.status_code == 200
    assert response2.status_code == 409
    
def test_get_categories(client):
    post1 = client.post("/categories", json={"name": "sweets", "description":"All candy, sweet baked gooods"})
    post2 = client.post("/categories", json={"name": "Speakers", "description":"Audio producing products"})
    
    response = client.get("/categories")
    
    assert post1.status_code == 200
    assert post2.status_code == 200
    
    assert response.status_code == 200
    assert len(response.json()) >=2

def test_create_category_without_description(client):
    response = client.post("/categories", json={"name": "books"})
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["description"] is None
    
    
def test_create_category_empty_name(client):
    response = client.post("/categories", json={"name": "", "description": "asdfgasdf"})
        
    assert response.status_code == 422

def test_create_category_blank_name(client):
    response = client.post("/categories", json={"name": " ", "description": "asdfasdf"})
        
    assert response.status_code == 422

def test_create_category_strips_name(client):
    response = client.post("/categories", json={"name": " spaced ", "description": "asdfasdf"})

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "spaced"


def test_get_category(client):
    created = client.post("/categories", json={"name": "tools", "description": "hardware"})
    category_id = created.json()["id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "tools"


def test_get_category_not_found(client):
    response = client.get("/categories/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_update_category(client):
    created = client.post("/categories", json={"name": "tools", "description": "hardware"})
    category_id = created.json()["id"]

    response = client.put(
        f"/categories/{category_id}",
        json={"name": "hand tools", "description": "manual hardware"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "hand tools"
    assert data["description"] == "manual hardware"


def test_update_category_not_found(client):
    response = client.put("/categories/999", json={"name": "ghost"})

    assert response.status_code == 404


def test_delete_category(client):
    created = client.post("/categories", json={"name": "temporary"})
    category_id = created.json()["id"]

    response = client.delete(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json() == {"deleted": category_id}
    assert client.get(f"/categories/{category_id}").status_code == 404


def test_delete_category_not_found(client):
    response = client.delete("/categories/999")

    assert response.status_code == 404


def test_delete_category_with_items(client):
    created = client.post("/categories", json={"name": "occupied"})
    category_id = created.json()["id"]
    client.post("/items", json={"name": "widget", "price": 1.0, "category_id": category_id})

    response = client.delete(f"/categories/{category_id}")

    assert response.status_code == 409
    assert client.get(f"/categories/{category_id}").status_code == 200
