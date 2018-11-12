from flask import current_app


from project import db, app
from project import bcrypt
import datetime
import jwt

import flask_marshmallow as fm
import marshmallow_mongoengine as ma
mm = fm.Marshmallow(app)


class TaskModel(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    duration = db.IntField()
    startdate = db.DateTimeField()
    status = db.BooleanField(default=True) #convert to enum

    # shouldnt need this on task model
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': {'id': str(user_id)}
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
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = TaskModel
    _links = mm.Hyperlinks({'uri': mm.UrlFor('tasks.task', _id='<id>')})
