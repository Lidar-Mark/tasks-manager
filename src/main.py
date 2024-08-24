from flask import Flask
from src.endpoints.create_task import create_task_blueprint
from src.endpoints.hello_world import hello_blueprint
from src.endpoints.read_task import read_task_blueprint


app = Flask(__name__)
app.register_blueprint(hello_blueprint)
app.register_blueprint(create_task_blueprint)
app.register_blueprint(read_task_blueprint)


if __name__ == '__main__':
    app.run(debug=True)

