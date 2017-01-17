from keepmealive.api.models import User
from keepmealive.extensions import jwt

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
