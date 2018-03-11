from datetime import datetime
from collections import defaultdict
from decimal import Decimal

from invoke import task
from spreadsheet import open_spreadsheet


CURRENT_YEAR = str(datetime.today().year)


@task
def checking_account(ctx, year=CURRENT_YEAR):
    """
    Print business checking account metrics.

    """
    ss = open_spreadsheet('Business Checking Account Activity')
    worksheet = ss.worksheet(year)

    debit = credit = revenue = Decimal(0.0)
    categories = defaultdict(Decimal)

    rows = worksheet.get_all_records()
    for row in rows:
        category = row['Category']
        if category == 'Revenue':
            revenue += get_decimal(row['Credit'])
        else:
            categories[category] += get_decimal(row['Debit'])

        debit += get_decimal(row['Debit'])
        credit += get_decimal(row['Credit'])

    print('Total debit: {:0.2f}'.format(debit))
    print('Total credit: {:0.2f}'.format(credit))
    print('Total revenue: {:0.2f}'.format(revenue))

    separator()

    print('Categories:')
    items = sorted(categories.items(), key=lambda x: -x[1])
    for k, v in items:
        if v > 0:
            print('- {}: {:0.2f}'.format(k, v))



@task
def home_office(ctx, year=CURRENT_YEAR):
    ss = open_spreadsheet('Home Office %s' % year)

    # Calculate utilities & rent amounts
    rent_fields = ['hoa assessments', 'homeowners insurance', 'gas', 'electric',
        'mortgage']
    worksheet = ss.worksheet('Monthly fees')
    assessment_total = 0
    insurance_total = 0
    utilities_total = 0

    print('Office rent by month:')
    for row in worksheet.get_all_records():
        total = sum(get_decimal(v) for k, v in row.items() if k in rent_fields)
        rent = total / 4
        print('{month}: {rent:0.2f} (total is {total:0.2f})'.format(
            month=row['Month'], total=total, rent=rent))

        assessment_total += get_decimal(row['hoa assessments'])
        insurance_total += get_decimal(row['homeowners insurance'])
        utilities_total += get_decimal(row['electric']) + get_decimal(row['gas'])

    separator()

    print('Total paid for hoa assessments: {:0.2f}'.format(assessment_total))
    print('Total paid for homeowners insurance: {:0.2f}'.format(insurance_total))
    print('Total paid for utilities (gas & electric): {:0.2f}'.format(utilities_total))

    separator()

    # Calculate repairs & maintenance total
    worksheet = ss.worksheet('Repairs & maintenance')
    total = 0
    for row in worksheet.get_all_records():
        total += get_decimal(row['Price'])

    print('Repairs & maintenance total: {:0.2f}'.format(total))


def get_decimal(text):
    if text.strip() == '':
        return 0
    text = text.replace(',', '')
    if text.startswith('-$'):
        return Decimal(text[2:])
    elif text.startswith('$'):
        return Decimal(text[1:])
    else:
        return Decimal(text)


def separator():
    print('='*75)
