from unittest import TestCase

from chargebee_byte.requests import CustomerRequest, ChargebeeRequest


class TestCustomerRequest(TestCase):
    def setUp(self):
        self.request = CustomerRequest()

    def test_inherits_from_chargebee_request(self):
        self.assertIsInstance(self.request, ChargebeeRequest)

    def test_path_is_set_to_subscriptions(self):
        self.assertEqual(self.request.path, '/customers')

    def test_has_correct_allowed_params_set(self):
        self.assertCountEqual(self.request.allowed_parameters, [
            'limit',
            'offset',
            'include_deleted',

            'sort_by[asc]',
            'sort_by[desc]',

            'id[is]',
            'id[is_not]',
            'id[starts_with]',
            'id[in]',
            'id[not_in]',

            'first_name[is]',
            'first_name[is_not]',
            'first_name[starts_with]',
            'first_name[is_present]',

            'last_name[is]',
            'last_name[is_not]',
            'last_name[starts_with]',
            'last_name[is_present]',

            'email[is]',
            'email[is_not]',
            'email[starts_with]',
            'email[is_present]',

            'company[is]',
            'company[is_not]',
            'company[starts_with]',
            'company[is_present]',

            'phone[is]',
            'phone[is_not]',
            'phone[starts_with]',
            'phone[is_present]',

            'auto_collection[is]',
            'auto_collection[is_not]',
            'auto_collection[in]',
            'auto_collection[not_in]',

            'taxability[is]',
            'taxability[is_not]',
            'taxability[in]',
            'taxability[not_in]',

            'created_at[after]',
            'created_at[before]',
            'created_at[on]',
            'created_at[between]',
            'updated_at[after]',
            'updated_at[before]',
            'updated_at[on]',
            'updated_at[between]',
        ])
