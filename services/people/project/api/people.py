from flask import request
from flask_restful import Resource

import flask_marshmallow as fm
import marshmallow_mongoengine as ma

from project import db
from project import app

mm = fm.Marshmallow(app)


class PersonModel(db.Document):
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    employeenumber = db.IntField()
    address = db.StringField()
    startdate = db.DateTimeField()


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

    def post(self):
        jsonrequest = request.get_json()
        result = PersonSchema().load(jsonrequest)

        if result.errors:
            return result.errors, 400
        result.data.save()
        return PersonSchema().dump(result.data).data, 201


class Ping(Resource):
    def get(self):
        return {'status': 'success', 'message': 'pong!'}, 200
