from __future__ import absolute_import

from flask import Blueprint, render_template
from sqlalchemy.orm.exc import NoResultFound

from .models import RenamedPage


blueprint = Blueprint('page_rename', 'ybtheta.page_rename',
        template_folder='templates')


registered_views = {}


def view_renamed(model):
    def register_wrap(func):
        registered_views[model.__name__] = func
        return func
    return register_wrap


@blueprint.route('/', defaults={'path': 'index'})
@blueprint.route('/<path:path>/')
def lookup(path):
    # using first as opposed to one as there's a first_or_404 convenience
    # function, and path already has a unique constraint
    try:
        model = RenamedPage.query.filter_by(renamed_path=path).one()
    except NoResultFound:
        if path == 'index':
            return render_template('index.html')
    else:
        return registered_views[model.type_](model)
