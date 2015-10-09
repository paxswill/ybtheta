from __future__ import absolute_import

from flask import Flask

from . import base
from .database import db

def create_app(config=None, **kwargs):
    app = Flask('ybtheta')
    db.init_app(app)
    app.register_blueprint(base.blueprint)
    return app
