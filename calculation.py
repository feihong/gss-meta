from collections import defaultdict
import arrow


def get_monthly_rent(rows):
    months = defaultdict(float)

    # Calculate month totals.
    for row in rows:
        dt = arrow.get(row['Date'], 'M/D/YYYY')
        key = dt.format('YYYY-MM')  # key that represents the month
        months[key] += row['Amount']

    items = list(months.items())
    items.sort(key=lambda x: x[0])  # sort by month
    for k, v in items:
        dt = arrow.get(k, 'YYYY-MM')
        yield dict(date=dt, total=v, rent=v/4)


def get_category_numbers(rows):
    categories = defaultdict(float)

    for row in rows:
        categories[row['Category']] += row['Amount']

    items = list(categories.items())
    items.sort(key=lambda x: -x[1])  # sort by descending value

    for k, v in items:
        yield dict(category=k, total=v)
