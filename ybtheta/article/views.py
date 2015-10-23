from __future__ import absolute_import

from flask import Blueprint, render_template, redirect, url_for
from flask.ext.wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length

from .models import Article
from ..database import db
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


class ArticleForm(Form):

    title = StringField(label=u"Title",
            validators=[InputRequired(), Length(min=1, max=100)])

    text = TextAreaField(description=u"""You can use Markdown style markup,
    like Reddit for making links and styling the text.""")

    # These are pretty simply just placeholders/dummy fields. The actual
    # widgets are manually coded buttons in the template.
    save = SubmitField(label=u"Save")

    preview = SubmitField(label=u"Preview")

    delete = SubmitField(label=u"Delete")


@blueprint.route('/create/', methods=['GET', 'POST'])
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        if form.preview.data:
            return render_template('preview.html', form=form)
        article = Article(form.title.data, form.text.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('.show_article', article_id=article.id))
    return render_template('edit.html', form=form)


@blueprint.route('/<int:article_id>/edit/', methods=['GET', 'POST'])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        if form.preview.data:
            return render_template('preview.html', form=form, edit=True)
        if form.delete.data:
            db.session.delete(article)
            db.session.commit()
            return redirect(url_for('.list_articles'))
        else:
            db.session.commit()
            return redirect(url_for('.show_article', article_id=article_id))
    return render_template('edit.html', form=form, edit=True)
