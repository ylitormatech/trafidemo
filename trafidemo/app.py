# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from trafidemo import public, user, api, angular1demo
from trafidemo.assets import assets
from trafidemo.extensions import bcrypt, cache, db, debug_toolbar, csrf_protect, login_manager, migrate
from trafidemo.settings import ProdConfig
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
#from flask_triangle import Triangle


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    # triangle helps Jinja2 to differentiate normal notations e.g. {{ municipal }} from angular {{ municipal|angular }}
    #Triangle(app)
    app.config.from_object(config_object)
    mongo = PyMongo(app, config_prefix='MONGO')
    register_extensions(app)
    register_blueprints(app)
    register_apis(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(angular1demo.views.blueprint)
    return None

def register_apis(app):
    """ Register Apis. """
    app.register_blueprint(api.trafi.blueprint)

    # api.add_resource(Trafi, '/api/trafi/')
    # api.add_resource(Trafi, '/api/trafi/<string:municipal>/', endpoint="municipal")


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
