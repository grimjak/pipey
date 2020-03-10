from flask_restful import Resource
from flask import request

from webargs.flaskparser import use_args
from marshmallow import fields

from project.api.model import PersonModel, PersonSchema
from project.api.model import SkillModel, SkillSchema
from project.api.utils import authenticate
from project import app

personSchema = PersonSchema()
peopleSchema = PersonSchema(many=True)

skillSchema = SkillSchema()
skillsSchema = SkillSchema(many=True)


class Person(Resource):

    def get(self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        result = personSchema.dump(data)

        if result.errors:
            return result.errors, 404  # need a test for this
        return result.data, 200

    @authenticate
    def put(resp, self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        app.logger.info("updating user: %s",request.get_json())
        new = personSchema.update(data, request.get_json())
        if new.errors:
            return new.errors, 400  # need a test for this, try bad json?
        new.data.save()
        result = personSchema.dump(new.data)
        return result.data, 200

    @authenticate
    def delete(resp, self, _id):
        data = PersonModel.objects.get_or_404(id=_id)
        data.delete()
        return 200

class People(Resource):
    #add a flag to enable response for UI, for now just filter all responses accordingly cause that's all we're using this endpoint for
    #should this be an API gateway anyway?
    @use_args(PersonSchema(exclude=["_links"]))
    @use_args({"page":fields.Int(missing=0, location="query"),
               "page_size":fields.Int(missing=10, location="query"),
               "search_term":fields.String(missing="", location="query")})
    def get(self,args, args2):       
        filter = PersonSchema(exclude=["_links"]).dump(args).data
        skip = args2['page'] * args2['page_size']
        search_term = args2['search_term']

        if filter: data = PersonModel.objects(**filter).limit(args2['page_size']).skip(skip)
        elif search_term != "" : data = PersonModel.objects.search_text(search_term).limit(args2['page_size']).skip(skip)
        else: data = PersonModel.objects().limit(args2['page_size']).skip(skip)
        
        #filtereddata = data.exclude('password','skills','avatar')
        filteredPeopleSchema = PersonSchema(many=True,exclude=('password','_links'))
        return filteredPeopleSchema.dump(data).data, 200

    @authenticate
    def post(resp, self):
        jsonrequest = request.get_json()
        result = PersonSchema().load(jsonrequest)
        if result.errors:
            print (result.errors)
            app.logger.warn(result.errors)
            return result.errors, 400
        if not resp['admin']:
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
        return PersonSchema().dump(result.data).data, 201

class PeopleTypes(Resource):

    def get(self):
        result = {}
        for k,v in PersonModel._fields.items() :
            result[k] = type(v).__name__
        return result, 200

class Skill(Resource):

    def get(self, _id):
        data = SkillModel.objects.get_or_404(id=_id)
        result = skillSchema.dump(data)

        if result.errors:
            return result.errors
        return result.data, 200

    @authenticate
    def put(resp, self, _id):
        data = SkillModel.objects.get_or_404(id=_id)
        new = skillSchema.update(data, request.get_json())
        if new.errors:
            return new.errors, 400  # need a test for this, try bad json?
        new.data.save()
        result = skillSchema.dump(new.data)
        return result.data, 200

    @authenticate
    def delete(resp, self, _id):
        data = SkillModel.objects.get_or_404(id=_id)
        data.delete()
        return 200

class Skills(Resource):
    
    @authenticate
    def post(resp, self):
        jsonrequest = request.get_json()
        result = SkillSchema().load(jsonrequest)

        if result.errors:
            return result.errors, 400

        if not resp['admin']:
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
        return SkillSchema().dump(result.data).data, 201

    def get(self):
        data = skillsSchema.dump(SkillModel.objects()).data
        return data, 200

class Ping(Resource):
    def get(self):
        return {'status': 'success', 'message': 'pong!'}, 200
