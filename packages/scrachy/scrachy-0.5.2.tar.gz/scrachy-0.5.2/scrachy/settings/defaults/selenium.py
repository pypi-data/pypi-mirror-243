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
The default settings for configuring the
:mod:`Selenium <scrachy.middleware.selenium>`. middleware.
"""

# Python Modules
from typing import Literal, Optional

# 3rd Party Modules

# Project Modules


WebDriverName = Literal['Chrome', 'ChromiumEdge', 'Firefox', 'Safari']


SCRACHY_SELENIUM_WEB_DRIVER: WebDriverName = 'Chrome'
"""
The name of the webdriver to use.
"""

SCRACHY_SELENIUM_WEB_DRIVER_OPTIONS: list[str] = []
"""
Initialize the webdriver with an ``Options`` object populated with these
options.

For a list of options see:
    
    * Chrome: `https://peter.sh/experiments/chromium-command-line-switches/`
    * Firefox: `https://www-archive.mozilla.org/docs/command-line-args`
"""

SCRACHY_SELENIUM_WEB_DRIVER_EXTENSIONS: list[str] = []
"""
A list of extensions for the webdriver to load. These should be paths to CRX
files for Chrome or XPI files for Firefox.
"""

SCRACHY_SELENIUM_LOG_FILE: Optional[str] = None
"""
A file to save logging statements made by a process launched from the
:class:`~scrachy.middleware.selenium.AsyncSeleniumMiddleware`. 
"""
