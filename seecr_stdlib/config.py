## begin license ##
#
# Seecr StdLib provides convenient tools for Seecr developers
#
# Copyright (C) 2026 Seecr (Seek You Too B.V.) https://seecr.nl
#
# This file is part of "Seecr Standard Library"
#
# "Seecr Standard Library" is released under the MIT License.
# See the LICENSE file for the full license text.
#
# SPDX-License-Identifier: MIT
#
## end license ##

import json
import pathlib
import warnings


def expand_dict(obj, context):
    if isinstance(obj, dict):
        return {k: expand_dict(v, context) for k, v in obj.items()}
    if isinstance(obj, list):
        return [expand_dict(v, context) for v in obj]
    if isinstance(obj, str):
        return obj.format_map(context)
    return obj  # ints, None, etc. unchanged


class Config:
    @classmethod
    def read(cls, path, **kwargs):
        return cls(json.loads(path.read_text()), **kwargs)

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

    def expand_with(self, values_dict):
        return Config(expand_dict(self._config, values_dict))
