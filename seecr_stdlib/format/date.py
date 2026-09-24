## begin license ##
#
# Seecr StdLib provides convenient tools for Seecr developers
#
# Copyright (C) 2025-2026 Seecr (Seek You Too B.V.) http://seecr.nl
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

__all__ = ["format_date"]

import zoneinfo
from functools import partial

from seecr_stdlib.time import float_as_datetime
from dateutil import parser
import datetime

NL_TZ = zoneinfo.ZoneInfo("Europe/Amsterdam")


def _iso_style(date):
    return date.isoformat().split("T")[0]


def _zulu_style(date):
    return date.isoformat(timespec="seconds").replace("+00:00", "Z")


def _nl_style(date, time=False, tzinfo=NL_TZ):
    if isinstance(date, datetime.datetime) and time:
        date = date.astimezone(tzinfo)

    fmt = "%d-%m-%Y"
    if time:
        fmt += " %H:%M"
    return date.strftime(fmt)


days_nl = list(
    zip(
        (
            "maandag",
            "dinsdag",
            "woensdag",
            "donderdag",
            "vrijdag",
            "zaterdag",
            "zondag",
        ),
        ("ma", "di", "wo", "do", "vr", "za", "zo"),
    )
)
months_nl = list(
    zip(
        (
            "januari",
            "februari",
            "maart",
            "april",
            "mei",
            "juni",
            "juli",
            "augustus",
            "september",
            "oktober",
            "november",
            "december",
        ),
        (
            "jan",
            "feb",
            "mrt",
            "apr",
            "mei",
            "jun",
            "jul",
            "aug",
            "sep",
            "okt",
            "nov",
            "dec",
        ),
    )
)


def _nllang_style(date, pos, time=False, tzinfo=NL_TZ):
    if isinstance(date, datetime.datetime) and time:
        date = date.astimezone(tzinfo)

    day_name = days_nl[date.weekday()][pos]
    month_name = months_nl[date.month - 1][pos]
    result = f"{day_name} {date.day} {month_name} {date.year}"
    if time:
        result += f" {date.hour:02}:{date.minute:02}"
    return result


styles = {
    "nl": _nl_style,
    "nl_tijd": partial(_nl_style, time=True),
    "nllang": partial(_nllang_style, pos=0),
    "nlkort": partial(_nllang_style, pos=1),
    "nllang_tijd": partial(_nllang_style, pos=0, time=True),
    "nlkort_tijd": partial(_nllang_style, pos=1, time=True),
    "zulu": _zulu_style,
}
styles["nl-t"] = styles["nl_tijd"]
styles["nl-l"] = styles["nllang"]
styles["nl-k"] = styles["nlkort"]
styles["nl-lt"] = styles["nllang_tijd"]
styles["nl-kt"] = styles["nlkort_tijd"]


def format_date(date, style="iso"):
    """Uniformly format a date according to the given style.

    To use as jinja filter, add 'format_date' to the filters dict in your jinja environment.
    Usage:
        {{ date | format_date('nl') }}
    """
    if date is None:
        return ""
    if isinstance(date, str):
        try:
            date = parser.isoparse(date)
        except ValueError:
            return date
    if isinstance(date, (int, float)):
        date = float_as_datetime(date)
    fn = styles.get(style, _iso_style)
    return fn(date)
