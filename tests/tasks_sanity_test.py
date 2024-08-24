import pytest
from pymongo import MongoClient
from src.main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# fix code duplication
@pytest.fixture(scope="module")
def mongo_client():
    # Use the same connection string as in your app
    client = MongoClient('mongodb://admin:admin@127.0.0.1:27017/')
    db = client['tasks']
    yield db
    # Cleanup after tests
    client.drop_database('tasks')



def test_create_task(client, mongo_client):
    # Test data
    task_data = {
        "name": "Write tests",
        "people_involved": ["John", "Jane"],
        "description": "Write tests for the task API."
    }

    # Send POST request to create a task
    response = client.post('/api/task', json=task_data)
    assert response.status_code == 201
    assert response.json == {"message": "Task created successfully"}

    # Verify the task was inserted into the database
    task_in_db = mongo_client['important-tasks'].find_one({"name": "Write tests"})
    assert task_in_db is not None
    assert task_in_db["name"] == "Write tests"
    assert task_in_db["people_involved"] == ["John", "Jane"]
    assert task_in_db["description"] == "Write tests for the task API."


def test_read_task(client, mongo_client):
    # Insert a task directly into the database for testing
    task_data = {
        "name": "Review code",
        "people_involved": ["Alice", "Bob"],
        "description": "Review the code for the new feature."
    }
    mongo_client['important-tasks'].insert_one(task_data)

    # Send GET request to read the task
    response = client.get('/api/task/Review%20code')
    assert response.status_code == 200

    # Check the response data
    task = response.json
    assert task["name"] == "Review code"
    assert task["people_involved"] == ["Alice", "Bob"]
    assert task["description"] == "Review the code for the new feature."