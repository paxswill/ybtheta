from __future__ import absolute_import

import datetime as dt
from flask import escape
from flask.ext.admin.contrib.sqla import ModelView

from ..database import db
from ..util import AutoID, AutoName, Timestamped, utc
from ..page_rename import RenamedPage
from ..admin_view import admin


class Article(RenamedPage, Timestamped):

    id = db.Column(db.Integer, db.ForeignKey('renamedpage.id'),
            primary_key=True)

    title = db.Column(db.String(100, convert_unicode=True), nullable=False)

    text = db.Column(db.UnicodeText(), nullable=False)

    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text

    def edit(self, new_text):
        if new_text != self.text:
            self.text = new_text
            self.timestamp = dt.datetime.now(utc)

    def __repr__(self):
        return "Article({a.id}, {a.title})".format(a=self)


class ExcludeTypeView(ModelView):
    column_exclude_list = ['type_']
    form_excluded_columns = column_exclude_list

article_admin = ExcludeTypeView(Article, db.session, endpoint='article_admin')
admin.add_view(article_admin)
