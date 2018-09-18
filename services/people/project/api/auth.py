from flask import Blueprint, request
from flask_restful import Resource, Api

from project.api.people import PersonModel, PersonSchema
from project import bcrypt

from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

personSchema = PersonSchema()


class Login(Resource):
    def post(self):
        post_data = request.get_json()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        if not post_data:
            return response_object, 400
        username = post_data.get('username')
        password = post_data.get('password')
        # now get the data from the db
        data = PersonModel.objects.get_or_404(username=username)

        if bcrypt.check_password_hash(data.password, password):
            auth_token = data.encode_auth_token(data.id)
            if auth_token:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                response_object['auth_token'] = auth_token.decode()
                return response_object, 200
        else:
            response_object['message'] = 'Password does not match'
            return response_object, 404


class Logout(Resource):
    def get(self):
        auth_header = request.headers.get('Authorisation')
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token'
        }
        if auth_header:
            auth_token = auth_header.split(' ')[1]
            resp = PersonModel.decode_auth_token(auth_token)
            if ObjectId.is_valid(resp):
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged out.'
                return response_object, 200
            else:
                response_object['message'] = resp
                return response_object, 401
        else:
            return response_object, 403


class Status(Resource):
    def get(self):
        auth_header = request.headers.get('Authorisation')
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token'
        }
        if auth_header:
            auth_token = auth_header.split(' ')[1]
            resp = PersonModel.decode_auth_token(auth_token)
            if ObjectId.is_valid(resp):
                user = PersonModel.objects.get_or_404(id=ObjectId(resp))
                response_object['status'] = 'success'
                response_object['message'] = 'SuSuccess.'
                print(user)
                response_object['data'] = personSchema.dump(user).data
                return response_object, 200
            else:
                response_object['message'] = resp
                return response_object, 401
        else:
            return response_object, 401


api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Status, "/status", endpoint="status")
