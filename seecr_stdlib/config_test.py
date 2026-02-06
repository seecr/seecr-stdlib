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

from .config import Config


def test_config_get(tmp_path):
    (config_file := tmp_path / "config.json").write_text(
        json.dumps(
            {
                "root": {
                    "text": "The text",
                    "number": 42,
                    "boolean": True,
                    "values": [1, 2, 3, 4, 5],
                    "sub": {
                        "boolean": False,
                    },
                },
                "complex": {"values": [{"1": ["one"]}, {"2": "two"}]},
            }
        )
    )

    config = Config(config_file=config_file)
    assert config.get("root.text") == "The text"
    assert config.get("root.texts") is None
    assert config.get("root.texts", default="X") == "X"
    assert config.get("root.number") == 42
    assert config.get("root.boolean") is True
    assert config.get("root.sub.boolean") is False
    assert config.get("root.values") == [1, 2, 3, 4, 5]
    assert config.get("root.values.0") == 1
    assert config.get("root.values.0") == 1
    assert config.get("root.values.5") is None
    assert config.get("root.values.5", default="X") == "X"
    assert config.get("values.sub") is None
    assert config.get("values.sub", default=1) == 1

    assert config.get("complex.values.0.1.0") == "one"
    assert config.get("complex.values.1.2") == "two"
