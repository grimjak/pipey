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
            return result.errors, 404
        return result.data, 200

    def put(self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        new = personSchema.update(data, request.get_json())
        if new.errors:
            return new.errors, 400
        new.data.save()
        result = personSchema.dump(new.data)
        if result.errors:
            return result.errors, 400
        return result.data, 200

    def delete(self, name):
        if db.people.delete_one({"fullName": name}):
            return 200
        else:
            return "Person not Found", 404


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


def empty_database():
    PersonModel.objects().delete()


def create_test_user():
        personSchema = PersonSchema()
        p, errors = personSchema.load({"firstname": "ted",
                                       "lastname": "bear",
                                       "employeenumber": "1",
                                       "address": "23 blodsfsdf"})
        p.save()
        return p


def create_test_users():
        peopleSchema = PersonSchema(many=True)
        p, errors = peopleSchema.load([{"firstname": "ted",
                                        "lastname": "bear",
                                        "employeenumber": "1",
                                        "address": "23 blodsfsdf"},
                                       {"firstname": "bob",
                                        "lastname": "holmes",
                                        "employeenumber": "2",
                                        "address": "77 verulam road"}])
        PersonModel.objects.insert(p)
        return p
