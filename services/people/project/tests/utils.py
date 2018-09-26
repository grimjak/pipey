import json
from functools import wraps

from project.api.people import PersonModel, \
                                PersonSchema


def empty_database():
    PersonModel.objects().delete()


def create_test_user(username="tb",
                     firstname="ted",
                     lastname="bear",
                     address="23 blodstaf",
                     password="greaterthaneight",
                     active=True,
                     admin=False):
        personSchema = PersonSchema()
        p, errors = personSchema.load({"username": username,
                                       "firstname": firstname,
                                       "lastname": lastname,
                                       "employeenumber": "1",
                                       "address": address,
                                       "password": password,
                                       "active": active,
                                       "admin": admin})
        p.save()
        return p


def create_test_users():
    result = []
    result.append(create_test_user(username='tb'))
    result.append(create_test_user(username='bh'))
    return result


def login(admin=False, active=True):
    def _login(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            create_test_user(username='test',
                             password='test',
                             active=active,
                             admin=admin)
            client = args[0].client
            with client:
                resp_login = client.post(
                    '/auth/login',
                    data=json.dumps({
                        'username': 'test',
                        'password': 'test'
                    }),
                    content_type='application/json'
                )
                token = json.loads(resp_login.data.decode())['auth_token']
            return f(token, *args, **kwargs)
        return decorated_function
    return _login
