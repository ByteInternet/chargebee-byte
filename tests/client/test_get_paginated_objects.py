from unittest.mock import MagicMock

from tests.test import TestBase


class TestGetPaginatedObjects(TestBase):
    def setUp(self):
        super().setUp()
        self.requests_get = self.set_up_patch('chargebee_byte.client.requests.get')
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
