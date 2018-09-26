from flask import current_app


from project import db
from project import bcrypt
import datetime
import jwt


class PersonModel(db.Document):
    username = db.StringField(required=True, unique=True)
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    employeenumber = db.IntField()
    address = db.StringField()
    startdate = db.DateTimeField()
    active = db.BooleanField(default=True)
    password = db.StringField()
    admin = db.BooleanField(default=False, required=True)

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
                'sub': str(user_id)
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
