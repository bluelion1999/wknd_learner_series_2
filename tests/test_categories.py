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
    
    