from unittest import TestCase, mock

from chargebee_byte.client import Client


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
            themock = mock.MagicMock(**kwargs)

        patcher = mock.patch(topatch, themock)
        self.addCleanup(patcher.stop)
        return patcher.start()


