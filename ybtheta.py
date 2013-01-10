from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/rush')
def rush():
    return render_template('rush.html')

@app.route('/brothers')
def brothers():
    return render_template('brothers.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
