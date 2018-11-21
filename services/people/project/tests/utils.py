import json
from functools import wraps

from project.api.model import PersonModel, PersonSchema, \
                              SkillModel, SkillSchema


def empty_database():
    PersonModel.objects().delete()
    SkillModel.objects().delete()


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


def create_test_skill(name="lighting",
                      level="junior",
                      description="shot lighting"):
    skillSchema = SkillSchema()
    s, errors = skillSchema.load({"name": name,
                                  "level": level,
                                  "description": description})
    s.save()
    return s

def create_test_skills():
    result = []
    result.append(create_test_skill(name='lighting'))
    result.append(create_test_skill(name='comp'))
    return result

def create_test_user_with_skills():
    result = create_test_user()
    skills = create_test_skills()
    result.skills = [skills[0].id,skills[1].id]
    result.save()
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
