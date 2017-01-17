import os
import datetime
from keepmealive.utils import make_dir, INSTANCE_FOLDER_PATH

class BaseConfig(object):
    """ Default configuration """

    PROJECT = "keepmealive"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret key'
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')

class DefaultConfig(BaseConfig):
    """ If nothing else is defined, use these configs"""

    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{username}:{password}@{server_name}:{port}/{db_name}'.format(
        username=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        server_name=os.environ['POSTGRES_ADDR'],
        port=os.environ['POSTGRES_PORT'],
        db_name=os.environ['POSTGRES_DB']
    )
    JWT_EXPIRATION_DELTA = datetime.timedelta(3600)

class TestConfig(BaseConfig):

    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    #@Todo
    #SQLALCHEMY_DATABASE_URI

