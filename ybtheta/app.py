from __future__ import absolute_import

from flask import Flask, escape
import markdown
import six

from . import article, page_rename
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
    app.register_blueprint(article.blueprint, url_prefix='/articles')
    app.register_blueprint(page_rename.blueprint)
    # Configure Jinja a little bit
    app.jinja_env.filters['markdown'] = markdown_filter
    return app


def markdown_filter(markup_text):
    escaped = escape(markup_text)
    formatted = markdown.markdown(escaped,
                                  extensions=[
                                      'markdown.extensions.tables',
                                      'markdown.extensions.smart_strong',
                                      'markdown.extensions.smarty',
                                      ],
                                  output_format='html5')
    return formatted
