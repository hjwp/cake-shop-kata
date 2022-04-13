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
            order_date=a_tuesday,
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
        calculate_delivery_date(
            cake_size="big",
            order_date=a_tuesday,
        )
        == three_days_later
    )


def test_orders_in_morning_start_same_day():
    """
    * If Marco receives a cake order in the morning (ie, before 12pm) he starts on the same day.
    """
    a_tuesday = a_day(TUESDAY)
    next_day = a_tuesday + timedelta(days=1)
    assert (
        calculate_delivery_date(
            order_date=a_tuesday,
            time="morning",
        )
        == next_day
    )


def test_orders_in_afternoon_on_fri_start_monday():
    """
    (possible edge case)
    """
    a_friday = a_day(FRIDAY)
    next_tuesday = a_friday + timedelta(days=4)
    assert next_tuesday.weekday() == TUESDAY  # sanity-check
    assert (
        calculate_delivery_date(
            order_date=a_friday,
            time="afternoon",
        )
        == next_tuesday
    )


def test_order_received_outside_marco_working_days():
    """
    * Marco works from Monday-Friday,
    """
    sunday = a_day(SUNDAY)
    tuesday = sunday + timedelta(days=2)
    assert tuesday.weekday() == TUESDAY  # sanity-check
    assert (
        calculate_delivery_date(
            order_date=sunday,
            time="morning",
        )
        == tuesday
    )

    saturday = a_day(SATURDAY)
    assert (
        calculate_delivery_date(
            order_date=saturday,
            time="morning",
        )
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
        calculate_delivery_date(
            order_date=friday,
            time="morning",
        )
        == monday
    )
    tuesday = friday + timedelta(days=4)
    assert (
        calculate_delivery_date(
            order_date=friday,
        )
        == tuesday
    )


def test_sandro_frosting_in_working_days():
    """
    * Custom frosting adds 2 days extra lead time. You can only frost a baked cake.
    """
    a_monday = a_day(MONDAY)
    four_days_later = a_monday + timedelta(days=4)
    assert four_days_later.weekday() == FRIDAY  # sanity-check
    assert (
        calculate_delivery_date(
            custom_frosting=True,
            order_date=a_monday,
        )
        == four_days_later
    )


def test_sandro_frosting_on_saturday():
    """
    * Custom frosting adds 2 days extra lead time. You can only frost a baked cake.
    * and Sandro works from Tuesday-Saturday.
    """
    a_tuesday = a_day(TUESDAY)
    four_days_later = a_tuesday + timedelta(days=4)
    assert four_days_later.weekday() == SATURDAY  # sanity-check
    assert (
        calculate_delivery_date(
            custom_frosting=True,
            order_date=a_tuesday,
        )
        == four_days_later
    )


def test_sandro_frosting_over_nonwork_days():
    """
    * Custom frosting adds 2 days extra lead time. You can only frost a baked cake.
    * and Sandro works from Tuesday-Saturday.
    eg if cake ordered on a wednesday,
    marco will be finished on friday,
    so sandro will need saturday and tuesday
    """
    a_wednesday = a_day(WEDNESDAY)
    following_tuesday = a_wednesday + timedelta(days=6)
    assert following_tuesday.weekday() == TUESDAY  # sanity-check
    assert (
        calculate_delivery_date(
            custom_frosting=True,
            order_date=a_wednesday,
        )
        == following_tuesday
    )


def test_sandro_frosting_handover_on_sandro_nonwork_day():
    """
    * Custom frosting adds 2 days extra lead time. You can only frost a baked cake.
    * Marco works from Monday-Friday,
    * and Sandro works from Tuesday-Saturday.
    -> if marco finishes on a monday, sandro still only starts on tuesday
    (just double-checking but this should "just work")
    """
    a_friday = a_day(FRIDAY)
    following_wednesday = a_friday + timedelta(days=5)
    assert following_wednesday.weekday() == WEDNESDAY  # sanity-check
    assert (
        calculate_delivery_date(
            cake_size="small",
            custom_frosting=True,
            order_date=a_friday,
            time="morning",
        )
        == following_wednesday
    )


def test_marco_does_nuts_simple():
    """
    * The shop can decorate cakes with nuts.
    Unfortunately, Sandro is allergic to nuts, so Marco does this job.
    Decorating a cake with nuts takes 1 extra day,
    ->
    """
    a_monday = a_day(MONDAY)
    three_days_later = a_monday + timedelta(days=3)
    assert (
        calculate_delivery_date(
            order_date=a_monday,
            nuts=True,
        )
        == three_days_later
    )


def test_marco_does_nuts_marco_holidays():
    """
    We can check it was marco by checking his holidays impact the d date
    """
    a_wednesday = a_day(WEDNESDAY)
    next_monday = a_wednesday + timedelta(days=5)
    assert (
        calculate_delivery_date(
            order_date=a_wednesday,
            nuts=True,
        )
        == next_monday
    )


def test_nuts_happen_after_frosting():
    """
    Decorating a cake with nuts takes 1 extra day,
    and has to happen after any frosting has finished.
    """
    a_monday = a_day(MONDAY)  # morning
    # marco will do cake by tuesday
    # sandro will do frosting weds + thu
    # marco will add nuts on friday
    five_days_later = a_monday + timedelta(days=4)
    assert five_days_later.weekday() == FRIDAY  # sanity-check
    assert (
        calculate_delivery_date(
            order_date=a_monday,
            time="morning",
            custom_frosting=True,
            nuts=True,
        )
        == five_days_later
    )


def test_marco_does_nuts_sandro_handover_on_marco_nonwork_day():
    """
    also confirms marco is the one doing nuts
    and that we calculate his working days right
    """
    a_tuesday = a_day(TUESDAY)  # afternoon
    # marco will do cake by thu
    # sandro will do frosting fri + sat
    # marco will add nuts on monday
    next_monday = a_tuesday + timedelta(days=6)
    assert next_monday.weekday() == MONDAY  # sanity-check
    assert (
        calculate_delivery_date(
            order_date=a_tuesday,
            time="afternoon",
            custom_frosting=True,
            nuts=True,
        )
        == next_monday
    )


def test_fancy_box_noop():
    """
    * The shop can gift-wrap cakes in fancy boxes. Fancy boxes have a lead time of 3 days.
    Boxes can arrive while the friends are working on the cake,
    -> if the cake will take 4 days anyway, the box will have no effect
    """
    a_monday = a_day(MONDAY)
    four_days_later = a_monday + timedelta(days=4)
    assert four_days_later.weekday() == FRIDAY  # sanity-check
    assert (
        calculate_delivery_date(
            custom_frosting=True,
            order_date=a_monday,
            fancy_box=True,
        )
        == four_days_later
    )


def test_fancy_box_adds_to_marco_time():
    """
    order monday morning
    cake would be ready tuesday
    but box takes 3 days, so it's thursday
    """
    a_monday = a_day(MONDAY)
    the_thursday = a_monday + timedelta(days=3)
    assert the_thursday.weekday() == THURSDAY  # sanity-check
    assert (
        calculate_delivery_date(
            order_date=a_monday,
            time="morning",
            fancy_box=True,
        )
        == the_thursday
    )


def test_fancy_box_adds_to_sandro_time():
    """
    order monday morning
    baking would be done tuesday, cake would be ready wednesday
    but box takes 3 days, so it's thursday
    """
    a_monday = a_day(MONDAY)
    the_thursday = a_monday + timedelta(days=3)
    assert the_thursday.weekday() == THURSDAY  # sanity-check
    assert (
        calculate_delivery_date(
            order_date=a_monday,
            time="morning",
            custom_frosting=True,
            fancy_box=True,
        )
        == the_thursday
    )


def test_christmas_marco():
    """
    * The shop closes for Christmas from the 23rd of December and is open again on the 2nd of January.
    Cakes that would be complete in that period will be unable to start production until re-opening.
    Fancy boxes will continue to arrive throughout the festive period.
    """
    dec_22 = date(2022, 12, 22)
    assert dec_22.weekday() not in (SATURDAY, SUNDAY)  # sanity-check
    jan_2 = date(2023, 1, 2)
    assert jan_2.weekday() not in (SATURDAY, SUNDAY)  # sanity check
    assert (
        calculate_delivery_date(
            order_date=dec_22,
            time="morning",
        )
        == jan_2
    )


def test_christmas_sandro():
    """
    marco finishes just before xmas
    """
    dec_22 = date(2022, 12, 22)
    assert dec_22.weekday() not in (SATURDAY, SUNDAY)  # sanity-check
    jan_2 = date(2023, 1, 2)
    assert jan_2.weekday() not in (SATURDAY, SUNDAY)  # sanity check

    dec_20 = dec_22 - timedelta(days=2)
    jan_4 = jan_2 + timedelta(days=2)
    assert (
        calculate_delivery_date(
            order_date=dec_20,
            time="afternoon",
            custom_frosting=True,
        )
        == jan_4
    )
