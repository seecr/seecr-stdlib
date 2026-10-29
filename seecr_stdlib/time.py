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

from datetime import datetime, timedelta, timezone
from dateutil import tz
from uuid import UUID

tz_utc = timezone.utc


def now_utc():
    return datetime.now(tz=tz_utc)


def now_local():
    return datetime.now(tz=tz.tzlocal())


def datetime_as_float(dt):
    return dt.timestamp()


def isoformat_as_datetime_utc(isoformat, timezone=None):
    dt = datetime.fromisoformat(isoformat)
    tzinfo = tz_utc
    if timezone:
        tzinfo = tz.gettz(timezone) or tz_utc
    dt = dt.replace(tzinfo=tzinfo)
    return dt.astimezone(tz=tz_utc)


def timestamp_local_to_utc(t):
    local_time = datetime.fromtimestamp(t, tz.tzlocal())
    utc_time = datetime_local_to_utc(local_time)
    return datetime_as_float(utc_time)


def datetime_local_to_utc(dt):
    return dt.replace(tzinfo=tz.tzlocal()).astimezone(tz=tz_utc)


def datetime_utc_to_local(dt):
    return dt.replace(tzinfo=tz_utc).astimezone(tz=tz.tzlocal())


def uuid_as_datetime_utc(uuid):
    tz_unaware = datetime(1582, 10, 15) + timedelta(microseconds=UUID(uuid).time // 10)

    return tz_unaware.replace(tzinfo=tz_utc)


def float_as_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=tz_utc)
