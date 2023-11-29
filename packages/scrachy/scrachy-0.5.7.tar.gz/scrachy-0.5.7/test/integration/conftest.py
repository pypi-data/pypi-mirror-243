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

# Python Modules
import logging
import pathlib

# 3rd Party Modules
import pytest

from scrapy.settings import Settings


# Project Modules
from scrachy.db.base import Base
from scrachy.db.engine import initialize_engine, reset_engine
from test.utils import update_database_settings

log = logging.getLogger(__name__)


@pytest.fixture
def manage_engine(request: pytest.FixtureRequest, tmp_path: pathlib.Path):
    dialect: str = request.getfixturevalue('dialect')
    settings: Settings = request.getfixturevalue('settings')

    update_database_settings(settings, dialect, tmp_path)

    engine = initialize_engine(settings)

    yield

    Base.metadata.drop_all(engine)
    reset_engine()
