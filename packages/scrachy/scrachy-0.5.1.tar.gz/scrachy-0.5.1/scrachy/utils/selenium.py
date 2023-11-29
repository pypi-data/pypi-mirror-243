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
Some utility classes for sending messages between the
:class:`~scrachy.middleware.selenium.AsyncSeleniumMiddleware` and the
:mod:`~scrachy.cli.webdriver_server`. It also includes the primary
functionality for processing requests with Selenium. Each Selenium middleware
is a thin wrapper around these functions.
"""

from __future__ import annotations

# Python Modules
import logging

from typing import Optional, Type, cast

# 3rd Party Modules
from scrapy.http import Request, HtmlResponse
from scrapy.utils.misc import load_object
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Project Modules
from scrachy.http_ import SeleniumRequest
from scrachy.settings.defaults.selenium import WebDriverName


log = logging.getLogger(__name__)


webdriver_import_base = 'selenium.webdriver'


class BufferIncompleteError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ShutdownRequest:
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnknownMessageType:
    def __init__(self, message_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message_type = message_type


class UnhandledError:
    def __init__(self, exception: Exception, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exception = exception


def initialize_driver(driver_name: WebDriverName, options: list[str], extensions: list[str]) -> WebDriver:
    driver_name: WebDriverName = driver_name
    driver_cls: Type[WebDriver] = load_object(f'{webdriver_import_base}.{driver_name}')
    driver_options: ArgOptions = load_object(f'{webdriver_import_base}.{driver_name}Options')()

    for option in options:
        driver_options.add_argument(option)

    # Chrome loads the extensions from the options
    if driver_name == 'Chrome' and extensions:
        driver_options = cast(ChromiumOptions, driver_options)
        for extension in extensions:
            driver_options.add_extension(extension)  # noqa

    driver = driver_cls(options=driver_options)

    # Firefox appears to lod the extension directly from the driver
    if driver_name == 'Firefox' and extensions:
        for extension in extensions:
            driver = cast(webdriver.Firefox, driver)
            driver.install_addon(extension, temporary=True)

    return driver


def process_request(driver: WebDriver, request: Request) -> Optional[HtmlResponse]:
    if not isinstance(request, SeleniumRequest):
        # Let some other downloader handle this request
        return None

    request = cast(SeleniumRequest, request)

    driver.get(request.url)

    set_cookies(driver, request)
    wait_for_page(driver, request)
    take_screenshot(driver, request)

    execute_script(driver, request)

    response = make_response(driver, request)

    return response


def set_cookies(driver: WebDriver, request: SeleniumRequest):
    for cookie_name, cookie_value in request.cookies.items():
        driver.add_cookie({'name': cookie_name, 'value': cookie_value})


def wait_for_page(driver: WebDriver, request: SeleniumRequest):
    if request.wait_until:
        try:
            WebDriverWait(
                driver,
                request.wait_timeout
            ).until(
                request.wait_until
            )
        except TimeoutException as e:
            log.error(f"Wait condition timed out for url: '{request.url}'")
            raise e


def take_screenshot(driver: WebDriver, request: SeleniumRequest):
    if request.screenshot:
        request.meta['screenshot'] = driver.get_screenshot_as_png()


def make_response(driver: WebDriver, request: SeleniumRequest) -> HtmlResponse:
    return HtmlResponse(
        url=driver.current_url,
        body=driver.page_source,
        encoding='utf-8',
        request=request
    )


def execute_script(driver: WebDriver, request: SeleniumRequest):
    if request.script_executor is not None:
        request.meta['script_result'] = request.script_executor(driver, request)
