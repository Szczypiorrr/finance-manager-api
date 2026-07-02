from datetime import datetime

def current_month():
    return datetime.now().month


def current_year():
    return datetime.now().year


def current_datetime():
    return datetime.now()

def month_range(month, year):
    start = datetime(year, month, 1)

    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    return start, end