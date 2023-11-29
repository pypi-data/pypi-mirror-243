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
Middleware for processing requests with Selenium.
"""

from __future__ import annotations

# Python Modules
import logging
import math
import os
import queue

from struct import pack, unpack
from sys import executable
from typing import Any, Optional

# 3rd Party Modules
import pickle

from scrapy import Spider
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.http import HtmlResponse, Request
from scrapy.settings import Settings
from selenium.webdriver.remote.webdriver import WebDriver
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ProcessProtocol
from twisted.python import failure

# Project Modules
from scrachy import PROJECT_ROOT
from scrachy.http_ import SeleniumRequest
from scrachy.cli.webdriver_server import DEFAULT_BUFFER_SIZE, Message
from scrachy.settings.defaults.selenium import WebDriverName
from scrachy.utils.selenium import ShutdownRequest, initialize_driver
from scrachy.utils.selenium import process_request as process_request_helper

log = logging.getLogger(__name__)


class SeleniumMiddleware:
    """
    A downloader middleware that uses a Selenium WebDriver to download
    the content and return an ``HtmlResponse`` if the incoming ``Response``
    is an instance of :class:`~scrachy.http_.SeleniumRequest`. Otherwise,
    it returns ``None`` to let another downloader process it.
    """
    webdriver_import_base = 'selenium.webdriver'

    def __init__(self, settings: Settings, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = settings
        self._driver = initialize_driver(self.driver_name, self.driver_options, self.driver_extensions)

    # region Properties
    def get(self, name: str) -> Any:
        return self.settings.get(f'SCRACHY_SELENIUM_{name}')

    @property
    def driver_name(self) -> WebDriverName:
        return self.get('WEB_DRIVER')

    @property
    def driver_options(self) -> list[str]:
        return self.get('WEB_DRIVER_OPTIONS')

    @property
    def driver_extensions(self) -> list[str]:
        return self.get('WEB_DRIVER_EXTENSIONS')

    @property
    def driver(self) -> WebDriver:
        return self._driver

    # endregion Properties

    # region API
    @classmethod
    def from_crawler(cls, crawler: Crawler) -> SeleniumMiddleware:
        middleware = cls(crawler.settings)

        # See: https://docs.scrapy.org/en/latest/topics/signals.html
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request: Request, spider: Optional[Spider] = None) -> Optional[HtmlResponse]:
        return process_request_helper(self.driver, request)

    def spider_closed(self, spider: Optional[Spider] = None):
        self.driver.quit()
    # endregion API


class AsyncSeleniumMiddleware:
    """
        A downloader middleware that creates a pool of Selenium WebDrivers
        and sends any incoming
        :class:`SeleniumRequests <~scrachy.http_.SeleniumRequest>` to an
        available driver to be processed.
        """
    def __init__(self, settings: Settings, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = settings

        concurrent_requests: int = settings.getint('CONCURRENT_REQUESTS')
        log_file: str = settings.get('SCRACHY_SELENIUM_LOG_FILE')

        # Create a pool of drivers to increase the throughput. Since there
        # isn't actually any parallelism involved I don't think I have to
        # be all that careful with synchronization (e.g., locks).
        self.drivers = queue.Queue(maxsize=concurrent_requests)
        for driver in [WebDriverProtocol(i) for i in range(concurrent_requests)]:
            self.drivers.put(driver)

            args = ['python', '-m', 'scrachy.cli.webdriver_server']
            args += ['-d', self.driver_name]
            args += [f'-o "{o}"' for o in self.driver_options]
            args += [f'-e "{e}"' for e in self.driver_extensions]

            if log_file:
                args += [f'-f "{log_file}"']

            # noinspection PyUnresolvedReferences
            reactor.spawnProcess(
                driver,
                executable,
                args,
                path=PROJECT_ROOT,
                env=os.environ,
            )

    # region Properties
    def get(self, name: str) -> Any:
        return self.settings.get(f'SCRACHY_SELENIUM_{name}')

    @property
    def driver_name(self) -> WebDriverName:
        return self.get('WEB_DRIVER')

    @property
    def driver_options(self) -> list[str]:
        return self.get('WEB_DRIVER_OPTIONS')

    @property
    def driver_extensions(self) -> list[str]:
        return self.get('WEB_DRIVER_EXTENSIONS')
    # endregion Properties

    # region API
    @classmethod
    def from_crawler(cls, crawler: Crawler) -> AsyncSeleniumMiddleware:
        middleware = cls(crawler.settings)

        # See: https://docs.scrapy.org/en/latest/topics/signals.html
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request: Request, spider: Optional[Spider] = None) -> Optional[Deferred[HtmlResponse]]:
        if not isinstance(request, SeleniumRequest):
            # Let some other downloader handle this request
            return None

        driver = self.drivers.get()

        d = driver.process_request(request)

        def enqueue_driver(r: HtmlResponse):
            self.drivers.put(driver)
            return r

        d.addCallback(enqueue_driver)

        return d

    def spider_closed(self, spider: Optional[Spider] = None):
        # Closing stdin should shut down the server
        while not self.drivers.empty():
            driver = self.drivers.get(block=False)
            driver.shutdown()

        # Uncommenting the following lines will allow any final messages
        # sent to stderr from the server just before exiting.
        # import time
        # from twisted.internet.threads import deferToThread
        # yield deferToThread(lambda: time.sleep(0.5))
    # endregion API


class WebDriverProtocol(ProcessProtocol):
    # The number of bytes in the response message.
    response_header_size = 4

    def __init__(self, id_: int, process_buffer_size: int = DEFAULT_BUFFER_SIZE):
        # An identifier for this process
        self.id = id_

        # The size of the read buffer on the spawned process. We need to send
        # at lest this many bytes in order for the server's read buffer
        # to flush. Otherwise, the server will hang until it gets more data.
        self.process_buffer_size = process_buffer_size

        # Buffer to accumulate incoming messages
        self.buffer = b''

        # The deferred object we will eventually return
        self.deferred_response: Optional[Deferred[HtmlResponse]] = None

        # This gets set once the shutdown message is sent and will be used
        # to prevent any further communication with the protocol.
        self.is_shutdown = False

    # region Interface Methods
    def connectionMade(self):
        log.debug(f"Connection made to: {self.id} with pid: {self.transport.pid}")

    def outReceived(self, data: bytes):
        self.buffer += data
        self._extract_message()

    def errReceived(self, data: bytes):
        log.error(f"Driver process error: {data.decode()}")

    def inConnectionLost(self):
        log.debug(f"Lost stdin")

    def outConnectionLost(self):
        log.debug(f"Lost stdout")

    def errConnectionLost(self):
        log.debug(f"Lost stderr")

    def processExited(self, reason: failure.Failure):
        log.info(f"Child process exited with exit code: {reason.value.exitCode}")

    def processEnded(self, reason: failure.Failure):
        log.info(f"Child process ended: {reason.value.exitCode}")
    # endregion Interface Methods

    def process_request(self, request: SeleniumRequest) -> Deferred[HtmlResponse]:
        if self.is_shutdown:
            raise ValueError("You cannot process requests after the server has been shut down.")

        # The original request has references to all sorts of unnecessary
        # and impossible to pickle objects. Just send over what we need.
        self._send_message(
            SeleniumRequest(
                url=request.url,
                wait_timeout=request.wait_timeout,
                wait_until=request.wait_until,
                screenshot=request.screenshot,
                script_executor=request.script_executor
            )
        )

        # We'll store the response here when it is ready.
        self.deferred_response = Deferred()

        return self.deferred_response

    def shutdown(self):
        self._send_message(ShutdownRequest())

        self.transport.closeStdin()
        self.is_shutdown = True

    def _send_message(self, message: Message):
        message_data = pickle.dumps(message)

        # The number of bytes to encode the pickled data
        data_length = len(message_data)

        # The total number of bytes sent in the message (including the header
        # and padding)
        msg_length = self._get_message_length(data_length + 8)

        # The number of bytes to pad the message by. The sum of the header,
        # message, and padding should be an exact multiple of the process
        # buffer size. This is the difference between the total message length
        # and the data length and excluding the header.
        pad_length = (msg_length - data_length) - 8

        data_field = pack('!I', data_length)
        msg_field = pack('!I', msg_length)

        self.transport.writeSequence([data_field, msg_field, message_data, b' ' * pad_length])  # noqa

    def _get_message_length(self, request_length: int) -> int:
        return self.process_buffer_size * math.ceil(request_length / self.process_buffer_size)

    def _extract_message(self):
        while len(self.buffer) >= self.response_header_size:
            msg_length = unpack('!I', self.buffer[:4])[0]
            if len(self.buffer) >= msg_length + 4:
                # Get the data from the buffer
                data = self.buffer[4:4+msg_length]

                # Remove the processed data from the buffer
                self.buffer = self.buffer[4+msg_length:]

                # Try to decode the message
                try:
                    obj = pickle.loads(data)
                except pickle.PickleError as e:
                    if self.deferred_response is not None:
                        self.deferred_response.errback(e)
                    else:
                        log.error(f"There was a pickle error but the deferred response was not ready.")
                    continue

                if self.deferred_response is None:
                    log.error(f"Deferred response is not ready!")
                    continue

                if not isinstance(obj, HtmlResponse):
                    log.error(f"The message was not an HtmlResponse.")
                    self.deferred_response.errback(obj)
                    continue

                self.deferred_response.callback(obj)
            else:
                break  # The message is not complete
