from tests.test import TestBase


class TestGetPaginatedInvoices(TestBase):
    def setUp(self):
        super(TestGetPaginatedInvoices, self).setUp()
        self.get_paginated_objects = self.set_up_patch('chargebee_byte.client.Client._get_paginated_objects')
        self.invoice_request = self.set_up_patch('chargebee_byte.client.InvoiceRequest')

    def test_calls_get_paginated_objects_with_correct_parameters(self):
        self.chargebee_client.get_paginated_invoices(parameters={'sort_by[asc]': 'first_name'})

        self.get_paginated_objects.assert_called_once_with(self.invoice_request({'sort_by[asc]': 'first_name'}))

    def test_calls_get_paginated_objects_with_empty_parameters(self):
        self.chargebee_client.get_paginated_invoices()

        self.get_paginated_objects.assert_called_once_with(self.invoice_request({}))

    def test_returns_get_paginated_objects_return_value(self):
        ret = self.chargebee_client.get_paginated_invoices()

        self.assertEqual(ret, self.get_paginated_objects.return_value)




