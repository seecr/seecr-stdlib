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

import json
import pathlib
import warnings


class Config:
    @classmethod
    def read(cls, path, required=None):
        return cls(json.loads(path.read_text()), required=required)

    def __init__(self, config_file, required=None):
        if isinstance(config_file, pathlib.Path):
            warnings.warn(
                "Specifying path in __init__ is deprecated, use Config.read(path, ..) instead",
                DeprecationWarning,
                stacklevel=2,
            )
            config = json.loads(config_file.read_text())
        elif isinstance(config_file, dict):
            config = config_file
        else:
            raise ValueError("config_file should be either a Path or dict")

        self._config = config
        if required is not None:
            for key in required:
                if self.get(key) is None:
                    raise RuntimeError(f"Mandatory key '{key}' not found in config")

    def get(self, key, default=None):
        value = self._config
        for k in key.split("."):
            if k.isdigit() and isinstance(value, list):
                try:
                    value = value[int(k)]
                except IndexError:
                    return default
            else:
                value = value.get(k)
            if value is None:
                return default
        return value
