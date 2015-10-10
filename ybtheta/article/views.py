from __future__ import absolute_import

from flask import Blueprint, render_template, abort

from .models import Article


blueprint = Blueprint('auth', 'ybtheta.article', template_folder='templates')


@blueprint.route('/<int:article_id>/')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article)
