from .time import utc_now, datetime_as_float


def test_utc_now():
    now = utc_now()
    assert now.tzname() == "UTC"


def test_datetime_as_float():
    now = utc_now()
    assert datetime_as_float(now) == float(now.strftime("%s"))
