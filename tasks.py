import csv
from collections import defaultdict
from decimal import Decimal

from invoke import task
from terminaltables import AsciiTable


@task
def business(ctx):
  """
  Print business checking account metrics.

  """
  categories = defaultdict(Decimal)

  with open('business.csv') as fp:
    reader = csv.DictReader(fp)
    for row in reader:
      category = row['Category']
      value = None
      try:
        value = Decimal(row['Debit'])
      except:
        value = Decimal(0)

      if category == 'Income':
        value = Decimal(row['Credit'])

      categories[category] += value

  data = sorted(categories.items(), key=lambda x: x[0])
  table = AsciiTable(data, 'Totals by category')
  table.inner_heading_row_border = False
  print(table.table)


@task
def oot(ctx):
  """
  Print breakdown of out-of-town expenses for each trip

  """
  trips = defaultdict(lambda: defaultdict(Decimal))

  with open('business.csv') as fp:
    reader = csv.DictReader(fp)
    for row in reader:
      category = row['Category']
      if not category.startswith('OOT:'):
        continue

      trip = trips[row['OOT code']]

      value = None
      try:
        value = Decimal(row['Debit'])
      except:
        value = Decimal(0)

      trip[category] += value

  for code, trip in trips.items():
    data = trip.items()
    table = AsciiTable(data, code)
    table.inner_heading_row_border = False
    print(table.table)
