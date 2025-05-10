import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, engine
from models import Base

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_recipe(test_db):
    response = client.post(
        "/recipes",
        json={
            "title": "Test Recipe",
            "cooking_time": 30,
            "ingredients": "Test Ingredients",
            "description": "Test Description"
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_read_recipes(test_db):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) == 1
