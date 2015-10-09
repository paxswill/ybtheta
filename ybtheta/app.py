from __future__ import absolute_import

from flask import Flask
from flask.ext import sqlalchemy as flask_sqlalchemy
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from . import base


db = flask_sqlalchemy.SQLAlchemy()
# Patch Flask-SQLAlchemy to use a custom Metadata instance with a naming scheme
# for constraints.
def _patch_metadata():
    naming_convention = {
        'fk': ('fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'
                '_%(referred_column_0_name)s'),
        'pk': 'pk_%(table_name)s',
        'ix': 'ix_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
    }
    metadata = MetaData(naming_convention=naming_convention)
    base = declarative_base(cls=flask_sqlalchemy.Model, name='Model',
                            metaclass=flask_sqlalchemy._BoundDeclarativeMeta,
                            metadata=metadata)
    base.query = flask_sqlalchemy._QueryProperty(db)
    db.Model = base
_patch_metadata()


def create_app(config=None, **kwargs):
    app = Flask('ybtheta')
    db.init_app(app)
    app.register_blueprint(base.blueprint)
    return app
