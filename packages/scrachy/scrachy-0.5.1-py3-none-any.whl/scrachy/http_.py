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
Additional ``Request`` and ``Response`` classes for working with Selenium
and the ``AlchemyCacheStorage`` backend.

Note: Naming this module ``http`` causes a circular import error, so I've appended
an underscore to avoid conflicts.
"""
from __future__ import annotations

# Python Modules
import datetime
import logging

from typing import Any, Optional, Protocol

# 3rd Party Modules
from scrapy.http import HtmlResponse, TextResponse, Request, Response, XmlResponse
from selenium.webdriver.remote.webdriver import WebDriver

# Project Modules
from scrachy.db.models import ScrapeHistory

log = logging.getLogger(__name__)


class WaitCondition(Protocol):
    def __call__(self, driver: WebDriver) -> Any:
        pass


class ScriptExecutor(Protocol):
    def __call__(self, driver: WebDriver, request: Request) -> Optional[Response | list[Response] | dict[str, Response]]:
        pass


class SeleniumRequest(Request):
    """
    A subclas of :class:`scrapy.http.Request` that provides extra information for downloading pages using
    Selenium.

    Based off the code from `Scrapy-Selenium <https://github.com/clemfromspace/scrapy-selenium>`_
    """

    def __init__(
            self,
            wait_timeout: Optional[float] = None,
            wait_until: Optional[WaitCondition] = None,
            screenshot: bool = False,
            script_executor: Optional[ScriptExecutor] = None,
            *args,
            **kwargs
    ):
        """
        A new ``SeleniumRequest``.

        :param wait_timeout: The number of seconds to wait before accessing the data.
        :param wait_until: One of the "selenium.webdriver.support.expected_conditions". The response
                           will be returned until the given condition is fulfilled.
        :param screenshot: If ``True``, a screenshot of the page will be taken and the data of the screenshot
                           will be returned in the response "meta" attribute.
        :param script_executor: A function that takes a webdriver and a response as its parameters and optionally
                                returns a list of new response objects as a side effect of its actions (e.g.,
                                executing arbitrary javascript code on the page). Any returned responses will
                                be returned in the ``request.meta`` attribute with the key ``script_result``.
                                Note that the returned responses will not be further processed by any other
                                middleware.

        """
        super().__init__(*args, **kwargs)

        self.wait_timeout = wait_timeout
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script_executor = script_executor


class CachedResponseMixin:
    def __init__(
            self,
            scrape_timestamp: Optional[datetime.datetime] = None,
            extracted_text: Optional[str] = None,
            body_length: Optional[int] = None,
            extracted_text_length: Optional[int] = None,
            scrape_history: Optional[list[ScrapeHistory]] = None,
            *args,
            **kwargs
    ):
        """
        A subclass of :class:`scrapy.http.HttpResponse` that contains a
        subset of the extra information stored in the cache.

        :param scrape_timestamp: The most recent date the request was scraped.
        :param body_number_of_bytes: The total number of bytes of the downloaded
               html.
        :param text_number_of_bytes: The number of bytes in the extracted
               plain text.
        :param body_text: The text extracted from the HTML.
        """
        super().__init__(*args, **kwargs)

        self.scrape_timestamp = scrape_timestamp
        self.extracted_text = extracted_text
        self.body_length = body_length
        self.extracted_text_length = extracted_text_length
        self.scrape_history = scrape_history


class CachedHtmlResponse(CachedResponseMixin, HtmlResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CachedTextResponse(CachedResponseMixin, TextResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CachedXmlResponse(CachedResponseMixin, XmlResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
