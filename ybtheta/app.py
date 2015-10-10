from __future__ import absolute_import

from flask import Flask
import six

from . import base, article
from .database import db
from .admin_view import admin


def create_app(config=None, **kwargs):
    app = Flask('ybtheta', **kwargs)
    # Configure the app using the passed in config
    if isinstance(config, dict):
        app.config.update(config)
    elif isinstance(config, six.string_types):
        if config.endswith(('.txt.', '.py', '.cfg')):
            app.config.from_pyfile(config)
        else:
            app.config.from_object(config)
    # initialize the various plugins and extensions
    db.init_app(app)
    admin.init_app(app)
    # Add the blueprints
    app.register_blueprint(base.blueprint)
    app.register_blueprint(article.blueprint, url_prefix='/articles')
    return app
