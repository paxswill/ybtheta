from __future__ import absolute_import

import datetime as dt
import markdown
from flask import escape
from flask.ext.admin.contrib.sqla import ModelView

from ..database import db
from ..util import AutoID, AutoName, Timestamped, utc
from ..admin_view import admin


class Article(db.Model, AutoID, AutoName, Timestamped):

    title = db.Column(db.String(100, convert_unicode=True), nullable=False)

    text = db.Column(db.UnicodeText(), nullable=False)

    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text

    def edit(self, new_text):
        if new_text != self.text:
            self.text = new_text
            self.timestamp = dt.datetime.now(utc)

    def markdown(self):
        escaped = escape(self.text)
        formatted = markdown.markdown(escaped,
                                      extensions=[
                                          'markdown.extensions.tables',
                                          'markdown.extensions.smart_strong',
                                          'markdown.extensions.smarty',
                                          ],
                                      output_format='html5')
        return formatted


article_admin = ModelView(Article, db.session, endpoint='article_admin')
admin.add_view(article_admin)
