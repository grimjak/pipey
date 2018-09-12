from flask import request, current_app
from flask_restful import Resource

import flask_marshmallow as fm
import marshmallow_mongoengine as ma

import datetime
import jwt

from project import db
from project import app
from project import bcrypt

mm = fm.Marshmallow(app)


class PersonModel(db.Document):
    username = db.StringField(required=True, unique=True)
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    employeenumber = db.IntField()
    address = db.StringField()
    startdate = db.DateTimeField()
    active = db.BooleanField(default=True)
    password = db.StringField()

    def clean(self):
        print(self.password)
        self.password = bcrypt.generate_password_hash(
            self.password,
            current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signiture expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


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

        try:
            result.data.save()
        except(ValueError) as e:
            return {'message': 'Invalid payload'}, 400
        return PersonSchema().dump(result.data).data, 201


class Ping(Resource):
    def get(self):
        return {'status': 'success', 'message': 'pong!'}, 200
