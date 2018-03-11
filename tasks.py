from datetime import datetime
from collections import defaultdict
from decimal import Decimal

from invoke import task
from terminaltables import AsciiTable
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

    data = [
        ('Total debit', debit),
        ('Total credit', credit),
        ('Total revenue', revenue)
    ]
    table = AsciiTable(data, 'Summary')
    table.inner_heading_row_border = False
    print(table.table)


    data = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    table = AsciiTable(data, 'Debits by category')
    table.inner_heading_row_border = False
    print(table.table)


@task
def home_office(ctx, year=CURRENT_YEAR):
    """
    Show home office expenses.

    """
    ss = open_spreadsheet('Home Office %s' % year)

    worksheet = ss.worksheet('Monthly fees')
    categories = defaultdict(Decimal)

    for row in worksheet.get_all_records():
        categories['hoa assessments'] += get_decimal(row['hoa assessments'])
        categories['homeowners insurance'] += get_decimal(row['homeowners insurance'])
        categories['mortgage'] += get_decimal(row['mortgage'])
        categories['utilities (gas & electric)'] += \
            get_decimal(row['electric']) + get_decimal(row['gas'])

    data = [(k.capitalize(), v) for k, v in categories.items()]

    data += [
        (f'Total for {year}', sum(categories.values())),
        (f'Office rent for {year}', sum(categories.values()) / 4),
        ('Repairs & maintenance', get_rm_total(ss)),
    ]
    table = AsciiTable(data, 'Home office')
    table.inner_heading_row_border = False
    print(table.table)


def get_rm_total(ss):
    "Calculate repairs & maintenance total"
    worksheet = ss.worksheet('Repairs & maintenance')
    total = 0
    for row in worksheet.get_all_records():
        total += get_decimal(row['Price'])
    return total


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
