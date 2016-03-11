"""
Source: https://github.com/google/oauth2client/issues/401

"""

YEAR = 2016

from collections import defaultdict
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import arrow


json_key = json.load(open('credentials.json'))
scopes = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes)

gc = gspread.authorize(credentials)
spreadsheet = gc.open('Home Office')
worksheet = spreadsheet.worksheet(str(YEAR))
records = worksheet.get_all_records()

print('\nBreakdown by category:\n')

categories = defaultdict(float)

for row in records:
    categories[row['Type of Bill']] += row['Amount']

for k, v in categories.items():
    print('%s => %0.2f' % (k, v))

print('\nBreakdown by month:\n')

months = defaultdict(float)

for row in records:
    dt = arrow.get(row['Date'], 'M/D/YYYY')
    key = dt.format('YYYY-MM')
    months[key] += row['Amount']

items = list(months.items())
items.sort(key=lambda x: x[0])
for k, v in items:
    dt = arrow.get(k, 'YYYY-MM')
    print('%s => %0.2f => %0.2f' % (dt.format('MMM YYYY'), v, v / 4))

print('\nTotal = %0.2f' % sum(categories.values()))
