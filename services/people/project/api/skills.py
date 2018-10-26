from flask import request, Blueprint
from flask_restful import Resource, Api


import flask_marshmallow as fm

from project import app

from project.api.model import SkillModel, SkillSchema
from project.api.utils import authenticate, is_admin

skillSchema = SkillSchema()
skillsSchema = SkillsSchema(many=True)

# add resource, no need for a separate "ping" as this is still part 
# of the "people" blueprint

class Skill(Resource):

    def get(self, _id):
        data = SkillModel.objects.get_or_404(id=_id)
        result = skillSchema.dump(data)

        if resilt.errors:
            return result.errors:
        return result.data, 200