from flask import Flask
from flask.ext.mako import MakoTemplates, render_template


app = Flask(__name__)
MakoTemplates(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home-office')
def home_office():
    return render_template('home-office.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
