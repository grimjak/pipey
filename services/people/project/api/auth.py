from flask import Blueprint, request
from flask_restful import Resource, Api

from project.api.people_resources import PersonSchema
from project.api.model import PersonModel
from project import bcrypt

from bson.objectid import ObjectId
from project.api.utils import authenticate

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

personSchema = PersonSchema()


class Login(Resource):
    def post(self):
        print("post")
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
        # need better error messages if no password
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
    @authenticate
    def get(resp, self):
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200


class Status(Resource):
    @authenticate
    def get(resp, self):
        user = PersonModel.objects.get_or_404(id=ObjectId(resp))
        response_object = {
            'status': 'success',
            'message': 'Success.',
            'data': personSchema.dump(user).data
        }
        print(response_object)
        return response_object, 200

# should this be centralised to keep all the endpoints in one place?
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Status, "/status", endpoint="status")
