#  Copyright 2020 Reid Swanson.
#
#  This file is part of scrachy.
#
#  scrachy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  scrachy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with scrachy.  If not, see <https://www.gnu.org/licenses/>.

"""
The basic data types and classes required to define the SqlAlchemy models.
"""

from __future__ import annotations

# Python Modules
import json
import logging

from json import JSONDecodeError
from typing import Annotated, Any, Optional, Sequence

# 3rd Party Modules
from sqlalchemy import MetaData, inspect, BigInteger, LargeBinary, SmallInteger
from sqlalchemy.orm import DeclarativeBase, NO_VALUE, QueryableAttribute, declared_attr

# Project Modules
from scrachy.settings import PROJECT_SETTINGS
from scrachy.utils.sqltypes import TimeStampTZ
from scrachy.utils.strings import camel_to_snake

bigint = Annotated[BigInteger, 64]
binary = Annotated[LargeBinary, None]
smallint = Annotated[int, 16]
timestamp = Annotated[TimeStampTZ, None]

log = logging.getLogger(__name__)


schema = PROJECT_SETTINGS.get('SCRACHY_DB_SCHEMA')
schema_prefix = f"{schema}." if schema else ""


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
        schema=schema
    )

    type_annotation_map = {
        bigint: BigInteger,
        binary: LargeBinary,
        smallint: SmallInteger,
        timestamp: TimeStampTZ(timezone=True),
    }

    # noinspection PyMethodParameters
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    # Modified from https://stackoverflow.com/a/55749579/4971706
    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True, default=str)

    def __eq__(self, other: Base) -> bool:
        """
        A model is equal to another if all of its columns are equal.

        :param other:
        :return:
        """
        columns: Sequence[str] = self.__table__.columns.keys()

        for col in columns:
            this_value = getattr(self, col)

            try:
                that_value = getattr(other, col)
            except AttributeError:
                return False

            if this_value != that_value:
                return False

        return True

    def __hash__(self):
        d = {k: getattr(self, k) for k in sorted(self.__table__.columns.keys())}

        return hash(tuple(d.items()))

    def to_dict(self, hide_missing: bool = True, exclude_keys: Optional[Sequence[str]] = None):
        # Adapted from: https://medium.com/@alanhamlett/part-1-sqlalchemy-models-to-json-de398bc2ef47
        # The only major change was to add a check to make sure the relationship
        # data is attached before trying to access it with getattr.
        path: str = self.__tablename__.lower()
        excluded: set[str] = set(exclude_keys) if exclude_keys else set()
        seen: set[Any] = {self}

        return self._to_dict(path, excluded, hide_missing, seen)

    def _to_dict(self, path: str, excluded: set[str], hide_missing: bool, seen: set[Any]) -> dict[str, Any]:
        columns: Sequence[str] = self.__table__.columns.keys()
        relationships: Sequence[str] = self.__mapper__.relationships.keys()
        properties: Sequence[str] = list(set(dir(self)) - set(columns) - set(relationships))

        result: dict[str, Any] = dict()

        # The columns
        self._columns_to_dict(columns, path, excluded, result, hide_missing)
        self._relationships_to_dict(relationships, path, excluded, result, hide_missing, seen)
        self._properties_to_dict(properties, path, excluded, result, hide_missing)

        return result

    def _columns_to_dict(
            self,
            columns: Sequence[str],
            path: str,
            excluded: set[str],
            result: dict[str, Any],
            hide_missing: bool
    ):
        for key in columns:
            if self._is_private(key):
                continue

            # Some keys might be an SqlAlchemy subclass of str
            key = str(key)

            qualified_key = self._qualified_key(path, key)
            if qualified_key in excluded:
                continue

            value = getattr(self, key)

            if value is None and hide_missing:
                continue

            result[key] = value.hex() if isinstance(value, bytes) else value

    def _relationships_to_dict(
            self,
            relationships: Sequence[str],
            path: str,
            excluded: set[str],
            result: dict[str, Any],
            hide_missing: bool,
            seen: set[Any]
    ):
        for key in relationships:
            if self._is_private(key):
                continue

            qualified_key = self._qualified_key(path, key)
            if qualified_key in excluded:
                continue

            key = str(key)

            excluded.add(qualified_key)

            relationship = self.__mapper__.relationships[key]

            if relationship.uselist:
                items: list[Base] = getattr(self, key)
                if relationship.query_class is not None:
                    if hasattr(items, "all"):
                        items = items.all()
                result[key] = [i._to_dict(qualified_key.lower(), excluded, hide_missing, seen) for i in items]
            else:
                if relationship.query_class is not None or relationship.instrument_class is not None:
                    state = inspect(self)
                    loaded_value = state.attrs[key].loaded_value
                    if loaded_value == NO_VALUE:
                        result[key] = '[DETACHED]'
                    else:
                        item: Base = getattr(self, key)

                        if item is not None and item not in seen:
                            seen.add(item)
                            result[key] = item._to_dict(qualified_key.lower(), excluded, hide_missing, seen)
                        elif not hide_missing:
                            result[key] = None
                else:
                    value = getattr(self, key)
                    if (value is not None or not hide_missing) and value not in seen:
                        seen.add(value)
                        result[key] = value

    def _properties_to_dict(
            self,
            properties: Sequence[str],
            path: str,
            excluded: set[str],
            result: dict[str, Any],
            hide_missing: bool
    ):
        for key in properties:
            if self._is_private(key):
                continue

            mycls = self.__class__
            if not hasattr(mycls, key):
                continue

            attr = getattr(mycls, key)
            if not isinstance(attr, property) or isinstance(attr, QueryableAttribute):
                continue

            qualified_key = self._qualified_key(path, key)
            if qualified_key in excluded:
                continue

            key = str(key)

            value = getattr(self, key)
            if hasattr(value, '_to_dict'):
                result[key] = value._to_dict(qualified_key.lower(), excluded, hide_missing)
            else:
                try:
                    result[key] = json.loads(json.dumps(value, sort_keys=True))
                except (RecursionError, ValueError, TypeError, JSONDecodeError):
                    pass

    @staticmethod
    def _qualified_key(path: str, key: str) -> str:
        return f"{path}.{key}"

    @staticmethod
    def _is_private(key: str) -> bool:
        return key.startswith('_')
