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
    # import ipdb; ipdb.set_trace()
    years = (w.title for w in ss.worksheets())
    print(years)
    return render_template('rent.html', years=years)


@app.route('/home-office/rent/<year>/')
def rent_for(year):
    ss = spreadsheet.open_spreadsheet('Home Office')
    worksheet = ss.worksheet(year)
    rows = calculation.get_monthly_rent(worksheet.get_all_records())
    return render_template(
        'rent-for-year.html',
        year_title='Monthly Rent for %s' % year, 
        rows=rows)


if __name__ == '__main__':
    app.debug = True
    app.run()
