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
import copy
import logging

from collections import defaultdict

# 3rd Party Modules
import pytest

from dotenv import load_dotenv
from scrapy.settings import Settings

# Project Modules
from scrachy.db.engine import session_scope
from scrachy.db.models import Response as CachedResponse, ScrapeHistory
from scrachy.db.repositories import ResponseRepository, ScrapeHistoryRepository


load_dotenv()


log = logging.getLogger('test_repositories')

log.debug(f"From test_repositories")


@pytest.fixture
def settings(settings_choices: dict[str, Settings], request: pytest.FixtureRequest) -> Settings:
    return settings_choices[request.param]  # noqa


# Note: It's difficult (maybe impossible?) to test if insert/upsert is
# working without also testing find and vice versa.
@pytest.mark.parametrize('dialect', ['sqlite', 'postgresql', 'other'])
@pytest.mark.parametrize('settings', ['defaults', 'settings_2'], indirect=True)
def test_upsert_and_find(
        manage_engine,
        dialect: str,
        settings: Settings,
        cached_responses: list[CachedResponse]
):
    # Create a copy because the objects could be modified by the upsert
    # process.
    cached_responses_copy = copy.deepcopy(cached_responses)

    with session_scope() as session:
        response_repo = ResponseRepository(session)
        history_repo = ScrapeHistoryRepository(session)

        response_repo.dialect = dialect

        for response in cached_responses_copy:
            history = ScrapeHistory(
                fingerprint=response.fingerprint,
                scrape_timestamp=response.scrape_timestamp,
                body=response.body
            )

            act_response = response_repo.upsert(response, returning=True)
            history_repo.insert(history)

            assert act_response == response

    with session_scope() as session:
        response_repo = ResponseRepository(session)
        response_repo.dialect = dialect

        sorted_responses = sorted(
            cached_responses,
            key=lambda e: (e.fingerprint, e.scrape_timestamp),
            reverse=True
        )
        expected_responses = []
        fingers = defaultdict(list)
        for r in sorted_responses:
            if r.fingerprint not in fingers:
                expected_responses.append(r)

            fingers[r.fingerprint].append(r.body)

        # One at a time
        assert all([e == response_repo.find_by_fingerprint(e.fingerprint) for e in expected_responses])

        # All of them
        act_responses = response_repo.find_all()
        assert len(expected_responses) == len(act_responses)
        assert all([e == a for e, a in zip(expected_responses, act_responses)])

        # Make sure the scrape history has the correct number of entries
        for act_response in act_responses:
            act_history = sorted(act_response.scrape_history, key=lambda h: h.scrape_timestamp, reverse=True)
            exp_history = fingers[act_response.fingerprint]

            assert len(exp_history) == len(act_history)
            assert all([exp == act.body for exp, act in zip(exp_history, act_history)])
