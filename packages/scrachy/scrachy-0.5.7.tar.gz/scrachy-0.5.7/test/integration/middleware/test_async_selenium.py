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
from contextlib import AbstractContextManager, nullcontext as does_not_raise
from typing import Optional

# 3rd Party Modules
import pytest
import pytest_twisted

from scrapy.crawler import Crawler
from scrapy.http import Request
from scrapy.settings import Settings, iter_default_settings

# Project Modules
from scrachy.http_ import SeleniumRequest
from scrachy.middleware.selenium import AsyncSeleniumMiddleware
from scrachy.settings.defaults import selenium as selenium_defaults
from scrachy.settings.defaults.selenium import WebDriverName
from test.integration.middleware.conftest import MockSpider, SettingsFactory
from test.integration.middleware.test_selenium import paginate

log = logging.getLogger("test_async_selenium")


@pytest.fixture(scope='module')
def middleware() -> AsyncSeleniumMiddleware:
    settings = Settings(dict(iter_default_settings()))
    settings.setmodule(selenium_defaults)
    settings.set('CONCURRENT_REQUESTS', 4)  # temporary
    settings.set('SCRACHY_SELENIUM_WEB_DRIVER', 'Chrome')
    settings.set('SCRACHY_SELENIUM_WEB_DRIVER_OPTIONS', ['--headless=new'])

    crawler = Crawler(
        spidercls=MockSpider,
        settings=settings
    )
    middleware = AsyncSeleniumMiddleware.from_crawler(crawler)

    yield middleware

    log.info(f"Calling spider_closed")
    middleware.spider_closed(crawler.spider)


@pytest_twisted.ensureDeferred
@pytest.mark.parametrize(
    'driver, options, extensions, raises_expectation',
    [
        (None, None, None, does_not_raise()),
        ('Chrome', ['--headless=new'], True, does_not_raise()),
        ('Firefox', ['-headless'], True, does_not_raise()),
    ],
    indirect=['extensions']
)
async def test_initialize_driver(
        settings_factory: SettingsFactory,
        driver: WebDriverName,
        options: Optional[list[str]],
        extensions: Optional[list[str]],
        raises_expectation: AbstractContextManager
):
    with raises_expectation:
        settings = settings_factory(driver, options, extensions)

        crawler = Crawler(
            spidercls=MockSpider,
            settings=settings
        )

        try:
            middleware = AsyncSeleniumMiddleware.from_crawler(crawler)
            assert len(middleware.drivers) == settings.getint('CONCURRENT_REQUESTS')
        except:  # noqa
            pass
        finally:
            middleware.spider_closed(crawler.spider)


@pytest_twisted.ensureDeferred
async def test_return_none_on_scrapy_request(middleware: AsyncSeleniumMiddleware):
    scrapy_request = Request(url='http://not-an-url')

    assert middleware.process_request(scrapy_request) is None


@pytest_twisted.ensureDeferred
async def test_return_response(middleware: AsyncSeleniumMiddleware):
    request = SeleniumRequest(url='https://www.scrapethissite.com/pages/forms/')
    response = await middleware.process_request(request)

    title = response.css('title::text').get()
    assert 'Hockey Teams' in title


@pytest_twisted.ensureDeferred
async def test_screenshot(middleware: AsyncSeleniumMiddleware):
    request = SeleniumRequest(
        url='https://www.scrapethissite.com/pages/forms/',
        screenshot=True
    )
    response = await middleware.process_request(request)

    assert response.meta['screenshot'] is not None


@pytest_twisted.ensureDeferred
async def test_script(middleware: AsyncSeleniumMiddleware):
    request = SeleniumRequest(
        url='https://www.scrapethissite.com/pages/ajax-javascript/',
        script_executor=paginate
    )

    response = await middleware.process_request(request)
    expected_titles = {
        '2015': 'Spotlight',
        '2014': 'Birdman',
        '2013': '12 Years a Slave',
        '2012': 'Argo',
        '2011': 'The Artist',
        '2010': 'The King\'s Speech'
    }

    for key, script_response in response.meta['script_result'].items():
        title = script_response.css('tbody#table-body > tr.film > td.film-title::text').get().strip()

        assert expected_titles[key] == title
