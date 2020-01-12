from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields, validate


db = MongoEngine()

ROLES = ['admin', 'user']


class UserModel(db.Document):
    username = db.StringField(primary_key=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
    )
    role = fields.Str(
        required=True,
        validate=[validate.OneOf(ROLES)],
    )
