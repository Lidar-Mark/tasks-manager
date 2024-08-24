from flask import Flask, jsonify, Blueprint
from src.databases.mongo import tasks_collection


read_task_blueprint = Blueprint('read_task_blueprint', __name__)


@read_task_blueprint.route('/api/task/<task_name>', methods=['GET'])
def read_task(task_name):
    task = tasks_collection.find_one({"name": task_name})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Exclude the ObjectId from the response
    try:
        task["_id"] = str(task["_id"])
        return jsonify(task), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

