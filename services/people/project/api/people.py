from flask import Blueprint
from flask_restful import Api

from project.api.people_resources import Ping, People, PeopleTypes, Person, Skill, Skills

# refactor to create central "peole" service which defines enpoints and blueprints and imports the
# relevant resources

api_bp = Blueprint('people', __name__)  # create api blueprint
api = Api(api_bp)  # register api with blueprint

# register resources with api
api.add_resource(Ping, "/ping", endpoint="ping")
api.add_resource(People, "/people", endpoint="people")
api.add_resource(PeopleTypes, "/peopletypes", endpoint="peopletypes")
api.add_resource(Person, "/people/<string:_id>", endpoint="person")
api.add_resource(Skill, "/skills/<string:_id>", endpoint="skill")
api.add_resource(Skills, "/skills", endpoint="skills")
