from flask import Blueprint, render_template, abort, flash, redirect, \
        url_for, request
from flask.ext import login as flask_login
from flask.ext.oauthlib.client import OAuth, OAuthException
from flask.ext.wtf import Form
import jwt
from sqlalchemy.orm.exc import NoResultFound
from wtforms.fields import SubmitField

from .models import Identity, GoogleIdentity
from ..database import db


blueprint = Blueprint('auth', 'ybtheta.auth', template_folder='templates')


login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'


oauth = OAuth()


google = None


@login_manager.user_loader
def load_user(user_id):
    return Identity.query.get(int(user_id))


@blueprint.record_once
def setup_google(state):
    # Doing setup in here so we have access to an app (used to grab
    # configuration secrets)
    global google
    google = oauth.remote_app(
        'Google',
        app_key='GOOGLE',
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        request_token_params={
            'scope': ' '.join(
                ['https://www.googleapis.com/auth/userinfo.profile',
                 'https://www.googleapis.com/auth/userinfo.email',]),
        }
    )
    @google.tokengetter
    def get_google_token():
        return (flask_login.current_user.token, '')


class LoginForm(Form):

    google = SubmitField()


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.google.data:
            return google.authorize(
                    callback=url_for('.login_google', _external=True))
    return render_template('login.html', title=u"Login", form=form)


@blueprint.route('/login/google')
def login_google():
    resp = google.authorized_response()
    # this is silly, not raising an exception but returning it
    if resp is None or isinstance(resp, OAuthException):
        if resp is None:
            reason = request.args['error_reason']
            description = request.args['error_description']
        else:
            reason = resp.data[u'error']
            description = resp.message
        flash(u"Access Denied: {} ({})".format(description, reason), "error")
        return redirect(url_for('.login'))
    # We can skip verification because this token came directly from Google
    # over an encrypted and authenticated connection.
    decoded_token = jwt.decode(resp['id_token'], verify=False)
    # Lookup or create a GoogleIdentity using the id token's "sub" value. This
    # value is guaranteed (by Google) to maintain constant for a user across
    # email changes (and I guess other things).
    try:
        identity = GoogleIdentity.query.filter_by(
                google_id=decoded_token['sub']).one()
    except NoResultFound:
        identity = GoogleIdentity(google_id=decoded_token['sub'])
        db.session.add(identity)
    # Save the access token so the token getter can access it
    identity.token = resp['access_token']
    flask_login.login_user(identity)
    # Get a few bits of extra information
    userinfo = google.get('userinfo').data
    identity.name = userinfo[u'name']
    identity.email = userinfo[u'email']
    db.session.commit()
    return redirect('/')


@blueprint.route('/logout/')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/')
