from collections import defaultdict

from invoke import task
from spreadsheet import open_spreadsheet


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


def get_float(text):
    if text.strip() == '':
        return 0
    text = text.replace(',', '')
    if text.startswith('-$'):
        return float(text[2:])
    else:
        return float(text[1:])
