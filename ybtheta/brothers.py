from flask import render_template
from ybtheta import app, db


@app.route('/brothers')
def brothers():
    return render_template('placeholder.html', name='brothers')

