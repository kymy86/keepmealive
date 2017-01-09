from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required, current_identity
from keepmealive.api.models import User
from keepmealive.extensions import jwt

api = Blueprint('api', __name__, url_prefix='/api')

def authenticate(username, password):
    user, authenticated = User.authenticate(username, password)
    if user and authenticated:
        return user
    else:
        return False

def identity(payload):
    user_id = payload['identity']
    user = User.get_by_id(user_id)
    if user is None:
        return False
    else:
        return user

jwt.authentication_handler(authenticate)
jwt.identity_handler(identity)


@api.route('/', methods=['GET'])
def index():
    return jsonify(msg='Hello world')

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(msg='Halo Halo')

@api.route('/freeforall', methods=['GET'])
def freeforall():
    return jsonify(msg='Hello world')



    