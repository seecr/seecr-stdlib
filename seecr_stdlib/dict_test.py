## begin license ##
#
# Seecr StdLib provides convenient tools for Seecr developers
#
# Copyright (C) 2025 Seecr (Seek You Too B.V.) http://seecr.nl
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

import copy
import json
import pickle

import pytest

from .dict import Dict


def test_dict():
    d = Dict()
    d["answer"] = 42
    assert d["answer"] == 42
    assert d.answer == 42

    d = Dict()
    d.answer = 42

    assert d.answer == 42
    assert d["answer"] == 42


def test_keys_do_not_override_methods():
    d = Dict(items=1, get=2, keys=3, update=4)
    assert callable(d.items) and callable(d.get) and callable(d.keys)
    assert d["items"] == 1 and d.get("get") == 2
    assert sorted(d.keys()) == ["get", "items", "keys", "update"]
    d.update(answer=42)
    assert d.answer == 42


def test_setting_method_name_as_attribute_is_refused():
    d = Dict()
    with pytest.raises(AttributeError):
        d.items = 1
    with pytest.raises(AttributeError):
        d.__class__ = dict
    assert d == {}
    d["items"] = 1                      # item syntax still works
    assert d["items"] == 1 and callable(d.items)


def test_missing_attribute():
    d = Dict(a=1)
    with pytest.raises(AttributeError):
        d.missing
    assert getattr(d, "missing", None) is None
    assert hasattr(d, "a") and not hasattr(d, "missing")


def test_delete_attribute():
    d = Dict(a=1)
    del d.a
    assert d == {}
    with pytest.raises(AttributeError):
        del d.a
    with pytest.raises(AttributeError):
        del d.items


def test_no_instance_dict():
    d = Dict()
    d.answer = 42
    assert d == {"answer": 42}
    assert not hasattr(d, "__dict__")


def test_dir_includes_keys():
    d = Dict(Name="x", **{"not valid": 1})
    assert "Name" in dir(d) and "items" in dir(d) and "not valid" not in dir(d)


def test_still_a_dict():
    d = Dict(a=1, b=Dict(c=2))
    assert isinstance(d, dict)
    assert json.loads(json.dumps(d)) == {"a": 1, "b": {"c": 2}}
    for clone in (copy.copy(d), copy.deepcopy(d), pickle.loads(pickle.dumps(d))):
        assert clone == d and type(clone) is Dict and clone.b.c == 2
