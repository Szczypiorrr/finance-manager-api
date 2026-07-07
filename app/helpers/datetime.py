from datetime import datetime

def current_month():
    """Returns current month number."""
    return datetime.now().month


def current_year():
    """Returns current year."""
    return datetime.now().year


def current_datetime():
    """Returns current date and time."""
    return datetime.now()

def month_range(month, year):
    """Returns start and end datetime for given month."""
    start = datetime(year, month, 1)

    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    return start, end