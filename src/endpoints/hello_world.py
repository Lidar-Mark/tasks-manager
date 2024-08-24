from flask import jsonify, Blueprint

# Create a Blueprint instance
hello_blueprint = Blueprint('hello_blueprint', __name__)


@hello_blueprint.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200
