from __future__ import absolute_import

from flask import Blueprint, render_template

from .models import Article


blueprint = Blueprint('article', 'ybtheta.article', template_folder='templates')


@blueprint.route('/')
def list_articles():
    articles = Article.query.all()
    return render_template('list_articles.html', articles=articles)


@blueprint.route('/<int:article_id>/')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article)
