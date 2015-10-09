from flask import Blueprint, render_template


blueprint = Blueprint('base', 'ybthete')


@blueprint.route('/')
def index():
    return render_template('index.html', title='Index')

