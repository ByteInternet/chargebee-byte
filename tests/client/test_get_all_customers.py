from unittest import mock

from chargebee_byte.requests import CustomerRequest
from tests.test import TestBase


class TestGetAllCustomers(TestBase):
    def setUp(self):
        super().setUp()
        self.requests_get = self.set_up_patch('chargebee_byte.client.requests.get')

        self.response = mock.Mock()
        self.response.json.return_value = {'list': []}
        self.requests_get.return_value = self.response

    def test_raises_value_error_if_unknown_parameter_supplied(self):
        parameter = 'banaan[henk]'
        self.assertNotIn(parameter, CustomerRequest().allowed_parameters)

        with self.assertRaises(ValueError):
            self.chargebee_client.get_all_subscriptions(parameters={parameter: 'bonobo'})

    def test_calls_raise_for_status_on_requests_response(self):
        self.chargebee_client.get_all_subscriptions()

        self.response.raise_for_status.assert_called_once_with()

    def test_keeps_querying_chargebee_if_next_offset_returned(self):
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

        self.chargebee_client.get_all_customers()

        self.requests_get.assert_has_calls([
            mock.call(
                self.chargebee_client.api_url + '/customers',
                auth=self.chargebee_client.auth,
                params={'offset': ''}
            ),
            mock.call(
                self.chargebee_client.api_url + '/customers',
                auth=self.chargebee_client.auth,
                params={'offset': '["1522747277000", "1522747277010"]'}
            ),
            mock.call(
                self.chargebee_client.api_url + '/customers',
                auth=self.chargebee_client.auth,
                params={'offset': '["1522747277010", "1522747277020"]'}
            ),
        ])

    def test_returns_all_customers(self):
        response_1 = mock.Mock()
        response_1.json.return_value = {
            'list': [{'customer': {'id': 1}}],
            'next_offset': '["1522747277000", "1522747277010"]'
        }
        response_2 = mock.Mock()
        response_2.json.return_value = {
            'list': [{'customer': {'id': 2}}],
            'next_offset': '["1522747277010", "1522747277020"]'
        }
        response_3 = mock.Mock()
        response_3.json.return_value = {
            'list': [{'customer': {'id': 3}}],
        }
        self.requests_get.side_effect = [response_1, response_2, response_3]

        ret = self.chargebee_client.get_all_customers()

        self.assertCountEqual(ret, [{'customer': {'id': 1}},
                                    {'customer': {'id': 2}},
                                    {'customer': {'id': 3}}])

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

        self.chargebee_client.get_all_customers({'sort_by[asc]': 'first_name'})

        self.requests_get.assert_has_calls([
            mock.call(
                self.chargebee_client.api_url + '/customers',
                auth=self.chargebee_client.auth,
                params={'sort_by[asc]': 'first_name', 'offset': ''}
            ),
            mock.call(
                self.chargebee_client.api_url + '/customers',
                auth=self.chargebee_client.auth,
                params={'sort_by[asc]': 'first_name', 'offset': '["1522747277000", "1522747277010"]'}
            ),
            mock.call(
                self.chargebee_client.api_url + '/customers',
                auth=self.chargebee_client.auth,
                params={'sort_by[asc]': 'first_name', 'offset': '["1522747277010", "1522747277020"]'}
            ),
        ])
