from flask import Blueprint
from flask_restful import Api

from project.api.tasks_resources import Ping, Tasks, Task

# refactor to create central "peole" service which defines enpoints and blueprints and imports the
# relevant resources

api_bp = Blueprint('tasks', __name__)  # create api blueprint
api = Api(api_bp)  # register api with blueprint

# register resources with api
api.add_resource(Ping, "/ping", endpoint="ping")
api.add_resource(Tasks, "/tasks", endpoint="tasks")
api.add_resource(Task, "/tasks/<string:_id>", endpoint="task")
