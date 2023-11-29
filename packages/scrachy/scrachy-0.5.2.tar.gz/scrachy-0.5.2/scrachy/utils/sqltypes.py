#  Copyright 2023 Reid Swanson.
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
Custom SqlAlchemy types.
"""

# Python Modules
import datetime

# 3rd Party Modules
from sqlalchemy import TypeDecorator
from sqlalchemy.types import TIMESTAMP

# Project Modules


LOCAL_TIMEZONE = datetime.datetime.utcnow().astimezone().tzinfo


class TimeStampTZ(TypeDecorator):
    """
    A custom timestamp type that ensures all datetimes are timezone aware
    before entering or exiting the database.
    """
    # See: https://mike.depalatis.net/blog/sqlalchemy-timestamps.html

    impl = TIMESTAMP

    # This might produce different results if the local timezone changes,
    # but that shouldn't happen while running.
    cache_ok = True

    def __init__(self, timezone: bool = False):
        super().__init__(timezone)

    @property
    def python_type(self):
        return datetime.datetime
    
    def process_literal_param(self, value, dialect):
        if value.tzinfo is None:
            value = value.astimezone(LOCAL_TIMEZONE)

        return value.astimezone(datetime.timezone.utc)

    def process_bind_param(self, value: datetime, dialect):
        if value.tzinfo is None:
            value = value.astimezone(LOCAL_TIMEZONE)

        return value.astimezone(datetime.timezone.utc)

    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            return value.replace(tzinfo=datetime.timezone.utc)

        return value.astimezone(datetime.timezone.utc)
