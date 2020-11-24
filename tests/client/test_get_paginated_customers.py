from tests.test import TestBase


class TestGetPaginatedCustomers(TestBase):
    def setUp(self):
        super(TestGetPaginatedCustomers, self).setUp()
        self.get_paginated_objects = self.set_up_patch('chargebee_byte.client.Client._get_paginated_objects')
        self.customer_request = self.set_up_patch('chargebee_byte.client.CustomerRequest')

    def test_calls_get_paginated_objects_with_correct_parameters(self):
        self.chargebee_client.get_paginated_customers(parameters={'sort_by[asc]': 'first_name'})

        self.get_paginated_objects.assert_called_once_with(self.customer_request({'sort_by[asc]': 'first_name'}))

    def test_calls_get_paginated_objects_with_empty_parameters(self):
        self.chargebee_client.get_paginated_customers()

        self.get_paginated_objects.assert_called_once_with(self.customer_request({}))

    def test_returns_get_paginated_objects_return_value(self):
        ret = self.chargebee_client.get_paginated_invoices()

        self.assertEqual(ret, self.get_paginated_objects.return_value)
