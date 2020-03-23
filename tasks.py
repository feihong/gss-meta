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
      # print('%r' % row['Debit'])
      value = None
      try:
        value = Decimal(row['Debit'])
      except:
        value = Decimal(0)

      if category == 'Income':
        value = Decimal(row['Credit'])

      categories[category] += value

  data = sorted(categories.items(), key=lambda x: x[1], reverse=True)
  table = AsciiTable(data, 'Totals by category')
  table.inner_heading_row_border = False
  print(table.table)
