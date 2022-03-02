import datetime
from unittest.mock import MagicMock
from libfaketime import freeze_time

from chargebee_byte.client import Client
from tests.test import TestBase


class TestGetPaginatedObjects(TestBase):
    def setUp(self):
        super().setUp()
        self.requests_get = self.set_up_patch('chargebee_byte.client.requests.get')
        self.mock_sleep = self.set_up_patch('chargebee_byte.client.time.sleep')
        self.request = MagicMock(path='/my_path', data={'sort_by[asc]': 'first_name'})

    def test_calls_chargebee_api_with_correct_parameters(self):
        self.chargebee_client._get_paginated_objects(self.request)

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + self.request.path,
            auth=self.chargebee_client.auth,
            params=self.request.data
        )

    def test_returns_json_result_from_requests_get_call(self):
        ret = self.chargebee_client._get_paginated_objects(self.request)

        self.assertEqual(self.requests_get.return_value.json(), ret)

    def test_calls_raise_for_status_on_requests_response(self):
        self.chargebee_client._get_paginated_objects(self.request)

        self.requests_get.return_value.raise_for_status.assert_called_once_with()

    @freeze_time('2021-01-01')
    def test_calls_time_sleep_when_rate_limit_exists_and_last_request_plus_rate_limit_is_more_recent_than_now(self):
        rate_limit_in_seconds = 5
        self.chargebee_client = Client('my_site', 'my_api_key', rate_limit_in_seconds)
        self.chargebee_client.last_request = datetime.datetime(2021, 1, 1, 0, 0, 6)

        self.chargebee_client._get_paginated_objects(self.request)

        self.mock_sleep.assert_called_once_with(rate_limit_in_seconds)

    @freeze_time('2021-01-01')
    def test_does_not_call_sleep_when_last_request_is_less_recent_than_now(self):
        rate_limit_in_seconds = 5
        self.chargebee_client = Client('my_site', 'my_api_key', rate_limit_in_seconds)
        self.chargebee_client.last_request = datetime.datetime(2021, 1, 1, 0, 0, 1)

        self.chargebee_client._get_paginated_objects(self.request)

        self.mock_sleep.assert_not_called()
