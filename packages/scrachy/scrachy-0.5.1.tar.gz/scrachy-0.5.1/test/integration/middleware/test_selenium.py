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

from scrapy.crawler import Crawler
from scrapy.http import HtmlResponse, Request
from scrapy.settings import Settings, iter_default_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# Project Modules
from scrachy.http_ import SeleniumRequest
from scrachy.middleware.selenium import SeleniumMiddleware
from scrachy.settings.defaults import selenium as selenium_defaults
from test.integration.middleware.conftest import MockSpider, SettingsFactory

logging.getLogger('selenium').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
log = logging.getLogger('test_selenium')


def paginate(driver: WebDriver, request_: Request):
    responses = dict()
    links = driver.find_elements(By.CLASS_NAME, 'year-link')

    for link in links:
        link_text = link.text
        link.click()

        table = driver.find_element(By.CSS_SELECTOR, 'table.table')
        WebDriverWait(
            driver,
            5
        ).until(
            expected_conditions.visibility_of(table)
        )

        responses[link_text] = HtmlResponse(
            url=request_.url,
            body=driver.page_source,
            encoding='utf-8',
            request=request_
        )

    return responses


@pytest.fixture(scope='module')
def middleware() -> SeleniumMiddleware:
    settings = Settings(dict(iter_default_settings()))
    settings.setmodule(selenium_defaults)
    settings.set('SCRACHY_SELENIUM_WEB_DRIVER', 'Chrome')
    settings.set('SCRACHY_SELENIUM_WEB_DRIVER_OPTIONS', ['--headless=new'])

    crawler = Crawler(
        spidercls=MockSpider,
        settings=settings
    )
    middleware = SeleniumMiddleware.from_crawler(crawler)

    yield middleware

    middleware.spider_closed(crawler.spider)


@pytest.mark.parametrize(
    'driver, options, extensions, raises_expectation',
    [
        (None, None, None, does_not_raise()),
        ('Chrome', ['--headless=new'], True, does_not_raise()),
        ('Firefox', ['-headless'], True, does_not_raise()),
    ],
    indirect=['extensions']
)
def test_initialize_driver(
        settings_factory: SettingsFactory,
        driver: Optional[str],
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
            middleware = SeleniumMiddleware.from_crawler(crawler)
            assert middleware.driver is not None
        except:  # noqa
            pass
        finally:
            middleware.spider_closed(crawler.spider)


def test_return_none_on_scrapy_request(middleware: SeleniumMiddleware):
    scrapy_request = Request(url='http://not-an-url')

    assert middleware.process_request(scrapy_request) is None


def test_return_response(middleware: SeleniumMiddleware):
    request = SeleniumRequest(url='https://www.scrapethissite.com/pages/forms/')
    response = middleware.process_request(request)

    title = response.css('title::text').get()
    assert 'Hockey Teams' in title


def test_screenshot(middleware: SeleniumMiddleware):
    request = SeleniumRequest(
        url='https://www.scrapethissite.com/pages/forms/',
        screenshot=True
    )
    response = middleware.process_request(request)

    assert response.meta['screenshot'] is not None


def test_script(middleware: SeleniumMiddleware):
    request = SeleniumRequest(
        url='https://www.scrapethissite.com/pages/ajax-javascript/',
        script_executor=paginate
    )

    response = middleware.process_request(request)
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
