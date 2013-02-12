from flask import (g, session, redirect, flash, request, render_template,
url_for, abort)

from ybtheta import app, db, oid
from ybtheta.models import User, OpenID
from ybtheta.forms import LoginForm, CreateAccountForm


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
    if openid is not None:
        flash(u'Logged in')
        g.user = openid.user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_account', next=oid.get_next_url(),
        real_name=resp.fullname, screen_name=resp.nickname, email=resp.email))


@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        real_name = request.form['real_name']
        screen_name = request.form['screen_name']
        email = request.form['email']
        if not real_name:
            flash(u'You need to provide a name.', 'error')
        elif not screen_name:
            flash(u'You need to provide a screen name', 'error')
        elif not email or '@' not in email:
            flash(u'You need to provide a valid email address.', 'error')
        else:
            flash(u'Account created', 'success')
            new_user = User(real_name, screen_name, email)
            new_id = OpenID(session['openid'], new_user)
            db.session.add(new_user)
            db.session.commit()
            return redirect(oid.get_next_url())
    return render_template('create_account.html', next_url=oid.get_next_url(),
            form=CreateAccountForm())


@app.route('/account/<screen_name>')
def show_account(screen_name):
    return abort(404)


@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'Logged out.', 'info')
    return redirect(oid.get_next_url())

