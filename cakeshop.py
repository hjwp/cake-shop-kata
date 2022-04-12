from datetime import date, timedelta
from typing import Iterator

SMALL_LEAD_TIME = timedelta(days=1)  
BIG_LEAD_TIME = timedelta(days=2)
MARCO_WORK_DAYS = [0, 1, 2, 3, 4]
SANDRO_WORK_DAYS = [1, 2, 3, 4, 5]

def _days_from(d: date) -> Iterator[date]:
    yield d
    yield from _days_from(d + timedelta(days=1))

def _marco_days_from(d: date) -> Iterator[date]:
    if d.weekday() in MARCO_WORK_DAYS:
        yield d
    yield from _marco_days_from(d + timedelta(days=1))

def _sandro_days_from(d: date) -> Iterator[date]:
    if d.weekday() in SANDRO_WORK_DAYS:
        yield d
    yield from _sandro_days_from(d + timedelta(days=1))



def _marco_lead_time(start_date: date, cake_size: str) -> date:
    marco_days = _marco_days_from(start_date)
    if cake_size == "small":
        next(marco_days)
        return next(marco_days)
    if cake_size == "big":
        next(marco_days)
        next(marco_days)
        return next(marco_days)

def _marco_start_date(order_date: date, time: str) -> date:
    next_workday = next(_marco_days_from(order_date))
    if next_workday != order_date:
        return next_workday
    if time == "morning":
        return order_date
    else:
        return order_date + timedelta(days=1)

def _sandro_frosting_lead_time(start_date: date) -> date:
    sandro_days = _sandro_days_from(start_date)
    next(sandro_days)
    next(sandro_days)
    return next(sandro_days)


def calculate_delivery_date(cake_size: str, custom_frosting: bool, order_date: date, time: str) -> date:
    start_date = _marco_start_date(order_date, time)
    marco_ready = _marco_lead_time(start_date, cake_size)
    if custom_frosting:
        return _sandro_frosting_lead_time(marco_ready)
    else:
        return marco_ready
