from __future__ import absolute_import

from unittest import TestCase
from unittest import mock

import requests

from chargebee_byte.client import Client
from chargebee_byte.requests.subscription_request import SubscriptionRequest


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


class TestGetSubscriptions(TestBase):
    def setUp(self):
        super(TestGetSubscriptions, self).setUp()
        self.requests_get = self.set_up_patch('chargebee_byte.client.requests.get')

    def test_calls_chargebee_api_with_correct_parameters(self):
        self.chargebee_client.get_subscriptions()

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + '/subscriptions',
            auth=self.chargebee_client.auth,
            params={}
        )

    def test_returns_json_result_from_requests_get_call(self):
        ret = self.chargebee_client.get_subscriptions()

        self.assertEqual(self.requests_get.return_value.json(), ret)

    def test_calls_chargebee_api_with_provided_parameters(self):
        self.chargebee_client.get_subscriptions(parameters={'status[is]': 'active'})

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + '/subscriptions',
            auth=self.chargebee_client.auth,
            params={'status[is]': 'active'}
        )

    def test_raises_value_error_if_unknown_parameter_supplied(self):
        parameter = 'banaan[henk]'
        self.assertNotIn(parameter, SubscriptionRequest().allowed_parameters)

        with self.assertRaises(ValueError):
            self.chargebee_client.get_subscriptions(parameters={parameter: 'bonobo'})
