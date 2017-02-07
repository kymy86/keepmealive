from sqlalchemy import Column, desc 
from sqlalchemy.orm import backref, validates

from werkzeug.security import generate_password_hash, check_password_hash

from keepmealive.extensions import db
from keepmealive.utils import get_current_time

class User(db.Model):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(225), nullable=False, unique=True)
    email = Column(db.String(225), nullable=False, unique=True)
    create_at = Column(db.DateTime, nullable=False, default=get_current_time())
    update_at = Column(db.DateTime)
    _password = Column('password', db.String(200), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self._set_password(password)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter(User.email == username).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
        