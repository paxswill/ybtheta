import os
import codecs
import sys

from markdown import markdown
from flask import Flask, render_template, g, session, redirect, flash, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import openid
from flask.ext.wtf import Form, TextField, Required

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg')
oid = openid.OpenID(app)
# Database configuration
db = SQLAlchemy(app)


# Flask Routes
@app.route('/')
def home():
    return render_template('placeholder.html', name='home')

@app.route('/about')
def about():
    mdown_html = markdown_file('content/about.mdown')
    return render_template('safe_content.html', name='about', content=mdown_html)

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


# Login stuff
@app.before_request
def lookup_openid():
    g.user = None
    if 'openid' in session:
        openid = OpenID.query.filter_by(openid=session['openid']).first()
        if openid is not None:
            g.user = openid.user


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'fullname',
                'nickname'])
    return render_template('login.html', name="login", next=oid.get_next_url(),
            error=oid.fetch_error(), form=LoginForm())


@oid.after_login
def process_login(resp):
    session['openid'] = resp.identity_url
    openid = OpenID.query.filter_by(openid=resp.identity_url).first()
    flash(u'Success!')
    if openid is not None:
        flash(u'Logged in')
        g.user = openid.user
        return redirect(oid.get_next_url())
    return home()


# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, nickname, email):
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        return "<User {}>".format(self.username)


class OpenID(db.Model):
    __tablename__ = 'openids'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(250), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('openids',
        lazy='dynamic'))


# WTForms
class LoginForm(Form):
    openid = TextField('OpenID URL', validators=[Required()])


# Misc functions
def markdown_file(path, relative=True):
    if relative:
        script_dir = os.path.dirname(__file__)
        real_path = os.path.join(script_dir, path)
    else:
        real_path = path
    md_file = codecs.open(real_path, mode='r', encoding='utf-8')
    md_text = md_file.read()
    return markdown(md_text, output_format='html5', safe_mode='escape')


if __name__ == '__main__':
    app.run()
