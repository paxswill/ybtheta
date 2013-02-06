import os

from flask import (Flask, render_template, g, session, redirect, flash, request,
send_from_directory)
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import openid

from ybtheta.markdown_page import markdown_page

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg')
oid = openid.OpenID(app)
# Database configuration
db = SQLAlchemy(app)

from ybtheta import accounts

# Register Blueprints
app.register_blueprint(markdown_page)

# Flask Routes
@app.route('/')
def home():
    return render_template('placeholder.html', name='home')

@app.route('/rush')
def rush():
    return render_template('placeholder.html', name='rush')

@app.route('/brothers')
def brothers():
    return render_template('placeholder.html', name='brothers')

@app.route('/activities')
def activities():
    return render_template('placeholder.html', name='activities')

@app.route('/contact')
def contact():
    return render_template('placeholder.html', name='contact')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root.path, 'static', 'img'),
            'favicon.png', mimetype='image/png')


# Misc functions

if __name__ == '__main__':
    app.run()
