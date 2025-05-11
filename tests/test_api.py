import os
import sys

import pytest
from fastapi.testclient import TestClient

from homework.database import engine
from homework.main import app
from homework.models import Base

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

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
            "description": "Test Description",
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_read_recipes(test_db):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) == 1
