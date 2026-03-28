import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from urllib import response

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_sheep():
    response = client.get("/sheep/1")

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    sheep_data = {
        "id": 10,
        "name": "Horsie",
        "breed": "Suffolk",
        "sex": "ewe"
    }

    response = client.post("/sheep", json=sheep_data)

    assert response.status_code == 201
    assert response.json() == sheep_data

    get_response = client.get("/sheep/10")
    assert get_response.status_code == 200
    assert get_response.json() == sheep_data

def test_update_sheep():
    updated_sheep_data = {
        "id": 1,
        "name": "SpiceUpdated",
        "breed": "Merino",
        "sex": "ram"
    }

    response = client.put("/sheep/1", json=updated_sheep_data)

    assert response.status_code == 200
    assert response.json() == updated_sheep_data

    get_response = client.get("/sheep/1")
    assert get_response.status_code == 200
    assert get_response.json() == updated_sheep_data

def test_delete_sheep():
    sheep_data = {
        "id": 11,
        "name": "TempSheep",
        "breed": "Dorper",
        "sex": "ewe"
    }

    client.post("/sheep", json=sheep_data)

    response = client.delete("/sheep/11")
    assert response.status_code == 200
    assert response.json() == {"message": "Sheep deleted successfully"}

    get_response = client.get("/sheep/11")
    assert get_response.status_code == 404

def test_read_all_sheep():
    response = client.get("/sheep")

    assert response.status_code == 200
    sheep_list = response.json()

    assert isinstance(sheep_list, list)
    assert len(sheep_list) >= 6

    ids = [sheep["id"] for sheep in sheep_list]
    assert 1 in ids
    assert 2 in ids
    assert 3 in ids