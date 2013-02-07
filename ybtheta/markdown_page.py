import os
import codecs

from markdown import markdown
from flask import Blueprint, render_template, abort

markdown_page = Blueprint('markdown_page', __name__)


@markdown_page.route('/<page>')
def render_markdown(page):
    try:
        mdown_html = markdown_file('content/{}.mdown'.format(page))
        return render_template('safe_content.html', name=page,
                content=mdown_html)
    except IOError:
        return abort(404)


def markdown_file(path, relative=True):
    if relative:
        script_dir = os.path.dirname(__file__)
        real_path = os.path.join(script_dir, path)
    else:
        real_path = path
    md_file = codecs.open(real_path, mode='r', encoding='utf-8')
    md_text = md_file.read()
    return markdown(md_text, output_format='html5', safe_mode='escape')

