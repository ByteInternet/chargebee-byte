from unittest import TestCase

from chargebee_byte.requests import SubscriptionRequest, ChargebeeRequest


class TestSubscriptionRequest(TestCase):
    def setUp(self):
        self.request = SubscriptionRequest()

    def test_inherits_from_chargebee_request(self):
        self.assertIsInstance(self.request, ChargebeeRequest)

    def test_path_is_set_to_subscriptions(self):
        self.assertEqual(self.request.path, '/subscriptions')

    def test_has_correct_allowed_params_set(self):
        self.assertCountEqual(self.request.allowed_parameters, [
            'limit',
            'offset',
            'include_deleted',

            'sort_by[asc]',
            'sort_by[desc]',

            'status[is]',
            'status[is_not]',
            'status[in]',
            'status[not_in]',
            'cancel_reason[is]',
            'cancel_reason[is_not]',
            'cancel_reason[in]',
            'cancel_reason[not_in]',
            'id[is]',
            'id[is_not]',
            'id[in]',
            'id[not_in]',
            'customer_id[is]',
            'customer_id[is_not]',
            'customer_id[in]',
            'customer_id[not_in]',
            'plan_id[is]',
            'plan_id[is_not]',
            'plan_id[in]',
            'plan_id[not_in]',

            'id[starts_with]',
            'customer_id[starts_with]',
            'plan_id[starts_with]',

            'cancel_reason[is_present]',
            'activated_at[is_present]',
            'remaining_billing_cycles[is_present]',

            'remaining_billing_cycles[is]',
            'remaining_billing_cycles[is_not]',
            'remaining_billing_cycles[lt]',
            'remaining_billing_cycles[lte]',
            'remaining_billing_cycles[gt]',
            'remaining_billing_cycles[gte]',
            'remaining_billing_cycles[between]',

            'has_scheduled_changes[is]',

            'created_at[after]',
            'created_at[before]',
            'created_at[on]',
            'created_at[between]',
            'activated_at[after]',
            'activated_at[before]',
            'activated_at[on]',
            'activated_at[between]',
            'next_billing_at[after]',
            'next_billing_at[before]',
            'next_billing_at[on]',
            'next_billing_at[between]',
            'cancelled_at[after]',
            'cancelled_at[before]',
            'cancelled_at[on]',
            'cancelled_at[between]',
            'updated_at[after]',
            'updated_at[before]',
            'updated_at[on]',
            'updated_at[between]',
        ])
