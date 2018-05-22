from unittest import TestCase, mock

import requests

from chargebee_byte.client import Client
from chargebee_byte.requests import SubscriptionRequest


class TestBase(TestCase):
    def setUp(self):
        self.chargebee_client = Client('my_site', 'my_api_key')

    def set_up_patch(self, topatch, themock=None, **kwargs):
        """
        Patch a function or class
        :param topatch: string The class to patch
        :param themock: optional object to use as mock
        :return: mocked object
        """
        if themock is None:
            themock = mock.Mock(**kwargs)

        patcher = mock.patch(topatch, themock)
        self.addCleanup(patcher.stop)
        return patcher.start()


class TestClient(TestBase):
    def test_sets_api_url_to_provided_site(self):
        self.assertEqual(self.chargebee_client.api_url, 'https://my_site.chargebee.com/api/v2')

    def test_sets_auth_to_hhtp_basic_auth_method_with_api_key_as_username(self):
        self.assertEqual(self.chargebee_client.auth, requests.auth.HTTPBasicAuth('my_api_key', ''))


class TestGetPaginatedSubscriptions(TestBase):
    def setUp(self):
        super(TestGetPaginatedSubscriptions, self).setUp()
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


class TestGetAllSubscriptions(TestBase):
    def setUp(self):
        super(TestGetAllSubscriptions, self).setUp()
        self.requests_get = self.set_up_patch('chargebee_byte.client.requests.get')

        self.response = mock.Mock()
        self.response.json.return_value = {'list': []}
        self.requests_get.return_value = self.response

    def test_raises_value_error_if_unknown_parameter_supplied(self):
        parameter = 'banaan[henk]'
        self.assertNotIn(parameter, SubscriptionRequest().allowed_parameters)

        with self.assertRaises(ValueError):
            self.chargebee_client.get_all_subscriptions(parameters={parameter: 'bonobo'})

    def test_calls_raise_for_status_on_requests_response(self):
        self.chargebee_client.get_all_subscriptions()

        self.response.raise_for_status.assert_called_once_with()

    def test_keeps_querying_chargebee_for_subscriptions_if_next_offset_returned(self):
        response_1 = mock.Mock()
        response_1.json.return_value = {
            'list': [],
            'next_offset': '["1522747277000", "1522747277010"]'
        }
        response_2 = mock.Mock()
        response_2.json.return_value = {
            'list': [],
            'next_offset': '["1522747277010", "1522747277020"]'
        }
        response_3 = mock.Mock()
        response_3.json.return_value = {
            'list': [],
        }
        self.requests_get.side_effect = [response_1, response_2, response_3]

        self.chargebee_client.get_all_subscriptions()

        self.requests_get.assert_has_calls([
            mock.call(
                self.chargebee_client.api_url + '/subscriptions',
                auth=self.chargebee_client.auth,
                params={}
            ),
            mock.call(
                self.chargebee_client.api_url + '/subscriptions',
                auth=self.chargebee_client.auth,
                params={'offset': '["1522747277000", "1522747277010"]'}
            ),
            mock.call(
                self.chargebee_client.api_url + '/subscriptions',
                auth=self.chargebee_client.auth,
                params={'offset': '["1522747277010", "1522747277020"]'}
            ),
        ])

    def test_returns_all_subscriptions(self):
        response_1 = mock.Mock()
        response_1.json.return_value = {
            'list': [{'subscription': {'id': 1}}],
            'next_offset': '["1522747277000", "1522747277010"]'
        }
        response_2 = mock.Mock()
        response_2.json.return_value = {
            'list': [{'subscription': {'id': 2}}],
            'next_offset': '["1522747277010", "1522747277020"]'
        }
        response_3 = mock.Mock()
        response_3.json.return_value = {
            'list': [{'subscription': {'id': 3}}],
        }
        self.requests_get.side_effect = [response_1, response_2, response_3]

        ret = self.chargebee_client.get_all_subscriptions()

        self.assertCountEqual(ret, [{'subscription': {'id': 1}},
                                    {'subscription': {'id': 2}},
                                    {'subscription': {'id': 3}}])

    def test_preserves_parameters_when_doing_multiple_requests_to_chargebee(self):
        response_1 = mock.Mock()
        response_1.json.return_value = {
            'list': [],
            'next_offset': '["1522747277000", "1522747277010"]'
        }
        response_2 = mock.Mock()
        response_2.json.return_value = {
            'list': [],
            'next_offset': '["1522747277010", "1522747277020"]'
        }
        response_3 = mock.Mock()
        response_3.json.return_value = {
            'list': [],
        }
        self.requests_get.side_effect = [response_1, response_2, response_3]

        self.chargebee_client.get_all_subscriptions({'status[is]': 'active'})

        self.requests_get.assert_has_calls([
            mock.call(
                self.chargebee_client.api_url + '/subscriptions',
                auth=self.chargebee_client.auth,
                params={'status[is]': 'active'}
            ),
            mock.call(
                self.chargebee_client.api_url + '/subscriptions',
                auth=self.chargebee_client.auth,
                params={'status[is]': 'active', 'offset': '["1522747277000", "1522747277010"]'}
            ),
            mock.call(
                self.chargebee_client.api_url + '/subscriptions',
                auth=self.chargebee_client.auth,
                params={'status[is]': 'active', 'offset': '["1522747277010", "1522747277020"]'}
            ),
        ])
