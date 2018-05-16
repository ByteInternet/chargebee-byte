import requests

from allowed_parameters import CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS

CHARGEBEE_SUBSCRIPTIONS_URI = '/subscriptions'


class Client(object):
    api_key = None
    api_url = None

    def __init__(self, site, api_key):
        self.api_key = api_key
        self.api_url = 'https://{}.chargebee.com/api/v2'.format(site)

    def get_subscriptions(self, parameters=None):
        if parameters is None:
            parameters = {}

        self._check_parameters(parameters, CHARGEBEE_SUBSCRIPTIONS_ALLOWED_PARAMETERS)

        subscription_url = self.api_url + CHARGEBEE_SUBSCRIPTIONS_URI
        ret = requests.get(subscription_url, auth=requests.auth.HTTPBasicAuth(self.api_key, ''), params=parameters)
        return ret.json()

    def _check_parameters(self, parameters, allowed_parameters):
        parameter_keys = set(parameters.keys())
        correct_parameters = parameter_keys.intersection(allowed_parameters)
        incorrect_parameters = parameter_keys.symmetric_difference(correct_parameters)

        if incorrect_parameters:
            raise ValueError('The following parameters are not allowed: {}'.format(', '.join(incorrect_parameters)))

