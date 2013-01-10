from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('placeholder.html', name='home')

@app.route('/about')
def about():
    return render_template('placeholder.html', name='about')

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

if __name__ == '__main__':
    app.debug = True
    app.run()
