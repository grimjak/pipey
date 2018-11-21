from functools import wraps

from flask import request
from bson.objectid import ObjectId

from project.api.model import PersonModel


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response_object, 403
        auth_token = auth_header.split(' ')[1]
        resp = PersonModel.decode_auth_token(auth_token)
        if not isinstance(resp,dict):
            response_object['message'] = resp
            return response_object, 401
        if not ObjectId.is_valid(resp['id']):
            response_object['message'] = resp['id']
            return response_object, 401
        #user = PersonModel.objects.get_or_404(id=ObjectId(resp['id']))
        if not resp['active']:
            return response_object, 401
        return f(resp, *args, **kwargs)
    return decorated_function


def is_admin(user_id):
    user = PersonModel.objects.get_or_404(id=user_id)
    return user.admin
