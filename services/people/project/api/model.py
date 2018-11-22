from flask import current_app


from project import db, app
from project import bcrypt
import datetime
import jwt

import flask_marshmallow as fm
import marshmallow_mongoengine as ma
mm = fm.Marshmallow(app)




class SkillModel(db.Document):
    name = db.StringField(required=True)
    level = db.StringField(required=True, unique_with="name")  # make name and level unique together
    description = db.StringField()

class Address(db.EmbeddedDocument):
    street_address = db.StringField()
    city = db.StringField()
    postal_code = db.StringField()
    country = db.StringField()

class PersonModel(db.Document):
    username = db.StringField(required=True, unique=True)
    title = db.StringField()
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    email = db.EmailField()
    gender = db.StringField()
    job_title = db.StringField()
    department = db.StringField()
    avatar = db.URLField()
    employeenumber = db.IntField()
    address = db.EmbeddedDocumentField(Address)
    startdate = db.DateTimeField()
    active = db.BooleanField(default=True)
    password = db.StringField()
    admin = db.BooleanField(default=False, required=True)
    skills = db.ListField(db.ReferenceField(SkillModel),default=[])

    def clean(self):
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
                'sub': {'id': str(user_id),
                        'admin': self.admin,
                        'active': self.active}
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


class PersonSchema(ma.ModelSchema):
    class Meta:
        model = PersonModel
    _links = mm.Hyperlinks({'uri': mm.UrlFor('people.person', _id='<id>')})


class SkillSchema(ma.ModelSchema):
    class Meta:
        model = SkillModel
    _links = mm.Hyperlinks({'uri': mm.UrlFor('people.skill', _id='<id>')})
