## begin license ##
#
# Seecr StdLib provides convenient tools for Seecr developers
#
# Copyright (C) 2026 Seecr (Seek You Too B.V.) https://seecr.nl
#
# This file is part of "Seecr Standard Library"
#
# "Seecr Standard Library" is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "Seecr Standard Library" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Seecr Standard Library".  If not, see <http://www.gnu.org/licenses/>.
#
## end license ##

from .time import (
    now_utc,
    now_local,
    datetime_as_float,
    float_as_datetime,
    isoformat_as_datetime_utc,
)
from datetime import timezone, datetime

from dateutil import tz
import pytest


def test_now_utc():
    now = now_utc()
    assert now.strftime("%Z") == "UTC"
    assert now.tzinfo == timezone.utc


def test_now_local():
    now = now_local()
    assert isinstance(now.tzinfo, tz.tzlocal)
    assert now.utcoffset() == datetime.now().astimezone().utcoffset()


def test_datetime_as_float():
    t = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert t.timestamp() == 0.0
    assert datetime_as_float(t) == 0.0


def test_timestamp_as_datetime():
    now = now_utc()
    now_dt = float_as_datetime(datetime_as_float(now))
    assert now_dt == now


@pytest.mark.parametrize(
    "isoformat, timezone_str, expected_timestamp",
    [
        ("2026-09-16 10:47:54", "Europe/Amsterdam", 1789548474.0),
        ("2026-09-16 05:47:54", "America/Sao_Paulo", 1789548474.0),
        ("2026-09-16 08:47:54", "UTC", 1789548474.0),
        ("1970-01-01 12:00", "UTC", 43200.0),
        ("1970-01-01 12:00", "Europe/Amsterdam", 43200.0 - 3600.0),
        ("1970-01-01 12:00", "America/Sao_Paulo", 43200.0 + 3 * 3600.0),
        ("1970-01-01 12:00", None, 43200.0),
        ("1970-01-01 12:00", "From/Nowhere", 43200.0),
    ],
)
def test_fromisoformat(isoformat, timezone_str, expected_timestamp):
    dt = isoformat_as_datetime_utc(isoformat, timezone_str)
    assert dt.timestamp() == expected_timestamp
    assert dt.tzinfo == timezone.utc


def test_isformat_as_datetime_utc_compared_to_datetime_fromisoformat():
    isoformat = "2026-09-16 10:47:54"
    dt1 = isoformat_as_datetime_utc(isoformat)
    dt2 = datetime.fromisoformat(isoformat + "+00:00")
    assert dt1.timestamp() == dt2.timestamp()
