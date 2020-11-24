from unittest import TestCase

from chargebee_byte.requests import ChargebeeRequest, InvoiceRequest


class TestInvoiceRequest(TestCase):
    maxDiff = None

    def setUp(self):
        self.request = InvoiceRequest()

    def test_inherits_from_chargebee_request(self):
        self.assertIsInstance(self.request, ChargebeeRequest)

    def test_path_is_set_to_subscriptions(self):
        self.assertEqual(self.request.path, '/invoices')

    def test_has_correct_allowed_params_set(self):
        self.assertCountEqual(self.request.allowed_parameters, [
            'limit',
            'offset',
            'include_deleted',

            'id[is]',
            'id[is_not]',
            'id[in]',
            'id[not_in]',
            'id[starts_with]',

            'subscription_id[is]',
            'subscription_id[is_not]',
            'subscription_id[in]',
            'subscription_id[not_in]',
            'subscription_id[starts_with]',
            'subscription_id[is_present]',

            'customer_id[is]',
            'customer_id[is_not]',
            'customer_id[in]',
            'customer_id[not_in]',
            'customer_id[starts_with]',

            'status[is]',
            'status[is_not]',
            'status[in]',
            'status[not_in]',

            'price_type[is]',
            'price_type[is_not]',
            'price_type[in]',
            'price_type[not_in]',

            'total[is]',
            'total[is_not]',
            'total[lt]',
            'total[lte]',
            'total[gt]',
            'total[gte]',
            'total[between]',

            'amount_paid[is]',
            'amount_paid[is_not]',
            'amount_paid[lt]',
            'amount_paid[lte]',
            'amount_paid[gt]',
            'amount_paid[gte]',
            'amount_paid[between]',

            'amount_adjusted[is]',
            'amount_adjusted[is_not]',
            'amount_adjusted[lt]',
            'amount_adjusted[lte]',
            'amount_adjusted[gt]',
            'amount_adjusted[gte]',
            'amount_adjusted[between]',

            'credits_applied[is]',
            'credits_applied[is_not]',
            'credits_applied[lt]',
            'credits_applied[lte]',
            'credits_applied[gt]',
            'credits_applied[gte]',
            'credits_applied[between]',

            'amount_due[is]',
            'amount_due[is_not]',
            'amount_due[lt]',
            'amount_due[lte]',
            'amount_due[gt]',
            'amount_due[gte]',
            'amount_due[between]',

            'dunning_status[is]',
            'dunning_status[is_not]',
            'dunning_status[in]',
            'dunning_status[not_in]',
            'dunning_status[is_present]',

            'payment_owner[is]',
            'payment_owner[is_not]',
            'payment_owner[in]',
            'payment_owner[not_in]',
            'payment_owner[starts_with]',

            'void_reason_code[is]',
            'void_reason_code[is_not]',
            'void_reason_code[in]',
            'void_reason_code[not_in]',
            'void_reason_code[starts_with]',

            'date[after]',
            'date[before]',
            'date[on]',
            'date[between]',

            'paid_at[after]',
            'paid_at[before]',
            'paid_at[on]',
            'paid_at[between]',

            'updated_at[after]',
            'updated_at[before]',
            'updated_at[on]',
            'updated_at[between]',

            'voided_at[after]',
            'voided_at[before]',
            'voided_at[on]',
            'voided_at[between]',

            'sort_by[asc]',
            'sort_by[desc]',

            'recurring[is]',
        ])
