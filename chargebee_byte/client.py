import requests
from copy import deepcopy

from chargebee_byte.requests import SubscriptionRequest


class Client(object):
    def __init__(self, site, api_key):
        self.auth = requests.auth.HTTPBasicAuth(api_key, '')
        self.api_url = 'https://{}.chargebee.com/api/v2'.format(site)

    def get_subscriptions(self, parameters=None):
        request = SubscriptionRequest(parameters)
        response = requests.get(self.api_url + request.path, auth=self.auth, params=request.data)
        response.raise_for_status()
        return response.json()

    def get_all_subscriptions(self, parameters=None):
        ret = self.get_subscriptions(parameters)
        subscriptions = ret['list']

        if 'next_offset' in ret:
            new_parameters = deepcopy(parameters) or {}
            new_parameters.update({'offset': ret['next_offset']})
            subscriptions += self.get_all_subscriptions(new_parameters)

        return subscriptions
