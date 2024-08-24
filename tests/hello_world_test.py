import pytest
from src.main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    response = client.get('/api/hello')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}
