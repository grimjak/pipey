from flask_restful import Resource
from flask import request

from project.api.model import TaskModel, TaskSchema
from project.api.utils import authenticate, is_admin

taskSchema = TaskSchema()
tasksSchema = TaskSchema(many=True)

class Task(Resource):

    def get(self, _id):
        data = TaskModel.objects.get_or_404(id=_id)
        result = taskSchema.dump(data)

        if result.errors:
            return result.errors, 404  # need a test for this
        return result.data, 200

    @authenticate
    def put(resp, self, _id):
        data = TaskModel.objects.get_or_404(id=_id)
        new = taskSchema.update(data, request.get_json())
        if new.errors:
            return new.errors, 400  # need a test for this, try bad json?
        new.data.save()
        result = taskSchema.dump(new.data)
        return result.data, 200

    @authenticate
    def delete(resp, self, _id):
        data = TaskModel.objects.get_or_404(id=_id)
        data.delete()
        return 200


class Tasks(Resource):
    def get(self):
        data = tasksSchema.dump(TaskModel.objects()).data
        return data, 200

    @authenticate
    def post(resp, self):
        jsonrequest = request.get_json()
        result = TaskSchema().load(jsonrequest)

        if result.errors:
            return result.errors, 400

        if not is_admin(resp):
            response_object = {
                'status': 'fail',
                'message': 'You do not have permission to do that.'
            }
            return response_object, 401
        try:
            result.data.save()
        except(ValueError) as e:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload'
            }
            return response_object, 400
        return TaskSchema().dump(result.data).data, 201


class Ping(Resource):
    def get(self):
        return {'status': 'success', 'message': 'pong!'}, 200
