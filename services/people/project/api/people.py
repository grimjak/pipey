from flask import request, Blueprint
from flask_restful import Resource, Api


import flask_marshmallow as fm
import marshmallow_mongoengine as ma

from project import app

from project.api.model import PersonModel
from project.api.utils import authenticate

mm = fm.Marshmallow(app)

api_bp = Blueprint('api', __name__)  # create api blueprint
api = Api(api_bp)  # register api with blueprint


class PersonSchema(ma.ModelSchema):
    class Meta:
        model = PersonModel
    _links = mm.Hyperlinks({'uri': mm.UrlFor('api.person', _id='<id>')})


personSchema = PersonSchema()
peopleSchema = PersonSchema(many=True)


class Person(Resource):

    def get(self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        result = personSchema.dump(data)

        if result.errors:
            return result.errors, 404  # need a test for this
        return result.data, 200

    def put(self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        new = personSchema.update(data, request.get_json())
        if new.errors:
            return new.errors, 400  # need a test for this, try bad json?
        new.data.save()
        result = personSchema.dump(new.data)
        return result.data, 200

    def delete(self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        data.delete()
        return 200


class People(Resource):
    def get(self):
        data = peopleSchema.dump(PersonModel.objects()).data
        return data, 200

    @authenticate
    def post(resp, self):
        jsonrequest = request.get_json()
        result = PersonSchema().load(jsonrequest)

        if result.errors:
            return result.errors, 400

        try:
            result.data.save()
        except(ValueError) as e:
            return {'message': 'Invalid payload'}, 400
        return PersonSchema().dump(result.data).data, 201


class Ping(Resource):
    def get(self):
        return {'status': 'success', 'message': 'pong!'}, 200


# register resources with api
api.add_resource(Ping, "/ping", endpoint="ping")
api.add_resource(People, "/people", endpoint="people")
api.add_resource(Person, "/people/<string:_id>", endpoint="person")
