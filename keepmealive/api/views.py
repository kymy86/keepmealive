from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required, current_identity
import keepmealive.authentication

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return jsonify(msg='Hello world')

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(msg='Halo Halo')



    