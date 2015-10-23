from __future__ import absolute_import

from flask import Blueprint, render_template

from .models import Article
from ..page_rename import view_renamed


blueprint = Blueprint('article', 'ybtheta.article', template_folder='templates')


@blueprint.route('/')
def list_articles():
    articles = Article.query.all()
    return render_template('list_articles.html', articles=articles)


@blueprint.route('/<int:article_id>/')
def show_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_article(article)


@view_renamed(Article)
def render_article(article):
    return render_template('article.html', article=article)
