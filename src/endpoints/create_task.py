from flask import Flask, jsonify, request, Blueprint
from src.databases.mongo import tasks_collection


create_task_blueprint = Blueprint('create_task_blueprint', __name__)

@create_task_blueprint.route('/api/task', methods=['POST'])
def create_task():
    task_data = request.json
    if not task_data:
        return jsonify({"error": "Invalid task data"}), 400

    task = {
        "name": task_data.get("name"),
        "people_involved": task_data.get("people_involved", []),
        "description": task_data.get("description")
    }

    try:
        tasks_collection.insert_one(task)
        return jsonify({"message": "Task created successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400