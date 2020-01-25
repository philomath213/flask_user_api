from flask import request, Blueprint, current_app
from flask_restful import Resource, abort, Api
import jwt

from secret import FLAG

flag_bp = Blueprint('flag', __name__)
flag_api = Api(flag_bp)


class Flag(Resource):
    def get(self):
        header = request.headers.get('Authorization', None)
        if header is None:
            abort(400, message='Authorization header is missing')

        _, token = header.split()
        try:
            identity = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms='HS256'
            )
        except jwt.DecodeError:
            abort(400, message='Token is not valid.')

        username = identity['username']
        role = identity['role']

        if role == 'admin':
            msg = f'welcome admin {username}, here is your flag {FLAG}'
        else:
            msg = f'welcome {username}, you need to be admin to get the flag'

        return {'message': msg}, 200


flag_api.add_resource(Flag, '/')
