from flask import Flask
from flask.ext.mako import MakoTemplates, render_template
import spreadsheet
import calculation


app = Flask(__name__)
MakoTemplates(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home-office/')
def home_office():
    return render_template('home-office.html')


@app.route('/home-office/rent/')
def rent():
    ss = spreadsheet.open_spreadsheet('Home Office')
    worksheet = ss.worksheet('2015')
    rows = calculation.get_monthly_rent(worksheet.get_all_records())
    return render_template('rent.html', rows=rows)


if __name__ == '__main__':
    app.debug = True
    app.run()
