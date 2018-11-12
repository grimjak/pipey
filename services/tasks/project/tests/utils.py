import json
from functools import wraps

from project.api.model import TaskModel, TaskSchema


def empty_database():
    TaskModel.objects().delete()


def create_test_task(name="light seq1",
                     description="lighting for sequence 1",
                     duration=1,
                     status=True):
        taskSchema = TaskSchema()
        p, errors = taskSchema.load({"name": name,
                                       "description": description,
                                       "duration": duration,
                                       "status": status
                                       })
        p.save()
        return p


def create_test_tasks():
    result = []
    result.append(create_test_task(name='light seq1'))
    result.append(create_test_task(name='light seq2'))
    return result

# need to mock the login so this can work without the people service
# login needs to create a token which will pass authentication
def login(admin=False, active=True):
    def _login(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = json.loads(resp_login.data.decode())['auth_token']
            return f(token, *args, **kwargs)
        return decorated_function
    return _login
