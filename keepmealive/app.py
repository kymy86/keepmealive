from flask import Flask
from flask_script import Manager
from flask_migrate import MigrateCommand
from keepmealive.config import DefaultConfig
from keepmealive.utils import INSTANCE_FOLDER_PATH
from keepmealive.extensions import db, jwt, migrate


__all__ = ['create_app', 'create_migration']


def init_app(config=None, app_name=None):
    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, config)
    return app

def create_app(config=None, app_name=None):

    app = init_app(config, app_name)
    configure_logging(app)
    configure_hook(app)
    configure_blueprints(app)
    configure_extensions(app)
    return app

def create_migration(config=None, app_name=None):

    app = init_app(config, app_name)
    configure_extensions(app, True)
    configure_migration(app)
    return app

def configure_app(app, config=None):
    """ Configuring application"""
    app.config.from_object(DefaultConfig)
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

def configure_blueprints(app):
    """ configure Flask Blueprints"""
    from keepmealive.api import api
    app.register_blueprint(api)

def configure_extensions(app, migration=False):
    """ configure flask sqlalchemy"""
    db.init_app(app)
    if not migration:
        jwt.init_app(app)

def configure_logging(app):
    """ Configure file logging"""

    if app.debug or app.testing:
        return

    import logging
    import os

    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))

    app.logger.addHandler(info_file_handler)

def configure_hook(app):

    @app.before_request
    def before_request():
        pass

def configure_migration(app):
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    @manager.command
    def drop_all():
        import keepmealive.api.models
        db.drop_all()

    @manager.command
    def create_all():
        import keepmealive.api.models
        db.create_all()

    manager.run()


