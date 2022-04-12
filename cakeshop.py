from datetime import date, timedelta
from typing import Iterator

SMALL_LEAD_TIME = timedelta(days=1)  
BIG_LEAD_TIME = timedelta(days=2)
MARCO_WORK_DAYS = [0, 1, 2, 3, 4]

def _days_from(d: date) -> Iterator[date]:
    yield d
    yield from _days_from(d + timedelta(days=1))


def _marco_start_date(order_date: date, time: str) -> date:
    next_workday = next(d for d in _days_from(order_date) if d.weekday() in MARCO_WORK_DAYS)
    if next_workday != order_date:
        return next_workday
    if time == "morning":
        return order_date
    else:
        return order_date + timedelta(days=1)

def calculate_delivery_date(cake_size: str, order_date: date, time: str) -> date:
    start_date = _marco_start_date(order_date, time)

    if cake_size == "small":
        return start_date + SMALL_LEAD_TIME
    else:
        return start_date + BIG_LEAD_TIME
