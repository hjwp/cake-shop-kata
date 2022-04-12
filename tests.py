"""
Connascent Cakes is an artisan baker that sells custom-made cakes for delivery.
Two friends, Sandro and Marco own the shop.
Marco does all the baking, while Sandro does decorations.

Sandro and Marco want to start selling cakes online
and need you to write code that can calculate the delivery date for their cakes.

The "lead time" is the number of days that it takes to make a cake.
The delivery date is the date the cake was ordered, plus the lead time.
For example, if a cake is ordered on the 1st of the month, and has a lead time of 2 days, the delivery date is the 3rd of the month.

* Cakes are always delivered on the day they're finished. Nobody likes stale cake.

* Marco works from Monday-Friday,
* and Sandro works from Tuesday-Saturday.
* Custom frosting adds 2 days extra lead time. You can only frost a baked cake.
* The shop can gift-wrap cakes in fancy boxes. Fancy boxes have a lead time of 3 days.
  Boxes can arrive while the friends are working on the cake,
* The shop can decorate cakes with nuts.
  Unfortunately, Sandro is allergic to nuts, so Marco does this job.
  Decorating a cake with nuts takes 1 extra day, and has to happen after any frosting has finished.
* The shop closes for Christmas from the 23rd of December and is open again on the 2nd of January.
  Cakes that would be complete in that period will be unable to start production until re-opening.
  Fancy boxes will continue to arrive throughout the festive period.
"""
from datetime import date, timedelta

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

from cakeshop import calculate_delivery_date


def a_day(day_of_week: int) -> date:
    month = 2
    return next(
        d
        for day in range(1, 9)
        if (d := date(2019, month, day)).weekday() == day_of_week
    )


def test_small_cake_simple_days():
    """
    * Small cakes have a lead time of 2 days.
    """
    a_tuesday = a_day(TUESDAY)
    two_days_later = a_tuesday + timedelta(days=2)
    assert two_days_later.weekday() == THURSDAY  # sanity-check
    assert (
        calculate_delivery_date(
            cake_size="small", order_date=a_tuesday, time="afternoon"
        )
        == two_days_later
    )


def test_big_cake_simple_days():
    """
    * Big cakes have a lead time of 3 days.
    """
    a_tuesday = a_day(TUESDAY)
    three_days_later = a_tuesday + timedelta(days=3)
    assert (
        calculate_delivery_date(cake_size="big", order_date=a_tuesday, time="afternoon")
        == three_days_later
    )


def test_orders_in_morning_start_same_day():
    """
    * If Marco receives a cake order in the morning (ie, before 12pm) he starts on the same day.
    """
    a_tuesday = a_day(TUESDAY)
    next_day = a_tuesday + timedelta(days=1)
    assert (
        calculate_delivery_date(cake_size="small", order_date=a_tuesday, time="morning")
        == next_day
    )


def test_order_received_outside_marco_working_days():
    """
    * Marco works from Monday-Friday,
    """
    sunday = a_day(SUNDAY)
    tuesday = sunday + timedelta(days=2)
    assert tuesday.weekday() == TUESDAY  # sanity-check
    assert (
        calculate_delivery_date(cake_size="small", order_date=sunday, time="morning")
        == tuesday
    )

    saturday = a_day(SATURDAY)
    assert (
        calculate_delivery_date(cake_size="small", order_date=saturday, time="morning")
        == tuesday
    )


def test_lead_time_spans_marco_nonworking_days():
    """
    * Marco works from Monday-Friday,
    """
    friday = a_day(FRIDAY)
    monday = friday + timedelta(days=3)
    assert monday.weekday() == MONDAY  # sanity-check
    assert (
        calculate_delivery_date(cake_size="small", order_date=friday, time="morning")
        == monday
    )
    tuesday = friday + timedelta(days=4)
    assert (
        calculate_delivery_date(cake_size="small", order_date=friday, time="afternoon")
        == tuesday
    )
