from flask import request, Blueprint, current_app
from flask_restful import Resource, abort, Api
from flask_mongoengine import DoesNotExist
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import ValidationError
import jwt

from model import UserModel, UserSchema

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)
user_schema = UserSchema()


class Login(Resource):
    def post(self):
        if not request.is_json:
            abort(400, message='Missing JSON in request')

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            abort(400, message='Missing username parameter')
        if not password:
            abort(400, message='Missing password parameter')

        try:
            user = UserModel.objects.get(username=username)
        except DoesNotExist:
            abort(401, message='Wrong username')

        if not check_password_hash(user.password, password):
            abort(401, message='Wrong password')

        identity = {
            'username': user.username,
            'role': user.role,
        }

        jwt_token = jwt.encode(
            identity,
            current_app.secret_key,
            algorithm='HS256',
        )
        return {'jwt_token': jwt_token.decode()}, 200


class Register(Resource):
    def post(self):
        json_input = request.get_json()
        try:
            data = user_schema.load(json_input)
        except ValidationError as err:
            abort(422, errors=err.messages)

        try:
            UserModel.objects.get(username=data['username'])
            abort(
                400,
                errors=f"user {data['username']} is already registered.",
            )
        except DoesNotExist:
            pass

        user = UserModel(
            username=data['username'],
            password=generate_password_hash(data['password']),
            role=data['role'],
        )
        user.save()
        message = f"Successfully created user: {user.username}"

        data = user_schema.dump(user)
        data['message'] = message
        return data, 201


auth_api.add_resource(Login, '/login')
auth_api.add_resource(Register, '/register')
