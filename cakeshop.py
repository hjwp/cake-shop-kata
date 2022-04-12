from datetime import date, timedelta

SMALL_LEAD_TIME = timedelta(days=1)  
BIG_LEAD_TIME = timedelta(days=2)


def calculate_delivery_date(cake_size: str, order_date: date, time: str) -> date:
    if time == "morning":
        start_date = order_date
    else:
        start_date = order_date + timedelta(days=1)

    if cake_size == "small":
        return start_date + SMALL_LEAD_TIME
    else:
        return start_date + BIG_LEAD_TIME
