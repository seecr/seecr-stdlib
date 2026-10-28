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

class Dict(dict):
    """A dict whose keys can also be read and written as attributes:
    d.answer is d["answer"].

    Attributes of the class itself (methods like get, items, keys, update,
    and dunder names) always win, so a key can never hide a method:
    d["items"] = 1 leaves d.items as the method; use d["items"] for the value.
    Assigning such a name as an attribute (d.items = 1) raises AttributeError
    instead of silently storing a key that could not be read back as d.items.
    """

    __slots__ = ()  # no instance __dict__: every attribute write goes to the keys

    def __getattr__(self, key):
        # Only called when normal lookup fails, i.e. never for methods.
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                f"{type(self).__name__!r} object has no attribute or key {key!r}"
            ) from None

    def __setattr__(self, key, value):
        if hasattr(type(self), key):
            raise AttributeError(
                f"{key!r} is a {type(self).__name__} attribute; use d[{key!r}] = ... instead"
            )
        self[key] = value

    def __delattr__(self, key):
        if hasattr(type(self), key):
            raise AttributeError(f"cannot delete {type(self).__name__} attribute {key!r}")
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key) from None

    def __dir__(self):
        # Include string keys that are valid identifiers, for tab completion.
        return sorted(set(super().__dir__()) | {k for k in self if isinstance(k, str) and k.isidentifier()})
