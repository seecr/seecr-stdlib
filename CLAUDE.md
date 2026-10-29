# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`seecr-stdlib` is a small Python (>=3.11) utility library shared across Seecr projects: `Dict` (attribute-access dict), `first`, `Config` (dotted-path JSON config access), `time` helpers (UTC/local conversion), and `format.format_date` (date formatting styles, usable as a Jinja filter). Runtime dependencies are only `python-dateutil` and `pytest`.

## Commands

A virtualenv lives in `env/`.

```sh
env/bin/python -m pytest                                          # all tests
env/bin/python -m pytest seecr_stdlib/config_test.py              # one file
env/bin/python -m pytest seecr_stdlib/dict_test.py::test_dict     # one test
```

Formatting follows black (isort is configured with `profile = "black"`).

## Conventions

- Tests sit next to the module they test as `<module>_test.py` (not in a separate `tests/` dir), written as plain pytest functions, often with `@pytest.mark.parametrize`.
- Every source file starts with the MIT `## begin license ## ... ## end license ##` header (template data in `doc/license.conf`). Copy it into new files and keep the copyright year(s) current.
- Versions come from git tags via `setuptools_scm` (tags like `0.6.3`); `seecr_stdlib/_version.py` is generated and git-ignored — don't edit it.
- Pushing a version tag to GitHub publishes that version to PyPI and makes a GitHub release (`.github/workflows/publish.yml`), and PyPI never accepts a version twice. Don't push tags unless asked.
- Only `Dict` and `first` are re-exported from the package root; other modules are imported by path (`seecr_stdlib.config`, `seecr_stdlib.time`, `seecr_stdlib.format`).
- `format_date` dispatches through the `styles` dict in `format/date.py`; add new styles (and their short aliases like `nl-t`) there. Unknown styles fall back to ISO date. Dutch styles convert aware datetimes to `Europe/Amsterdam` when showing time.
- `Config(path)` is deprecated in favour of `Config.read(path, ...)`; `Config.get` resolves dotted keys including list indices (`"a.values.0"`), returning `default` for missing/`None` values.
- `Dict` deliberately never lets keys shadow dict methods and refuses attribute-assignment of method names; preserve that behaviour.
