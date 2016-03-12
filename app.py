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
    ss = spreadsheet.open_spreadsheet('Home Office')
    years = (w.title for w in ss.worksheets())
    return render_template('home-office.html', years=years)


@app.route('/home-office/<year>/')
def home_office_for(year):
    ss = spreadsheet.open_spreadsheet('Home Office')
    worksheet = ss.worksheet(year)
    rows = worksheet.get_all_records()
    month_rows = calculation.get_monthly_rent(rows)
    category_rows = calculation.get_category_numbers(rows)
    # import ipdb; ipdb.set_trace()
    return render_template(
        'home-office-for-year.html',
        year=year,
        # title='Home Office Numbers for %s' % year,
        month_rows=month_rows,
        category_rows=category_rows)


if __name__ == '__main__':
    app.debug = True
    app.run()
