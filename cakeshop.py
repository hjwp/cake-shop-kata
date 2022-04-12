from datetime import date, timedelta


def calculate_delivery_date(cake_size: str, order_date: date, time: str) -> date:
    return order_date + timedelta(days=2)
