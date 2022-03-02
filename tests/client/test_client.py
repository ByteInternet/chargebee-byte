import requests

from chargebee_byte.client import Client
from tests.test import TestBase


class TestClient(TestBase):
    def test_sets_api_url_to_provided_site(self):
        self.assertEqual(self.chargebee_client.api_url, 'https://my_site.chargebee.com/api/v2')

    def test_sets_auth_to_http_basic_auth_method_with_api_key_as_username(self):
        self.assertEqual(self.chargebee_client.auth, requests.auth.HTTPBasicAuth('my_api_key', ''))

    def test_sets_rate_limit_to_none_when_rate_limit_is_not_provided(self):
        self.assertIsNone(self.chargebee_client.rate_limit)

    def test_sets_rate_limit_to_provided_rate_limit(self):
        self.chargebee_client = Client('my_site', 'my_api_key', rate_limit=10)

        self.assertEqual(self.chargebee_client.rate_limit, 10)
