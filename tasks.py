from datetime import datetime
from collections import defaultdict

from invoke import task
from spreadsheet import open_spreadsheet


CURRENT_YEAR = datetime.today().year


@task
def checking_account(ctx):
    ss = open_spreadsheet('Business Checking Account Activity')
    worksheet = ss.worksheet('2016')

    totals = defaultdict(float)
    revenue = 0.0

    rows = worksheet.get_all_records()
    for row in rows:
        if row['Category'] == 'Revenue':
            revenue += get_float(row['Credit'])
        totals['Debit'] += get_float(row['Debit'])
        totals['Credit'] += get_float(row['Credit'])

    print('Total debit: {:0.2f}'.format(totals['Debit']))
    print('Total credit: {:0.2f}'.format(totals['Credit']))
    print('Revenue: {:0.2f}'.format(revenue))


@task
def home_office(ctx, year=None):
    year = CURRENT_YEAR if year is None else year
    ss = open_spreadsheet('Home Office %s' % year)

    # Calculate utilities & rent amounts
    rent_fields = ['hoa assessments', 'homeowners insurance', 'gas', 'electric',
        'mortgage']
    worksheet = ss.worksheet('Monthly fees')
    assessment_total = 0
    insurance_total = 0

    print('Office rent by month:')
    for row in worksheet.get_all_records():
        total = sum(get_float(v) for k, v in row.items() if k in rent_fields)
        print('{month}: {total:0.2f} (rent is {rent:0.2f})'.format(
            month=row['Month'], total=total, rent=total/4))

        assessment_total += get_float(row['hoa assessments'])
        insurance_total += get_float(row['homeowners insurance'])

    separator()
    
    print('Total paid for hoa assessments:', assessment_total)
    print('Total paid for homeowners insurance:', insurance_total)

    separator()

    # Calculate repairs & maintenance total
    worksheet = ss.worksheet('Repairs & maintenance')
    total = 0
    for row in worksheet.get_all_records():
        total += get_float(row['Price'])

    print('Repairs & maintenance total: {:0.2f}'.format(total))

def get_float(text):
    if text.strip() == '':
        return 0
    text = text.replace(',', '')
    if text.startswith('-$'):
        return float(text[2:])
    elif text.startswith('$'):
        return float(text[1:])
    else:
        return float(text)


def separator():
    print('='*75)
