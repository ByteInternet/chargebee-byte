from unittest.mock import patch

import requests
from unittest import TestCase
from unittest import mock

from client import Client, CHARGEBEE_SUBSCRIPTIONS_URI
from allowed_parameters import CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS


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

    def test_sets_api_key_to_provided_api_key(self):
        self.assertEqual(self.chargebee_client.api_key, 'my_api_key')


class TestGetSubscriptions(TestBase):
    def setUp(self):
        super(TestGetSubscriptions, self).setUp()
        self.requests_get = self.set_up_patch('client.requests.get')

    def test_calls_chargebee_api_with_correct_parameters(self):
        self.chargebee_client.get_subscriptions()

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + CHARGEBEE_SUBSCRIPTIONS_URI,
            auth=requests.auth.HTTPBasicAuth(self.chargebee_client.api_key, ''),
            params={}
        )

    def test_returns_json_result_from_requests_get_call(self):
        ret = self.chargebee_client.get_subscriptions()

        self.assertEqual(self.requests_get.return_value.json(), ret)

    def test_calls_chargebee_api_with_provided_parameters(self):
        self.chargebee_client.get_subscriptions(parameters={'status[is]': 'active'})

        self.requests_get.assert_called_once_with(
            self.chargebee_client.api_url + CHARGEBEE_SUBSCRIPTIONS_URI,
            auth=requests.auth.HTTPBasicAuth(self.chargebee_client.api_key, ''),
            params={'status[is]': 'active'}
        )

    def test_raises_value_error_if_unknown_parameter_supplied(self):
        parameter = 'banaan[henk]'
        self.assertNotIn(parameter, CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS)

        with self.assertRaises(ValueError):
            self.chargebee_client.get_subscriptions(parameters={parameter: 'bonobo'})

    @patch('client.Client._check_parameters')
    def test_calls_check_parameters_for_parameter_checks(self, check_parameters):
        parameters = {'status[is]': 'active'}

        self.chargebee_client.get_subscriptions(parameters=parameters)

        check_parameters.assert_called_once_with(parameters, CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS)


class TestCheckParameters(TestBase):
    def test_raises_value_error_with_message_specifying_which_parameters_are_wrong_if_invalid_parameters_supplied(self):
        parameters = {'not_allowed': 'something', 'also_not_allowed': 'something', 'status[is]': 'something'}

        try:
            self.chargebee_client._check_parameters(parameters, CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS)
        except ValueError as e:
            self.assertTrue(str(e).startswith('The following parameters are not allowed: '))
            self.assertTrue(str(e).endswith(('not_allowed, also_not_allowed', 'also_not_allowed, not_allowed')))
        else:
            self.fail('Exception not raised')

    def test_does_not_raise_value_error_if_valid_parameters_supplied(self):
        parameters = {'status[is]': 'something', 'status[is_not]': 'something'}

        # Should not raise error
        self.chargebee_client._check_parameters(parameters, CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS)
