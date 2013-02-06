from flask import g, session, redirect, flash, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, Required

from ybtheta import app, db, oid


# Flask hooks
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
    flash(u'Success!', 'success')
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

