import os
import codecs

from markdown import markdown
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('placeholder.html', name='home')

@app.route('/about')
def about():
    mdown_html = markdown_file('content/about.mdown')
    return render_template('safe_content.html', name='about', content=mdown_html)

@app.route('/rush')
def rush():
    return render_template('placeholder.html', name='rush')

@app.route('/brothers')
def brothers():
    return render_template('placeholder.html', name='brothers')

@app.route('/activities')
def activities():
    return render_template('placeholder.html', name='activities')

@app.route('/contact')
def contact():
    return render_template('placeholder.html', name='contact')

def markdown_file(path, relative=True):
    if relative:
        script_dir = os.path.dirname(__file__)
        real_path = os.path.join(script_dir, path)
    else:
        real_path = path
    md_file = codecs.open(real_path, mode='r', encoding='utf-8')
    md_text = md_file.read()
    return markdown(md_text, output_format='html5', safe_mode='escape')


if __name__ == '__main__':
    app.debug = True
    app.run()
