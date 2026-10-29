## begin license ##
#
# Seecr StdLib provides convenient tools for Seecr developers
#
# Copyright (C) 2025-2026 Seecr (Seek You Too B.V.) https://seecr.nl
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

import pytest

from seecr_stdlib.format import format_date
from datetime import datetime, timezone, date


@pytest.mark.parametrize(
    "date,expected",
    [
        (None, ""),
        (datetime(2024, 6, 15, 13, 45, 30), "2024-06-15"),
        (datetime(2023, 1, 1), "2023-01-01"),
        (datetime(2022, 12, 31, 23, 59, 59), "2022-12-31"),
        (date(2022, 12, 31), "2022-12-31"),
    ],
)
def test_format_date(date, expected):
    assert format_date(date) == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (None, ""),
        (datetime(2024, 6, 15, 13, 45, 30), "15-06-2024"),
        (datetime(2023, 1, 1), "01-01-2023"),
        (date(2023, 1, 1), "01-01-2023"),
        (datetime(2022, 12, 31, 23, 59, 59), "31-12-2022"),
    ],
)
def test_format_date_nl(date, expected):
    assert format_date(date, "nl") == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (None, ""),
        (datetime(2024, 6, 15, 13, 45, 30), "15-06-2024 13:45"),
        (datetime(2023, 1, 1), "01-01-2023 00:00"),
        (datetime(2022, 12, 31, 23, 59, 59), "31-12-2022 23:59"),
        (
            datetime(2026, 7, 13, 13, 40, 48, 727405, tzinfo=timezone.utc),
            "13-07-2026 15:40",
        ),
    ],
)
def test_format_date_nl_tijd(date, expected):
    assert format_date(date, "nl_tijd") == expected
    assert format_date(date, "nl-t") == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (None, ""),
        (datetime(2024, 6, 15, 13, 45, 30), "zaterdag 15 juni 2024"),
        (datetime(2023, 1, 1), "zondag 1 januari 2023"),
        (date(2023, 1, 1), "zondag 1 januari 2023"),
        (datetime(2022, 12, 31, 23, 59, 59), "zaterdag 31 december 2022"),
        (datetime(2025, 12, 9), "dinsdag 9 december 2025"),
    ],
)
def test_format_date_nllang(date, expected):
    assert format_date(date, "nllang") == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (None, ""),
        (datetime(2024, 6, 15, 13, 45, 30), "za 15 jun 2024"),
        (datetime(2023, 1, 1), "zo 1 jan 2023"),
        (datetime(2022, 12, 31, 23, 59, 59), "za 31 dec 2022"),
        (datetime(2025, 12, 9), "di 9 dec 2025"),
    ],
)
def test_format_date_nlkort(date, expected):
    assert format_date(date, "nlkort") == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (None, ""),
        (datetime(2024, 6, 15, 13, 45, 30), "zaterdag 15 juni 2024 13:45"),
        (datetime(2023, 1, 1, 0, 0), "zondag 1 januari 2023 00:00"),
    ],
)
def test_format_date_nllang_tijd(date, expected):
    assert format_date(date, "nllang_tijd") == expected
    assert format_date(date, "nl-lt") == expected


@pytest.mark.parametrize(
    "string_date,style,expected",
    [
        ("", "iso", ""),
        ("2024-06-15", "iso", "2024-06-15"),
        ("invalid-date", "iso", "invalid-date"),
        ("2024-06-15", "nllang", "zaterdag 15 juni 2024"),
        ("2023-01-01", "nlkort", "zo 1 jan 2023"),
        ("gewoon tekst", "nlkort", "gewoon tekst"),
        ("2023-01-01", "unknown-style", "2023-01-01"),
        ("2026-07-30 09:53:55", "nllang_tijd", "donderdag 30 juli 2026 09:53"),
    ],
)
def test_format_date_with_string_input(string_date, style, expected):
    assert format_date(string_date, style) == expected


@pytest.mark.parametrize(
    "nr,style,expected",
    [
        (0, "iso", "1970-01-01"),
        (0, "nllang", "donderdag 1 januari 1970"),
        (0, "nlkort", "do 1 jan 1970"),
        (1789395323, "iso", "2026-09-14"),
        (1789395323, "nllang_tijd", "maandag 14 september 2026 16:15"),
        (1789395323, "zulu", "2026-09-14T14:15:23Z"),
    ],
)
def test_format_date_from_timestamp(nr, style, expected):
    assert format_date(nr, style) == expected
