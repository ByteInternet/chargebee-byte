from unittest import mock

from chargebee_byte.requests import SubscriptionRequest
from tests.test import TestBase


class TestGetPaginatedSubscriptions(TestBase):
    def setUp(self):
        super().setUp()
        self.requests_get = self.set_up_patch('chargebee_byte.client.requests.get')

    def test_calls_chargebee_api_with_correct_parameters(self):
        self.chargebee_client.get_paginated_subscriptions()

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + '/subscriptions',
            auth=self.chargebee_client.auth,
            params={}
        )

    def test_returns_json_result_from_requests_get_call(self):
        ret = self.chargebee_client.get_paginated_subscriptions()

        self.assertEqual(self.requests_get.return_value.json(), ret)

    def test_calls_chargebee_api_with_provided_parameters(self):
        self.chargebee_client.get_paginated_subscriptions(parameters={'status[is]': 'active'})

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + '/subscriptions',
            auth=self.chargebee_client.auth,
            params={'status[is]': 'active'}
        )

    def test_raises_value_error_if_unknown_parameter_supplied(self):
        parameter = 'banaan[henk]'
        self.assertNotIn(parameter, SubscriptionRequest().allowed_parameters)

        with self.assertRaises(ValueError):
            self.chargebee_client.get_paginated_subscriptions(parameters={parameter: 'bonobo'})

    def test_calls_raise_for_status_on_requests_response(self):
        response = mock.Mock()
        self.requests_get.return_value = response

        self.chargebee_client.get_paginated_subscriptions()

        response.raise_for_status.assert_called_once_with()
