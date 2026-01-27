## begin license ##
#
# Seecr StdLib provides convenient tools for Seecr developers
#
# Copyright (C) 2026 Seecr (Seek You Too B.V.) http://seecr.nl
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

from .time import utc_now, datetime_as_float


def test_utc_now():
    now = utc_now()
    assert now.tzname() == "UTC"


def test_datetime_as_float():
    now = utc_now()
    assert datetime_as_float(now) == float(now.strftime("%s"))
