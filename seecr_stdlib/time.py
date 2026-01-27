from datetime import datetime, timezone


def utc_now():
    return datetime.now(tz=timezone.utc)


def datetime_as_float(dt):
    return float(dt.strftime("%s"))
