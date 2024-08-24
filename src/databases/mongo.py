from pymongo import MongoClient

client = MongoClient('mongodb://admin:admin@127.0.0.1:27017/', serverSelectionTimeoutMS=5000)
db = client['tasks']
tasks_collection = db['important-tasks']


def init_mongodb():
    # MongoDB connection string
    try:

        # Attempt to connect to verify MongoDB connection
        client.server_info()

        # Ensure the collection is created by inserting a dummy document
        if tasks_collection.estimated_document_count() == 0:
            dummy_task = {
                "name": "dummy_task",
                "people_involved": [],
                "description": "This is a dummy task to create the collection."
            }
            tasks_collection.insert_one(dummy_task)
            tasks_collection.delete_one({"name": "dummy_task"})

        print("Connected to MongoDB and ensured collection is created.")
    except Exception as err:
        print(f"Failed to connect to MongoDB: {err}")
        raise
