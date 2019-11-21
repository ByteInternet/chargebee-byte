from unittest import TestCase

from chargebee_byte.requests import CustomerRequest


class TestCustomerRequest(TestCase):
    def setUp(self):
        self.request = CustomerRequest()

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

    def test_raises_value_error_with_message_specifying_invalid_parameters(self):
        parameters = {'not_allowed': 'something', 'also_not_allowed': 'something',
                      'sort_by[asc]': 'something'}

        try:
            CustomerRequest(parameters)
        except ValueError as e:
            self.assertTrue(str(e).startswith('The following parameters are not allowed: '))
            self.assertTrue(str(e).endswith(('not_allowed, also_not_allowed',
                                             'also_not_allowed, not_allowed')))
        else:
            self.fail('Exception not raised')

    def test_does_not_raise_value_error_if_valid_parameters_supplied(self):
        parameters = {'sort_by[asc]': 'something', 'sort_by[desc]': 'something'}

        # Should not raise error
        CustomerRequest(parameters)

    def test_sets_data_to_parameters(self):
        parameters = {'sort_by[asc]': 'created_at', 'updated_at[on]': 'something'}

        request = CustomerRequest(parameters)

        self.assertEqual(request.data, parameters)

    def test_sets_data_to_empty_dict_if_no_parameters(self):
        self.assertEqual(self.request.data, {})
