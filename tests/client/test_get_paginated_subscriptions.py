from tests.test import TestBase


class TestGetPaginatedSubscriptions(TestBase):
    def setUp(self):
        super(TestGetPaginatedSubscriptions, self).setUp()
        self.get_paginated_objects = self.set_up_patch('chargebee_byte.client.Client._get_paginated_objects')
        self.subscription_request = self.set_up_patch('chargebee_byte.client.SubscriptionRequest')

    def test_calls_get_paginated_objects_with_correct_parameters(self):
        self.chargebee_client.get_paginated_subscriptions(parameters={'sort_by[asc]': 'first_name'})

        self.get_paginated_objects.assert_called_once_with(self.subscription_request({'sort_by[asc]': 'first_name'}))

    def test_calls_get_paginated_objects_with_empty_parameters(self):
        self.chargebee_client.get_paginated_subscriptions()

        self.get_paginated_objects.assert_called_once_with(self.subscription_request({}))
