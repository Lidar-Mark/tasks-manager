import pytest
from pymongo import MongoClient
from datetime import datetime


@pytest.fixture(scope="module")
def mongo_client():
    # Connect to MongoDB
    client = MongoClient('mongodb://admin:admin@127.0.0.1:27017/')
    db = client['tasks']
    yield db
    # Optional: Cleanup specific collections if needed
    # db['important-tasks'].delete_many({})


def test_delete_last_created_task(mongo_client):
    collection = mongo_client['important-tasks']

    # Ensure the collection is clean before the test
    collection.delete_many({})

    # Insert tasks
    tasks = [
        {"name": "Task 1", "description": "First task", "created_at": datetime.utcnow()},
        {"name": "Task 2", "description": "Second task", "created_at": datetime.utcnow()},
        {"name": "Task 3", "description": "Third task", "created_at": datetime.utcnow()}
    ]

    # Insert tasks into the collection
    collection.insert_many(tasks)

    # Retrieve the last created task based on the 'created_at' timestamp
    last_task = collection.find_one(sort=[("created_at", -1)])

    assert last_task is not None, "No tasks found in the collection."

    # Store the ID of the last task to verify deletion
    last_task_id = last_task["_id"]

    # Delete the last created task
    result = collection.delete_one({"_id": last_task_id})

    assert result.deleted_count == 1, "Failed to delete the last task."

    # Verify that the task has been deleted
    deleted_task = collection.find_one({"_id": last_task_id})
    assert deleted_task is None, "The last task was not deleted."

    # Optional: Verify the remaining tasks
    remaining_tasks = list(collection.find())
    assert len(remaining_tasks) == len(tasks) - 1, "There should be only 2 tasks remaining."
