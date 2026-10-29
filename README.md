# Seecr Standard Library

Small, dependency-light Python utilities shared across [Seecr](https://seecr.nl) projects.

[![Tests](https://github.com/seecr/seecr-stdlib/actions/workflows/test.yml/badge.svg)](https://github.com/seecr/seecr-stdlib/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/seecr-stdlib.svg)](https://pypi.org/project/seecr-stdlib/)

## Installation

```sh
pip install seecr-stdlib
```

Requires Python 3.11 or newer.

## What's inside

### `Dict`: attribute access for dicts

```python
from seecr_stdlib import Dict

d = Dict(answer=42)
d.answer           # 42
d.question = "?"   # same as d["question"] = "?"
```

Keys never shadow dict methods: `Dict(items=1).items` is still the method, and
assigning `d.items = 1` raises `AttributeError`.

### `first`

```python
from seecr_stdlib import first

first([1, 2, 3])   # 1
first([])          # None
```

### `Config`: dotted-path access to JSON configuration

```python
from pathlib import Path
from seecr_stdlib.config import Config

config = Config.read(Path("config.json"), required=["db.host"])
config.get("db.host")
config.get("db.ports.0")                   # list indices work too
config.get("db.user", default="postgres")  # default for missing keys

# Fill in {placeholders} in all string values
config = config.expand_with({"host": "localhost"})
```

### `seecr_stdlib.time`: timezone-aware helpers

`now_utc()`, `now_local()`, `datetime_as_float()`, `float_as_datetime()`,
`isoformat_as_datetime_utc()`, `datetime_local_to_utc()`,
`datetime_utc_to_local()`, `timestamp_local_to_utc()` and
`uuid_as_datetime_utc()` (the timestamp of a version 1 UUID).

### `format_date`: uniform date formatting

Accepts `date`/`datetime` objects, ISO 8601 strings and Unix timestamps.
Dutch styles that show time convert to `Europe/Amsterdam`.

```python
from datetime import datetime, timezone
from seecr_stdlib.format import format_date

d = datetime(2026, 10, 29, 13, 45, tzinfo=timezone.utc)
format_date(d)                   # '2026-10-29'
format_date(d, "nl")             # '29-10-2026'
format_date(d, "nl_tijd")        # '29-10-2026 14:45'
format_date(d, "nllang")         # 'donderdag 29 oktober 2026'
format_date(d, "nlkort_tijd")    # 'do 29 okt 2026 14:45'
format_date(d, "zulu")           # '2026-10-29T13:45:00Z'
```

Short aliases: `nl-t`, `nl-l`, `nl-k`, `nl-lt`, `nl-kt`. It also works as a
Jinja filter:

```python
env.filters["format_date"] = format_date
```

```jinja
{{ created | format_date('nl') }}
```

## Development

```sh
python -m venv env --prompt seecr-stdlib
source env/bin/activate
pip install -e .
pytest
```

Tests live next to the code as `<module>_test.py`.

## License

Copyright (C) 2025-2026 Seecr (Seek You Too B.V.)

Licensed under the [MIT License](https://github.com/seecr/seecr-stdlib/blob/master/LICENSE).
